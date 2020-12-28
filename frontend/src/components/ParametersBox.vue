<template>
  <div class="parameters_box">
    <div class="parameter_list">
      <div v-for="parameter in parametersList" :key="parameter.field">
        <span class="parameter_field">{{ parameter.field }}: </span>
        <span>{{ parameter.values.toString() }}</span>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Vue, Prop } from 'vue-property-decorator';
import { namespace, Mutation } from 'vuex-class';

const parametersBoxStore = namespace('gecoAgent/parametersBox');

@Component
export default class Choice extends Vue {
  @parametersBoxStore.State
  parametersList!: Parameter[];
  // parametersList: Parameter[] = [
  //   {
  //     field: 'Marinara',
  //     values: ['a-value-like-13-a-value-like-13-a-value-like-13']
  //   },
  //   {
  //     field: 'Marinara',
  //     values: ['a-value-like-13-a-value-like-13-a-value-like-13']
  //   }
    // {
    //   field: 'Marinara',
    //   values: ['a-value-like-13-a-value-like-13-a-value-like-13']
    // },
    // {
    //   field: 'Marinara',
    //   values: ['a-value-like-13-a-value-like-13-a-value-like-13']
    // }
  ];

  created() {
    // this.setParametersList([
    //   { field: 'Marinara', values: ['a value like 13'] },
    //   { field: 'Margherita', values: ['a value like 1 '] },
    //   { field: 'Napoli', values: ['a value like 12'] }
    // ]);
    // console.log('Parameters Box');
    // console.log(this.parametersList);
    // console.log();
  }
}
</script>

<style lang="scss" scoped>
@import '@/style/base.scss';
.parameters_box {
  height: 100%;
  overflow: auto;
}

.parameter_list {
  //
  // display: flex;
  // flex-direction: column;
  // flex-wrap: wrap;
  // height: 8vh;
  // width: 30vw;
  // column-width: auto;
  text-align: left;
  display: grid;
  grid-template-rows: repeat(2, 1fr);
  grid-auto-flow: column;
  grid-template-columns: repeat(12, 350px);
  margin: 20px;
}

.parameter_field {
  font-weight: bold;
  overflow-wrap: anywhere;
  max-width: 300px;
}
</style>
