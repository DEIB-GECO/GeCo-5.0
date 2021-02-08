// import { VuexModule, Module, Mutation, Action } from 'vuex-module-decorators';
import Vue from 'vue';
import Vuex from 'vuex';
Vue.use(Vuex);

import conversation from './geco_agent_modules/conversation';
import queryParameters from './geco_agent_modules/queryParameters';
import functionsArea from './geco_agent_modules/functionsArea';
import parametersBox from './geco_agent_modules/parametersBox';
import DataViz from './geco_agent_modules/dataviz';
import process from './geco_agent_modules/process';
import TableViewer from './geco_agent_modules/tableViewer';

export default {
  namespaced: true,
  state: {
    activeTool: 'dataset',
    lastMessageId: -1
  },
  modules: {
    conversation,
    queryParameters,
    functionsArea,
    parametersBox,
    DataViz,
    process,
    TableViewer
  }
};
