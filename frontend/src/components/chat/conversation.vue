<template>
  <div>
    <div class="chat" id="chat">
      <message
        v-for="item in conversation"
        :key="item.id"
        :text="item.text"
        :sender="item.sender"
      ></message>
    </div>
  </div>
</template>

<script lang="ts">
// import Vue from 'vue';
import Message from './message.vue';

import { Component, Vue, Prop } from 'vue-property-decorator';
import { namespace } from 'vuex-class';

const conversationStore = namespace('gecoAgent/conversation');

import { mapState } from 'vuex';

@Component({
  components: {
    Message
  }
})
export default class Conversation extends Vue {
  @conversationStore.State conversation!: MessageObject[];

  scrollToEnd() {
    const container = this.$el.querySelector('#chat');
    // console.log(container);
    if (container) {
      container.scrollTop = container.scrollHeight;
    }
  }

  updated() {
    // console.log('chiamato updated');
    this.scrollToEnd();
  }

  mounted() {
    this.$nextTick(function() {
      this.scrollToEnd();
    });
  }
}
</script>

<style scoped lang="scss">
@import '../../style/base.scss';

.chat {
  display: grid;
  margin: auto;
  overflow-y: auto;
  overflow-x: hidden;
  max-height: 46vh;
  padding: 10px;
}
</style>
