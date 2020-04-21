<template>
  <div class="container">
    <h1>First draft of the Chat!</h1>
    <div class="grid_container">
      <chat
        @emit-send="sendMessage()"
        :textMessage.sync="message"
        :conversation="conversation"
      ></chat>
      <toolbox :concatenateToMessage="concatenateToMessage"></toolbox>
    </div>
    <!-- <chat @emit-send="sendMessage()" :textMessage.sync="message" :conversation="conversation"></chat> -->
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
    ...mapMutations("tools", ["updateFieldList"]),
    sendMessage: function() {
      if (this.message != "") {
        conversation.push({ sender: "user", text: this.message });
        console.log("I sent: " + this.message);
        socket.emit("my_event", { data: this.message });
        this.message = "";
      }
      // this.message += "ciao";
    },
    concatenateToMessage: function(newPiece: string) {
      // this.updateFieldList([{ field: "Ciao", values: ["uno", "due"] }]);
      this.message += " " + newPiece;
    },
    parseResponse: function(data: any) {
      this.pushBotMessage(data.message);
      console.log("PARSE RESPONSE, type: " + data.type);
      switch (data.type) {
        case "select_annotations":
          console.log("SELECT ANNOTATIONS: " + data.payload);
          this.updateFieldList(data.payload);
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
  /* grid-template-rows: auto; */
  grid-gap: 10px;
  /* background-color: #2196f3; */
  height: 90%;
  width: 80%;
  /* display: flex; */
}
</style>
