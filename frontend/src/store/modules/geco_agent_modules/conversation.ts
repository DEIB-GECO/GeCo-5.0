export default {
  namespaced: true,
  state: {
    conversation: [
      // { sender: "bot", text: "Ciao!" },
      // { sender: "user", text: "Ciao!" },
      // { sender: "bot", text: "How can I help You?" },
      // { sender: "user", text: "Please, let me do some analysis!" },
      // { sender: "bot", text: "Sure!" },
      // { sender: "user", text: "Thank you!" },
    ],
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
