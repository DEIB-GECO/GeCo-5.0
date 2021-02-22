export default {
  namespaced: true,
  state: {
    queryParameters: {
      annType: 'start codon',
      assembly: 'hg19',
      data: 'annotations',
      name: 'ds_1',
      source: 'roadmap epigenomics'
    }
  },
  mutations: {
    parseJsonResponse(state: any, payload: any) {
      state.queryParameters = payload;
    }
  }
};
