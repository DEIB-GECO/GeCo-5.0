<template>
  <div>
    <h1>Fields Explorer</h1>
    <div class="list_container">
      <ul>
        <li v-for="element in oldfieldList" :key="element.field">
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
    </div>
  </div>
</template>

<script lang="ts">
import Vue from "vue";
import { mapState } from "vuex";

import { fieldList } from "../../../test/field_list";

export default Vue.extend({
  data() {
    return {
      oldfieldList: fieldList,
    };
  },
  props: {
    copyName: {
      type: Function,
    },
  },
  computed: {
    ...mapState({
      fieldList: (state: any) => state.tools.fieldList,
    }),
  },
  methods: {
    elementClicked(msg: string) {
      this.copyName(msg);
      // console.log(this.$store.getters["getFieldList"]);
      console.log(this.fieldList);
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
