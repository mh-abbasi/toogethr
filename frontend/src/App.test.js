import React from 'react';
import { shallow } from 'enzyme';
import App from './App';
import NavigationSetup from "./pages/index"

test('App should render navigation setup', () => {
  const wrapper = shallow(<App />);
  expect(wrapper).toContainReact(<NavigationSetup />);
});
