<template>
  <div class="header">
    <div class="serviceName">
      <router-link to="/">C4</router-link>
    </div>
  </div>
  <div class="menuBar">
    <div class="menuItem"><router-link to="/???">메뉴1</router-link></div>
    <div class="menuItem"><router-link to="/???">메뉴1</router-link></div>
    <div class="menuItem"><router-link to="/???">메뉴1</router-link></div>
  </div>
  <div class="body">
    <table class="boardTable">
      hi
    </table>
  </div>
</template>

<script>
export default {
  name: "App",
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
  color: white;
  font-size: 40px;
  font-weight: 900;
}

.menuBar {
  background-color: #323232;
  height: 30px;
  margin-bottom: 3px;
  overflow: hidden;
}

.menuItem {
  float: right;
  margin-right: 15px;
  color: white;
  line-height: 30px;
}

.body {
  background-color: #323232;
  min-height: 400px;
  height: 62vh;
  margin: 40px;
  padding: 40px;
}
</style>
