import * as html from '@hyperapp/html'


export default function view(hostname)
{
  return html.nav(
    {
      className: 'header'
    },
    [
      html.div({className: 'header-logo'},
        [
        html.img({src: '/static/assets/logo.png'})
        ]
      ),
      html.div({className: 'header-hostname'}, [hostname]),
      html.div({className: 'header-datetime'},
        [
          html.div({style: {textAlign: 'end'}}, [new Date().toLocaleTimeString()]),
          html.div({style: {textAlign: 'end'}}, [new Date().toLocaleDateString()])
        ]
      ),
      html.div({className: 'header-datetime'}, [])
    ]
  )
}
