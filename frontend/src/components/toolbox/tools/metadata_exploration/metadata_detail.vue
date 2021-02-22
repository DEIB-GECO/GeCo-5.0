<template>
  <div class="metadata_detail">
    <div class="metadata_detail_header">
      <div class="to_previous_button">
        <font-awesome-icon
          class="fa_icon"
          :icon="['fas', 'chevron-left']"
          size="2x"
        ></font-awesome-icon>
        <div class="to_previous_button_text">
          Back to XXX
        </div>
      </div>
      <div class="close_detail_button" @click="emitCloseButton">
        <font-awesome-icon
          class="fa_icon"
          :icon="['fas', 'times-circle']"
          size="2x"
        >
        </font-awesome-icon>
      </div>
    </div>
    <div class="detail_body">
      <h2>Title is:{{ metadataKey }}</h2>
      <div class="metadata_table_container">
        <table>
          <thead>
            <th>
              Value

              <font-awesome-icon
                :icon="isValueCaretDown ? 'caret-down' : 'caret-up'"
                size="1x"
                @click="orderByValue"
              ></font-awesome-icon>
            </th>
            <th>
              count
              <font-awesome-icon
                @click="orderByCount"
                :icon="isCountCaretDown ? 'caret-down' : 'caret-up'"
                size="1x"
              ></font-awesome-icon>
            </th>
          </thead>
          <tbody>
            <tr v-for="pair in valuesList" :key="pair.name">
              <td>{{ pair.name }}</td>
              <td>{{ pair.count }}</td>
            </tr>
          </tbody>
        </table>
      </div>
      <div class="suggestions_box">
        <div class="suggestions_box_title">
          Not satisfied?
        </div>
        <div class="suggestions">
          Try with XXX, YYY, ZZZ
        </div>
      </div>
      <div class="use_this_button" @click="emitCopyName('NAME')">
        Use XXX
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import Vue from 'vue';
import { metadataValuesList } from '../../../../test/metadata_values_list';

export default Vue.extend({
  data() {
    return {
      valuesList: metadataValuesList,
      orderBy: 'value-down',
      isValueCaretDown: false,
      isCountCaretDown: true
    };
  },
  props: {
    metadataKey: {
      type: String
      // default: "",
    },
    copyName: {
      type: Function
    }
  },
  methods: {
    emitCloseButton() {
      this.$emit('closeDetails');
    },
    orderByValue() {
      const greaterNumber = this.isValueCaretDown ? -1 : 1;
      const smallerNumber = -greaterNumber;

      this.valuesList = this.valuesList.sort((a, b) =>
        a.name > b.name ? greaterNumber : smallerNumber
      );

      console.log(this.valuesList);

      this.isValueCaretDown = !this.isValueCaretDown;
    },
    orderByCount() {
      const greaterNumber = this.isCountCaretDown ? -1 : 1;
      const smallerNumber = -greaterNumber;

      this.valuesList = this.valuesList.sort((a, b) =>
        a.count > b.count ? greaterNumber : smallerNumber
      );

      this.isCountCaretDown = !this.isCountCaretDown;
    },
    emitCopyName(msg: string) {
      // console.log(typeof this.functToCall);
      if (this.copyName) {
        this.copyName(msg);
      } else {
        console.log('error-funct not found');
      }
    }
  }
});
</script>

<style scoped lang="scss">
@import '../../../../style/base.scss';
.metadata_detail {
  position: absolute;
  height: 100%;
  width: 100%;
  /* height: inherit; */
  z-index: 100;
  background-color: white;
}

.metadata_detail_header {
  margin-top: 15px;
  margin-bottom: 15px;
  margin-left: 5%;
  margin-right: 5%;
  display: flex;
  justify-content: space-between;
  /* grid-template-columns: 20% 30% auto; */
}

.fa_icon {
  color: #187795;
}

.to_previous_button {
  display: inline-flex;
  align-items: center;
}

.to_previous_button_text {
  margin-left: 10px;
  color: #187795;
}

.detail_body {
  height: 80%;
}

.metadata_table_container {
  overflow: auto;
  height: 60%;
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

.suggestions_box {
  margin-left: 15px;
  margin-top: 10px;
}
.suggestions_box_title {
  text-align: left;
}

.suggestions {
  text-align: left;
}

.use_this_button {
  border: solid 2px #0b3142;
  width: 50%;
  padding: 8px;
  margin: auto;
  margin-top: 10px;
  border-radius: 10px;
}

.use_this_button:hover {
  background-color: #0b3142;
  color: white;
}
</style>
