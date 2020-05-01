const choices: AvailableChoice[] = [
  {
    name: 'Name',
    value: 'NAme',
    description:
      'I read the code of popper.js recently. I found you change the algorithm of getting the reference position after the 1.0.8 version. I think the original algorithm still works in this case. when the boundariesNode of popper is body. You didt calculate the offset that from boundariesNode to the offsetParent of popper is the cause of the problem. You could change the code in the getBoundaries function to fix this bug. when the boundariesElement is not viewport, always run this line of code:',
    synonyms: ['fabio', 'pietro', 'sara', 'menne']
  },
  {
    name: 'Long Name',
    value: 'NAme',
    description:
      'I read the code of popper.js recently. I found you change the algorithm of getting the reference position after the 1.0.8 version. I think the original algorithm still works in this case. when the boundariesNode of popper is body. You didt calculate the offset that from boundariesNode to the offsetParent of popper is the cause of the problem. You could change the code in the getBoundaries function to fix this bug. when the boundariesElement is not viewport, always run this line of code:',
    synonyms: ['fabio', 'pietro', 'sara', 'menne']
  },
  {
    name: 'srt',
    value: 'NAme',
    description:
      'I read the code of popper.js recently. I found you change the algorithm of getting the reference position after the 1.0.8 version. I think the original algorithm still works in this case. when the boundariesNode of popper is body. You didt calculate the offset that from boundariesNode to the offsetParent of popper is the cause of the problem. You could change the code in the getBoundaries function to fix this bug. when the boundariesElement is not viewport, always run this line of code:',
    synonyms: ['fabio', 'pietro', 'sara', 'menne']
  },
  {
    name: 'This is a very long name',
    value: 'NAme',
    description:
      'I read the code of popper.js recently. I found you change the algorithm of getting the reference position after the 1.0.8 version. I think the original algorithm still works in this case. when the boundariesNode of popper is body. You didt calculate the offset that from boundariesNode to the offsetParent of popper is the cause of the problem. You could change the code in the getBoundaries function to fix this bug. when the boundariesElement is not viewport, always run this line of code:',
    synonyms: ['fabio', 'pietro', 'sara', 'menne']
  },
  {
    name: 'Oh this is such a long name... Will i stay inside?',
    value: 'NAme',
    description:
      'I read the code of popper.js recently. I found you change the algorithm of getting the reference position after the 1.0.8 version. I think the original algorithm still works in this case. when the boundariesNode of popper is body. You didt calculate the offset that from boundariesNode to the offsetParent of popper is the cause of the problem. You could change the code in the getBoundaries function to fix this bug. when the boundariesElement is not viewport, always run this line of code:',
    synonyms: ['fabio', 'pietro', 'sara', 'menne']
  }
];

export { choices };
