import React from 'react'
import PageLayout from '../layout/index'
import { getDisplayName } from '../../common/helpers'

const withPageLayout = Component => {
  const WrappedComponent = props => {
    return (
      <PageLayout>
        <Component {...props} />
      </PageLayout>
    )
  }

  WrappedComponent.displayName = getDisplayName(`WithPageLayout(${getDisplayName(Component)})`)

  return WrappedComponent
}

export default withPageLayout
