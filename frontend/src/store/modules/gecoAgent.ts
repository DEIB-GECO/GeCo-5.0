import conversation from './geco_agent_modules/conversation';
import queryParameters from './geco_agent_modules/queryParameters';
import functionsArea from './geco_agent_modules/functionsArea';
import parametersBox from './geco_agent_modules/parametersBox';

export default {
  namespaced: true,
  state: {
    activeTool: 'dataset'
  },
  modules: {
    conversation,
    queryParameters,
    functionsArea,
    parametersBox
  }
};
