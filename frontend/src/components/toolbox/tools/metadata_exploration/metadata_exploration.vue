<template>
  <div class="metadata_exploration">
    <metadata-detail v-if="isDetailVisible"></metadata-detail>
    <div class="metadata_list">
      <h1>metadata exploration</h1>
      <div class="metadata_item">
        <div class="metadata_name">This is a metadatum</div>
        <div class="explore_button_container" @click="isDetailVisible = true">
          <font-awesome-icon
            class="close_icon"
            :icon="['fas', 'chevron-right']"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { library } from "@fortawesome/fontawesome-svg-core";
import { faChevronRight } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";

import MetadataDetail from "./metadata_detail.vue";

library.add(faChevronRight);

export default {
  data() {
    return {
      isDetailVisible: false
    };
  },
  components: {
    FontAwesomeIcon,
    MetadataDetail
  }
};
</script>

<style lang="scss" scoped>
.metadata_exploration {
  height: 100%;
  position: relative;
}

.metadata_list {
  height: 85%;
}

.metadata_item {
  padding-top: 10px;
  padding-top: 10px;
  padding-left: 3%;
  padding-right: 3%;

  margin-left: 5%;
  margin-right: 5%;

  height: 5%;

  border-bottom: solid 1px grey;

  .metadata_name {
    float: left;
  }

  .metadata_name:hover {
    color: #187795;
  }

  .explore_button_container {
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
}
</style>
