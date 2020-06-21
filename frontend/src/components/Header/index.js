import React from 'react'
import PropTypes from 'prop-types'
import {useHistory} from "react-router";

import { withStyles } from '@material-ui/core/styles'
import {AppBar, Toolbar, Typography, Button, IconButton, Tooltip} from "@material-ui/core"
import ExitToApp from "@material-ui/icons/ExitToApp"
import MenuIcon from "@material-ui/icons/Menu"

const styles = {
  root: {
    flexGrow: 1,
  },
  flex: {
    flex: 1,
  },
  menuButton: {
    marginLeft: -12,
    marginRight: 20,
  },
};

function ButtonAppBar(props) {
  const { classes } = props;

  const history = useHistory()

  const handleLogout = () => {
    history.push('/logout')
  }
  return (
      <div className={classes.root}>
        <AppBar position="static" color={"primary"}>
          <Toolbar>
            {/*<IconButton className={classes.menuButton} color="inherit" aria-label="Menu">*/}
            {/*  <MenuIcon />*/}
            {/*</IconButton>*/}
            <Typography variant="h6" color="inherit" className={classes.flex}>
              Parking Lot
            </Typography>
            <Tooltip title="Logout">
              <Button color="inherit" onClick={handleLogout}><ExitToApp /></Button>
            </Tooltip>
          </Toolbar>
        </AppBar>
      </div>
  );
}

ButtonAppBar.propTypes = {
  classes: PropTypes.object.isRequired,
};

const StyledHeader = withStyles(styles)(ButtonAppBar)

export default React.memo(StyledHeader)