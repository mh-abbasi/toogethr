import React, { useState } from 'react'
import { Redirect } from 'react-router-dom'
import withPage from '../pages/withPage'
import useLoginFlow, { isSignedIn } from '../hooks/useLoginFlow'
import useTitle from '../hooks/useTitle'
import {LOGIN_URL, RESERVATIONS} from '../common/urlConstants'
import { httpCore } from '../packages/http-core/src/index'
import Button from '@material-ui/core/Button'
import CssBaseline from '@material-ui/core/CssBaseline'
import TextField from '@material-ui/core/TextField'
import Grid from '@material-ui/core/Grid'
import Box from '@material-ui/core/Box'
import Typography from '@material-ui/core/Typography'
import { makeStyles } from '@material-ui/core/styles'
import Container from '@material-ui/core/Container'
import Logo from '../logo.svg'
import {useSnackbar} from "notistack";
import Copyright from "../components/Copyright";
import { Link } from "react-router-dom"

const useStyles = makeStyles((theme) => ({
  paper: {
    marginTop: theme.spacing(8),
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
  },
  logo: {
    margin: theme.spacing(1),
    marginBottom: '30px',
  },
  form: {
    width: '100%', // Fix IE 11 issue.
    marginTop: theme.spacing(1),
  },
  submit: {
    margin: theme.spacing(3, 0, 2),
  },
  error: {
    color: '#FFF',
    fontSize: '.9rem',
    textAlign: 'center',
    padding: '7px 10px',
    backgroundColor: 'darkred',
    borderRadius: '5px',
    margin: '10px 0'
  }
}));


const Register = ({ history }) => {

  const classes = useStyles();
  const [userData, setUserData] = useState({})
  const { enqueueSnackbar, closeSnackbar } = useSnackbar()

  useTitle('Register')

  const onChange = ev => {
    const {name : inputName, value} = ev.target
    setUserData(prevState => {
      const newData = {
        ...prevState,
        [inputName]: value
      }
      return newData
    })
  }

  const onKeydown = ev => {
    if( ev.keyCode === 13 )
      register()
  }

  const register = async () => {
    try {
      const res = await httpCore.register(userData)
      enqueueSnackbar('Registration complete, You can login using your credentials')
      history.replace(LOGIN_URL)
    } catch (error) {
      console.log(error)
      const { message: msg } = error
      const message = typeof msg === 'string' ? msg : 'Unknown error'
      enqueueSnackbar(message, {variant: "error"})
    }
  }

  if (isSignedIn()) {
    return <Redirect to={RESERVATIONS} />
  }



  return (
      <Container component="main" maxWidth="xs">
        <CssBaseline />
        <div className={classes.paper}>
          <img className={classes.logo} src={Logo}  alt="Toogethr Logo"/>
          <Typography component="h1" variant="h5">
            Register
          </Typography>
          <TextField
              variant="outlined"
              margin="normal"
              required
              fullWidth
              name="first_name"
              label="First Name"
              type="text"
              id="first_name"
              autoFocus
              autoComplete="first_name"
              onChange={onChange}
              onKeyDown={onKeydown}
          />
          <TextField
              variant="outlined"
              margin="normal"
              required
              fullWidth
              name="last_name"
              label="Last Name"
              type="text"
              id="last_name"
              autoComplete="last_name"
              onChange={onChange}
              onKeyDown={onKeydown}
          />
          <TextField
              variant="outlined"
              margin="normal"
              required
              fullWidth
              id="email"
              label="Email Address"
              name="email"
              autoComplete="email"
              onChange={onChange}
              onKeyDown={onKeydown}
          />
          <TextField
              variant="outlined"
              margin="normal"
              required
              fullWidth
              name="password"
              label="Password"
              type="password"
              id="password"
              autoComplete="current-password"
              onChange={onChange}
              onKeyDown={onKeydown}
          />
          <Button
              type="button"
              fullWidth
              variant="contained"
              color="primary"
              size={"large"}
              className={classes.submit}
              onClick={register}
          >
            Register
          </Button>
          <Grid container>
            <Grid item>
              <Link to={LOGIN_URL} variant="body2">
                {"Have an account? Sign In"}
              </Link>
            </Grid>
          </Grid>
        </div>
        <Box mt={8}>
          <Copyright />
        </Box>
      </Container>
  )
}

export default withPage(Register)
