import * as html from '@hyperapp/html'


export default function ScalarComponent({label, data})
{
  return html.div(
    {className: 'card scalar-container'},
    [
      html.div({ class: 'scalar-label' }, [label]),
      html.pre({ class: 'scalar-value' }, [data])
    ]
  )
}
