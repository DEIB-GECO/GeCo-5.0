<template>
  <div class="metadata_detail">
    <div class="metadata_detail_header">
      <div class="to_previous_button">
        <font-awesome-icon
          class="fa_icon"
          :icon="['fas', 'chevron-left']"
          size="2x"
        ></font-awesome-icon>
        <div class="to_previous_button_text">
          Back to XXX
        </div>
      </div>
      <div class="close_detail_button" @click="emitCloseButton">
        <font-awesome-icon
          class="fa_icon"
          :icon="['fas', 'times-circle']"
          size="2x"
        >
        </font-awesome-icon>
      </div>
    </div>
    <div class="detail_body">
      here is the list
      <div class="metadata_table">
        <table>
          <thead>
            <th>Value</th>
            <th>count</th>
          </thead>
          <tbody>
            <tr>
              <td>Ciao</td>
              <td>4</td>
            </tr>
            <td>Culo</td>
            <td>3</td>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import Vue from "vue";

import { library } from "@fortawesome/fontawesome-svg-core";
import {
  faTimesCircle,
  faChevronLeft,
} from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";

library.add(faTimesCircle, faChevronLeft);

export default Vue.extend({
  components: {
    FontAwesomeIcon,
  },
  methods: {
    emitCloseButton() {
      console.log("emit close details");
      this.$emit("closeDetails");
    },
  },
});
</script>

<style scoped>
.metadata_detail {
  position: absolute;
  height: 100%;
  width: 100%;
  /* height: inherit; */
  z-index: 100;
  background-color: white;
}

.metadata_detail_header {
  margin-top: 15px;
  margin-bottom: 15px;
  margin-left: 5%;
  margin-right: 5%;
  display: flex;
  justify-content: space-between;
  /* grid-template-columns: 20% 30% auto; */
}

.fa_icon {
  color: #187795;
}

.to_previous_button {
  display: inline-flex;
  align-items: center;
}

.to_previous_button_text {
  margin-left: 10px;
  color: #187795;
}
</style>
