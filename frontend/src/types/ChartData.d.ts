interface ChartData {
  vizType: string;
  title: string;
  data: {
    value: string;
    count: number;
  }[];
  options?: object;
}
