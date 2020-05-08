<template>
  <div class="data_viz">
    <pie-chart :chartTitle="'these'"></pie-chart>
    <pie-chart :chartTitle="'are'"></pie-chart>
    <pie-chart :chartTitle="'some'"></pie-chart>
    <pie-chart :chartTitle="'examples'"></pie-chart>
    <pie-chart :chartTitle="'of'"></pie-chart>
    <pie-chart :chartTitle="'graphs'"></pie-chart>
    <pie-chart :chartTitle="'graphs'"></pie-chart>
    <pie-chart :chartTitle="'graphs'"></pie-chart>
  </div>
</template>

<script lang="ts">
import { Component, Vue, Prop } from 'vue-property-decorator';
// import { namespace } from 'vuex-class';
import PieChart from './charts/pie_chart.vue';

@Component({
  components: {
    PieChart
  }
})
export default class DataVisualization extends Vue {}
</script>

<style scoped lang="scss">
@import '@/style/base.scss';
.data_viz {
  max-height: 70vh !important;
  overflow-y: scroll;
  overflow-x: hidden;
  position: relative;
  display: grid;
  grid-template-columns: auto auto auto;
}
</style>
