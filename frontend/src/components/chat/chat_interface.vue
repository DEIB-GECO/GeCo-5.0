<template>
  <div class="chat_container">
    <div class="chat" id="chat">
      <div
        v-for="item in conversation"
        :key="item.id"
        :class="['chat_line', item.sender]"
      >
        <div class="icon_container">
          <font-awesome-icon
            class="icon"
            :icon="['fas', item.sender == 'user' ? 'user-astronaut' : 'robot']"
            size="2x"
          />
        </div>
        <div class="message_box">{{ item.text }}</div>
      </div>
    </div>
    <div class="interface">
      <textarea
        name="message_box"
        id="message_box"
        v-model="message"
        @keyup.enter="emitSend()"
      ></textarea>
      <button class="send_button" @click="emitSend()">
        <font-awesome-icon
          class="icon"
          :icon="['fas', 'paper-plane']"
          size="2x"
        />
      </button>
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import { namespace } from 'vuex-class';

const conversationStore = namespace('gecoAgent/conversation');

@Component({})
export default class ChatInterface extends Vue {
  @conversationStore.State('currentMessage') storeMessage!: string;
  @conversationStore.State conversation!: MessageObject[];

  @conversationStore.Mutation editMessage!: (newMsg: string) => void;

  get message() {
    return this.storeMessage;
  }
  set message(newMsg: string) {
    this.editMessage(newMsg);
  }

  emitSend() {
    this.$emit('emit-send');
  }

  scrollToEnd() {
    const container = this.$el.querySelector('#chat');
    console.log(container);
    if (container) {
      container.scrollTop = container.scrollHeight;
    }
  }
  updated() {
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
.chat_container {
  margin: auto;
  margin-bottom: 0vh;
  width: 95%;
}

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
  }
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
  min-width: 40px;
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

::-webkit-scrollbar {
  width: 7px;
}
</style>
