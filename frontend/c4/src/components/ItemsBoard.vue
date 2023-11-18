<template>
  <div class="itemsBoardBody">
    <div class="btnGroup">
      <button
        v-for="(row, idx) in categories"
        :key="idx"
        class="btn categoryBtn"
        :class="row.isSel ? 'selBtn' : ''"
        @click="setCategoy(row.name, idx)"
      >
        {{ row.name }}
      </button>
    </div>

    <div class="itemsBoardMiddle">
      <table class="boardTable">
        <colgroup>
          <col style="width: 7%" />
          <col style="width: 63%" />
          <col style="width: 8%" />
          <col style="width: 10%" />
          <col style="width: 12%" />
        </colgroup>
        <thead class="bt1">
          <tr>
            <th class="th_category">분류</th>
            <th class="th_title">제목</th>
            <th class="th_price">가격</th>
            <th class="th_member">이름</th>
            <th class="th_data">날짜</th>
            <th></th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(row, idx) in itemsList" :key="idx" class="item">
            <td>{{ row.categories }}</td>
            <td v-on:click="title_onClick(row._id)">
              {{ row.title }}
            </td>
            <td>{{ row.prices }}</td>
            <td>{{ row.members }}</td>
            <td>{{ row.date }}</td>
          </tr>
        </tbody>
      </table>
    </div>

    <div class="pageGroup">
      <div class="pageGroupItem pageCurrent">
        <input
          class="pageInputBox"
          maxlength="7"
          v-model="dmSearch.pageIndex"
          @blur="checkInputValue"
          @keyup="pageInputBox_keyup"
        />
      </div>
      <div class="pageGroupItem pageGB">&nbsp;/&nbsp;</div>
      <div class="pageGroupItem pageTotal">
        {{ Math.ceil(dmSearch.itemsLength / dmSearch.pageSize) }}
      </div>
    </div>
    <div class="pageGroup">
      <div class="pageGroupItem">
        <button class="btn" v-on:click="movePageStart()">&lt;&lt;</button>
      </div>
      <div class="pageGroupItem pageBack">
        <button class="btn" v-on:click="movePage(-1)">&lt;</button>
      </div>
      <div class="pageGroupItem">
        <button class="btn" v-on:click="btn_search_onclick()">검색</button>
      </div>
      <div class="pageGroupItem pageNext">
        <button class="btn" v-on:click="movePage(1)">&gt;</button>
      </div>
      <div class="pageGroupItem">
        <button class="btn" v-on:click="movePageEnd()">&gt;&gt;</button>
      </div>
    </div>
  </div>
</template>

<script>
import { computed } from "vue";
import { useStore } from "vuex";

export default {
  setup() {
    const store = useStore();
    let dmSearch = computed(() => store.state.dmSearch);
    let categories = computed(() => store.state.categories);

    return { dmSearch, categories };
  },
  data() {
    return {
      itemsList: [],
    };
  },
  mounted() {
    this.search();
  },
  methods: {
    setCategoy(data, idx) {
      this.dmSearch.category = data;
      this.dmSearch.pageIndex = 1;
      for (let i = 0; i < this.categories.length; i++) {
        if (i == idx) {
          this.categories[i].isSel = true;
        } else {
          this.categories[i].isSel = false;
        }
      }
      this.search();
    },
    movePage(BN) {
      if (this.dmSearch.pageIndex == 1 && BN == -1) {
        return;
      }
      if (
        this.dmSearch.pageIndex ==
          Math.ceil(this.dmSearch.itemsLength / this.dmSearch.pageSize) &&
        BN == 1
      ) {
        return;
      }

      this.dmSearch.pageIndex += BN;
      this.search();
    },
    movePageStart() {
      this.dmSearch.pageIndex = 1;
      this.search();
    },
    movePageEnd() {
      this.dmSearch.pageIndex = Math.ceil(
        this.dmSearch.itemsLength / this.dmSearch.pageSize
      );
      this.search();
    },
    pageInputBox_keyup(e) {
      if (e.key === "Enter") {
        this.checkInputValue();
        this.search();
      }
    },
    btn_search_onclick() {
      this.checkInputValue();
      this.search();
    },
    checkInputValue() {
      if (isNaN(this.dmSearch.pageIndex)) {
        if (isNaN(parseInt(this.dmSearch.pageIndex))) {
          this.dmSearch.pageIndex = 1;
        } else {
          this.dmSearch.pageIndex = parseInt(this.dmSearch.pageIndex);
        }
        return;
      }

      if (this.dmSearch.pageIndex < 1) {
        this.dmSearch.pageIndex = 1;
      } else if (
        this.dmSearch.pageIndex >
        Math.ceil(this.dmSearch.itemsLength / this.dmSearch.pageSize)
      ) {
        this.dmSearch.pageIndex = Math.ceil(
          this.dmSearch.itemsLength / this.dmSearch.pageSize
        );
      }
    },
    search() {
      this.$axios
        .post(process.env.VUE_APP_URL_ITMES + "/selectListOnBoard", {
          params: this.dmSearch,
        })
        .then((res) => {
          this.itemsList = res.data.itemsList;
          this.dmSearch.itemsLength = res.data.itemsLength;
        })
        .catch((err) => {
          console.log(err);
        });
    },
    title_onClick(row_id) {
      this.$router.push({
        name: "Detail",
        params: { _id: row_id },
      });
    },
  },
};
</script>

<style scoped>
.itemsBoardBody {
  background-color: #323232;
  margin: 40px;
  padding: 20px;
}

.itemsBoardMiddle {
  height: 80%;
  overflow: auto;
}

.boardTable {
  width: 100%;
  border-spacing: 0 11px;
  table-layout: fixed;
}

.bt1 {
  border-bottom: 2px solid white;
  background: #262626;
}

td {
  overflow: hidden;
  white-space: nowrap;
  text-overflow: ellipsis;
  padding-left: 5px;
  padding-right: 5px;
}

td:nth-child(1),
td:nth-child(3),
td:nth-child(4),
td:nth-child(5) {
  text-align: center;
}

.item {
  text-decoration: none;
}

.item > td:nth-child(2):hover {
  cursor: pointer;
  color: aqua;
}

.btnGroup {
  margin-bottom: 20px;
}

.categoryBtn {
  margin-right: 5px;
  margin-bottom: 2px;
  border-radius: 3px;
  padding: 2px 5px;
}

.btn {
  background: #1a1a1a;
  margin-right: 5px;
  margin-bottom: 2px;
  border-radius: 3px;
  padding: 2px 5px;
}

.btn:hover {
  cursor: pointer;
  background: transparent;
}

.pageGroup {
  margin-top: 10px;
  text-align: center;
}

.pageGroupItem {
  display: inline-block;
  margin: 0 2px;
}

.pageInputBox {
  background: transparent;
  min-width: 40px;
  width: 2.5vw;
  text-align: center;
}

.selBtn {
  background: transparent;
}
</style>
