import React from 'react';
import './index.css'
import './App.css';
import Header from './components/Header.tsx';
import Body from './components/PointsPerPosition.tsx';
import { Route, Routes } from 'react-router-dom';
import Dash from './components/Dash.tsx';
import { TeamProvider } from './components/TeamContext.tsx';

function App() {
  return (
    <TeamProvider>
      <div className='App'>
        <Header></Header>
        <Routes>
          <Route path='/' element={<Dash></Dash>} />
          <Route path='/points-per-position' element={<Body></Body>} />
        </Routes>
      </div>
    </TeamProvider>
  );
}

export default App;
