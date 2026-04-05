import React from 'react';
import { Routes, Route, Link } from 'react-router-dom';
import Home from './pages/Home';
import About from './pages/About';
import Dashboard from './pages/Dashboard';
import Auth from './pages/Auth';


function Layout() {
  return (
    <div>
      <header>
        
        <nav>
          <img src="Cheasy_logo_with_cheerful_chef-removebg-preview.png" alt="CHEASY Logo" style={{ height: 75, verticalAlign: 'middle' }} />
          <Link to="/">Home</Link> | <Link to="/about">About</Link> | <Link to="/dashboard">Dashboard</Link> | <Link to="/login"><i class="fa-solid fa-arrow-right-to-bracket"></i></Link> 
        </nav>
      </header>
      <main style={{ marginTop: 20 }}>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/about" element={<About />} />
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/login" element={<Auth />} />
        
        </Routes>
      </main>
    </div>
  );
}

export default Layout;