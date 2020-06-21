import React from 'react'
import withPageLayout from '../components/layout/withPageLayout'
import withPage from '../pages/withPage'
import useTitle from '../hooks/useTitle'

const ProfilePage = () => {
  useTitle('Profile')
  return <div>Profile page</div>
}

const WrapperProfile = withPageLayout(ProfilePage)
export default withPage(WrapperProfile)
