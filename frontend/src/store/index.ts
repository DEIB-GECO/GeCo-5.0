import Vue from "vue";
import Vuex from "vuex";

import tools from "./modules/tools";
import gecoAgent from "./modules/gecoAgent";

Vue.use(Vuex);

export default new Vuex.Store({
  state: {},
  mutations: {},
  actions: {},
  modules: {
    tools,
    gecoAgent,
  },
});
