import React, { useState } from 'react'
import {Redirect, Route} from 'react-router-dom'
import withPage from '../pages/withPage'
import useLoginFlow, { isSignedIn } from '../hooks/useLoginFlow'
import useTitle from '../hooks/useTitle'
import {RESERVATIONS} from '../common/urlConstants'
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
import {Link} from "react-router-dom"

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


const Login = ({ history }) => {

  const classes = useStyles();
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const { login } = useLoginFlow()
  const { enqueueSnackbar, closeSnackbar } = useSnackbar()

  useTitle('Signin')

  const onChange = ev => {
    const inputName = ev.target.name
    if( inputName === 'email' )
      setEmail(ev.target.value)

    else if( inputName === 'password' )
      setPassword(ev.target.value)
  }

  const onKeydown = ev => {
    if( ev.keyCode === 13 )
      signIn()
  }

  const signIn = async () => {

    const payload = {
      email,
      password,
    }
    try {
      const res = await httpCore.login(payload)
      login(res.access, res.refresh)
      enqueueSnackbar('Login Successful!', {variant: "success"})
      history.replace(RESERVATIONS)
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
            Sign in
          </Typography>
          <TextField
              variant="outlined"
              margin="normal"
              required
              fullWidth
              id="email"
              label="Email Address"
              name="email"
              autoComplete="email"
              autoFocus
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
              onClick={signIn}
          >
            Sign In
          </Button>
          <Grid container>
            <Grid item>
              <Link to="/register" variant="body2">
                {"Don't have an account? Sign Up"}
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

export default withPage(Login)
