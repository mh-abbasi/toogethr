import React from 'react'
import { getDisplayName } from '../common/helpers'
import useLoginFlow, { isTokenExpired, isSignedIn } from '../hooks/useLoginFlow'
import {useSnackbar} from "notistack";

/**
 * This HOC is used for checking token exp time when user go through each page.
 * @param {Component} PageComponent
 */
const withPage = PageComponent => {
  const WrappedComponent = props => {
    const { logout } = useLoginFlow()
    const {enqueueSnackbar} = useSnackbar()

    if (isSignedIn() && isTokenExpired()) {
      enqueueSnackbar('Your token is expired, Please login again.', {variant: "info"})
      logout()
      return
    }


    return <PageComponent {...props} />
  }

  WrappedComponent.displayName = getDisplayName(`WithPage(${getDisplayName(PageComponent)})`)

  return WrappedComponent
}

export default withPage
