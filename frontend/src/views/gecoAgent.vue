<template>
  <div class="container">
    <h1>First draft of the Chat!</h1>
    <div class="grid_container_upper_row">
      <chat @emit-send="sendMessage()" :textMessage.sync="message"></chat>
      <functions-area></functions-area>
      <toolbox :concatenateToMessage="concatenateToMessage"></toolbox>
    </div>
    <div class="grid_container_lower_row">
      <div class="prova pane_border">
        <h1>boxes</h1>
      </div>
      <div class="prova pane_border"><h1>parameters</h1></div>
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
import { conversation } from './../test/conversation';

const socket = io('http://localhost:5980/test');
const tools = namespace('tools');
const conversationStore = namespace('gecoAgent/conversation');
const parametersStore = namespace('gecoAgent/queryParameters');
const functionsAreaStore = namespace('gecoAgent/functionsArea');

@Component({
  components: {
    Chat,
    Toolbox,
    FunctionsArea
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
  @parametersStore.Mutation('parseJsonResponse') parameterParser!: (
    payload: any
  ) => void;
  @functionsAreaStore.Mutation('parseJsonResponseXXX')
  availableChoicesParser!: (newChoices: AvailableChoiceJsonPayload) => void;

  // message = '';

  conversation?: MessageObject[] = [];
  fieldList = [];
  messageTypes = [
    { typeName: 'query', nameSpace: 'gecoAgent/queryParameters' },
    { typeName: 'message', nameSpace: 'gecoAgent/conversation' },
    { typeName: 'select_annotations', nameSpace: 'tools' }
  ];

  jsonResponseParsingFunctions = {
    message: this.messageParser,
    parameters_list: this.parameterParser
  };

  functionPaneParsingFunctions = {
    available_choices: this.availableChoicesParser,
    prova2: this.availableChoicesParser
  };

  created() {
    socket.on(
      'function_pane_operation',
      (payload: FunctionPaneOperationJson) => {
        console.log('server sent function_pane_operation ');
        console.log(payload);
        const operationType = payload.type;
        // this.functionPaneParsingFunctions[operationType];
        this.functionPaneParsingFunctions[payload.type](payload.payload);
        // this.availableChoicesParser(payload.payload);
      }
    );
    socket.on('json_response', (payload: any) => {
      console.log(payload);
      console.log('server sent:' + 'json response');
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

  parseResponse(data: any) {
    console.log('PARSE RESPONSE, type: ' + data.type);
    console.log(data);
    switch (data.type) {
      case 'message':
        console.log('MESSAGE ');
        console.log(data);
        this.$store.commit(
          'gecoAgent/conversation/parseJsonResponse',
          data.payload
        );
      case 'select_annotations':
        console.log('SELECT ANNOTATIONS: ' + data.payload);
        this.updateFieldList([data.payload]);
        break;
      case 'query':
        console.log('UPDATE QUERY: ' + data.payload);
        this.updateQueryParameters(data.payload);
        this.$store.commit(
          'gecoAgent/queryParameters/parseJsonResponse',
          data.payload
        );
        break;
      default:
        console.log(data.type + 'not found');
        break;
    }
  }

  pushBotMessage(msg: string) {
    if (msg != '') {
      conversation.push({ sender: 'bot', text: msg });
    }
  }
}

// export default Vue.extend({
//   data() {
//     return {
//       message: '',
//       conversation,
//       fieldList: [],
//       messageTypes: [
//         { typeName: 'query', nameSpace: 'gecoAgent/queryParameters' },
//         { typeName: 'message', nameSpace: 'gecoAgent/conversation' },
//         { typeName: 'select_annotations', nameSpace: 'tools' }
//       ]
//     };
//   },
//   components: {
//     Chat,
//     Toolbox
//   },

//   created: function() {
//     socket.on('my_response', (payload: any) => {
//       // conversation.push({ sender: "Geco", text: payload.data });
//       console.log('server sent:' + 'msg');
//       this.parseResponse(payload.data);
//     });
//     socket.on('json_response', (payload: any) => {
//       console.log(payload);
//       this.parseResponse(payload);
//     });
//   },

//   methods: {
//     ...mapMutations('tools', ['updateFieldList', 'updateQueryParameters']),
//     sendMessage: function() {
//       if (this.message != '') {
//         this.$store.commit(
//           'gecoAgent/conversation/addUserMessage',
//           this.message
//         );
//         console.log('I sent: ' + this.message);
//         socket.emit('my_event', { data: this.message });
//         this.message = '';
//       }
//     },
//     concatenateToMessage: function(newPiece: string) {
//       this.message += ' ' + newPiece;
//     },
//     parseResponse: function(data: any) {
//       console.log('PARSE RESPONSE, type: ' + data.type);
//       console.log(data);
//       switch (data.type) {
//         case 'message':
//           console.log('MESSAGE ');
//           console.log(data);
//           this.$store.commit(
//             'gecoAgent/conversation/parseJsonResponse',
//             data.payload
//           );
//         case 'select_annotations':
//           console.log('SELECT ANNOTATIONS: ' + data.payload);
//           this.updateFieldList([data.payload]);
//           break;
//         case 'query':
//           console.log('UPDATE QUERY: ' + data.payload);
//           this.updateQueryParameters(data.payload);
//           this.$store.commit(
//             'gecoAgent/queryParameters/parseJsonResponse',
//             data.payload
//           );
//           break;
//         default:
//           console.log(data.type + 'not found');
//           break;
//       }
//     },
//     pushBotMessage(msg: string) {
//       if (msg != '') {
//         this.conversation.push({ sender: 'bot', text: msg });
//       }
//     }
//   }
// });
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
  height: 65%;
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
  /* border: solid 3px #ecebe4; */
}
</style>
