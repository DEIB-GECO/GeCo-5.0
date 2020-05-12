import { VuexModule, Module, Mutation, Action } from 'vuex-module-decorators';

@Module({ namespaced: true })
class DataViz extends VuexModule {
  charts: ChartData[] = [];

  @Mutation
  setCharts(newCharts: DataSummaryPayload): void {
    this.charts = newCharts.viz;
  }
}

export default DataViz;
