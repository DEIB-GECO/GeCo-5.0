<div class="hist_container">
    <div class="piechart_title">{{ chartTitle }}</div>
    <div :id="chartDivId"></div>
  </div>

<script lang="ts">
import { Bar } from 'vue-chartjs';
import { bars, optionsTest } from '@/test/barchart_js';

export default {
  name: 'Histogram',
  extends: Bar,
  props: {
    chartData: {
      default: () => {
        return bars['datasets'][0]['data'];
      }
    },
    data: {
      default: () => {
        return bars;
      }
    },
    options: {
      default: () => {
        return optionsTest;
      }
    }
  },
  data: () => {
    return {
      frequencies: [[0, 0]]
    };
  },

  mounted() {
    this.computeFrequencies(this.chartData);
    this.renderChart(this.data, this.options);
    // console.log("ciaoooo");
  },
  methods: {
    computeFrequencies(numberList: number[]) {
      const map = numberList.reduce(
        (acc: any, e: number) => acc.set(e, (acc.get(e) || 0) + 1),
        new Map()
      );
      const keys: any = Array.from(map.keys()).sort((a: any, b: any) => {
        return a - b;
      });
      const values: any = [];
      keys.forEach((x: number | string) => values.push(map.get(x)));
      console.log(values);
      this.data.datasets[0].data = values;
      this.data.labels = keys;
    }
  }
};

// import { Component, Vue, Prop, Watch } from 'vue-property-decorator';
// import makeid from '@/utils/makeid';
// import {bars, options} from "@/test/barchart_js";
// import { Bar } from 'vue-chartjs';

// @Component
// export default class ChartJs extends Bar {

//   @Prop({
//      default: () => bars
//        })
//   barsData!: any;

//   @Prop({
//      default: () => options
//   })
//   optionsData!: any;

//   chartDivId!: string;

//   @Prop({
//     default: () => 'title'
//   })
//   chartTitle!: string;

// //   @Watch('chartData')
// //   dataChanged() {
// //   }

// //   created() {
// //     this.chartDivId = 'histdist_' + makeid(8);
// //   }

//   mounted() {
//       this.renderChart(this.barsData, this.optionsData)
//   }
// }
</script>

<style lang="scss">
.hist_container {
  //border: solid 1px #0b3142;
  // overflow: auto;
  position: relative;
  height: 99.5%;
}

.piechart_title {
  padding-top: 10px;
  font-weight: bold;
}

.tooltip {
  // NOTE: the css written here is not recognized for
  // some reason --  use tooltip.style as above!
  background: #eee;
  box-shadow: 0 0 5px #999999;
  color: #333;
  display: none;
  font-size: 18px;
  left: 130px;
  padding: 10px;
  position: fixed;
  text-align: center;
  top: 95px;
  min-width: 80px;
  // max-width: 130px;
  z-index: 10;
}
</style>
