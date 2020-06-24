import { VuexModule, Module, Mutation, Action } from 'vuex-module-decorators';

@Module({ namespaced: true })
class Process extends VuexModule {
  stepList: ProcessStep[] = [
    // {
    //   name: 'Data Selection',
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
      if (lastElement) {
        lastElement.urlList = payload.url;
        lastElement.isDownloadButtonVisible = true;
        this.stepList.push(lastElement);
      }
    } else {
      if (this.lastElementName != payload.state) {
        if (lastElement) {
          lastElement.state = 'completed';
          this.stepList.push(lastElement);
        }
        this.stepList.push({
          name: payload.state,
          urlList: [],
          isDownloadButtonVisible: false,
          state: 'active'
        });
        this.lastElementName = payload.state;
      }
    }
  }
}

export default Process;
