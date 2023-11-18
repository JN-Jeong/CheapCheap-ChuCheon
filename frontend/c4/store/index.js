import { createStore } from "vuex";

export default createStore({
  state: {
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
  },
});
