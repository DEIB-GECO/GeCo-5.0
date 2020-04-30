import conversation from './geco_agent_modules/conversation';
import queryParameters from './geco_agent_modules/queryParameters';
import functionsArea from './geco_agent_modules/functionsArea';

export default {
  namespaced: true,
  state: {
    activeTool: 'dataset'
  },
  modules: {
    conversation,
    queryParameters,
    functionsArea
  }
};
