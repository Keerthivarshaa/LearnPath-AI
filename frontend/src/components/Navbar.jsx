import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { Compass, LogOut, User as UserIcon, LayoutDashboard, LogIn, UserPlus } from 'lucide-react';

const Navbar = () => {
  const navigate = useNavigate();
  const token = localStorage.getItem('token');
  const userString = localStorage.getItem('user');
  const user = userString ? JSON.parse(userString) : null;

  const handleLogout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    navigate('/login');
  };

  return (
    <nav className="navbar-container">
      <div className="container nav-content">
        <Link to={token ? "/dashboard" : "/login"} className="nav-logo">
          <Compass className="logo-icon" />
          <span>LearnPath <span className="gradient-text">AI</span></span>
        </Link>
        
        <div className="nav-links">
          {token ? (
            <>
              <Link to="/dashboard" className="nav-link-item">
                <LayoutDashboard size={18} />
                <span>Dashboard</span>
              </Link>
              
              <div className="user-profile-badge">
                <UserIcon size={16} />
                <span>{user?.name || 'User'}</span>
              </div>
              
              <button onClick={handleLogout} className="btn-logout">
                <LogOut size={16} />
                <span>Logout</span>
              </button>
            </>
          ) : (
            <>
              <Link to="/login" className="nav-link-item">
                <LogIn size={18} />
                <span>Login</span>
              </Link>
              <Link to="/register" className="btn btn-primary nav-register-btn">
                <UserPlus size={16} />
                <span>Get Started</span>
              </Link>
            </>
          )}
        </div>
      </div>
      
      <style>{`
        .navbar-container {
          background: rgba(11, 15, 25, 0.85);
          backdrop-filter: blur(12px);
          border-bottom: 1px solid var(--border-color);
          position: sticky;
          top: 0;
          z-index: 100;
          height: 70px;
          display: flex;
          align-items: center;
        }
        .nav-content {
          display: flex;
          justify-content: space-between;
          align-items: center;
        }
        .nav-logo {
          display: flex;
          align-items: center;
          gap: 0.75rem;
          font-family: var(--font-display);
          font-size: 1.4rem;
          font-weight: 800;
          color: white;
        }
        .logo-icon {
          color: var(--accent-cyan);
          animation: spin-slow 15s linear infinite;
        }
        @keyframes spin-slow {
          from { transform: rotate(0deg); }
          to { transform: rotate(360deg); }
        }
        .gradient-text {
          background: linear-gradient(135deg, var(--accent-purple) 0%, var(--accent-cyan) 100%);
          -webkit-background-clip: text;
          -webkit-text-fill-color: transparent;
        }
        .nav-links {
          display: flex;
          align-items: center;
          gap: 1.5rem;
        }
        .nav-link-item {
          display: flex;
          align-items: center;
          gap: 0.5rem;
          font-size: 0.95rem;
          color: var(--text-secondary);
          padding: 0.5rem 0.75rem;
          border-radius: var(--radius-sm);
        }
        .nav-link-item:hover {
          color: white;
          background: rgba(255, 255, 255, 0.05);
        }
        .user-profile-badge {
          display: flex;
          align-items: center;
          gap: 0.5rem;
          background: rgba(6, 182, 212, 0.1);
          border: 1px solid rgba(6, 182, 212, 0.2);
          color: var(--accent-cyan);
          padding: 0.4rem 0.8rem;
          border-radius: 50px;
          font-size: 0.85rem;
          font-weight: 600;
        }
        .btn-logout {
          display: flex;
          align-items: center;
          gap: 0.5rem;
          background: transparent;
          border: none;
          color: #fca3a3;
          cursor: pointer;
          font-family: var(--font-sans);
          font-size: 0.95rem;
          padding: 0.5rem 0.75rem;
          border-radius: var(--radius-sm);
          transition: all 0.2s ease;
        }
        .btn-logout:hover {
          background: rgba(239, 68, 68, 0.1);
          color: #ef4444;
        }
        .nav-register-btn {
          padding: 0.5rem 1rem;
          font-size: 0.9rem;
        }
      `}</style>
    </nav>
  );
};

export default Navbar;
