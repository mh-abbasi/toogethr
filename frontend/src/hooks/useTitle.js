/**
 * Simple function for change page title when user navigate through app
 * @param {String} title
 */
const useTitle = title => {
  if (title) document.title = title
}

export default useTitle
