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
// import { entries } from 'd3-collection';
import { sum, histogram, min, max, bin, Bin, extent } from 'd3-array';
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
    // pie,
    // arc,
    // entries,
    histogram,
    min,
    max,
    axisBottom,
    axisLeft,
    bin,
    extent
  }
);

@Component
export default class HistDistChart extends Vue {
  @Prop({
    default: () => histDistExampleData
  })
  chartData!: any[];

  chartDivId!: string;

  @Prop({
    default: () => 'title'
  })
  chartTitle!: string;

  //   @Watch('chartData')
  //   dataChanged() {
  //     const svg = d3.select<Element, PieDataPairs>('#' + this.chartDivId);
  //     svg.selectAll('*').remove();
  //     this.plotPie();
  //   }

  width = 400;
  height = 300;
  margin = 40;

  nBin = 10;

  created() {
    this.chartDivId = 'histdist_' + makeid(8);
  }

  // deatiled guide: https://codepen.io/thecraftycoderpdx/pen/jZyzKo
  plotPie() {
    const svg = d3.select<Element, any>('#' + this.chartDivId);

    const g = svg
      .append('svg')
      .attr('width', this.width)
      .attr('height', this.height);
    // .append('g')
    // .attr('transform', `translate(${this.width / 2}, ${this.height / 2})`);

    const bin = d3.bin();
    // .domain([min, max])
    // .thresholds(x.ticks(40));

    const bins = bin(this.chartData);

    const maxBins = d3.max(bins, (d) => d.length);
    const count = this.chartData.length;

    const y = d3
      .scaleLinear()
      .domain([0, maxBins])
      .nice()
      .range([this.height - this.margin, this.margin]);

    const x = d3
      .scaleLinear()
      .domain(d3.extent(this.chartData))
      .nice()
      .range([this.margin, this.width - this.margin]);

    // const yAxis = (g) =>
    //   g
    //     .attr('transform', `translate(${this.margin},0)`)
    //     .call(d3.axisLeft(y).ticks(this.height / 25))
    //     .call((g) => g.select('.domain').remove());

    const yAxis = (g) =>
      g
        .attr('transform', `translate(${this.margin},0)`)
        .call(d3.axisLeft(y).ticks(this.height / 40))
        .call((g) => g.select('.domain').remove());
    // .call((g) =>
    //   g
    //     .select('.tick:last-of-type text')
    //     .clone()
    //     .attr('x', 4)
    //     .attr('text-anchor', 'start')
    //     .attr('font-weight', 'bold')
    //     .text('ciao')
    // );

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
      .attr('x', (d: Bin<any, any>) => x(d.x0) + 1)
      .attr('width', (d: Bin<any, any>) => Math.max(0, x(d.x1) - x(d.x0) - 1))
      .attr('height', (d: Bin<any, any>) => y(0) - y(d.length))
      .attr('y', (d: Bin<any, any>) => y(d.length));

    g.append('g')
      .attr('transform', 'translate(0,' + (this.height - this.margin) + ')')
      .call(d3.axisBottom(x));

    g.append('g').call(yAxis);
    // svg.append("g")
    //   .call(d3.axisLeft(y));

    return svg.node();
  }

  mounted() {
    this.plotPie();
    // console.log(this.chartData);
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
