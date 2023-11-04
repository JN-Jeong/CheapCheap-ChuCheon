import { createWebHistory, createRouter } from "vue-router";

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: "/", redirect: "/home" },
    {
      path: "/home",
      name: "Home",
      component: () => import("@/components/ItemsBoard"),
    },
    {
      path: "/board",
      name: "Board",
      component: () => import("@/components/ItemsBoard"),
    },
    {
      path: "/detail/:_id",
      name: "Detail",
      component: () => import("@/components/ItemDetail"),
    },
  ],
});

export default router;
