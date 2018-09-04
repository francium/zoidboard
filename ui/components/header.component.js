import * as html from '@hyperapp/html'


// eslint-disable-next-line no-unused-vars
export default function view(state, actions)
{
  return html.nav(
    {
      className: 'header',
    },
    [
      html.div(
        {className: 'header-logo'},
        [
          html.img({src: '/static/assets/logo.png'}),
        ]
      ),
      html.div({className: 'header-hostname'}, [state.hostname]),
      html.div(
        {className: 'header-datetime'},
        [
          html.div({style: {textAlign: 'end'}}, [state.last_update.toLocaleTimeString()]),
          html.div({style: {textAlign: 'end'}}, [state.last_update.toLocaleDateString()]),
        ]
      ),
      html.div({className: 'header-datetime'}, []),
    ]
  )
}
