import { VuexModule, Module, Mutation, Action } from 'vuex-module-decorators';

@Module({ namespaced: true })
class Conversation extends VuexModule {
  currentMessage = '';
  isSendButtonActive = true;
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

  @Mutation
  setSendButtonStatus(newValue: boolean) {
    this.isSendButtonActive = newValue;
  }
}
export default Conversation;
