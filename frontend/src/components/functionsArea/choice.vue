<template>
  <div class="choice_wrapper">
    <button :id="'choice_' + id" class="choice">
      {{ choice.name }}
    </button>
    <div :id="'tooltip_' + id" class="tooltip">
      {{ choice.description }}
      <div id="arrow" data-popper-arrow></div>
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Vue, Prop } from 'vue-property-decorator';
import { createPopper } from '@popperjs/core';
import makeid from '@/utils/makeid';

@Component
export default class Choice extends Vue {
  //   @Prop({required: true})
  @Prop()
  choice!: AvailableChoice;

  id!: string;
  button: any;
  tooltip: any;
  showEvents = ['mouseenter', 'focus'];
  hideEvents = ['mouseleave', 'blur'];

  created() {
    this.id = makeid(8);
  }

  createTooltip() {
    createPopper(this.button, this.tooltip, {
      placement: 'right',
      modifiers: [
        {
          name: 'offset',
          options: {
            offset: [0, 10]
          }
        }
      ]
    });
  }

  showTooltip() {
    this.tooltip.setAttribute('data-show', '');
  }

  hideTooltip() {
    this.tooltip.removeAttribute('data-show');
  }

  mounted() {
    this.button = document.querySelector('#choice_' + this.id);
    this.tooltip = document.querySelector('#tooltip_' + this.id);

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

<style lang="scss">
.choice {
  margin-top: 3px;
  margin-right: 10px;
  background-color: #0b3142;
  color: white;
  border-width: 0;
  padding: 5px;
  max-width: 80%;
  float: left;
  //   text-shadow: 0px -2px #2980b9;
}

.tooltip {
  background-color: #333;
  color: white;
  padding: 5px 10px;
  border-radius: 4px;
  font-size: 13px;
  display: none;
  max-width: 30%;
}

.tooltip[data-show] {
  display: block;
}

.tooltip[data-popper-placement^='top'] > #arrow {
  bottom: -4px;
}

#arrow,
#arrow::before {
  position: absolute;
  width: 4px;
  height: 4px;
  z-index: -1;
}

#arrow::before {
  content: '';
  transform: rotate(45deg);
  background: #333;
}

#tooltip[data-popper-placement^='bottom'] > #arrow {
  top: -4px;
}

#tooltip[data-popper-placement^='left'] > #arrow {
  right: -8px;
}

#tooltip[data-popper-placement^='right'] > #arrow {
  left: -4px;
}
</style>
