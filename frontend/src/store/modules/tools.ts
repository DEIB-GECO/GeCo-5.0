// import { fieldList } from "@/test/field_list";

export default {
  namespaced: true,
  state: {
    fieldList: ["gigi"],
  },
  getters: {
    getFieldList(state: any) {
      return state.fieldList;
    },
  },
  mutations: {
    updateFieldList(state: any, newList: any) {
      state.fieldList = newList;
      console.log("UPDATE invoked");
    },
  },
};
