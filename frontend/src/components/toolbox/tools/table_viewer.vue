<template>
  <div class="metadata_table_container">
    <table>
      <thead>
        <th>
          Id

          <!-- <font-awesome-icon
            :icon="isValueCaretDown ? 'caret-down' : 'caret-up'"
            size="1x"
            @click="orderByValue"
          ></font-awesome-icon> -->
        </th>
        <th
          v-for="(item, column, index) in tableData[Object.keys(tableData)[0]]"
          :key="index + item"
        >
          {{ column }}
          <!-- <font-awesome-icon
            @click="orderByCount"
            :icon="isCountCaretDown ? 'caret-down' : 'caret-up'"
            size="1x"
          ></font-awesome-icon> -->
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
import { tableDataTest } from '@/test/table_data.ts';

@Component({})
export default class TableViewer extends Vue {
  @Prop({
    default: () => tableDataTest
  })
  tableData!: any;

  created() {
    console.log('TABLE', this.tableData, typeof this.tableData);
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
