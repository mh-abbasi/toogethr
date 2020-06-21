import React from 'react'
import { Route, Redirect } from 'react-router-dom'
import {LOGIN_URL, RESERVATIONS} from '../../common/urlConstants'
import {isSignedIn, isSuperuser} from '../../hooks/useLoginFlow'

const AdminRoute = ({ component: Component, ...rest }) => {

    return (
        <Route
            {...rest}
            render={props =>
                (isSignedIn() && isSuperuser()) ? (
                    <Component {...props} />
                ) : (
                    isSignedIn() ?
                        <Redirect
                            to={{
                                pathname: RESERVATIONS,
                            }}
                        />
                        :
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

export default AdminRoute
