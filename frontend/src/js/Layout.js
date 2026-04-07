import React from 'react';
import { Routes, Route, Link } from 'react-router-dom';
import Home from './pages/Home';
import About from './pages/About';
import {TeacherDashboard, StudentDashboard} from './pages/Dashboard';
import Auth from './pages/Auth';
import { useStore } from './flux/appContext';


function Layout() {
  const { data, actions } = useStore();
  const dashboardElement = data.session.role === 'teacher'
    ? <TeacherDashboard /> : data.session.role === 'student' ? <StudentDashboard /> : null;

  return (
    <div>
      
        <nav className='d-flex align-items-center px-4 '>
          <img src="Cheasy_logo_with_cheerful_chef-removebg-preview.png" alt="CHEASY Logo" style={{ height: 75, verticalAlign: 'middle' }} />
          <div className='ms-3' >
          <Link to="/">Home</Link> | <Link to="/about">About</Link> {data.isAuthenticated && (<span>| <Link to="/dashboard">Dashboard</Link></span>)}</div>
          <div className='ms-auto'>{data.isAuthenticated ? (<>
            
               {' '} <span>Hi, {data.session.username}!</span>{' '}
              <button className="btn" type="button" onClick={actions.logout} style={{ marginLeft: 8 }}>
                <i class="fa-solid fa-arrow-right-from-bracket"></i>
              </button>
            </>) : (<>| <Link to="/login"><i className="fa-solid fa-arrow-right-to-bracket"></i></Link></> )}</div>
          
        </nav>
      
      <main >
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/about" element={<About />} />
          <Route path="/dashboard" element={dashboardElement} />
          <Route path="/login" element={<Auth />} />
        
        </Routes>
      </main>
    </div>
  );
}

export default Layout;