import React from 'react'
import withPage from '../pages/withPage'
import withPageLayout from "../components/layout/withPageLayout";
import useTitle from "../hooks/useTitle";
import Reservations from "../components/Reservations"

const ReservationsPage = () => {
  useTitle('Reservations')
  return (
    <Reservations />
  )
}

export default withPage(withPageLayout(ReservationsPage))
