import React from 'react'
import loadable from '@loadable/component'
import { Switch, Route } from 'react-router-dom'
import PrivateRoute from '../components/PrivateRoute'
import AdminRoute from '../components/AdminRoute'
import {
    PROFILE,
    LOGIN_URL,
    ABOUT,
    USERS,
    RESERVATIONS,
    REGISTER_URL
} from '../common/urlConstants'
import { LogOut } from './LogOut'

const Profile = loadable(() => import('./profile'))
const Login = loadable(() => import('./login'))
const Register = loadable(() => import('./register'))
const NotFound = loadable(() => import('./404'))
const AboutPage = loadable(() => import('./about'))
const ReservationsPage = loadable( () => import('./reservations'))
const NavigationSetup = () => {
    return (
        <Switch>
            <Route exact path='/' component={Login} />
            <Route exact path={`${LOGIN_URL}`} component={Login} />
            <Route exact path={`${REGISTER_URL}`} component={Register} />
            <PrivateRoute exact path={RESERVATIONS} component={ReservationsPage} />
            <PrivateRoute exact path="/logout" component={LogOut} />
            <PrivateRoute exact path={PROFILE} component={Profile} />
            {/*<PrivateRoute path={ABOUT} component={AboutPage} />*/}
            <Route exact path={ABOUT} component={AboutPage} />
            {/*<AdminRoute path={USERS} component={AboutPage} />*/}
            <Route component={NotFound} />
        </Switch>
    )
}

export default NavigationSetup
