import { app } from 'hyperapp'
import * as html from '@hyperapp/html'

import * as models from './models.js';
import { ChartComponent } from './components/chart.component.js'
import { ScalarComponent } from './components/scalar.component.js'


main()


async function main()
{
  let plugins = await getPlugins()

  const state = {plugins}

  const actions = {}

  const view = (state, actions) =>
      html.div(
      {
        oncreate: async _ => plugins = await getPlugins()
      },
      [
        ...Object.keys(plugins).map(key =>
          create_plugin_element(plugins[key]))
      ])

  app(state, actions, view, document.querySelector('#root'))
}


function create_plugin_element(plugin)
{
  if (plugin.schema.typeof[0] === 'vector')
  {
    return create_chart_element(plugin)
  }
  else if (plugin.schema.typeof[0] === 'scalar')
  {
    return create_scalar_element(plugin)
  }
}


function create_scalar_element(plugin)
{
  return ScalarComponent({label: plugin.schema.label, data: plugin.data})
}


function create_chart_element(plugin)
{
  const MILLI_IN_SEC = 1000

  const labels = []
  const data = []

  for (let i = 0; i < plugin.data.length; i++)
  {
    const timestamp = plugin.data[i][0]
    const datum = plugin.data[i][1]

    labels.push(new Date(timestamp * MILLI_IN_SEC).toLocaleTimeString())
    data.push(datum)

    // If gap in data
    if (i + 1 >= plugin.data.length) { continue }

    // Fill in missing data if any interval data is missing
    const next_timestamp = plugin.data[i + 1][0]
    if (next_timestamp > (timestamp + plugin.schema.update_period))
    {
      const [missing_labels, missing_data] =
        generate_missing_labels_and_data(
          timestamp, next_timestamp, plugin.update_interval)
      labels.push(
        ...missing_labels.map(missing_label =>
          new Date(missing_label * MILLI_IN_SEC).toLocaleTimeString()))
      data.push(...missing_data)
    }
  }

  return ChartComponent({
    id: `chart-{plugin.label.toLowerCase().replace(' ', '-')}`,
    label: plugin.schema.label,
    labels,
    data,
    min: 0,
    max: 1
  })
}


async function get_schemas()
{
  const schemas = await (await fetch('/api/plugin/schemas')).json()
  return schemas.reduce((acc, schema) =>
  {
    acc[schema.name] = schema.plugin
    return acc
  }, {})
}


async function get_stats()
{
  const stats = await (await fetch('/api/plugin/stats')).json()
  return stats.reduce((acc, stat) =>
  {
    acc[stat.name] = stat.data
    return acc
  }, {})
}


async function getPlugins()
{
  let stats
  let schemas

  await Promise.all(
  [
    get_schemas().then(data => schemas = data),
    get_stats().then(data => stats = data)
  ])

  const plugins = {}
  Object.keys(stats).forEach(key =>
  {
    const data = stats[key]
    const schema = schemas[key]
    plugins[key] = new models.Plugin(data, schema)
  })

  return plugins
}


function generate_missing_labels_and_data(start, end, interval)
{
  const labels = []
  for (let i = start; i < end; i++)
    labels.push(i)
  return [labels, labels.map(_ => null)]
}
