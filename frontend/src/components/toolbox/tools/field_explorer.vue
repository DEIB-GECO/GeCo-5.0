<template>
  <div>
    <h1>Fields Explorer</h1>
    <div class="list_container">
      <ul>
        <li>
          Field 1
          <ul>
            <li @click="elementClicked('ciao')">1.1</li>
            <li>1.2</li>
          </ul>
        </li>
      </ul>
    </div>
  </div>
</template>

<script lang="ts">
import Vue from "vue";

export default Vue.extend({
  methods: {
    elementClicked(msg: string) {
      this.copyName(msg);
    },
  },
  props: {
    copyName: {
      type: Function,
    },
  },
});
</script>
<style scoped>
.list_container {
  text-align: left;
}
</style>
