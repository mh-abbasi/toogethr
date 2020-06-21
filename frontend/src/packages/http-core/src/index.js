import { HttpClient } from './http-client'

export class PersistManager {

  static get ACCESS_TOKEN_KEY() {
    return 'toogethr-parking-lot-token'
  }

  static get REFRESH_TOKEN_KEY() {
    return 'toogethr-parking-lot-refresh-token'
  }

  static setAccessToken(token, refresh=null) {
    if (token) {
      localStorage.setItem(PersistManager.ACCESS_TOKEN_KEY, token)
    } else {
      localStorage.removeItem(PersistManager.ACCESS_TOKEN_KEY)
      localStorage.removeItem(PersistManager.REFRESH_TOKEN_KEY)
    }
    if( refresh ) {
      localStorage.setItem(PersistManager.REFRESH_TOKEN_KEY, refresh)
    }
  }

  static getAccessToken() {
    const token = localStorage.getItem(PersistManager.ACCESS_TOKEN_KEY)
    return token || ''
  }

  static getRefreshToken() {
    const token = localStorage.getItem(PersistManager.REFRESH_TOKEN_KEY)
    return token || ''
  }
}

const HttpCore = {
  configure(options = {}) {
    const config = {
      baseURL: options.apiUrl,
      timeout: 300000,
    }
    return new HttpClient(config)
  },
}

const apiUrl = process.env.REACT_APP_API_URL
const httpCore = HttpCore.configure({
  apiUrl,
})
const token = PersistManager.getAccessToken()
httpCore.updateHeadersWithAccessToken(token)

if (process.env.NODE_ENV !== 'production') {
  // eslint-disable-next-line no-underscore-dangle
  window.__httpCore_for_debugging_purposes = httpCore
}

export { httpCore }

export default Object.assign({}, HttpCore, { HttpClient })
