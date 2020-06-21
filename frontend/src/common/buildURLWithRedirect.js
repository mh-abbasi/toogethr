export const buildURLWithRedirect = (targetPath, redirectPath) => {
  return `${targetPath}/?redirect=${encodeURIComponent(redirectPath)}`
}
