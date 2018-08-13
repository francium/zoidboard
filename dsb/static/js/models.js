export class Plugin
{
  constructor(data, schema)
  {
    this.data = data
    this.schema = schema
  }
}


export class PluginSchema
{
  constructor(label, type, update_period)
  {
    this.label = label
    this.type = type
    this.update_period = update_period
  }
}
