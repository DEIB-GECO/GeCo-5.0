<template>
  <div class="functionChoice">
    <div class="search_bar_module" v-if="searchBarVisible">
      <!-- <div class="search_bar_title">Filter:</div> -->
      <div class="search_bar">
        <font-awesome-icon class="search_icon" :icon="['fas', 'search']" />
        <input type="text" v-model="searchBarContent" />
      </div>
    </div>
    <div class="choice_pane">
      <div class="choice_pane_header">
        <div id="help_icon" class="help_button_container" v-if="showHelpIcon">
          <font-awesome-icon
            class="info_icon"
            :icon="['fas', 'question-circle']"
          />
        </div>
        <div class="choice_title">{{ choicesTitle }}</div>
      </div>
      <div class="help_tooltip" id="help_tooltip">
        {{ helpContent }}
      </div>
      <div class="choice_list">
        <!-- <div v-for="choice in filteredChoices" :key="choice.name"> -->
        <!-- <div v-for="choice in choicesArray" :key="choice.name"> -->
        <choice
          v-for="choice in filteredChoices"
          :key="choice.name"
          :choice="choice"
        >
        </choice>
        <!-- </div> -->
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import { namespace } from 'vuex-class';
import { createPopper } from '@popperjs/core';
import Choice from './choice.vue';
// import { choices } from '@/test/choices';

const functionsAreaStore = namespace('gecoAgent/functionsArea');

@Component({
  components: {
    Choice
  }
})
export default class FunctionsArea extends Vue {
  searchBarContent = '';
  helpButton: any;
  tooltip: any;
  showEvents = ['mouseenter', 'focus'];
  hideEvents = ['mouseleave', 'blur'];

  @functionsAreaStore.State
  choicesArray!: AvailableChoice[];
  // choicesArray!: AvailableChoice[];

  @functionsAreaStore.State
  searchBarVisible!: boolean;

  @functionsAreaStore.State
  choicesTitle!: string;

  @functionsAreaStore.State
  showHelpIcon!: boolean;

  @functionsAreaStore.State
  helpContent!: string;

  get filteredChoices(): AvailableChoice[] {
    if (!this.searchBarVisible || this.searchBarContent === '') {
      return this.choicesArray;
    }
    const newArray = this.choicesArray.filter((element: AvailableChoice) => {
      return this.choiceContainsKeyword(element, this.searchBarContent);
    });
    console.log(newArray);
    // return this.choicesArray;
    return newArray;
  }

  choiceContainsKeyword(choice: AvailableChoice, keyWord: string): boolean {
    const isInTheName = choice.name.includes(keyWord);

    const filteredSynonims = choice.synonyms
      ? choice.synonyms.filter((item) => {
          return item.includes(keyWord);
        })
      : [];
    const isInTheSynonims = filteredSynonims.length > 0;
    // const isInTheSynonims = true;

    return isInTheName || isInTheSynonims;
  }

  createTooltip() {
    createPopper(this.helpButton, this.tooltip, {
      placement: 'bottom',
      modifiers: [
        {
          name: 'offset',
          options: {
            offset: [0, 5]
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
    this.helpButton = document.querySelector('#help_icon');
    this.tooltip = document.querySelector('#help_tooltip');
    if (this.showHelpIcon) {
      this.createTooltip();

      this.showEvents.forEach((event) => {
        this.helpButton.addEventListener(event, this.showTooltip);
      });

      this.hideEvents.forEach((event) => {
        this.helpButton.addEventListener(event, this.hideTooltip);
      });
    }
  }

  updated() {
    this.helpButton = document.querySelector('#help_icon');
    this.tooltip = document.querySelector('#help_tooltip');
    if (this.showHelpIcon) {
      this.createTooltip();

      this.showEvents.forEach((event) => {
        this.helpButton.addEventListener(event, this.showTooltip);
      });

      this.hideEvents.forEach((event) => {
        this.helpButton.addEventListener(event, this.hideTooltip);
      });
    }
  }
}
</script>

<style lang="scss">
@import '@/style/base.scss';

.functionChoice {
  height: inherit;
  // border: solid 3px #ecebe4;
}
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
  max-height: 55vh;
  overflow: auto;
}

.choice_pane_header {
  margin-top: 10px;
  display: flex;
}

.choice_title {
  margin-left: 5 px;
  font-weight: bold;
}

.info_icon {
  margin: 3px;
}

.choice_list {
  display: block;
  height: 90%;
  overflow: auto;
  // align-content: left;
}

.choice {
  background-color: #0b3142;
  color: white;
  border-width: 0;
  padding: 5px;
  //   text-shadow: 0px -2px #2980b9;
}

#help_tooltip {
  background-color: white;
  border: solid 2px;
  padding: 5px 10px;
  border-radius: 4px;
  font-size: 13px;
  display: none;
  max-width: 30%;
  text-align: left;
  z-index: 100;
}

#help_tooltip[data-show] {
  display: block;
}
</style>
