import conversation from "./geco_agent_modules/conversation";
import queryParameters from "./geco_agent_modules/queryParameters";

export default {
  namespaced: true,
  state: {
    activeTool: "dataset",
  },
  modules: {
    conversation,
    queryParameters,
  },
};
