<template>
  <div class="function_canvas">
    <!-- <h1>Functions Area</h1>
    <h2>{{ viewType }}</h2> -->
    <div class="tips_pane_wrapper" v-if="viewType == 'tip'">
      <div class="tips_pane">
        <div class="title_row">
          <div class="icon_wrapper">
            <font-awesome-icon
              class="tip_icon"
              :icon="['fas', 'lightbulb']"
              size="2x"
            />
          </div>
          <div class="tip_title">
            Tip
          </div>
        </div>
        <div class="tip_content">
          {{ tipContent }}
        </div>
      </div>
    </div>
    <functionChoice v-if="viewType == 'options'"></functionChoice>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import { namespace } from 'vuex-class';
import FunctionChoice from './functionChoice.vue';

const functionsAreaStore = namespace('gecoAgent/functionsArea');

@Component({
  components: {
    FunctionChoice
  }
})
export default class FunctionsArea extends Vue {
  @functionsAreaStore.State
  viewType!: string;

  @functionsAreaStore.State
  tipContent!: string;
}
</script>

<style lang="scss">
.function_canvas {
  height: 100%;
  width: 100%;
  border: solid 3px #ecebe4;
}

.tips_pane_wrapper {
  height: 100%;
  position: relative;
}

.tips_pane {
  position: absolute;
  bottom: 10px;
}

.title_row {
  display: grid;
  grid-template-columns: 25% 75%;
  align-items: center;
}

.tip_icon {
  color: #fdd100;
}

.tip_title {
  text-align: left;
  align-content: center;
  font-size: larger;
  font-weight: bold;
}

.tip_content {
  text-align: left;
  margin-top: 10px;
  margin-right: 15px;
  margin-left: 30px;
}
</style>
