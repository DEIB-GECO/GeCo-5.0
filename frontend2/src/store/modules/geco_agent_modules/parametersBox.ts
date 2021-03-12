import { VuexModule, Module, Mutation, Action } from 'vuex-module-decorators';

import ParametersValuesList from '@/test/parametersList';

@Module({ namespaced: true })
class ParametersListBox extends VuexModule {
  parametersList: Parameter[] = [];
  // parametersList: Parameter[] = [
  //   { field: 'Marinara', values: ['a value like 13'] },
  //   { field: 'Margherita', values: ['a value like 1 '] },
  //   { field: 'Napoli', values: ['a value like 12'] }
  // ];

  @Mutation
  setParametersList(newParametersList: Parameter[]): void {
    this.parametersList = newParametersList;
  }

  @Mutation
  clearParametersList(): void {
    this.parametersList = [];
  }
}

export default ParametersListBox;
