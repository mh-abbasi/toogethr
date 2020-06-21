import React from 'react'
import withPageLayout from '../components/layout/withPageLayout'
import withPage from '../pages/withPage'
import useTitle from '../hooks/useTitle'
import About from '../components/About/index'

const AboutPage = () => {
  useTitle('About')
  return <About />
}

const AboutWithLayout = withPageLayout(AboutPage)
export default withPage(AboutWithLayout)
