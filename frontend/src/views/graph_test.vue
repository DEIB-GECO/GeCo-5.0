<template>
  <div>
    <piechart></piechart>
  </div>
</template>

<script lang="ts">
import Vue from "vue";
import piechart from "../components/toolbox/tools/data_visualization/charts/piechart.vue";

export default Vue.extend({
  components: {
    piechart,
  },
});
</script>

<style scoped></style>
