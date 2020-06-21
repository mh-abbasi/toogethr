import { Redirect } from 'react-router-dom'
import React from 'react'
import { LOGIN_URL } from '../common/urlConstants'
import useLoginFlow from '../hooks/useLoginFlow'

export const LogOut = () => {
  const { logout } = useLoginFlow()

  logout()

  return (
    <Redirect
      to={{
        pathname: LOGIN_URL,
      }}
    />
  )
}
