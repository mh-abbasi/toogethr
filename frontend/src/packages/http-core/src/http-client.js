import axios from 'axios'
import { createHttpError } from './utils'

class HttpClient {
  constructor(config) {
    this.config = config
    this.axiosInstance = axios.create(config)
  }

  getConfig() {
    return this.config
  }

  /**
   * Update axios instance for sending Bearer token with each request after successful authorization
   */
  updateHeadersWithAccessToken(token) {
    if (token) {
      this.axiosInstance.defaults.headers.common['Authorization'] = `Bearer ${token}`
    } else {
      delete this.axiosInstance.defaults.headers.common['Authorization']
    }
  }

  createFetch({ url, Model, ...rest }) {
    return (params = {}) => {
      const requestSettings = Object.assign({ method: 'GET' }, rest, params)
      return this.axiosInstance(url, requestSettings).then(
        response => (Model ? new Model(response.data) : response.data),
        error => {
          console.log(error.response)
          throw createHttpError(error)
        },
      )
    }
  }

  /**
   * Login request. Returns JWT token after successful authorization
   */
  login = payload => {
    const endpoint = this.createFetch({
      url: '/auth/login',
      method: 'POST',
      data: payload,
    })

    return endpoint()
  }

  /**
   * Register user
   */
  register = payload => {
    const endpoint = this.createFetch({
      url: '/auth/register',
      method: 'POST',
      data: payload,
    })

    return endpoint()
  }

  /**
   * Getting reservations list for the current user
   */

  getReservations = params => {
    const endpoint = this.createFetch({
      url: '/reservations',
      params
    })

    return endpoint()
  }

  /**
   * Create a new reservation
   */
  createReservation = payload => {
    const endpoint = this.createFetch({
      url: `/reservations`,
      method: 'POST',
      data: payload,
    })

    return endpoint()
  }

  /**
   * Update existing reservation
   */
  editReservation = (id, payload) => {
    const endpoint = this.createFetch({
      url: `/user/units-profiles/${id}`,
      method: 'PUT',
      data: payload,
    })

    return endpoint()
  }

  /**
   * Get available slots for a time window
   */
  getSlotsAvailability = (from_datetime, to_datetime) => {
    const endpoint = this.createFetch({
      url: '/slots',
      method: 'GET',
      params: {
        empty: true,
        from_datetime,
        to_datetime
      },
    })

    return endpoint()
  }

  /**
   * Delete reservation
   */
  deleteReservation = id => {
    const endpoint = this.createFetch({
      url: `/reservations/${id}`,
      method: 'DELETE',
    })

    return endpoint()
  }

  /**
   * Check JWT token sender in headers by provided email string in request body
   */
  checkJwtToken = payload => {
    const endpoint = this.createFetch({
      url: '/user/test_auth',
      method: 'POST',
    })

    return endpoint(payload)
  }

  getServerInfo = () => {
    const endpoint = this.createFetch({
      url: `/server/info`,
      method: 'GET',
    })

    return endpoint()
  }
}

export { HttpClient }
