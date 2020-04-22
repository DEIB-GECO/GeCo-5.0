export default {
  namespaced: true,
  state: {
    conversation: [],
  },
  mutations: {
    parseJsonResponse(state: any, msg: string) {
      console.log("ARRIVATO! " + msg);
      state.conversation.push({ sender: "bot", text: msg });
    },
    addUserMessage(state: any, msg: string) {
      state.conversation.push({ sender: "user", text: msg });
    },
  },
};
