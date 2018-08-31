const html = window.hyperappHtml


export function ScalarComponent({label, data})
{
  return html.div(
    {className: 'scalar-container'},
    [
      html.div({ class: 'scalar-label' }, [label]),
      html.pre({ class: 'scalar-value' }, [data])
    ]
  )
}
