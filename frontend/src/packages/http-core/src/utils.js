class HttpError extends Error {
  constructor(args) {
    const { message = 'Unknown HttpError', code, status, statusText, error, errors } = args
    super(message)
    this.status = status
    this.code = code
    this.statusText = statusText
    this.error = error
    this.errors = errors

    if (Error.captureStackTrace) {
      Error.captureStackTrace(this, HttpError)
    } else {
      this.stack = new Error().stack
    }
  }
}

export const createHttpError = (error = {}) => {
  const response = error.response || {}
  const data = response.data || {}
  const errorMessage = data.detail || data.errors || data.message || data.msg || {}
  const message = errorMessage.message || response.statusText
  const errorMessages = data.errors ? data.errors.fields || [] : []

  return new HttpError({
    message,
    error: errorMessage,
    errors: errorMessages,
    code: errorMessage.code,
    status: response.status,
    statusText: response.statusText,
  })
}
