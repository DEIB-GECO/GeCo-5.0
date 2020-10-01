interface HistDistData extends ChartData {
  data: number[];
  options: {
    showHist: boolean;
    showDist: boolean;
  };
}
