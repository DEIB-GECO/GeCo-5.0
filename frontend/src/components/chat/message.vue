<template>
  <div :class="['chat_line', sender]">
    <div class="icon_container">
      <!-- <img src="./../../assets/logo.png" alt class="icon" /> -->
      <font-awesome-icon
        class="icon"
        :icon="['fas', sender == 'user' ? 'user-astronaut' : 'robot']"
        size="2x"
      />
    </div>
    <div class="message_box">{{ text }}</div>
  </div>
</template>

<script lang="ts">
import Vue from "vue";

export default Vue.extend({
  props: {
    sender: {
      type: String,
    },
    text: {
      type: String,
    },
  },
});
</script>

<style scoped lang="scss">
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
