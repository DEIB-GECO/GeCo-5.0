import { VuexModule, Module, Mutation, Action } from 'vuex-module-decorators';

@Module({ namespaced: true })
class TableViewer extends VuexModule {
  tableData: TableDictionary = {
    // 'tcga-25-1320-01a': {
    //   A1BG: 0.6849,
    //   'A1BG-AS1': 0.8926,
    //   A1CF: 0.0,
    //   A2M: 35.32,
    //   'A2M-AS1': 7.29,
    //   A2ML1: 0.0057,
    //   A4GALT: 6.5476,
    //   A4GNT: 0.0852
    // },
    // 'tcga-25-1627-01a': {
    //   A1BG: 0.689,
    //   'A1BG-AS1': 0.926,
    //   A1CF: 2.3,
    //   A2M: 5.32,
    //   'A2M-AS1': 0.29,
    //   A2ML1: 2.0057,
    //   A4GALT: 6.5476,
    //   A4GNT: 1.0
    // },
    // 'tcga-3p-a9wa-01a': {
    //   A1BG: 0.689,
    //   'A1BG-AS1': 2.926,
    //   A1CF: 3.3,
    //   A2M: 53.332,
    //   'A2M-AS1': 0.229,
    //   A2ML1: 2.0057,
    //   A4GALT: 36.546,
    //   A4GNT: 1.543
    // }
  };

  options: TableOptions = {
    showIndex: true,
    orderBy: ''
  };

  @Mutation
  setTable(tablePayload: TablePayload): void {
    this.tableData = tablePayload.data;
    if (tablePayload.options) {
      this.options = tablePayload.options;
      //TODO: call order function
    }
  }
}

export default TableViewer;
