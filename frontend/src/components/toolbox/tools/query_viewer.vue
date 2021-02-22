<template>
  <div class="query_viewer">
    <h1>Query Parameters</h1>
    <div class="table_container">
      <table>
        <thead>
          <th>Parameter</th>
          <th>Value</th>
        </thead>
        <tbody>
          <tr>
            <td>Name</td>
            <td>{{ queryParameters.name }}</td>
          </tr>
          <tr></tr>
          <tr>
            <td>Data</td>
            <td>{{ queryParameters.data }}</td>
          </tr>
          <tr>
            <td>Assembly</td>
            <td>{{ queryParameters.assembly }}</td>
          </tr>
          <tr>
            <td>Annotation Type</td>
            <td>{{ queryParameters.ann_type }}</td>
          </tr>
          <tr>
            <td>Source</td>
            <td>{{ queryParameters.source }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script lang="ts">
import Vue from 'vue';
import { mapState, mapGetters } from 'vuex';

export default Vue.extend({
  computed: {
    ...mapState({
      queryParameters: (state: any) =>
        state.gecoAgent.queryParameters.queryParameters
    })
  }
});
</script>

<style scoped lang="scss">
.query_viewer {
  height: 100%;
  width: 100%;
}
.table_container {
  overflow: auto;
  height: 80%;
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
