import * as html from '@hyperapp/html'
import { Chart } from 'chart.js'
import * as chartjs from 'chart.js'


chartjs.defaults.global.elements.point.radius = 0
chartjs.defaults.global.elements.line.tension = 0.4
chartjs.defaults.global.elements.line.tension = 0.4


export function ChartComponent({id, label, labels, data, min, max})
{
  return html.div(
  {
    id,
    className: 'chart-container'
  },
  [
    ChartCanvasComponent({label, labels, data, min, max})
  ])
}


function ChartCanvasComponent({label, labels, data, min, max})
{
  return html.canvas(
    {
      oncreate: el => create_chart(el, label, labels, data, min, max)
    }
  )
}


function create_chart(host, label, labels, data, min = undefined, max = undefined)
{
  return new Chart(
    host,
    {
      type: 'line',
      data: {
        labels,
        datasets: [
          {
            backgroundColor: 'black',
            borderWidth: 1,
            borderColor: 'black',
            label,
            data
          }
        ]
      },
      options: {
        animation: { duration: 0 },
        scales: {
          yAxes: [{
            gridLines: {
              drawBorder: false
            },
            ticks: {
              fontSize: 9,
              min,
              max,
              padding: 10
            }
          }],
          xAxes: [{
            gridLines: {
              display: false
            },
            ticks: {
              fontSize: 9,
              minRotation: 0,
              maxRotation: 0,
              autoSkip: true,
              maxTicksLimit: 6,
            }
          }]
        }
      }
    }
  )
}
