<template>
  <div class="metadata_detail">
    <div class="metadata_detail_header">
      <div class="to_list_button">Back to Metadata</div>
      <div class="to_previous_button">Back to XXX</div>
    </div>
    <div class="detail_body">
      here is the list
    </div>
  </div>
</template>

<script lang="ts">
import Vue from "vue";

export default Vue.extend({});
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
  display: grid;
  grid-template-columns: 20% 30% auto;
}
</style>
