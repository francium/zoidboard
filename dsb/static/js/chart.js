const Chart = window.Chart
Chart.defaults.global.elements.point.radius = 0;

const MILLI_IN_SEC = 1000

export function create_chart(host, plugin)
{
  const labels = plugin.data.map(data => new Date(data[0] * MILLI_IN_SEC).toLocaleTimeString())
  const data = plugin.data.map(dataum => dataum[1])
  return new Chart(
    host,
    {
      type: 'line',
      data: {
        labels: labels,
        datasets: [
          {
            label: plugin.schema.label,
            data: data,
          }
        ]
      },
      options: {
        animation: { duration: 0 },
        scales: {
          yAxes: [{
            ticks: {
              min: 0,
              max: 1
            }
          }]
        }
      }
    }
  )
}
