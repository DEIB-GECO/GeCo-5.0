<template>
  <div>
    <div class="background" @click="emitHidePopUp"></div>
    <div class="popup_pane">
      <div class="popup_header">
        <div class="close_button_container">
          <div class="close_button" @click="emitHidePopUp">
            <font-awesome-icon
              class="close_icon"
              :icon="['fas', 'times-circle']"
              size="2x"
            />
          </div>
        </div>
        <div class="dataset_name">Dataset Name</div>
      </div>
      <div class="dataset_description">
        <div
          class="dataset_description_line"
          v-for="line in datasetDetail"
          :key="line.name"
        >
          <div class="feature_name">{{ line.name }}</div>
          <div class="feature_description">{{ line.value }}</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import Vue from "vue";

import { datasetDetail } from "../../../../test/dataset_detail";

export default Vue.extend({
  data() {
    return {
      datasetDetail,
    };
  },
  methods: {
    emitHidePopUp() {
      console.log("Emit Hide Pop Up");
      this.$emit("hidePopUp");
    },
  },
});
</script>

<style scoped lang="scss">
.background {
  background: #00000055;
  z-index: 1000;
  width: 100vw;
  height: 100vh;
  position: fixed;
  top: 0;
  left: 0;
}

.popup_pane {
  background-color: white;
  /* opacity: 1; */
  width: 70vw;
  height: 80vh;
  z-index: 1001;
  position: fixed;
  top: 10vh;
  left: 15vw;

  border-radius: 30px;
  border: solid 4px #187795;

  .popup_header {
    .close_button_container {
      // align-content: right;
      width: 97%;
      height: 3vh;
      padding-right: 3%;
      margin-top: 2vh;

      .close_button {
        float: right;

        .close_icon {
          color: #187795;
        }
      }
    }
  }

  .dataset_description {
    width: inherit;
    margin: 5%;
  }

  .dataset_description_line {
    display: grid;
    grid-template-columns: 30% 60%;
    margin-top: 20px;
    text-align: left;
  }
}
</style>
