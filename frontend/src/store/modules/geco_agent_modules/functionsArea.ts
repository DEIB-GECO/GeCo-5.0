import { VuexModule, Module, Mutation, Action } from 'vuex-module-decorators';
type Type = 'options' | 'tip';

// import AvailableChoice from '@/types/AvailableChoice';

@Module({ namespaced: true })
class FunctionArea extends VuexModule {
  name = '';
  searchBarVisible = true;
  viewType: Type = 'options';
  choicesTitle = '';
  choicesArray: AvailableChoice[] = [];
  showHelpIcon = true;
  helpContent =
    'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Curabitur sagittis lacus varius, pulvinar dolor a, dapibus dolor. Quisque facilisis mi sit amet tempor efficitur. Proin eleifend neque tellus, sed facilisis.';
  tipContent =
    'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Curabitur sagittis lacus varius, pulvinar dolor a, dapibus dolor. Quisque facilisis mi sit amet tempor efficitur. Proin eleifend neque tellus, sed facilisis.';

  @Mutation
  setSearchBarVisible(isVisible: boolean): void {
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