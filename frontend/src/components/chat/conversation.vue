<template>
  <div>
    <div class="chat" id="chat">
      <div
        v-for="item in conversation"
        :key="item.id"
        :class="['chat_line', item.sender]"
      >
        <div class="icon_container">
          <!-- <img src="./../../assets/logo.png" alt class="icon" /> -->
          <font-awesome-icon
            class="icon"
            :icon="['fas', item.sender == 'user' ? 'user-astronaut' : 'robot']"
            size="2x"
          />
        </div>
        <div class="message_box">{{ item.text }}</div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Vue, Prop } from 'vue-property-decorator';
import { namespace } from 'vuex-class';

const conversationStore = namespace('gecoAgent/conversation');

@Component({})
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

.chat_line {
  display: flex;
  height: fit-content;
}

.message_box {
  width: fit-content;
  max-width: 300px;
  padding: 20px;
  border-radius: 10px;
  margin-bottom: 10px;
  text-align: left;
}

.icon_container {
  display: flex;
  align-items: center;
}

.icon {
  height: 40px;
}

.user {
  flex-direction: row-reverse;

  .icon {
    margin-left: 10px;
  }

  .message_box {
    color: white;
    background-color: #187795;
    // text-align: right;
  }
}

.bot {
  flex-direction: row;

  .icon {
    margin-right: 10px;
  }

  .message_box {
    color: white;
    background-color: #38686a;
    // text-align: left;
  }
}
</style>
