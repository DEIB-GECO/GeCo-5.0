<template>
  <div class="container">
    <h1>First draft of the Chat!</h1>
    <div class="grid_container">
      <chat @emit-send="sendMessage()" :textMessage.sync="message"></chat>
      <toolbox :concatenateToMessage="concatenateToMessage"></toolbox>
    </div>
  </div>
</template>
<script src="/socket.io/socket.io.js"></script>
<script lang="ts">
import Chat from "./../components/chat/chat_interface.vue";
import Toolbox from "./../components/toolbox/toolbox_interface.vue";

import { conversation } from "./../test/conversation";

import Vue from "vue";

import io from "socket.io-client";
import { mapMutations } from "vuex";

const socket = io("http://localhost:5980/test");

export default Vue.extend({
  data() {
    return {
      message: "",
      conversation,
      fieldList: [],
      messageTypes: [
        { typeName: "query", nameSpace: "gecoAgent/queryParameters" },
        { typeName: "message", nameSpace: "gecoAgent/conversation" },
        { typeName: "select_annotations", nameSpace: "tools" },
      ],
    };
  },
  components: {
    Chat,
    Toolbox,
  },

  created: function() {
    socket.on("my_response", (payload: any) => {
      // conversation.push({ sender: "Geco", text: payload.data });
      console.log("server sent:" + "msg");
      this.parseResponse(payload.data);
    });
    socket.on("json_response", (payload: any) => {
      console.log(payload);
      this.parseResponse(payload);
    });
  },

  methods: {
    ...mapMutations("tools", ["updateFieldList", "updateQueryParameters"]),
    sendMessage: function() {
      if (this.message != "") {
        this.$store.commit(
          "gecoAgent/conversation/addUserMessage",
          this.message
        );
        console.log("I sent: " + this.message);
        socket.emit("my_event", { data: this.message });
        this.message = "";
      }
    },
    concatenateToMessage: function(newPiece: string) {
      this.message += " " + newPiece;
    },
    parseResponse: function(data: any) {
      console.log("PARSE RESPONSE, type: " + data.type);
      console.log(data);
      switch (data.type) {
        case "message":
          console.log("MESSAGE ");
          console.log(data);
          this.$store.commit(
            "gecoAgent/conversation/parseJsonResponse",
            data.payload
          );
        case "select_annotations":
          console.log("SELECT ANNOTATIONS: " + data.payload);
          this.updateFieldList([data.payload]);
          break;
        case "query":
          console.log("UPDATE QUERY: " + data.payload);
          this.updateQueryParameters(data.payload);
          this.$store.commit(
            "gecoAgent/queryParameters/parseJsonResponse",
            data.payload
          );
          break;
        default:
          console.log(data.type + "not found");
          break;
      }
    },
    pushBotMessage(msg: string) {
      if (msg != "") {
        this.conversation.push({ sender: "bot", text: msg });
      }
    },
  },
});
</script>
<style scoped>
.container {
  height: 88vh;
  overflow: hidden;
}

.grid_container {
  display: inline-grid;
  grid-template-columns: 30% 70%;
  grid-gap: 10px;
  height: 90%;
  width: 80%;
}
</style>