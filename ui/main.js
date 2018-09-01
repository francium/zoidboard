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
        className: 'app-container',
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

  return ChartComponent({
    id: `chart-${plugin.schema.label.toLowerCase().replace(' ', '-')}`,
    label: plugin.schema.label,
    data: plugin.data
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
