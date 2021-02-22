const fieldList = [
  { field: 'source', values: ['refseq', 'gencode', 'roadmap epigenomics'] },
  {
    field: 'project_name',
    values: [
      'refseq reference genome annotation',
      'comprehensive gene annotation chr',
      'gen10.gtf.gz'
    ]
  },
  {
    field: 'source_site',
    values: [
      'gencode@sanger.ac.uk',
      'gencode-help@sanger.ac.uk',
      'andrea.tanzer@crg.eu'
    ]
  },
  {
    field: 'content_type',
    values: [
      'exon',
      'gene',
      'transcript',
      'cds',
      'selenocysteine',
      'start codon',
      'stop codon',
      'utr',
      'antisense rna',
      'c gene segment',
      'd gene segment',
      'd loop',
      'enhancer',
      'j gene segment',
      'lnc rna',
      'mirna',
      'mrna',
      'ncrna',
      'primary transcript',
      'promoter',
      'region',
      'repeat region',
      'rnase mrp rna',
      'rnase p rna',
      'rrna',
      'sequence feature',
      'snorna',
      'snrna',
      'srp rna',
      'telomerase rna',
      'trna',
      'vault rna',
      'v gene segment',
      'y rna',
      'centromere',
      'intron'
    ]
  },
  { field: 'assembly', values: ['grch38', 'hg19'] },
  {
    field: 'technique',
    values: [
      'refseq annotation',
      'gencode annotation',
      'roadmap epigenomics annotation'
    ]
  }
];

export { fieldList };
