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
    <div class="kakao-share-back" @click="kakaoShare">
      <img class="kakao-share" src="../../public/KAKAO_SHARE_IMG.png" />
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

.kakao-share-back {
  position: fixed;
  bottom: 2vw;
  right: 2vw;
  border: 2px solid #cccccc;
  background-color: #fee500;
  width: 3.5vw;
  height: 3.5vw;
  border-radius: 10px;
  text-align: center;
}

.kakao-share-back:hover {
  cursor: pointer;
  background: yellow;
}

.kakao-share-back:after {
  display: inline-block;
  height: 100%;
  content: "";
  vertical-align: middle;
}

.kakao-share {
  width: 2.5vw;
  vertical-align: middle;
}
</style>
