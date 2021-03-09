<div class="hist_container">
    <div class="piechart_title">{{ chartTitle }}</div>
    <div :id="chartDivId"></div>
  </div>

<script lang="ts">
import Vue from 'vue';
import { Bar } from 'vue-chartjs';
import { bars, optionsTest } from '@/test/barchart_js';
import { ChartData, ChartOptions } from 'chart.js';

export default Vue.extend({
  // name: 'Histogram',
  extends: Bar,
  props: {
    chartData: {
      default: function() {
        return bars['datasets'][0]['data'];
      },
      type: Object as () => number[]
    },
    myData: {
      default: function() {
        return bars;
      },
      type: Object as () => ChartData
    },
    options: {
      default: function() {
        return optionsTest;
      },
      type: Object as () => ChartOptions
    },
    chartTitle: {
      default: ''
    }
  },
  data() {
    return {
      frequencies: [[0, 0]],
      localData: {
        default: function() {
          return bars;
        },
        type: Object as () => ChartData
      }
    };
  },

  mounted: function() {
    this.computeDiscreteFrequencies(this.chartData);
    // @ts-ignore
    this.renderChart(this.myData, this.options);
  },
  methods: {
    computeFrequencies(numberList: number[]) {
      const map = numberList.reduce((acc: any, e: number) => {
        return acc.set(e, (acc.get(e) || 0) + 1);
      }, new Map());
      const keys: any = Array.from(map.keys()).sort((a: any, b: any) => {
        return a - b;
      });
      const values: any = [];
      keys.forEach((x: number | string) => values.push(map.get(x)));
      if (this.myData.datasets != undefined) {
        this.myData.datasets[0].data = values;
        this.myData.labels = keys;
      }

      // if(this.localData.datasets!= undefined){
      //   this.localData.datasets[0].data = values;
      //   this.localData.labels= keys;
      // }
    },
    computeDiscreteFrequencies(numberList: number[]) {
      const binNumber = Math.ceil(Math.sqrt(numberList.length));
      const min = Math.min(...numberList);
      const max = Math.max(...numberList);
      const step = Math.ceil((max - min) / binNumber);
      const values = [];
      const keys = [];

      let binMin = 0;
      let binMax = 0;
      let filteredArray = [];
      const colorBgArray = [];
      const colorBorderArray = [];

      for (let i = 0; i < binNumber; i++) {
        binMin = i * step + min;
        binMax = Math.min((i + 1) * step + min, max);
        filteredArray = numberList.filter(this.isInInterval(binMin, binMax));
        values.push(filteredArray.length);
        keys.push(binMin.toString() + ' - ' + binMax.toString());
        colorBgArray.push('rgba(75, 192, 192, 0.2)');
        colorBorderArray.push('rgba(75, 192, 192, 1)');
      }

      if (this.myData.datasets != undefined) {
        this.myData.datasets[0].data = values;
        this.myData.labels = keys;
        this.myData.datasets[0].backgroundColor = colorBgArray;
        this.myData.datasets[0].borderColor = colorBorderArray;
        this.myData.datasets[0].label = this.chartTitle;
      }
    },
    isInInterval(min: number, max: number) {
      return (x: number) => {
        return x >= min && x <= max;
      };
    }
  }
});

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
