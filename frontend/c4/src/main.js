import { createApp } from "vue";
import App from "./App.vue";
import axios from "axios";
import router from "../router/index";
import store from "../store/index";

const app = createApp(App);

app.config.globalProperties.$axios = axios;

app.use(store).use(router).mount("#app");
