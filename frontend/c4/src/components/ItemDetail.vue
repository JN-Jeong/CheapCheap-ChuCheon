<template>
  <div class="itemDetailBody">
    <div class="title">
      {{ item.title }}
    </div>
    <div class="boardInfo">{{ item.date }}</div>
    <div class="content">
      <div>제품명 : 제품명</div>
      <div>가격 : {{ item.prices }}</div>
      <div>
        링크 :
        <a :href="item.page_link" target="_blank">{{ item.page_link }}</a>
      </div>
      <div>
        구매링크 :
        <a :href="item.purchase_link" target="_blank">{{
          item.purchase_link
        }}</a>
      </div>
    </div>
    <div class="imgs">
      <img
        v-for="(row, idx) in item.images"
        :key="idx"
        :src="row"
        style="width: 60%"
      />
    </div>
    <Bar id="my-chart-id" :options="chartOptions" :data="chartData" />
    <div class="scroll-move">
      <div class="scroll-move-item" @click="moveScroll('TOP')">&uarr;</div>
      <div class="scroll-move-item" @click="moveScroll('BOT')">&darr;</div>
      <div class="scroll-move-item" @click="kakaoShare">
        <img class="kakao-share" src="../../public/KAKAO_SHARE_IMG2.png" />
      </div>
    </div>
  </div>
  <ItemsBoard />
</template>

<script>
import ItemsBoard from "./ItemsBoard.vue";

import { Bar } from "vue-chartjs";
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  BarElement,
  CategoryScale,
  LinearScale,
} from "chart.js";

export default {
  components: { ItemsBoard, Bar },
  data() {
    return {
      item: {
        _id: "",
        categories: "",
        title: "",
        page_link: "",
        purchase_link: "",
        prices: "",
        members: "",
        date: "",
        hits: "",
        recommendations: "",
        contents: "",
        images: [],
      },
      chartData: {
        labels: ["January", "February", "March"],
        datasets: [{ data: [40, 20, 12] }],
      },
      chartOptions: {
        responsive: true,
      },
    };
  },
  created() {
    ChartJS.register(
      Title,
      Tooltip,
      Legend,
      BarElement,
      CategoryScale,
      LinearScale
    );

    this.selectItem();
  },
  methods: {
    selectItem() {
      this.$axios
        .post(process.env.VUE_APP_URL_ITMES + "/selectOneById", {
          params: this.$route.params._id,
        })
        .then((res) => {
          this.item = res.data.item[0];
        })
        .catch((err) => {
          console.log(err);
        });
    },
    kakaoShare() {
      window.Kakao.Share.sendDefault({
        objectType: "feed",
        content: {
          title: this.item.title,
          description: `${this.item.prices}\n${this.item.purchase_link}`,
          imageUrl: window.location.href,
          link: {
            mobileWebUrl: window.location.href,
            webUrl: window.location.href,
          },
        },
        itemContent: {
          titleImageUrl: window.location.href,
          titleImageText: "제품명",
          titleImageCategory: this.item.categories,
        },
        installTalk: true,
      });
    },
    moveScroll(TB) {
      if (TB == "TOP") {
        window.scrollTo(0, 0);
      } else if (TB == "BOT") {
        window.scrollTo(0, document.body.scrollHeight);
      }
    },
  },
};
</script>

<style scoped>
.itemDetailBody {
  background-color: #323232;
  margin: 40px;
  padding: 20px;
  margin-left: 20vw;
  margin-right: 20vw;
}

.itemsBoardBody {
  background-color: #323232;
  margin: 40px;
  padding: 20px;
  margin-left: 10vw;
  margin-right: 10vw;
}

.title {
  text-align: center;
  margin-bottom: 20px;
}

@media screen and (min-width: 320px) {
  .title {
    font-size: calc(25px + 6 * ((100vw - 320px) / 1000));
  }
}

@media screen and (min-width: 1000px) {
  .title {
    font-size: 30px;
  }
}

.boardInfo {
  text-align: right;
  margin-bottom: 20px;
}

.content {
  margin-bottom: 20px;
}

a {
  word-break: break-all;
}

.imgs {
  text-align: center;
  margin-bottom: 20px;
}

.graph {
  text-align: center;
  margin-bottom: 20px;
}

.kakao-share {
  width: 2.5vw;
  vertical-align: middle;
  background-color: black;
  color: white;
  border-radius: 100%;
}

.scroll-move {
  position: fixed;
  bottom: 2vw;
  right: 2vw;
  width: 3.5vw;
  height: 10.5vw;
  text-align: center;
}

.scroll-move-item {
  height: 33%;
  border: 2px solid #cccccc;
  font-size: 2vw;
  -webkit-user-select: none;
  -moz-user-select: none;
  -ms-use-select: none;
  user-select: none;
}

.scroll-move-item:hover {
  background-color: #aaaaaa;
  cursor: pointer;
}
</style>
