<template>
  <div class="function_canvas">
    <h1>Functions Area</h1>
  </div>
</template>

<script lang="ts">
import { Component, Vue, Prop } from 'vue-property-decorator';

@Component
export default class FunctionsArea extends Vue {
  firstVariable!: number;
}
</script>

<style lang="scss">
.function_canvas {
  height: 100%;
  width: 100%;
  border: solid 3px #ecebe4;
}
</style>
