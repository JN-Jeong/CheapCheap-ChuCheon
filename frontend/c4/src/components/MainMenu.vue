<template>
  <div class="menuBar">
    <router-link to="/board"><div class="menuItem">게시글</div></router-link>
  </div>
</template>

<style scoped>
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
</style>
