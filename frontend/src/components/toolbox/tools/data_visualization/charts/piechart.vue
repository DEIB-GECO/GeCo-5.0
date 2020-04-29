<template>
  <div>
    <div id="piechart"></div>
    <div id="whatever"></div>
  </div>
</template>

<script lang="ts">
import Vue from "vue";
import { select } from "d3-selection";
import { scaleOrdinal } from "d3-scale";
import { pie, arc } from "d3-shape";
import { entries } from "d3-collection";
// import PieLayout from "D3";s
// import {pie} as pppp from layout;
import * as d3 from "D3";
interface PieData {
  label: string;
  value: number;
}

// const d3 = Object.assign(
//   {},
//   {
//     select: Function,
//   }
// );

export default Vue.extend({
  data() {
    return {
      width: 450,
      height: 450,
      margin: 40,
    };
  },
  props: {
    chartData: {
      type: Array,
      default: () => {
        return [
          { label: "primo", value: 4 },
          { label: "secondo", value: 5 },
          { label: "terzo", value: 2 },
          { label: "quarto", value: 5 },
        ];
      },
    },
  },
  methods: {
    plotPie() {
      // The radius of the pieplot is half the width or half the height (smallest one). I subtract a bit of margin.
      const radius = Math.min(this.width, this.height) / 2 - this.margin;

      //   append the svg object to the div called 'my_dataviz'
      const svg = select("#piechart")
        .append("svg")
        .attr("width", this.width)
        .attr("height", this.height)
        .append("g")
        .attr(
          "transform",
          "translate(" + this.width / 2 + "," + this.height / 2 + ")"
        );

      const dataArray: any = this.chartData.reduce(
        (acc: any, item: any) => ((acc[item.label] = item.value), acc),
        {}
      );
      console.log(dataArray);

      //FINO A QUA

      // set the color scale
      const color = scaleOrdinal()
        // .domain(dataArray)
        .range(["#98abc5", "#8a89a6", "#7b6888", "#6b486b", "#a05d56"]);

      // Compute the position of each group on the pie:
      const myPie = pie().value(function(d: any) {
        return d.value;
      });
      // const dataReady = pie(entries(dataArray));
      const dataReady = pie();
      console.log(dataReady);

      // Build the pie chart: Basically, each part of the pie is a path that we build using the arc function.
      svg
        .selectAll("whatever")
        .data(pie(dataReady))
        .enter()
        .append("path")
        .attr(
          "d",
          arc<any>()
            .innerRadius(0)
            .outerRadius(radius)
        )
        // .attr("fill", (d: any) => {
        //   console.log(d);
        //   return color(d.data.key);
        // })
        .attr("stroke", "black")
        .style("stroke-width", "2px")
        .style("opacity", 0.7);
    },
  },
  mounted() {
    this.plotPie();
  },
});
</script>

<style scoped></style>
