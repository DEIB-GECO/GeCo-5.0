import { VuexModule, Module, Mutation, Action } from 'vuex-module-decorators';

@Module({ namespaced: true })
class Conversation extends VuexModule {
  conversation: MessageObject[] = [];

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
