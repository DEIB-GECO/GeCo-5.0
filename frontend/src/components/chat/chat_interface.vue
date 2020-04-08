<template>
  <div class="chat">
    <message v-for="item in conversation" :key="item.id" :text="item.text" :sender="item.sender"></message>
  </div>
</template>

<script lang="ts">
import Message from "./message.vue";
import Vue from "vue";

import { conversation } from "./../../test/conversation";

export default Vue.extend({
  data() {
    return {
      conversation
    };
  },
  components: {
    Message
  }
});
</script>

<style scoped>
.chat {
  display: grid;
  width: 50%;
  margin: auto;
}
</style>