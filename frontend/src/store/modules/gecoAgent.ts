import conversation from './geco_agent_modules/conversation';
import queryParameters from './geco_agent_modules/queryParameters';
import functionsArea from './geco_agent_modules/functionsArea';
import parametersBox from './geco_agent_modules/parametersBox';
import DataViz from './geco_agent_modules/dataviz';

export default {
  namespaced: true,
  state: {
    activeTool: 'dataset'
  },
  modules: {
    conversation,
    queryParameters,
    functionsArea,
    parametersBox,
    DataViz
  }
};
