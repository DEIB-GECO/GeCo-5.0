import { VuexModule, Module, Mutation, Action } from 'vuex-module-decorators';

@Module({ namespaced: true })
class DataViz extends VuexModule {
  charts: ChartData[] = [
    {
      title: 'Ciao',
      vizType: 'scatter'
    }
  ];

  @Mutation
  setCharts(newCharts: DataSummaryPayload): void {
    console.log("ricevuti dei dati, li sto salvando", newCharts)
    newCharts.viz.map((singleChart) => {
      const newData = singleChart;
      if (newData.vizType == 'pie-chart') {
        newData.data = singleChart.data.map((x) => {
          x.value = x.value ? x.value : 'N/D';
          return x;
        });
      }
      return newData;
    });
    this.charts = newCharts.viz;
  }

  removeNulls(chartData: PieData): PieData {
    const newData = chartData;
    newData.data = chartData.data.map((x) => {
      x.value = x.value ? x.value : 'N/D';
      return x;
    });
    return newData;
  }
}

export default DataViz;
