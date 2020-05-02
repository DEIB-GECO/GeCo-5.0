import { VuexModule, Module, Mutation, Action } from 'vuex-module-decorators';

@Module({ namespaced: true })
class Conversation extends VuexModule {
  conversation = [
    // { sender: 'bot', text: 'Ciao!' },
    // { sender: 'user', text: 'Ciao!' }
    // { sender: 'bot', text: 'How can I help You?' },
    // { sender: 'user', text: 'Please, let me do some analysis!' },
    // { sender: 'bot', text: 'Sure!' },
    // { sender: 'user', text: 'Thank you!' }
  ];

  @Mutation
  parseJsonResponse(msg: string) {
    this.conversation.push({ sender: 'bot', text: msg });
  }

  @Mutation
  addUserMessage(msg: string) {
    this.conversation.push({ sender: 'user', text: msg });
  }
}
export default Conversation;
// export default {
//   namespaced: true,
//   state: {
//     conversation: [
//       // { sender: "bot", text: "Ciao!" },
//       // { sender: "user", text: "Ciao!" },
//       // { sender: "bot", text: "How can I help You?" },
//       // { sender: "user", text: "Please, let me do some analysis!" },
//       // { sender: "bot", text: "Sure!" },
//       // { sender: "user", text: "Thank you!" },
//     ],
//   },
//   mutations: {
//     parseJsonResponse(state: any, msg: string) {
//       // console.log("ARRIVATO! " + msg);
//       state.conversation.push({ sender: "bot", text: msg });
//     },
//     addUserMessage(state: any, msg: string) {
//       state.conversation.push({ sender: "user", text: msg });
//     },
//   },
// };
