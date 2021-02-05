<template>
  <div class="data_viz" :style="gridDimension">
    <div
      v-for="chart in charts"
      :key="chart.title"
      :is="chart.vizType"
      :chartData="chart.data"
      :chartTitle="chart.title"
    ></div>
  </div>
</template>

<script lang="ts">
import { Component, Vue, Prop } from 'vue-property-decorator';
import { namespace } from 'vuex-class';
import PieChart from './charts/pie_chart.vue';
import HistDistChart from './charts/HistDistChart.vue';
import Histogram from './charts/Histogram.vue'

const datavizStore = namespace('gecoAgent/DataViz');

@Component({
  components: {
    PieChart,
    HistDistChart,
    Histogram
  }
})
export default class DataVisualization extends Vue {
  availableCharts = {
    pieChart: 'PieChart',
    histogram: 'Histogram'
  };

  @datavizStore.State charts!: ChartData[];

  created() {
    console.log('data_visualizaiton has the following data:', this.charts);
  }

  updated() {
    console.log('data_visualizaiton updated with following data:', this.charts);
  }

  get gridDimension() {
    const gridSizeDefinition =
      this.charts.length > 1 ? 'auto auto auto' : 'auto';
    return {
      'grid-template-columns': gridSizeDefinition
    };
  }
}
</script>

<style scoped lang="scss">
@import '@/style/base.scss';
.data_viz {
  max-height: 70vh !important;
  overflow-y: scroll;
  margin: auto;
  position: relative;
  display: grid;
}
</style>
