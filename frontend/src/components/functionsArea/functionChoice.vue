<template>
  <div class="functionChoice">
    <div class="search_bar_module">
      <!-- <div class="search_bar_title">Filter:</div> -->
      <div class="search_bar">
        <font-awesome-icon class="search_icon" :icon="['fas', 'search']" />
        <input type="text" />
      </div>
    </div>
    <div class="choice_pane">
      <div class="choice_title">Here you are:</div>
      <div class="choice_list">
        <div v-for="choice in choicesList" :key="choice.name">
          <choice :choice="choice"> </choice>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Vue, Prop } from 'vue-property-decorator';
import { createPopper } from '@popperjs/core';
import Choice from './choice.vue';

@Component({
  components: {
    Choice
  }
})
export default class FunctionsArea extends Vue {
  //   @Prop({required: true})
  @Prop()
  choicesList!: AvailableChoice[];

  created() {
    console.log('CH LIST');
    console.log(this.choicesList);
  }
  // button: any;
  // tooltip: any;
  // showEvents = ['mouseenter', 'focus'];
  // hideEvents = ['mouseleave', 'blur'];

  // createTooltip() {
  //   createPopper(this.button, this.tooltip, {
  //     placement: 'right',
  //     modifiers: [
  //       {
  //         name: 'offset',
  //         options: {
  //           offset: [0, 10]
  //         }
  //       }
  //     ]
  //   });
  // }

  // showTooltip() {
  //   this.tooltip.setAttribute('data-show', '');
  //   console.log('entrato');
  // }

  // hideTooltip() {
  //   this.tooltip.removeAttribute('data-show');
  //   console.log('uscito');
  // }

  // mounted() {
  //   this.button = document.querySelector('#choice');
  //   this.tooltip = document.querySelector('#tooltip');

  //   this.createTooltip();

  //   this.showEvents.forEach((event) => {
  //     this.button.addEventListener(event, this.showTooltip);
  //   });

  //   this.hideEvents.forEach((event) => {
  //     this.button.addEventListener(event, this.hideTooltip);
  //   });
  // }
}
</script>

<style lang="scss">
.search_bar_module {
  width: 90%;
  margin-top: 15px;
  margin-left: 5%;
}

.search_bar {
  display: inline;

  input {
    width: 80%;
  }
}

.choice_pane {
  margin-left: 5px;
}

.choice_list {
  display: block;
  height: 90%;
  // align-content: left;
}

.choice {
  background-color: #0b3142;
  color: white;
  border-width: 0;
  padding: 5px;
  //   text-shadow: 0px -2px #2980b9;
}

#tooltip {
  background-color: #333;
  color: white;
  padding: 5px 10px;
  border-radius: 4px;
  font-size: 13px;
  display: none;
  max-width: 30%;
}

#tooltip[data-show] {
  display: block;
}

#tooltip[data-popper-placement^='top'] > #arrow {
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
