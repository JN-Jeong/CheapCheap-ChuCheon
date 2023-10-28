<template>
  <div>
    <main-head />
    <main-menu />
    <router-view :key="$route.fullPath"></router-view>
  </div>
</template>

<script>
import MainHead from "./components/MainHead.vue";
import MainMenu from "./components/MainMenu.vue";

export default {
  components: { MainHead, MainMenu },
  name: "App",
};
</script>

<style scoped></style>
