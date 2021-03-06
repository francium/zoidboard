import * as html from '@hyperapp/html'
import Highcharts from 'highcharts'


export default function ChartComponent({id, label, data})
{
  return html.div(
    {
      id,
      className: 'card chart-container',
      oncreate: () => create_chart(id, label, data),
      onupdate: () => create_chart(id, label, data),
    }
  )
}


function create_chart(id, title, data)
{
  // Highcharts uses milliseconds since epoch, backend provides time in secs
  const normalizedData = data.map(d => [d[0] * 1000, d[1]])

  return new Highcharts.chart(
    id,
    chart_config(title, normalizedData),
  )
}

function chart_config(title, data)
{
    return {
      time: {
        timezoneOffset: new Date().getTimezoneOffset(),
      },
      chart: {
        zoomType: 'x',
      },
      title: {
        text: title,
      },
      xAxis: {
        type: 'datetime',
      },
      yAxis: {
        title: null,
        min: 0,
        max: 1,
      },
      legend: {
        enabled: false,
      },
      plotOptions: {
        area: {
          fillColor: '#f5f5f5',
          marker: {
            radius: 2,
          },
          lineWidth: 2,
          states: {
            hover: {
              lineWidth: 1,
            },
          },
          threshold: null,
        },
        series: {
          animation: false,
        },
      },
      series: [
        {
          type: 'area',
          name: title,
          data,
          color: '#4a4a4a',
        },
      ],
    }
}
