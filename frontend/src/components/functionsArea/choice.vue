<template>
  <div class="choice_wrapper">
    <button
      :id="'choice_' + id"
      class="choice"
      @click="concatenateToMessage(choice.value)"
    >
      {{ choice.name }}
    </button>
    <div :id="'tooltip_' + id" class="tooltip" v-show="showDetails">
      {{ choice.description }}
      <!-- <div id="arrow" data-popper-arrow></div> -->
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Vue, Prop } from 'vue-property-decorator';
import { namespace, Mutation } from 'vuex-class';
import { createPopper } from '@popperjs/core';
import makeid from '@/utils/makeid';

const conversationStore = namespace('gecoAgent/conversation');
const functionsAreaStore = namespace('gecoAgent/functionsArea');

@Component
export default class Choice extends Vue {
  //   @Prop({required: true})
  @Prop()
  choice!: AvailableChoice;

  @functionsAreaStore.State
  showDetails!: boolean;

  @conversationStore.Mutation
  concatenateToMessage!: (newPiece: string) => void;

  id!: string;
  button: any;
  tooltip: any;
  showEvents = ['mouseenter', 'focus'];
  hideEvents = ['mouseleave', 'blur'];
  popperInstance!: any;

  created() {
    this.id = makeid(8);
  }

  createTooltip() {
    this.popperInstance = createPopper(this.button, this.tooltip, {
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
    this.createTooltip();
  }

  hideTooltip() {
    this.tooltip.removeAttribute('data-show');
    this.destroyTooltip();
  }

  destroyTooltip() {
    if (this.popperInstance) {
      this.popperInstance.destroy();
      this.popperInstance = null;
    }
  }

  mounted() {
    this.button = document.querySelector('#choice_' + this.id);
    this.tooltip = document.querySelector('#tooltip_' + this.id);

    if (this.showDetails) {
      this.createTooltip();

      this.showEvents.forEach((event) => {
        this.button.addEventListener(event, this.showTooltip);
      });

      this.hideEvents.forEach((event) => {
        this.button.addEventListener(event, this.hideTooltip);
      });
    }
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
