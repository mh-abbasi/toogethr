import { decode } from 'jsonwebtoken'
import { httpCore, PersistManager } from '../packages/http-core/src/index'

const useLoginFlow = () => {

  const login = (token, refresh=null) => {
    PersistManager.setAccessToken(token, refresh)
    httpCore.updateHeadersWithAccessToken(token)
  }

  const logout = () => {
    PersistManager.setAccessToken()
    httpCore.updateHeadersWithAccessToken()
  }

  return { login, logout }
}

export const isSignedIn = () => {
  const token = PersistManager.getAccessToken()
  return !!token
}

export const getToken = () => {
  if(isSignedIn()) {
    return  PersistManager.getAccessToken()
  }
  return false
}

export const getRefreshToken = () => {
  if(isSignedIn()) {
    return  PersistManager.getRefreshToken()
  }
  return false
}

export const isSuperuser = () => {
  if( isSignedIn() ) {
    const token = PersistManager.getAccessToken()
    const decoded = decode(token)
    if (decoded != null) {
      const { is_superuser } = decoded
      return !!is_superuser
    }

    return false
  }
}

export const getTokenDetails = () => {
  if( isSignedIn() ) {
    const token = PersistManager.getAccessToken()
    const decoded = decode(token)
    if (decoded != null) {
      return decoded
    }
  }
  return false

}

export const isTokenExpired = () => {
  const token = PersistManager.getAccessToken()
  const decoded = decode(token)
  if (decoded != null) {
    const { exp } = decoded
    if (exp * 1000 < new Date().getTime()) {
      return true
    }

    return false
  }

  return true
}

export const isRefreshExpired = () => {
  const token = PersistManager.getRefreshToken()
  const decoded = decode(token)
  if (decoded != null) {
    const { exp } = decoded
    if (exp * 1000 < new Date().getTime()) {
      return true
    }

    return false
  }

  return true
}
export default useLoginFlow
