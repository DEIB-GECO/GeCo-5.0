import { VuexModule, Module, Mutation, Action } from 'vuex-module-decorators';

@Module({ namespaced: true })
class Process extends VuexModule {
  stepList: ProcessStep[] = [
    // {
    //   name: 'Data Selection',
    //   urlList: [],
    //   isDownloadButtonVisible: false,
    //   state: 'active'
    // },
    // {
    //   name: 'Data',
    //   urlList: [],
    //   isDownloadButtonVisible: false,
    //   state: 'active'
    // },
    // {
    //   name: 'Data data data data data data',
    //   urlList: [],
    //   isDownloadButtonVisible: false,
    //   state: 'active'
    // }
  ];
  lastElementName = '';

  @Mutation
  parseJsonResponse(payload: ProcessPanePayload): void {
    const lastElement = this.stepList.pop();
    if (payload.url) {
      console.log("PROCESS: c'e' un url!");
      if (lastElement) {
        lastElement.urlList = payload.url;
        lastElement.isDownloadButtonVisible = true;
        this.stepList.push(lastElement);
      }
    } else {
      if (this.lastElementName != payload.state) {
        if (lastElement) {
          console.log('PROCESS: completo il precedente step');
          lastElement.state = 'completed';
          this.stepList.push(lastElement);
        }
        if (payload.state != 'END') {
          console.log('PROCESS: inserisco nuovo step');
          this.stepList.push({
            name: payload.state,
            urlList: [],
            isDownloadButtonVisible: false,
            state: 'active'
          });
          this.lastElementName = payload.state;
        }
      } else {
        console.log('PROCESS: si chiama uguale-> salto ');

        if (lastElement) {
          console.log('PROCESS: pusho quello vecchio');
          this.stepList.push(lastElement);
        }
      }
    }
  }

  @Mutation
  resetProcess() {
    this.stepList = [];
    this.lastElementName = '';
  }
}

export default Process;
