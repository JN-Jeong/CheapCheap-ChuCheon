<template>
  <div class="itemDetailBody">
    <div class="title">
      {{ item.title }}
    </div>
    <div class="boardInfo">{{ item.date }}</div>
    <div class="content">
      <p>제품명 : 제품명</p>
      <p>가격 : {{ item.prices }}</p>
      <p>
        링크 :
        <a :href="item.page_link" target="_blank">{{ item.page_link }}</a>
      </p>
      <p>
        구매링크 :
        <a :href="item.purchase_link" target="_blank">{{
          item.purchase_link
        }}</a>
      </p>
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
    <div>
      <img
        class="kakao-share"
        @click="kakaoShare"
        src="https://developers.kakao.com/assets/img/about/logos/kakaolink/kakaolink_btn_medium.png"
      />
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
          description: this.item.prices,
          imageUrl: this.item.images[0],
          link: {
            mobileWebUrl: this.item.page_link,
            webUrl: this.item.page_link,
          },
        },
        itemContent: {
          titleImageUrl: this.item.images[0],
          titleImageText: "제품명",
          titleImageCategory: this.item.categories,
        },
        buttons: [
          {
            title: "웹 페이지",
            link: {
              mobileWebUrl: window.location.href,
              webUrl: window.location.href,
            },
          },
          {
            title: "본문 페이지",
            link: {
              mobileWebUrl: this.item.page_link,
              webUrl: this.item.page_link,
            },
          },
        ],
        installTalk: true,
      });
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
  min-height: 400px;
  height: 480px;
  margin: 40px;
  padding: 20px;
  margin-left: 10vw;
  margin-right: 10vw;
}

.title {
  text-align: center;
  font-size: 30px;
  margin-bottom: 20px;
}

.boardInfo {
  text-align: right;
  margin-bottom: 20px;
}

.content {
  margin-bottom: 20px;
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
  position: fixed;
  bottom: 50px;
  right: 50px;
}

.kakao-share:hover {
  cursor: pointer;
}
</style>
