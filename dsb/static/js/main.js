import * as models from './models.js';
import { create_chart } from './chart.js';


main()


async function main()
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

    const root = document.querySelector('#root')
    root.appendChild(create_plugin_element(plugins[key]))
  })
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
  const scalar_container = document.createElement('div')
  scalar_container.classList.add('scalar-container')
  const label_el = document.createElement('div')
  const data_el = document.createElement('div')
  label_el.appendChild(document.createTextNode(plugin.schema.label))
  data_el.appendChild(document.createTextNode(plugin.data))
  scalar_container.appendChild(label_el)
  scalar_container.appendChild(data_el)
  return scalar_container
}

function create_chart_element(plugin)
{
  const canvas_container = document.createElement('div')
  canvas_container.classList.add('chart-container')
  const canvas = document.createElement('canvas')
  canvas_container.appendChild(canvas)
  root.appendChild(canvas_container)

  create_chart(canvas, plugin)
  return canvas_container
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
