interface ProcessStep {
  name: string;
  urlList: string[];
  isDownloadButtonVisible: boolean;
  state: 'active' | 'completed';
}
