<template>
  <div class="container">
    <div class="title_bar">
      <h1>
        GeCo Agent
        <font-awesome-icon class="icon" :icon="['fas', 'dna']" size="1x" />
      </h1>
      <div class="reset_button">
        <font-awesome-icon class="icon" :icon="['fas', 'redo']" size="2x" />
        Reset
      </div>
    </div>

    <div class="grid_container_upper_row">
      <chat @emit-send="sendMessage()" :textMessage.sync="message"></chat>
      <functions-area></functions-area>
      <toolbox :concatenateToMessage="concatenateToMessage"></toolbox>
    </div>
    <div class="grid_container_lower_row">
      <div class="prova pane_border box_pane">
        <div class="data_selection_box">
          <div>
            Data Selection
          </div>
          <font-awesome-icon
            class="download_icon"
            :icon="['fas', 'download']"
            size="1x"
            @click="downloadFile(linkList, 'esempio.txt', 'text/plain')"
            v-if="isDownloadButtonVisible"
          />
        </div>
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

const socket = io('/test', { path: '/geco_agent/socket.io' });
// const socket = io('http://localhost:5980/test');
const tools = namespace('tools');
const gecoAgentStore = namespace('gecoAgent');
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
  @gecoAgentStore.State('lastMessageId') lastMessageId!: number;

  @tools.Mutation updateFieldList!: (newList: any) => void;
  @tools.Mutation updateQueryParameters!: (newTool: string) => void;
  @conversationStore.Mutation addUserMessage!: (msg: string) => void;
  @conversationStore.Mutation editMessage!: (msg: string) => void;
  @conversationStore.Mutation setSendButtonStatus!: (newValue: boolean) => void;

  @conversationStore.Mutation('parseJsonResponse') messageParser!: (
    msg: MessageObject
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
  @gecoAgentStore.Mutation updateLastMessageId!: (newValue: number) => void;

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
  isDownloadButtonVisible = false;
  linkList!: any;
  messageTypes = [
    // { typeName: 'query', nameSpace: 'gecoAgent/queryParameters' },
    { typeName: 'message', nameSpace: 'gecoAgent/conversation' },
    { typeName: 'select_annotations', nameSpace: 'tools' }
  ];

  jsonResponseParsingFunctions = {
    message: this.unlockButtonAndParseMessage,
    parameters_list: this.parameterParser,
    available_choices: this.availableChoicesParser,
    tools_setup: this.addRemoveTools,
    data_summary: this.setCharts,
    dataset_download: this.updateFileToDownload
  };

  updateFileToDownload(payload: any) {
    console.log('UPDATE LINK', payload);
    this.linkList = payload.urls;
    this.isDownloadButtonVisible = true;
  }

  unlockButtonAndParseMessage(msg: MessageObject) {
    console.log('unlockButtonAndParseMessage invoked');
    this.setSendButtonStatus(true);
    this.messageParser(msg);
  }

  created() {
    socket.emit('ack', { message_id: this.lastMessageId });
    socket.on('json_response', (payload: any) => {
      if (payload.type) {
        console.log('server sent JSON_response', payload);
        this.parseResponse(payload);
      } else {
        console.log('ERRORE STRANO', payload);
      }
    });
  }

  sendMessage() {
    if (this.message != '') {
      this.setSendButtonStatus(false);
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
    this.updateLastMessageId(data.message_id);
    socket.emit('ack', { message_id: this.lastMessageId });
    // @ts-ignore
    this.jsonResponseParsingFunctions[data.type](data.payload);
  }

  pushBotMessage(msg: string) {
    if (msg != '') {
      conversation.push({ sender: 'bot', text: msg });
    }
  }

  downloadFile(content: any, fileName: string, contentType: string) {
    var a = document.createElement('a');
    var file = new Blob([content], { type: contentType });
    a.href = URL.createObjectURL(file);
    a.download = fileName;
    a.click();
    // Per chiamarla:
    // this.downloadFile(this.message, 'esempio.txt', 'text/plain');
  }
}
</script>
<style scoped>
@import '../style/base.scss';
.container {
  height: 95vh;
  overflow: hidden;
}

.title_bar {
  display: inline-grid;
  grid-template-columns: 90% 10%;
  width: 100%;
}

.reset_button {
  float: right;
  display: inline;
  margin: auto;
  font-weight: bold;
}

.grid_container_upper_row {
  display: inline-grid;
  grid-template-columns: 25% 24% 50%;
  grid-gap: 10px;
  height: 60vh;
  width: 80%;
}

.grid_container_lower_row {
  display: inline-grid;
  margin-top: 15px;
  grid-template-columns: 49.7% 50%;
  grid-gap: 10px;
  height: 15%;
  width: 80%;
}

.data_selection_box {
  width: 100px;
  position: relative;
  border: solid 3px #0b3142;
  border-radius: 5px;
  padding: 20px;
  float: left;
  margin-left: 10px;
  font-weight: bold;
}

.prova {
  display: flex;
  width: 100%;
  align-items: center;
}

.download_icon {
  position: absolute;
  bottom: 3px;
  right: 3px;
}
</style>
