import * as html from '@hyperapp/html'
import {app} from 'hyperapp'

import * as models from './models.js';
import ChartComponent from './components/chart.component.js'
import HeaderComponent from './components/header.component.js'
import ScalarComponent from './components/scalar.component.js'


main()


async function main()
{
  let plugins = await get_plugins()
  const config = await get_config()

  const state = {plugins}

  const actions = {}

  function view()
  {
    return html.div(
      {
        className: 'app',
      },
      [
        HeaderComponent(config.hostname),
        html.div(
          {
            className: 'main-content',
            oncreate: async () => plugins = await get_plugins(),
          },
          [
            ...Object.keys(plugins).map(key =>
              create_plugin_element(plugins[key])),
          ]
        ),
      ]
    )
  }

  app(state, actions, view, document.querySelector('#root'))
}


// eslint-disable-next-line consistent-return
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
  return ChartComponent({
    id: `chart-${plugin.schema.label.toLowerCase().replace(' ', '-')}`,
    label: plugin.schema.label,
    data: plugin.data,
  })
}


async function get_config()
{
  return (await fetch('/api/config')).json()
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


async function get_plugins()
{
  let stats
  let schemas

  await Promise.all(
    [
      get_schemas().then(data => schemas = data),
      get_stats().then(data => stats = data),
    ]
  )

  const plugins = {}
  Object.keys(stats).forEach(key =>
  {
    const data = stats[key]
    const schema = schemas[key]
    plugins[key] = new models.Plugin(data, schema)
  })

  return plugins
}
