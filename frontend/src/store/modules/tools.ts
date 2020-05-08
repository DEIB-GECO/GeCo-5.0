// import { fieldList } from "@/test/field_list";
import { VuexModule, Module, Mutation, Action } from 'vuex-module-decorators';

@Module({ namespaced: true })
class Tools extends VuexModule {
  availableTools = [
    { name: 'Dataset List', component: 'dataset' },
    { name: 'Metadata', component: 'metadata' },
    { name: 'Field Explorer', component: 'field' },
    { name: 'Query', component: 'query' },
    { name: 'Data', component: 'dataviz' }
  ];

  fieldList: string[] = [];
  toolToShow = 'dataset';
  // activeTools = this.availableTools;
  activeTools = [
    { name: 'Dataset List', component: 'dataset' },
    { name: 'Metadata', component: 'metadata' },
    { name: 'Field Explorer', component: 'field' },
    { name: 'Query', component: 'query' }
    // { name: 'Data', component: 'dataviz' }
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
    this.toolToShow = newTool;
  }

  @Mutation
  addRemoveTools(jsonPayload: ToolsSetUpPayload) {
    this.addToolsToPane(jsonPayload.add);
    this.removeToolsFromPane(jsonPayload.remove);
  }

  @Action
  addToolsToPane(newToolsList: string[]): void {
    // this.addSingleToolToPane(newToolsList[0]);
    newToolsList.forEach((newTool) => {
      this.context.commit('addSingleToolToPane', newTool);
    });
  }

  @Mutation
  addSingleToolToPane(newTool: string): void {
    //I check if the tool is not already in the tools list
    if (
      !this.activeTools.find((elem) => {
        return elem.component == newTool;
      })
    ) {
      //If not, I search it and I add it
      const newToolTuple = this.availableTools.find((elem) => {
        return elem.component == newTool;
      });
      if (newToolTuple) {
        this.activeTools.push(newToolTuple);
      }
    }
  }

  @Action
  removeToolsFromPane(toolsList: string[]): void {
    toolsList.forEach((tool) => {
      this.context.commit('removeSingleToolFromPane', tool);
      // this.removeSingleToolFromPane(tool)
      // const toolToRemove = this.activeTools.find((elem) => {
      //   return elem.component == tool;
      // });

      // if (toolToRemove) {
      //   const index = this.activeTools.indexOf(toolToRemove);
      //   this.activeTools.splice(index);
      // }
    });
  }

  @Mutation
  removeSingleToolFromPane(tool: string): void {
    const toolToRemove = this.activeTools.find((elem) => {
      return elem.component == tool;
    });

    if (toolToRemove) {
      if (this.toolToShow == tool) {
        this.toolToShow = this.activeTools[0].component;
      }
      const index = this.activeTools.indexOf(toolToRemove);
      this.activeTools.splice(index);
    }
  }
}

export default Tools;
// export default {
//   namespaced: true,
//   state: {
//     fieldList: ["gigi"],
//     toolToShow: "field",
//     queryParameters: {},
//   },
//   getters: {
//     getFieldList(state: any) {
//       return state.fieldList;
//     },
//     getToolToShow(state: any) {
//       return state.toolToShow;
//     },
//     getQueryParameters(state: any) {
//       return state.queryParameters;
//     },
//   },
//   mutations: {
//     updateFieldList(state: any, newList: any) {
//       state.fieldList = newList;
//       console.log("UPDATE invoked, new list=");
//       console.log(state.fielList);
//     },
//     updateToolToShow(state: any, newTool: string) {
//       if (newTool != "") {
//         state.toolToShow = newTool;
//       }
//     },
//     updateQueryParameters(state: any, newParameters: any) {
//       state.queryParameters = newParameters;
//     },
//   },
// };
