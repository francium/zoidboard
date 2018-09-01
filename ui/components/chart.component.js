import * as html from '@hyperapp/html'
import Highcharts from 'highcharts'


export function ChartComponent({id, label, data})
{
  return html.div(
    {
      id,
      class: 'chart-container',
      oncreate: el => create_chart(id, label, data)
    }
  )
}


function create_chart(id, title, data)
{
  return new Highcharts.chart(
    id,
    {
      chart: {
        zoomType: 'x'
      },
      title: {
        text: title
      },
      xAxis: {
        type: 'datetime'
      },
      yAxis: {
        min: 0,
        max: 1
      },
      legend: {
        enabled: false
      },
      plotOptions: {
        area: {
          fillColor: {
            linearGradient: {
              x1: 5,
              y1: 0,
              x2: 0,
              y2: 0
            },
            stops: [
              [0, 'black'],
              [1, 'white']
            ]
          },
          marker: {
            radius: 2
          },
          lineWidth: 1,
          states: {
            hover: {
              lineWidth: 1
            }
          },
          threshold: null
        }
      },
      series: [{
        type: 'area',
        name: title,
        data,
        color: 'black'
      }]
    }
  )
}
