import conversation from "./geco_agent_modules/conversation";

export default {
  namespaced: true,
  state: {
    activeTool: "dataset",
  },
  modules: {
    conversation,
  },
};
