<template>
  <div class="header">
    <div class="serviceName">C4</div>
  </div>
  <div class="menuBar">
    <div class="menuItem">메뉴</div>
  </div>
  <div class="body">
    <div class="btnGroup">
      <button
        v-for="(row, idx) in categories"
        :key="idx"
        class="btn categoryBtn"
        :class="row.isSel ? 'selBtn' : ''"
        v-on:click="setCategoy(row.name, idx)"
      >
        {{ row.name }}
      </button>
    </div>
    <table class="boardTable bt1">
      <thead>
        <tr>
          <th class="th_category">분류</th>
          <th class="th_title">제목</th>
          <th class="th_price">가격</th>
          <th class="th_member">이름</th>
          <th class="th_data">날짜</th>
          <th></th>
        </tr>
      </thead>
    </table>
    <div class="boardTableBody">
      <table class="boardTable">
        <tbody>
          <tr v-for="(row, idx) in itemsList" :key="idx">
            <td>{{ row.categories }}</td>
            <td>{{ row.title }}</td>
            <td>{{ row.prices }}</td>
            <td>{{ row.members }}</td>
            <td>{{ row.date }}</td>
          </tr>
        </tbody>
      </table>
    </div>
    <div class="pageGroup">
      <div class="pageGroupItem pageBack">
        <button class="btn" v-on:click="movePage(-1)">이전 페이지</button>
      </div>
      <div class="pageGroupItem pageCurrent">
        <input
          class="pageInputBox"
          maxlength="7"
          v-bind:value="dmSearch.pageIndex"
          v-on:keyup="pageInputBox_keyup"
        />
      </div>
      <div class="pageGroupItem pageGB">&nbsp;/&nbsp;</div>
      <div class="pageGroupItem pageTotal">
        {{ Math.ceil(dmSearch.itemsLength / dmSearch.pageSize) }}
      </div>
      <div class="pageGroupItem pageNext">
        <button class="btn" v-on:click="movePage(1)">다음 페이지</button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "App",
  data() {
    return {
      itemsList: [],
      dmSearch: {
        pageSize: 10,
        pageIndex: 1,
        category: "전체",
        itemsLength: 0,
      },
      categories: [
        { name: "전체", isSel: true },
        { name: "PC관련", isSel: false },
        { name: "가전", isSel: false },
        { name: "게임", isSel: false },
        { name: "식품", isSel: false },
        { name: "인터넷", isSel: false },
        { name: "모바일", isSel: false },
        { name: "이벤트", isSel: false },
        { name: "쿠폰", isSel: false },
        { name: "의류잡화", isSel: false },
        { name: "화장품", isSel: false },
        { name: "기타", isSel: false },
      ],
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
    pageInputBox_keyup(e) {
      if (e.key === "Enter") {
        if (e.target.value < 1) {
          this.dmSearch.pageIndex = 1;
        } else if (
          e.target.value >
          Math.ceil(this.dmSearch.itemsLength / this.dmSearch.pageSize)
        ) {
          this.dmSearch.pageIndex = Math.ceil(
            this.dmSearch.itemsLength / this.dmSearch.pageSize
          );
        } else {
          this.dmSearch.pageIndex = Number(e.target.value);
        }
        this.search();
      }
    },
    search() {
      this.$axios
        .post("http://localhost:3000/items", { params: this.dmSearch })
        .then((res) => {
          this.itemsList = res.data.itemsList;
          this.dmSearch.itemsLength = res.data.itemsLength;
        })
        .catch((err) => {
          console.log(err);
        });
    },
  },
};
</script>

<style>
.header {
  background-color: #323232;
  height: 70px;
  text-align: center;
  margin-bottom: 3px;
}

.serviceName {
  display: inline-block;
  height: 100%;
  line-height: 70px;
  font-size: 40px;
  font-weight: 900;
}

.menuBar {
  background-color: #323232;
  height: 30px;
  margin-bottom: 3px;
  overflow: hidden;
  text-align: center;
}

.menuItem {
  display: inline-block;
  margin-left: 7px;
  margin-right: 7px;
  line-height: 30px;
}

.body {
  background-color: #323232;
  min-height: 400px;
  height: 480px;
  margin: 40px;
  padding: 20px;
}

.boardTable {
  width: 100%;
}

.boardTableBody {
  height: 75%;
  overflow-y: auto;
  margin-bottom: 10px;
}

.bt1 {
  border-bottom: 2px solid white;
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
  text-align: center;
}

.pageGroupItem {
  display: inline-block;
  margin: 0 2px;
}

.pageInputBox {
  background: transparent;
  width: 50px;
  text-align: center;
}

.selBtn {
  background: transparent;
}
</style>
