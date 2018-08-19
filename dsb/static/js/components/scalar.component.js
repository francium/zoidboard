const html = window.hyperappHtml


export function ScalarComponent({label, data})
{
  return html.div(
    {className: 'scalar-container'},
    [
      html.div([label]),
      html.div([data])
    ]
  )
}
