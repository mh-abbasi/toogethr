import React from 'react'
import { BrowserRouter as Router } from 'react-router-dom'
import NavigationSetup from './pages/index'
import { SnackbarProvider } from 'notistack'


const App = () => {
    return (
        <Router>
            <SnackbarProvider>
                <NavigationSetup />
            </SnackbarProvider>
        </Router>
    )
}

export default App
