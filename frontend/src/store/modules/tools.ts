// import { fieldList } from "@/test/field_list";
import { VuexModule, Module, Mutation, Action } from 'vuex-module-decorators';

interface ToolTuple {
  name: string;
  component: string;
}

@Module({ namespaced: true })
class Tools extends VuexModule {
  cleanCanvas = true;
  availableTools: ToolTuple[] = [
    { name: 'Dataset List', component: 'dataset' },
    { name: 'Metadata', component: 'metadata' },
    { name: 'Field Explorer', component: 'field' },
    { name: 'Query', component: 'query' },
    { name: 'Data', component: 'dataviz' },
    { name: 'Table', component: 'tableViewer' }
  ];

  fieldList: string[] = [];
  toolToShow = '';

  activeTools: ToolTuple[] = [
    // { name: 'Dataset List', component: 'dataset' },
    // { name: 'Metadata', component: 'metadata' },
    // { name: 'Table', component: 'tableViewer' }
    // { name: 'Field Explorer', component: 'field' },
    // { name: 'Query', component: 'query' }
    { name: 'Data', component: 'dataviz' }
  ];

  @Mutation
  updateFieldList(newList: any): void {
    this.fieldList = newList;
    console.log('UPDATE invoked, new list=');
    console.log(this.fieldList);
  }

  @Action
  updateToolToShow(newTool: string): void {
    console.log('update toool to show');
    //I check if the new tool exists
    if (newTool != '') {
      this.context.commit('addSingleToolToPane', newTool);
      this.context.commit('setToolToShow', newTool);
      // this.toolToShow = newTool;
    }
  }

  //This is a Helper function that should NOT
  //be called from outside the store. Use updateToolToShow
  //Action instead
  @Mutation
  setToolToShow(newTool: string): void {
    this.cleanCanvas = false;
    this.toolToShow = newTool;
  }

  @Mutation
  addSingleToolToPane(newTool: string): void {
    //I check if the tool is not already in the tools list
    console.log('Tool: ' + newTool);
    if (
      !this.activeTools.find((elem) => {
        return elem.component == newTool;
      })
    ) {
      const newToolTuple = this.availableTools.find((elem) => {
        return elem.component == newTool;
      });
      if (newToolTuple) {
        console.log('c');
        this.activeTools.push(newToolTuple);
        this.cleanCanvas = false;
        this.toolToShow = newToolTuple.component;
      }
    }
  }

  @Mutation
  removeSingleToolFromPane(tool: string): void {
    const toolToRemove = this.activeTools.find((elem) => {
      return elem.component == tool;
    });

    if (toolToRemove) {
      if (this.toolToShow == tool) {
        this.cleanCanvas = true;
      }
      const index = this.activeTools.indexOf(toolToRemove);
      this.activeTools.splice(index, 1);
    }
  }

  @Mutation
  resetToolPane(){
    this.toolToShow = '';
    this.cleanCanvas = true;
    this.activeTools = [];
  }
}

export default Tools;
