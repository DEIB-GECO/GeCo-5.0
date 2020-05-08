<template>
  <div class="toolbox_interface">
    <keep-alive>
      <div class="canvas" :is="active" :copyName="sendMessageToConcat"></div>
    </keep-alive>
    <div class="buttons_grid">
      <div
        v-for="tool in activeTools"
        v-bind:key="tool.component"
        :class="[
          'tool',
          active == tool.component ? 'active_tool' : 'inactive_tool'
        ]"
        @click="updateToolToShow(tool.component)"
      >
        {{ tool.name }}
      </div>
    </div>
  </div>
</template>

<script lang="ts">
// import Vue from 'vue';
// import { mapState, mapMutations } from 'vuex';

import { Component, Vue, Prop } from 'vue-property-decorator';
import { namespace } from 'vuex-class';

import DatasetList from './tools/dataset_list/dataset_list.vue';
import MetadataExploration from './tools/metadata_exploration/metadata_exploration.vue';
import FieldExplorer from './tools/field_explorer.vue';
import QueryViewer from './tools/query_viewer.vue';
import DataVisualization from './tools/data_visualization/data_visualization.vue';

const toolsNamespace = namespace('tools');

@Component({
  components: {
    dataset: DatasetList,
    metadata: MetadataExploration,
    field: FieldExplorer,
    query: QueryViewer,
    dataviz: DataVisualization
  }
})
export default class ToolboxInterface extends Vue {
  // tools = [
  //   { name: 'Dataset List', component: 'dataset' },
  //   { name: 'Metadata', component: 'metadata' },
  //   { name: 'Field Explorer', component: 'field' },
  //   { name: 'Query', component: 'query' },
  //   { name: 'Data', component: 'dataviz' }
  // ];

  @toolsNamespace.State('toolToShow') active!: string;
  @toolsNamespace.State activeTools!: string[];

  @Prop()
  concatenateToMessage!: Function;

  @toolsNamespace.Action updateToolToShow!: (newTool: string) => void;

  sendMessageToConcat(msg: string) {
    console.log('sendMessageToConcat invoked');
    if (this.concatenateToMessage) {
      this.concatenateToMessage(msg);
    } else {
      console.log('concat non esiste');
    }
  }
}

// export default Vue.extend({
//   data() {
//     return {
//       // active: "dataset",
//       tools: [
//         { name: 'Dataset List', component: 'dataset' },
//         { name: 'Metadata', component: 'metadata' },
//         { name: 'Field Explorer', component: 'field' },
//         { name: 'Query', component: 'query' },
//         { name: 'Data', component: 'dataviz' }
//       ]
//     };
//   },
//   props: {
//     concatenateToMessage: {
//       type: Function
//     }
//   },
//   computed: {
//     ...mapState({
//       active: (state: any) => state.tools.toolToShow
//     })
//   },
//   methods: {
//     ...mapMutations('tools', ['updateToolToShow']),
//     sendMessageToConcat(msg: string) {
//       console.log('sendMessageToConcat invoked');
//       if (this.concatenateToMessage) {
//         this.concatenateToMessage(msg);
//       } else {
//         console.log('concat non esiste');
//       }
//     }
//   },
//   components: {
//     dataset: DatasetList,
//     metadata: MetadataExploration,
//     field: FieldExplorer,
//     query: QueryViewer,
//     dataviz: DataVisualization
//   }
// });
</script>

<style scoped>
.toolbox_interface {
  height: 100%;
  width: 100%;
}

.canvas {
  height: 85%;
  border: solid 3px #ecebe4;
  /* border: solid 3px #0f5257; */
}

.buttons_grid {
  height: 10vh;
  margin-top: 1%;
  width: 90%;
  display: inline-grid;
  grid-template-columns: auto auto auto auto auto auto;
}

.tool {
  height: 5vh;
  /* margin-left: 2%; */
  color: white;
  border-width: 0;
  border-radius: 20px;
  text-shadow: 0px -2px #2980b9;
  width: 90%;
  /* background-color: #0b3142; */
  padding-top: 3vh;
  padding-bottom: 0;
  /* border-radius: 15px; */
  /* color: white; */
}

.active_tool {
  background-color: #be6e46;
  text-shadow: 0px -2px #c98867;
}

.inactive_tool {
  background-color: #0b3142;
  text-shadow: 0px -2px #2980b9;
}
</style>
