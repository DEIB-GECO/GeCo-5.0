<template>
  <div class="metadata_table_container">
    <table>
      <thead>
        <th>
          Id
        </th>
        <th
          v-for="(item, column, index) in tableData[
            Object.keys(tableData)[0]
          ]"
          :key="index + item"
        >
          {{ column }}
        </th>
      </thead>
      <tbody>
        <tr v-for="(row, key, index) in tableData" :key="index">
          <td>{{ key }}</td>
          <td v-for="value in row" :key="value">{{ value }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script lang="ts">
import { Component, Vue, Prop } from 'vue-property-decorator';
import { namespace } from 'vuex-class';

const tableStore = namespace('gecoAgent/TableViewer');

@Component({})
export default class TableViewer extends Vue {
  @tableStore.State tableData!: TableDictionary;
  //TODO: implement options
  @tableStore.State options!: TableOptions;

  shortTable!: TableDictionary;

  created() {
    // if(this.tableData.keys.length < 100){
    //   this.shortTable = this.tableData;
    // } else {
    //   const filteredKeys = Object.keys(this.tableData).slice(0,100);
    //   this.shortTable = {}
    //   for(const el of filteredKeys){
    //     this.shortTable[el] = this.tableData[el];
    //   }
    // }
    // const filteredKeys = Object.keys(this.tableData).slice(0,100);
    // console.log("KEYS", filteredKeys);
    // console.log("KEYS", this.tableData);
    // this.shortTable = {}
    // for(const el of filteredKeys){
    //   this.shortTable[el] = this.tableData[el];
    // }
    // console.log('TABLE', this.shortTable, typeof this.tableData);
  }
}
</script>

<style scoped lang="scss">
@import '@/style/base.scss';
.metadata_table_container {
  overflow: auto;
  //   height: 60%;
  table {
    margin: auto;
    margin-top: 0;
    border-collapse: separate;
  }
  thead {
    border: 3px solid #ddd;
    margin: 0;
  }

  th {
    position: sticky;
    top: 0px;
    background-color: white;
    border: 3px solid #ddd;
    padding: 10px;
    margin: 0;
  }

  td {
    border: 1px solid #ddd;
    padding: 8px;
    border-spacing: 0;
  }

  tr:nth-child(even) {
    background-color: #f2f2f2;
  }

  tr:hover {
    background-color: #ddd;
  }
}
</style>
