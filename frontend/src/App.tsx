import React from 'react';
import './index.css'
import './App.css';
import Header from './components/Header.tsx';
import { Route, Routes } from 'react-router-dom';
import Dash from './components/Cards.tsx';
import { TeamProvider } from './components/TeamContext.tsx';
import PointsPerPosition from './components/PointsPerPosition.tsx';

function App() {
  return (
    <TeamProvider>
      <div className="d-flex flex-column min-vh-100">
        <Header />
        <div className="flex-grow-1 bg-light d-flex flex-column pt-3">
          <Routes>
            <Route path="/" element={<Dash />} />
            <Route path="/points-per-position" element={<PointsPerPosition />} />
          </Routes>
        </div>
      </div>
    </TeamProvider>
  );
}

export default App;
