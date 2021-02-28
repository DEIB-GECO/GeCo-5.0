
  <div class="hist_container">
    <div class="piechart_title">{{ chartTitle }}</div>
    <div :id="chartDivId"></div>
  </div>

<script lang="ts">
import { Scatter } from 'vue-chartjs';
import {optionsTest, scatterTestData} from "@/test/scatter.ts";
import {ScatterJSON} from "@/test/ScatterJSON.ts";
import Vue from 'vue';

const pointColors = [
            'rgba(255, 99, 132, 0.2)',
            'rgba(54, 162, 235, 0.2)',
            'rgba(255, 206, 86, 0.2)',
            'rgba(75, 192, 192, 0.2)',
            'rgba(153, 102, 255, 0.2)',
            'rgba(255, 159, 64, 0.2)',
            'rgba(12, 202, 74, 0.2)',
            'rgba(46, 71, 86, 0.2)',
            'rgba(127, 178, 133, 0.2)',
            'rgba(130, 32, 74, 0.2)'
        ];
const borderColors = [
            'rgba(255, 99, 132, 1)',
            'rgba(54, 162, 235, 1)',
            'rgba(255, 206, 86, 1)',
            'rgba(75, 192, 192, 1)',
            'rgba(153, 102, 255, 1)',
            'rgba(255, 159, 64, 1)',
            'rgba(12, 202, 74, 1)',
            'rgba(46, 71, 86, 1)',
            'rgba(127, 178, 133, 1)',
            'rgba(130, 32, 74, 1)'
        ];

export default Vue.extend({
    name: 'Scatter',
    // extends: Scatter,
    props:{
        chartData: {
          // type: [ScatterPointJSON],
          default: () => {return ScatterJSON},
        },
        data : {
            default: ()=> {return scatterTestData}
        },
        options : {
            default: ()=> {return optionsTest}
        }
    },
    data: ()=> {
        return{
          dataPoints: {
            datasets: []
          }
        }
    },
  
  mounted () {
  //   this.transformDataset(this.chartData);
  //   console.log("DataPoints", this.dataPoints);
  //   this.renderChart(this.dataPoints, this.options);    
   },
  methods: {
      transformDataset (serverData : ScatterPointJSON[]) {
          const labelsSet = [...new Set(serverData.map(item => item.label))];
          console.log(labelsSet);
          labelsSet.forEach((label, i) => {
            const sameLabelPoints = serverData.filter((point:ScatterPointJSON) => {
              return point.label === label;
            })

            let currentPointColor = pointColors[0];
            let currentBorderColor = borderColors[0];

            if(i<10){
               currentPointColor = pointColors[i];
               currentBorderColor = borderColors[i];
            } else {
              const red = Math.random() * 255;
              const green = Math.random() * 255;
              const blue = Math.random() * 255;
              
              currentPointColor = `rgba(${red}, ${blue}, ${green}, 0.2)`;
              currentBorderColor = `rgba(${red}, ${blue}, ${green}, 1)`;
            }

            const backgroundColorArray = Array(sameLabelPoints.length);
            backgroundColorArray.fill(currentPointColor);

            const borderColorArray = Array(sameLabelPoints.length);
            borderColorArray.fill(currentBorderColor);


            const dataGroup = {
              label: label,
              data: sameLabelPoints,
              backgroundColor: backgroundColorArray,
              borderColor: borderColorArray
            };
            //FIXA
            // this.dataPoints.datasets.push(dataGroup);
            // console.log(label, dataGroup);
          });

          console.log(this.dataPoints);
      }
  }
})

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
