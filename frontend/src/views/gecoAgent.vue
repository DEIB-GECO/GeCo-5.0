<template>
  <div class="container">
    <h1>
      GeCo Agent
      <font-awesome-icon class="icon" :icon="['fas', 'dna']" size="1x" />
    </h1>
    <div class="grid_container_upper_row">
      <chat @emit-send="sendMessage()" :textMessage.sync="message"></chat>
      <functions-area></functions-area>
      <toolbox :concatenateToMessage="concatenateToMessage"></toolbox>
    </div>
    <div class="grid_container_lower_row">
      <div class="prova pane_border">
        <h1>boxes</h1>
      </div>
      <div class="prova pane_border"><parameters-box></parameters-box></div>
    </div>
  </div>
</template>

<script src="/socket.io/socket.io.js"></script>
<script lang="ts">
import { Component, Vue, Prop } from 'vue-property-decorator';
import { namespace } from 'vuex-class';
import io from 'socket.io-client';
import Chat from './../components/chat/chat_interface.vue';
import FunctionsArea from '../components/functionsArea/functionsArea.vue';
import Toolbox from './../components/toolbox/toolbox_interface.vue';
import ParametersBox from '@/components/ParametersBox.vue';
import { conversation } from './../test/conversation';

const socket = io('http://localhost:5980/test');
const tools = namespace('tools');
const conversationStore = namespace('gecoAgent/conversation');
const parametersStore = namespace('gecoAgent/parametersBox');
const functionsAreaStore = namespace('gecoAgent/functionsArea');
const dataVizStore = namespace('gecoAgent/DataViz');

@Component({
  components: {
    Chat,
    Toolbox,
    FunctionsArea,
    ParametersBox
  }
})
export default class GecoAgent extends Vue {
  @conversationStore.State('currentMessage') message!: string;

  @tools.Mutation updateFieldList!: (newList: any) => void;
  @tools.Mutation updateQueryParameters!: (newTool: string) => void;
  @conversationStore.Mutation addUserMessage!: (msg: string) => void;
  @conversationStore.Mutation editMessage!: (msg: string) => void;

  @conversationStore.Mutation('parseJsonResponse') messageParser!: (
    msg: string
  ) => void;
  @parametersStore.Mutation('setParametersList') parameterParser!: (
    payload: Parameter[]
  ) => void;
  @functionsAreaStore.Mutation('parseJsonResponse')
  availableChoicesParser!: (newChoices: AvailableChoiceJsonPayload) => void;
  @tools.Mutation addSingleToolToPane!: (newTool: string) => void;
  @tools.Mutation removeSingleToolFromPane!: (tool: string) => void;
  @dataVizStore.Mutation setCharts!: (newCharts: DataSummaryPayload) => void;
  @dataVizStore.Action updateToolToShow!: (newTool: string) => void;

  addRemoveTools(jsonPayload: ToolsSetUpPayload) {
    if (jsonPayload.add) {
      jsonPayload.add.forEach((newTool) => {
        this.addSingleToolToPane(newTool);
      });
    }
    if (jsonPayload.remove) {
      jsonPayload.remove.forEach((tool) => {
        this.removeSingleToolFromPane(tool);
      });
    }

    // this.removeToolsFromPane(jsonPayload.remove);
    // this.addToolsToPane(jsonPayload.add);
  }
  conversation?: MessageObject[] = [];
  fieldList = [];
  messageTypes = [
    // { typeName: 'query', nameSpace: 'gecoAgent/queryParameters' },
    { typeName: 'message', nameSpace: 'gecoAgent/conversation' },
    { typeName: 'select_annotations', nameSpace: 'tools' }
  ];

  jsonResponseParsingFunctions = {
    message: this.messageParser,
    parameters_list: this.parameterParser,
    available_choices: this.availableChoicesParser,
    tools_setup: this.addRemoveTools,
    data_summary: this.setCharts
  };

  temporaryFunction(obg: any) {
    console.log('TemporaryFunciton', obg);
  }

  created() {
    socket.on('json_response', (payload: any) => {
      console.log('server sent JSON_response', payload);
      this.parseResponse(payload);
    });
  }

  sendMessage() {
    if (this.message != '') {
      this.addUserMessage(this.message);
      socket.emit('my_event', { data: this.message });
      this.editMessage('');
    }
  }

  concatenateToMessage(newPiece: string) {
    this.message += ' ' + newPiece;
  }

  parseResponse(data: SocketJsonResponse) {
    console.log('PARSE RESPONSE, type: ' + data.type);
    console.log(data);
    if (data.show) {
      this.updateToolToShow(data.show);
    }
    // @ts-ignore
    this.jsonResponseParsingFunctions[data.type](data.payload);
  }

  pushBotMessage(msg: string) {
    if (msg != '') {
      conversation.push({ sender: 'bot', text: msg });
    }
  }
}
</script>
<style scoped>
@import '../style/base.scss';
.container {
  height: 95vh;
  overflow: hidden;
}

.grid_container_upper_row {
  display: inline-grid;
  grid-template-columns: 25% 25% 50%;
  grid-gap: 10px;
  height: 60vh;
  width: 80%;
}

.grid_container_lower_row {
  display: inline-grid;
  margin-top: 15px;
  grid-template-columns: 50% 50%;
  grid-gap: 10px;
  height: 15%;
  width: 80%;
}

.prova {
  width: 100%;
}
</style>
