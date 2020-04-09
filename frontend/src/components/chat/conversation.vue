<template>
  <div>
    <div class="chat" id="chat">
      <message
        v-for="item in conversationHistory"
        :key="item.id"
        :text="item.text"
        :sender="item.sender"
      ></message>
    </div>
  </div>
</template>

<script lang="ts">
import Vue from "vue";
import Message from "./message.vue";

export default Vue.extend({
  props: {
    conversationHistory: {
      type: Array
    }
  },
  components: {
    Message
  }
});
</script>

<style scoped>
.chat {
  display: grid;
  margin: auto;
  overflow-y: auto;
  overflow-x: hidden;
  height: 60vh;
  padding: 10px;
}

::-webkit-scrollbar {
  width: 10px;
}

/* Track */
::-webkit-scrollbar-track {
  border-radius: 5px;
  /* background: #f1f1f1;*/
  /* background: white; */
}

/* Handle */
::-webkit-scrollbar-thumb {
  background: #d2d9dc;
  border-radius: 5px;
}

/* Handle on hover */
::-webkit-scrollbar-thumb:hover {
  background: #a6b4ba;
}
</style>