import styled from 'styled-components/macro'
import { Box } from 'rebass'

export const PageWrapper = styled(Box)`
  height: 100vh;
  position: relative;
`

export const PageBodyContainer = styled(Box)`
  position: absolute;
  bottom: 0;
  right: 0;
  left: 0;
  top: 60px;
  overflow-x: hidden;
`
