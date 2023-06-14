import argparse
import logging
import os
import re
import sys
from datetime import datetime
from time import sleep

import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from tqdm import tqdm

sys.path.append("..")
from database import mongodb


def str2bool(v):
    if isinstance(v, bool):
        return v
    if v.lower() in ("yes", "true", "t", "y", "1"):
        return True
    elif v.lower() in ("no", "false", "f", "n", "0"):
        return False
    else:
        raise argparse.ArgumentTypeError("Boolean value expected.")


def main():
    if args.update_db:
        db_name = "C4"
        collection_name = "items"
        db = mongodb.MongoDB(db_name, collection_name)
        logger.info(f"DB : {db_name}, collection : {collection_name}")

    # 페이지가 존재하는지 체크하는 count 값
    cnt = 0
    # DB에 존재하는 데이터인지 확인하는 flag
    exit_flag = False

    last_page = start
    for idx in tqdm(range(start, end + 1)):
        page_url = f"https://coolenjoy.net/bbs/jirum?page={idx}"
        driver.get(page_url)
        # BeautifulSoup을 사용하기 위해 현재 페이지의 HTML을 가져옵니다.
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, "html.parser")

        # 분류 - class가 "float-left3 d-md-table-cell nw-8 nw-md-auto font-weight-normal py-md-2 px-md-1"인 요소를 추출
        categories = soup.find_all(class_="float-left3 d-md-table-cell nw-8 nw-md-auto font-weight-normal py-md-2 px-md-1")

        # 제목 - class가 "na-subject"인 요소를 추출
        title = soup.find_all(class_="na-subject")

        if cnt >= 3:
            logger.info(f"마지막 페이지 : {last_page}")
            logger.info(f"더 이상 페이지가 존재하지 않아 크롤링을 종료합니다.")
            break

        if not (categories and title):
            cnt += 1
            continue

        # 가격 - class가 "float-right float-md-none d-md-table-cell nw-7 nw-md-auto text-right f-sm font-weight-normal pl-2 py-md-2 pr-md-1"인 요소를 추출
        prices = soup.find_all(
            class_="float-right float-md-none d-md-table-cell nw-7 nw-md-auto text-right f-sm font-weight-normal pl-2 py-md-2 pr-md-1"
        )

        # 작성자 - span class가 "sv_wrap"인 요소를 추출
        members = soup.find_all("span", {"class": "sv_wrap"})

        # 조회수
        hits = soup.find_all(class_="float-left float-md-none d-md-table-cell nw-4 nw-md-auto f-sm font-weight-normal py-md-2 pr-md-1")

        # 추천수
        recommendations = soup.find_all(class_="float-left float-md-none d-md-table-cell nw-3 nw-md-auto f-sm font-weight-normal py-md-2 pr-md-1")

        # 추출한 데이터를 pandas DataFrame으로 저장
        if args.filename:
            data = {
                "categories": [],
                "title": [],
                "page_link": [],
                "purchase_link": [],
                "prices": [],
                "members": [],
                "date": [],
                "hits": [],
                "recommendations": [],
                "contents": [],
                "images": [],
            }

        except_categories = []  # 크롤링 제외 할 카테고리
        for i in range(len(title)):
            if categories[i] in except_categories:
                logger.info(f"{categories[i]} 제외")
                continue

            post_page_url = re.sub(r"\?.*", "", title[i].attrs["href"])
            # 게시글로 이동
            sleep(0.3)
            driver.get(post_page_url)
            # BeautifulSoup을 사용하기 위해 현재 페이지의 HTML을 가져옵니다.
            page_source = driver.page_source
            soup = BeautifulSoup(page_source, "html.parser")

            # 제목 추출
            content_title = soup.find("h1")
            if not content_title:
                logger.info(f"게시글 제목이 없습니다 - {post_page_url}")
                continue
            content_title = content_title.text.split("|")[-1].strip()

            # 본문 내용 추출
            content = soup.find(class_="mb-4 px-3")
            if not content:
                logger.info(f"게시글 본문 내용이 없습니다 - {post_page_url}")
                content = ""

            # 이미지 추출
            images = []
            if content:
                imgs = content.find_all("img")

                for img in imgs:
                    if img:
                        images.append(img.get("src"))
                    else:
                        logger.info(f"게시글 이미지가 없습니다 - {post_page_url}")
                        images.append([])

            # 시간 추출
            content_time = soup.find("time")
            if not content_time:
                logger.info(f"게시글 content time이 없습니다 - {post_page_url}")
                content_time = ""

            # 구매 링크
            purchase_link = soup.find(class_="pl-3 flex-grow-1 text-break-all")
            if not purchase_link:
                logger.info(f"게시글 구매 링크가 없습니다 - {post_page_url}")
                purchase_link = ""

            # 작성자 형식 변경
            member = members[i].text.strip().split()[0]

            # 조회수 형식 변경
            hit = re.sub(r"\s+", " ", hits[i].text).strip().split(" ")[1]

            # 추천수 형식 변경
            recommendation = re.sub(r"\s+", " ", recommendations[i].text).strip().split(" ")[1]

            try:
                content = content.text.strip()
            except:
                content = ""

            try:
                content_time = content_time.text
            except:
                content_time = ""

            try:
                purchase_link = re.sub(r"\d+회 연결", "", purchase_link.text.strip().replace("\n", "")).strip()
            except:
                purchase_link = ""

            try:
                price = prices[i].find("font").text.strip()
            except:
                price = "본문참고"

            # DB에 이미 존재하는 데이터인지 확인, 존재한다면 continue_flag를 True로 변경
            continue_flag = False
            if args.update_db and db.is_in({"page_link": post_page_url}):
                if not args.ignore:  # ignore 옵션이 False라면 코드 종료를 위해 exit_flag를 True로 변경
                    exit_flag = True
                    break
                continue_flag = True
                logger.info(f"DB에 이미 존재하는 데이터입니다 - {post_page_url}")

            if args.filename:
                data["categories"].append(categories[i].text.strip())
                data["title"].append(content_title)
                data["page_link"].append(post_page_url)
                data["purchase_link"].append(purchase_link)
                data["prices"].append(price)
                data["members"].append(member)
                data["date"].append(content_time)
                data["hits"].append(hit)
                data["recommendations"].append(recommendation)
                data["contents"].append(content)
                data["images"].append(images)

            if continue_flag:  # DB에 이미 존재하는 데이터라면 DB에 추가하지 않고 continue
                continue
            if args.update_db:
                row = {
                    "categories": categories[i].text.strip(),
                    "title": content_title,
                    "page_link": post_page_url,
                    "purchase_link": purchase_link,
                    "prices": price,
                    "members": member,
                    "date": content_time,
                    "hits": hit,
                    "recommendations": recommendation,
                    "contents": content,
                    "images": images,
                }
                # DB에 저장
                db.insert_one(row)

        if args.filename:
            df = pd.DataFrame(data)

            # csv 파일로 저장
            if not os.path.exists(file_name):
                df.to_csv(file_name, index=False, mode="w", encoding="utf-8-sig")
            else:
                df.to_csv(file_name, index=False, mode="a", encoding="utf-8-sig", header=False)

            if idx % 500 == 0:
                logger.info(f"{idx}페이지까지 저장이 완료되었습니다.")

        # count 초기화
        cnt = 0
        # last_page 갱신
        last_page = idx

        sleep(0.2)

        if exit_flag:
            break

    else:
        logger.info(f"{idx}페이지까지 크롤링 완료")
    driver.quit()


if __name__ == "__main__":
    # Selenium을 통해 Chrome 브라우저를 엽니다.
    driver = webdriver.Chrome()

    date_now = datetime.now()

    parser = argparse.ArgumentParser()
    parser.add_argument("--filename", "-fn", default=None, type=str)
    parser.add_argument("--start", "-s", type=int, default=1)
    parser.add_argument("--end", "-e", type=int, default=5000)
    parser.add_argument("--update_db", "-udb", help="if true, crawling data and insert to db (boolean flag)", default=False, type=str2bool)
    parser.add_argument(
        "--ignore", "-ign", help="if true, continue crawling even if there is data in db (boolean flag)", default=False, type=str2bool
    )

    args, _ = parser.parse_known_args()

    start = args.start
    end = args.end
    if args.filename:
        if not os.path.exists("./data"):
            os.makedirs("./data")
        file_name = "data/" + args.filename + ".csv"

    logger = logging.getLogger(__name__)

    class CustomFormatter(logging.Formatter):
        def formatTime(self, record, datefmt=None):
            return super().formatTime(record, "%Y-%m-%d %H:%M:%S")

    # logging 설정
    if not os.path.exists("./logs"):
        os.makedirs("./logs")

    log_file = f"./logs/{date_now.strftime('%Y.%m.%d')}.log"
    if not os.path.exists("./logs"):
        with open(log_file, "w+") as f:
            f.write(f"******{date_now.strftime('%Y.%m.%d %H:%M')} Log file Start *****\n")
    else:
        with open(log_file, "a+") as f:
            f.write(f"******{date_now.strftime('%Y.%m.%d %H:%M')} Log file Start *****\n")

    LOG_FORMAT = "%(asctime)s - %(message)s"
    formatter = CustomFormatter(LOG_FORMAT)

    logging.basicConfig(
        level=logging.INFO,
        format=LOG_FORMAT,
        datefmt="%Y.%m.%d %H:%M:%S",
        handlers=[logging.StreamHandler(sys.stdout)],
    )
    file_handler = logging.FileHandler(log_file, mode="a", encoding="utf-8")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    main()
