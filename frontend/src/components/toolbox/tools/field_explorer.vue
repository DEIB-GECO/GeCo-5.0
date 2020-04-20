<template>
  <div>
    <h1>Fields Explorer</h1>
    <div class="list_container">
      <ul>
        <li v-for="element in fieldList" :key="element.field">
          {{ element.field }}
          <ul>
            <li
              v-for="item in element.values"
              :key="item"
              @click="elementClicked(item)"
            >
              {{ item }}
            </li>
          </ul>
        </li>
      </ul>
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

import { fieldList } from "../../../test/field_list";

export default Vue.extend({
  data() {
    return {
      fieldList,
    };
  },
  props: {
    copyName: {
      type: Function,
    },
  },
  methods: {
    elementClicked(msg: string) {
      this.copyName(msg);
    },
  },
});
</script>
<style scoped lang="scss">
@import "../../../style/base.scss";
.list_container {
  height: 80%;
  text-align: left;
  overflow: auto;
}
</style>
