import { VuexModule, Module, Mutation, Action } from 'vuex-module-decorators';

@Module({ namespaced: true })
class Conversation extends VuexModule {
  currentMessage = '';

  conversation: MessageObject[] = [];

  @Mutation
  parseJsonResponse(msg: string) {
    this.conversation.push({ sender: 'bot', text: msg });
  }

  @Mutation
  addUserMessage(msg: string) {
    this.conversation.push({ sender: 'user', text: msg });
  }

  @Mutation
  concatenateToMessage(newPiece: string) {
    this.currentMessage = this.currentMessage + ' ' + newPiece;
  }

  @Mutation
  editMessage(newMsg: string) {
    this.currentMessage = newMsg;
  }
}
export default Conversation;
