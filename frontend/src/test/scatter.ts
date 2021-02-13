const scatterTestData = {
    labels: ['Red', 'Blue', 'Yellow', 'Green', 'Purple', 'Orange'],
    datasets: [{
        label: '# of Votes',
        data: [{
            x: -10,
            y: 0,
        }, {
            x: 0,
            y: 10,
        }, {
            x: 10,
            y: 5,
        }
    ],
    backgroundColor: [
        'rgba(255, 99, 132, 0.2)',
        'rgba(255, 99, 132, 0.2)',
        'rgba(255, 99, 132, 0.2)'],
    borderColor: [
        'rgba(255, 99, 132, 1)',
        'rgba(255, 99, 132, 1)',
        'rgba(255, 99, 132, 1)']
    },
    {
        label: '# ',
        data: [{
            x: -13,
            y: 0,
        }, {
            x: 3,
            y: 10,
        }, {
            x: 10,
            y: 2,
        },
    ],
    backgroundColor: [
        'rgba(54, 162, 235, 0.2)',
        'rgba(54, 162, 235, 0.2)',
        'rgba(54, 162, 235, 0.2)'],
    borderColor: [
        'rgba(54, 162, 235, 1)',
        'rgba(54, 162, 235, 1)',
        'rgba(54, 162, 235, 1)']
    }
]
}

const optionsTest =  {
    scales: {
        xAxes: [{
            type: 'linear',
            position: 'bottom'
        }]
    }
}

export {optionsTest, scatterTestData};