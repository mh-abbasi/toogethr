import React from 'react'
import { Redirect } from 'react-router-dom'
import { isSignedIn } from '../hooks/useLoginFlow'
import { LOGIN_URL, RESERVATIONS } from '../common/urlConstants'
import withPage from '../pages/withPage'

const NotFound = () => {
  return (
      <h3>404</h3>
  )
  if (isSignedIn()) {
    return <Redirect to={RESERVATIONS} />
  }

  return <Redirect to={LOGIN_URL} />
}

export default withPage(NotFound)
