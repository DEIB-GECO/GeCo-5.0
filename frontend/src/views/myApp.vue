<template>
  <div>
    <h1>First draft of the Chat!</h1>
    <chat></chat>
  </div>
</template>


<script lang="ts">
import Chat from "./../components/chat/chat_interface.vue";
import Vue from "vue";

export default Vue.extend({
  components: {
    Chat
  }
});
</script>
<style scoped>
</style>