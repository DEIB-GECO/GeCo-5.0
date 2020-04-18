<template>
  <div class="dataset_list">
    <pop-up v-if="isPopUpVisible" @hidePopUp="isPopUpVisible = false"></pop-up>
    <!-- <pop-up v-if="isPopUpVisible" @hidePopUp="isPopupVisible = false"></pop-up> -->
    <h2>Dataset List</h2>
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

export default Vue.extend({
  data() {
    return {
      isPopUpVisible: false
    };
  },
  props: {
    copyName: {
      type: Function
    }
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
    }
  },
  components: {
    PopUp
  }
});
</script>

<style scoped lang="scss">
.dataset_list {
  height: 100%;
}

.list_item {
  padding-top: 10px;
  padding-top: 10px;
  padding-left: 3%;
  padding-right: 3%;

  margin-left: 5%;
  margin-right: 5%;

  height: 5%;

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
