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
import { entries } from 'd3-collection';
import { sum, histogram, min, max } from 'd3-array';
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
    entries,
    histogram,
    min,
    max,
    axisBottom,
    axisLeft
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

  width = 200;
  height = 200;
  margin = 10;

  nBin = 10;

  created() {
    this.chartDivId = 'histdist_' + makeid(8);
  }

  // deatiled guide: https://codepen.io/thecraftycoderpdx/pen/jZyzKo
  plotPie() {
    const svg = d3.select<Element, PieData>('#' + this.chartDivId);

    const g = svg
      .append('g')
      .attr('transform', 'translate(' + this.margin + ',' + this.margin + ')');

    const x = scaleLinear<number>().rangeRound([0, this.width]);
    const y = d3.scaleLinear().range([this.height, 0]);

    var histogram = d3
      .histogram()
      .value(function(d) {
        return d.date;
      })
      .domain(x.domain())
      .thresholds(x.ticks(d3.timeMonth));

    console.log('DATA: ', bins);
    console.log('BINS:', bins);

    y.domain([
      0,
      +d3.max(bins, function(d: any) {
        console.log("questo e' d: ", d);
        return d.length;
      })
    ]);

    svg
      .selectAll('rect')
      .data(bins)
      .enter()
      .append('rect')
      .attr('class', 'bar')
      .attr('x', 1)
      .attr('transform', function(d: any) {
        return 'translate(' + x(d.x0) + ',' + y(d.length) + ')';
      })
      .attr('width', function(d: any) {
        return x(d.x1) - x(d.x0) - 1;
      })
      .attr('height', function(d: any) {
        return +this.height - y(d.length);
      });

    svg
      .append('g')
      .attr('transform', 'translate(0,' + this.height + ')')
      .call(d3.axisBottom(x));

    svg.append('g').call(d3.axisLeft(y));

    return svg.node();
  }

  mounted() {
    this.plotPie();
    console.log(this.chartData);
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
