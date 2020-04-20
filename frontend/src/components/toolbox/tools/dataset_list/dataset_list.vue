<template>
  <div class="dataset_list">
    <pop-up v-if="isPopUpVisible" @hidePopUp="isPopUpVisible = false"></pop-up>
    <!-- <pop-up v-if="isPopUpVisible" @hidePopUp="isPopupVisible = false"></pop-up> -->
    <h2>Dataset List</h2>
    <div v-for="item in datasetList" :key="item" class="list_item">
      <div class="dataset_name" @click="emitCopyName(item)">
        {{ item }}
      </div>
      <div class="info_button"><button @click="showPopUp">i</button></div>
    </div>
    <div class="list_item">
      <div class="dataset_name" @click="emitCopyName('NAME_NAME_NAME')">
        NAME_NAME_NAME
      </div>
      <div class="info_button"><button @click="showPopUp">i</button></div>
    </div>
  </div>
</template>

<script lang="ts">
import Vue from "vue";
import PopUp from "./pop_up.vue";
import { datasetList } from "../../../../test/dataset_list";

export default Vue.extend({
  data() {
    return {
      isPopUpVisible: false,
      datasetList,
    };
  },
  props: {
    copyName: {
      type: Function,
    },
  },
  methods: {
    showPopUp() {
      this.isPopUpVisible = true;
    },
    emitCopyName(msg: string) {
      // console.log(typeof this.functToCall);
      if (this.copyName) {
        this.copyName(msg);
      } else {
        console.log("error-funct not found");
      }
    },
  },
  components: {
    PopUp,
  },
});
</script>

<style scoped lang="scss">
.dataset_list {
  height: 60vh;
  overflow: auto;
}

.list_item {
  padding-top: 10px;
  padding-bottom: 3px;
  padding-left: 3%;
  padding-right: 3%;

  margin-left: 5%;
  margin-right: 5%;

  height: 30px;

  border: solid 2px #187795;
  border-radius: 10px;
}

.dataset_name {
  float: left;
}

.dataset_name:hover {
  color: #187795;
}

.info_button {
  float: right;

  button {
    border-radius: 50%;
    background-color: #fff;
    border: solid 2px #187795;
    font-weight: bold;
  }

  button:hover {
    background-color: #187795;
    color: white;
  }
}
</style>
