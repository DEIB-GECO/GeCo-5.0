import { VuexModule, Module, Mutation, Action } from 'vuex-module-decorators';
import AvailableChoice from '@/types/AvailableChoice';

@Module({ namespaced: true })
class FunctionArea extends VuexModule {
  name: string = '';
  searchBarVisible: Boolean = false;
  viewType: 'options' | 'tip' = 'options';
  choicesTitle: string = '';
  choicesArray: AvailableChoice[] = [];
  tipContent: string = '';

  @Mutation
  setSearchBarVisible(isVisible: Boolean): void {
    this.searchBarVisible = isVisible;
  }

  @Mutation
  setChoicesArray(newChoices: AvailableChoice[]): void {
    this.choicesArray = newChoices;
  }

  @Mutation
  setTipContent(newContent: string): void {
    this.tipContent = newContent;
  }

  @Mutation
  clearAll(): void {
    this.searchBarVisible = false;
    this.viewType = 'options';
    this.choicesTitle = '';
    this.choicesArray = [];
    this.tipContent = '';
  }

  @Action
  updateName(newName: string): void {
    this.context.commit('setName', newName);
  }
}
export default FunctionArea;
