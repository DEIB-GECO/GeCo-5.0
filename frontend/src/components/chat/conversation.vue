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
import Vue from 'vue';
import Message from './message.vue';

import { mapState } from 'vuex';

export default Vue.extend({
  computed: {
    ...mapState({
      conversation: (state: any) => state.gecoAgent.conversation.conversation
    })
  },
  components: {
    Message
  },
  methods: {
    scrollToEnd: function() {
      const container = this.$el.querySelector('#chat');
      // console.log(container);
      if (container) {
        container.scrollTop = container.scrollHeight;
      }
    }
  },
  updated: function() {
    // console.log('chiamato updated');
    this.scrollToEnd();
  },
  mounted: function() {
    this.$nextTick(function() {
      this.scrollToEnd();
    });
  }
});
</script>

<style scoped lang="scss">
@import '../../style/base.scss';

.chat {
  display: grid;
  margin: auto;
  overflow-y: auto;
  overflow-x: hidden;
  max-height: 49vh;
  padding: 10px;
}

// ::-webkit-scrollbar {
//   width: 10px;
// }

// /* Track */
// ::-webkit-scrollbar-track {
//   border-radius: 5px;
//   /* background: #f1f1f1;*/
//   /* background: white; */
// }

// /* Handle */
// ::-webkit-scrollbar-thumb {
//   background: #d2d9dc;
//   border-radius: 5px;
// }

// /* Handle on hover */
// ::-webkit-scrollbar-thumb:hover {
//   background: #a6b4ba;
// }
</style>
