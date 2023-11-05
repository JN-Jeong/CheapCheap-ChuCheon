<template>
  <div class="header">
    <router-link to="/"><div class="serviceName">C4</div></router-link>
  </div>
</template>

<style scoped>
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
  font-size: 2.5vw;
  font-weight: 900;
}

@media screen and (min-width: 320px) {
  .serviceName {
    font-size: calc(40px + 6 * ((100vw - 320px) / 1000));
  }
}
@media screen and (min-width: 1000px) {
  .serviceName {
    font-size: 45px;
  }
}
</style>
