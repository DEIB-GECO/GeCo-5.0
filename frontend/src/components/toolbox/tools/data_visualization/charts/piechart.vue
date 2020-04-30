<template>
  <div>
    <div id="piechart"></div>
  </div>
</template>

<script lang="ts">
import { Component, Vue, Prop } from 'vue-property-decorator';
import { select } from 'd3-selection';
import { scaleOrdinal } from 'd3-scale';
import { pie, arc, PieArcDatum } from 'd3-shape';
import { entries } from 'd3-collection';

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
    arc,
    entries
  }
);

@Component
export default class Piechart extends Vue {
  @Prop({
    default: () => [
      { label: 'primo', value: 4 },
      { label: 'secondo', value: 5 },
      { label: 'terzo', value: 2 },
      { label: 'quarto', value: 5 }
    ]
  })
  chartData!: PieData[];

  width = 450;
  height = 450;
  margin = 40;

  plotPie() {
    const data = this.chartData.map((x) => {
      return {
        label: x.label,
        value: x.value
      };
    });
    const radius = Math.min(this.width, this.height) / 2 - this.margin;

    const svg = d3.select<Element, PieData>('#piechart');
    const g = svg
      .append('svg')
      .attr('width', this.width)
      .attr('height', this.height)
      .append('g')
      .attr('transform', `translate(${this.width / 2}, ${this.height / 2})`);

    const color = d3.scaleOrdinal(['#4daf4a', '#377eb8', '#ff7f00', '#984ea3']);
    const myPie = d3.pie<PieData>().value(function(d) {
      return d.value;
    });

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

    arc
      .append('text')
      .attr('transform', function(d) {
        return `translate(${label.centroid(d)})`;
      })
      .text(function(d) {
        return d.data.label;
      });
  }

  mounted() {
    this.plotPie();
  }
}
</script>

<style scoped></style>
