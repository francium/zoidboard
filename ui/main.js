import * as html from '@hyperapp/html'
import {app as hyperapp} from 'hyperapp'

import * as models from './models.js'
import ChartComponent from './components/chart.component.js'
import HeaderComponent from './components/header.component.js'
import ScalarComponent from './components/scalar.component.js'


main()


async function main()
{
  const {config, plugins} = await get_init_data()

  const state =
    {
      hostname: config.hostname,
      plugins,
      last_update: new Date(),
    }

  const actions =
    {
      update_plugin_data: () => async (state, actions) =>
        {
          const plugins = await get_plugins()
          actions.plugin_data_updated({plugins: plugins, last_update: new Date()})
        },

      plugin_data_updated: ({plugins, last_update}) => () => ({plugins, last_update}),
    }

  function view(state, actions)
  {
    return html.div(
      {
        className: 'app',
      },
      [
        HeaderComponent(state, actions),
        html.div(
          {
            className: 'main-content',
          },
          [
            ...Object.keys(plugins).map(key =>
              create_plugin_element(state.plugins[key])),
          ]
        ),
      ]
    )
  }

  const app = hyperapp(state, actions, view, document.querySelector('#root'))
  setInterval(app.update_plugin_data, 5000)
}


async function get_init_data()
{
  let config,
      plugins

  await Promise.all(
    [
      get_plugins().then(data => plugins = data),
      get_config().then(data => config = data),
    ],
  )

  return {config, plugins}
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
