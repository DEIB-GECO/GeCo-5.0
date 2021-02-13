<template>
  <div>
    <scatter></scatter>
  </div>
</template>

<script lang="ts">
import Vue from 'vue';
import scatter from '../components/toolbox/tools/data_visualization/charts/Scatter.vue';

export default Vue.extend({
  components: {
    scatter
  }
});
</script>

<style scoped></style>
