<template>
  <div class="chart_container">
    <div class="piechart_title">{{ chartTitle }}</div>
    <div :id="chartDivId"></div>
  </div>
</template>

<script lang="ts">
import { Component, Vue, Prop, Watch } from 'vue-property-decorator';
import { select, event } from 'd3-selection';
import { scaleOrdinal, scaleLinear } from 'd3-scale';
import { schemeCategory10 } from 'd3-scale-chromatic';
import { axisBottom, axisLeft } from 'd3-axis';
import { line } from 'd3-shape';

import { sum, histogram, min, max, Bin, extent, bin} from 'd3-array';
import makeid from '@/utils/makeid';
import { histDistExampleData } from '@/test/histDistExampleData';

interface PieDataPairs {
  label: string;
  value: number;
}

const d3 = Object.assign(
  {},
  {
    select,
    scaleOrdinal,
    scaleLinear,
    histogram,
    min,
    max,
    axisBottom,
    axisLeft,
    bin,
    extent,
    line
  }
);

@Component
export default class HistDistChart extends Vue {
  @Prop({
    // default: () => histDistExampleData
    // default: () => [5, 5, 5, 6, 7, 8, 2, 3, 4, 4, 2, 5]
  })
  chartData!: any[];

  chartDivId!: string;

  @Prop({
    default: () => 'title'
  })
  chartTitle!: string;

  frequencyArray: [number, number][] = [];

  @Watch('chartData')
  dataChanged() {
    const svg = d3.select<Element, PieDataPairs>('#' + this.chartDivId);
    svg.selectAll('*').remove();
    this.plotPie();
  }

  width = 400;
  height = 300;
  margin = 40;

  nBin = 10;

  created() {
    this.chartDivId = 'histdist_' + makeid(8);
  }

  // deatiled guide: https://codepen.io/thecraftycoderpdx/pen/jZyzKo
  // guide no. 2: https://www.d3-graph-gallery.com/graph/shape.html#myline
  plotPie() {
    this.frequencyArray = this.computeFrequencies(this.chartData);

    const svg = d3.select<Element, any>('#' + this.chartDivId);

    const g = svg
      .append('svg')
      .attr('width', this.width)
      .attr('height', this.height);

    //Histogram
    const bin = d3.bin();

    const bins = bin(this.chartData);

    const maxBins = d3.max(bins, (d: Array<number>) => d.length);
    const count = this.chartData.length;

    const y = d3
      .scaleLinear()
      .domain([0, maxBins ? maxBins : 0])
      .nice()
      .range([this.height - this.margin, this.margin]);

    const dataDomain = d3.extent(this.chartData)
      ? d3.extent(this.chartData)
      : [0, 1];
    console.log('Data Domain: ', dataDomain);

    const x = d3
      .scaleLinear()
      .domain(dataDomain)
      .nice()
      .range([this.margin, this.width - this.margin]);

    const yAxis = (g: any) =>
      g
        .attr('transform', `translate(${this.margin},0)`)
        .call(d3.axisLeft(y).ticks(this.height / 40))
        .call((g: any) => g.select('.domain').remove());

    console.log('BINS:', bins);

    const xAxis = (g: any) =>
      g
        .attr('transform', `translate(0,${this.height - this.margin})`)
        .call(d3.axisBottom(x).tickSizeOuter(0))
        .call((g: any) =>
          g
            .append('text')
            .attr('x', this.width - this.margin)
            .attr('y', -4)
            .attr('fill', '#000')
            .attr('font-weight', 'bold')
            .attr('text-anchor', 'end')
            .text(this.chartTitle)
        );

    g.append('g')
      .selectAll('rect')
      .data(bins)
      .join('rect')
      .attr('fill', '#444')
      .attr('x', (d: any) => x(d.x0) + 1)
      .attr('width', (d: any) => Math.max(0, x(d.x1) - x(d.x0) - 1))
      .attr('height', (d: any) => y(0) - y(d.length))
      .attr('y', (d: any) => y(d.length));

    //Line plot
    /*
    const xDist = d3
      .scaleLinear()
      .domain(dataDomain)
      .nice()
      .range([this.margin, this.width - this.margin]);

    const yDist = d3
      .scaleLinear()
      .domain([0, 4]) // input
      .range([this.height, 0]); // output

    const lineFunc = d3
      .line()
      .x(function(d) {
        return xDist(d[0]);
      })
      .y(function(d) {
        return yDist(d[1]);
      });

    g.append('path')
      .datum(this.frequencyArray)
      .attr('fill', 'none')
      .attr('stroke', '#187795')
      .attr('stroke-width', 1.5)
      .attr('stroke-linejoin', 'round')
      .attr('d', lineFunc);

    */

    g.append('g')
      .attr('transform', 'translate(0,' + (this.height - this.margin) + ')')
      .call(d3.axisBottom(x));

    g.append('g').call(yAxis);

    console.log('frequencies:', this.frequencyArray);
    console.log('frequencies:', this.frequencyArray);
    return svg.node();
  }

  computeFrequencies(numberList: number[]): Array<[number, number]> {
    const map = numberList.reduce(
      (acc: any, e: any) => acc.set(e, (acc.get(e) || 0) + 1),
      new Map()
    );
    const myArray = [...map.entries()].sort();
    return myArray;
  }

  mounted() {
    this.plotPie();
    this.computeFrequencies(this.chartData);
  }
}
</script>

<style lang="scss">
.chart_container {
  border: solid 1px #0b3142;
  // overflow: auto;
  position: relative;
  max-height: 330px;
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
