import React, {useState} from 'react'
import {Container} from "@material-ui/core"
import Header from '../Header/index'
import {makeStyles} from "@material-ui/core/styles";

const useStyles = makeStyles({
    container: {
        paddingTop: '20px',
        paddingBottom: '60px'
    }

})
const Layout = ({ children }) => {
    const [isDrawerOpen, setIsDrawerOpen] = useState(true)
    const classes = useStyles()
    const toggleDrawer = () => {
        setIsDrawerOpen(!isDrawerOpen)
    }
    return (
        <main className='pageWrapper'>
            <Header toggleDrawer={toggleDrawer}/>
            <Container className={classes.container} maxWidth={false}>{children}</Container>
        </main>
    )
}

Layout.displayName = 'Layout'

export default Layout
