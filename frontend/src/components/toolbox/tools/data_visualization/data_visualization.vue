<template>
  <div class="data_viz">
    <!-- <div
      v-for="chart in charts"
      :key="chart.title"
      :is="availableCharts[chart.vizType]"
      :chartData="chart.data"
      :chartTitle="chart.title"
    ></div> -->
    <div
      v-for="chart in charts"
      :key="chart.title"
      :is="'pie-chart'"
      :chartData="chart.data"
      :chartTitle="chart.title"
    ></div>
    <!-- <div
      v-for="chart in charts"
      :key="chart.title"
      :chartData="chart.data"
      :chartTitle="chart.title"
    >
      chart: {{ chart }}, ChartData: {{ chart.data }}, chartTitle:
      {{ chart.title }}
    </div>
    <div>charts: {{ charts }}</div> -->
  </div>
</template>

<script lang="ts">
import { Component, Vue, Prop } from 'vue-property-decorator';
import { namespace } from 'vuex-class';
import PieChart from './charts/pie_chart.vue';

const datavizStore = namespace('gecoAgent/DataViz');

@Component({
  components: {
    PieChart
  }
})
export default class DataVisualization extends Vue {
  availableCharts = {
    pieChart: 'PieChart'
  };

  @datavizStore.State charts!: ChartData[];

  created() {
    console.log('data_visualizaiton has the following data:', this.charts);
  }

  updated() {
    console.log('data_visualizaiton updated with following data:', this.charts);
  }
}
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
