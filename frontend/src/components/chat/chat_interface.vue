<template>
  <div class="chat_container">
    <chat :conversationHistory="conversation"></chat>
    <div class="interface">
      <textarea
        name="message_box"
        id="message_box"
        @change="$emit('update:textMessage', $event.target.value)"
        v-bind:value="textMessage"
      ></textarea>
      <button class="send_button" @click="emitSend()">Send</button>
    </div>
  </div>
</template>

<script lang="ts">
import Message from "./message.vue";
import Chat from "./conversation.vue";
import Vue from "vue";

export default Vue.extend({
  props: {
    textMessage: {
      type: String
    },
    conversation: {
      type: Array
    }
  },
  methods: {
    emitSend() {
      this.$emit("emit-send");
    },
    scrollToEnd: function() {
      const container = this.$el.querySelector("#chat");
      console.log(container);
      if (container) {
        container.scrollTop = container.scrollHeight;
      }
    }
  },
  components: {
    Chat
  },
  updated: function() {
    console.log("chiamato updated");
    this.scrollToEnd();
  }
});
</script>

<style scoped>
.chat_container {
  margin: auto;
}

.interface {
  width: 100%;
  height: 10vh;
  padding: 2%;
  display: flex;
}

.send_button {
  height: 100%;
  width: 13%;
  margin-left: 2%;
  background-color: #0b3142;
  color: white;
  border-width: 0;
  border-radius: 20px;
  text-shadow: 0px -2px #2980b9;
}

#message_box {
  height: 100%;
  width: 85%;
  resize: none;
}

textarea {
  width: 500px;
  border: none;
  border-radius: 20px;
  outline: none;
  padding: 10px;
  font-size: 1em;
  color: #676767;
  transition: border 0.5s;
  -webkit-transition: border 0.5s;
  -moz-transition: border 0.5s;
  -o-transition: border 0.5s;
  border: solid 3px #0b3142;
  -webkit-box-sizing: border-box;
  -moz-box-sizing: border-box;
  box-sizing: border-box;
}
</style>