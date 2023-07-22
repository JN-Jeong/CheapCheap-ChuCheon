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
        v-on:click="setCategoy(row.name)"
      >
        {{ row.name }}
      </button>
    </div>
    <table class="boardTable bt1">
      <thead>
        <colgroup>
          <col width="20%" />
          <col width="20%" />
          <col width="20%" />
          <col width="20%" />
          <col width="20%" />
        </colgroup>
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
          <colgroup>
            <col width="20%" />
            <col width="20%" />
            <col width="20%" />
            <col width="20%" />
            <col width="20%" />
          </colgroup>
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
  </div>
</template>

<script>
export default {
  name: "App",
  data() {
    return {
      itemsList: [],
      dmSearch: { pageSize: 10, pageIndex: 1, category: "전체" },
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
        { name: "의류", isSel: false },
        { name: "잡화", isSel: false },
        { name: "화장품", isSel: false },
        { name: "기타", isSel: false },
      ],
    };
  },
  mounted() {
    this.search();
  },
  methods: {
    setCategoy(data) {
      this.dmSearch.category = data;
      this.search();
    },
    search() {
      this.$axios
        .post("http://localhost:3000/items", { params: this.dmSearch })
        .then((res) => {
          this.itemsList = res.data.itemsList;
          console.log(res.data.itemsLength);
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
  height: 276px;
  overflow-y: auto;
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
  background: transparent;
  border-radius: 3px;
  padding: 2px 5px;
  border: 1px solid white;
}

.btn:hover {
  cursor: pointer;
}
</style>
