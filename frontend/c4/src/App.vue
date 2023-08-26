<template>
  <main-head />
  <main-menu />
  <items-board />
</template>

<script>
import MainHead from "./components/MainHead.vue";
import MainMenu from "./components/MainMenu.vue";
import ItemsBoard from "./components/ItemsBoard.vue";

export default {
  components: { MainHead, MainMenu, ItemsBoard },
  name: "App",
};
</script>

<style scoped></style>
