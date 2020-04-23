// import { fieldList } from "@/test/field_list";

export default {
  namespaced: true,
  state: {
    fieldList: ["gigi"],
    toolToShow: "field",
    queryParameters: {},
  },
  getters: {
    getFieldList(state: any) {
      return state.fieldList;
    },
    getToolToShow(state: any) {
      return state.toolToShow;
    },
    getQueryParameters(state: any) {
      return state.queryParameters;
    },
  },
  mutations: {
    updateFieldList(state: any, newList: any) {
      state.fieldList = newList;
      console.log("UPDATE invoked, new list=");
      console.log(state.fielList);
    },
    updateToolToShow(state: any, newTool: string) {
      if (newTool != "") {
        state.toolToShow = newTool;
      }
    },
    updateQueryParameters(state: any, newParameters: any) {
      state.queryParameters = newParameters;
    },
  },
};
