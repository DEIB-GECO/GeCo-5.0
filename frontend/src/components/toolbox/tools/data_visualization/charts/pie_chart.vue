<template>
  <div class="chart_container">
    <div class="piechart_title">{{ chartTitle }}</div>
    <div :id="chartDivId"></div>
  </div>
</template>

<script lang="ts">
import { Component, Vue, Prop, Watch } from 'vue-property-decorator';
import { select, event } from 'd3-selection';
import { scaleOrdinal } from 'd3-scale';
import { schemeCategory10 } from 'd3-scale-chromatic';
import { pie, arc, PieArcDatum } from 'd3-shape';
// import { entries } from 'd3-collection';
import { sum } from 'd3-array';
import makeid from '@/utils/makeid';

interface PieData {
  label: string;
  value: number;
}

const d3 = Object.assign(
  {},
  {
    select,
    scaleOrdinal,
    pie,
    arc
    // entries
  }
);

@Component
export default class PieChart extends Vue {
  @Prop({
    // default: () => [
    //   { value: 'primo', count: 4 },
    //   { value: 'secondo', count: 5 },
    //   { value: 'terzo', count: 2 },
    //   { value: 'terzo2', count: 2 },
    //   { value: 'terzo3', count: 3 },
    //   { value: 'quarto', count: 5 }
    // ]
  })
  chartData!: any[];

  chartDivId!: string;

  @Prop({
    // default: () => 'title'
  })
  chartTitle!: string;

  @Watch('chartData')
  dataChanged() {
    const svg = d3.select<Element, PieData>('#' + this.chartDivId);
    svg.selectAll('*').remove();
    this.plotPie();
  }

  width = 200;
  height = 200;
  margin = 10;

  created() {
    this.chartDivId = 'pie_' + makeid(8);
  }

  // deatiled guide: https://codepen.io/thecraftycoderpdx/pen/jZyzKo
  plotPie() {
    const data = this.chartData.map((x) => {
      return {
        label: x.value,
        value: x.count
      };
    });
    const radius = Math.min(this.width, this.height) / 2 - this.margin;

    const svg = d3.select<Element, PieData>('#' + this.chartDivId);
    const g = svg
      .append('svg')
      .attr('width', this.width)
      .attr('height', this.height)
      .append('g')
      .attr('transform', `translate(${this.width / 2}, ${this.height / 2})`);

    //const color = d3.scaleOrdinal(['#941946', '#164ba4', '#fbacc9', '#a2f0fb']);
    const color = d3.scaleOrdinal(schemeCategory10);
    // const color = d3.scaleOrdinal([
    //   '#5ca4a9',
    //   '#e6ebe0',
    //   '#ed6a5a',
    //   '#9bc1bc',
    //   '#f4f1bb'
    // ]);
    // const color = d3.scaleOrdinal([
    //   '#1B998B',
    //   '#54457F',
    //   '#D62828',
    //   '#3D314A',
    //   '#F77F00',
    //   '#335C81',
    //   '#FCBF49',
    //   '#465362',
    //   '#F87060'
    // ]);
    // const color = d3.scaleOrdinal(schemeCategory10);
    const myPie = d3.pie<PieData>().value(function(d) {
      return d.value;
    });

    //PETER

    const tooltip = d3
      .select('#' + this.chartDivId) // select element in the DOM with id 'chart'
      .append('div') // append a div element to the element we've selected
      .attr('class', 'tooltip'); // add class 'tooltip' on the divs we just selected

    tooltip
      .append('div') // add divs to the tooltip defined above
      .attr('class', 'label'); // add class 'label' on the selection

    tooltip
      .append('div') // add divs to the tooltip defined above
      .attr('class', 'count'); // add class 'count' on the selection

    tooltip
      .append('div') // add divs to the tooltip defined above
      .attr('class', 'percent'); // add class 'percent' on the selection

    //FINE peter

    const path = d3
      .arc<PieArcDatum<PieData>>()
      .outerRadius(radius - 10)
      .innerRadius(0);

    const label = d3
      .arc<PieArcDatum<PieData>>()
      .outerRadius(radius)
      .innerRadius(radius - 80);

    const arc = g
      .selectAll('.arc')
      .data(myPie(data))
      .enter()
      .append('g')
      .attr('class', 'arc');

    arc
      .append('path')
      .attr('d', path)
      .attr('fill', function(d) {
        return color(d.data.label);
      });

    //PETER
    // mouse event handlers are attached to path so they need to come after its definition
    arc.on('mouseover', function(d) {
      // when mouse enters div
      const total = sum(
        data.map(function(d) {
          // calculate the total number of tickets in the dataset
          return d.value; // checking to see if the entry is enabled. if it isn't, we return 0 and cause other percentages to increase
        })
      );
      const percent = Math.round((1000 * d.data.value) / total) / 10; // calculate percent
      tooltip.select('.label').html(d.data.label); // set current label
      tooltip.select('.count').html(d.data.value + ' '); // set current count
      tooltip.select('.percent').html(percent + '%'); // set percent calculated above
      tooltip.style('display', 'block'); // set display
    });

    arc.on('mouseout', function() {
      // when mouse leaves div
      tooltip.style('display', 'none'); // hide tooltip for that element
    });

    arc.on('mousemove', function(d) {
      // when mouse moves
      tooltip
        .style('top', event.pageY + 10 + 'px') // always 10px below the cursor
        .style('left', event.pageX + 10 + 'px'); // always 10px to the right of the mouse
    });
    //FINE PETER

    // arc
    //   .append('text')
    //   .attr('transform', function(d) {
    //     return `translate(${label.centroid(d)})`;
    //   })
    //   .text(function(d) {
    //     return d.data.label;
    //   });
  }

  mounted() {
    this.plotPie();
  }
}
</script>

<style lang="scss">
.chart_container {
  border: solid 1px #0b3142;
  // overflow: auto;
  position: relative;
  max-height: 230px;
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
