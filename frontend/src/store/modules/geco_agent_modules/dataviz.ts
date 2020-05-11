import { VuexModule, Module, Mutation, Action } from 'vuex-module-decorators';

@Module({ namespaced: true })
class DataViz extends VuexModule {
  charts: ChartData[] = [
    {
      vizType: 'pieChart',
      title: 'Source',
      data: [
        { value: 'refseq', count: 61 },
        { value: 'gencode', count: 40 },
        { value: 'roadmap epigenomics', count: 4 }
      ]
    }
  ];
}

export default DataViz;
