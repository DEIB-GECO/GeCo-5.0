<template>
  <div class="functionChoice">
    <button id="choice">
      name
    </button>
    <div id="tooltip">
      ciao ciao ciao
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Vue, Prop } from 'vue-property-decorator';
import { createPopper } from '@popperjs/core';

@Component
export default class FunctionsArea extends Vue {
  //   @Prop({required: true})
  @Prop()
  choice!: AvailableChoice;

  button: any;
  tooltip: any;
  showEvents = ['mouseenter', 'focus'];
  hideEvents = ['mouseleave', 'blur'];

  createTooltip() {
    createPopper(this.button, this.tooltip, {
      placement: 'right',
      modifiers: [
        {
          name: 'offset',
          options: {
            offset: [0, 8]
          }
        }
      ]
    });
  }

  showTooltip() {
    this.tooltip.setAttribute('data-show', '');
    console.log('entrato');
  }

  hideTooltip() {
    this.tooltip.removeAttribute('data-show');
    console.log('uscito');
  }

  mounted() {
    this.button = document.querySelector('#choice');
    this.tooltip = document.querySelector('#tooltip');

    this.createTooltip();

    this.showEvents.forEach((event) => {
      this.button.addEventListener(event, this.showTooltip);
    });

    this.hideEvents.forEach((event) => {
      this.button.addEventListener(event, this.hideTooltip);
    });
  }
}
</script>

<style>
#tooltip {
  background-color: #333;
  color: white;
  padding: 5px 10px;
  border-radius: 4px;
  font-size: 13px;
  /* display: none; */
}

#tooltip[data-show] {
  display: block;
}
</style>
