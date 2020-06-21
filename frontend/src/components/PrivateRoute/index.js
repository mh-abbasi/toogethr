import React from 'react'
import { Route, Redirect } from 'react-router-dom'
import { LOGIN_URL } from '../../common/urlConstants'
import { isSignedIn } from '../../hooks/useLoginFlow'

const PrivateRoute = ({ component: Component, ...rest }) => {
  return (
    <Route
      {...rest}
      render={props =>
        isSignedIn() ? (
          <Component {...props} />
        ) : (
          <Redirect
            to={{
              pathname: LOGIN_URL,
            }}
          />
        )
      }
    />
  )
}

export default PrivateRoute
