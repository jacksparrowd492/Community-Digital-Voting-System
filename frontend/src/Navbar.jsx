import React from 'react';
import { NavLink, useLocation } from 'react-router-dom';
import { Vote as VoteIcon, ShieldCheck, Users } from 'lucide-react';

export default function Navbar() {
  const location = useLocation();
  const isAdmin = location.pathname === '/admin';

  return (
    <header className="app-navbar">
      <NavLink to="/" className="navbar-brand">
        <div className="navbar-brand-icon">
          <VoteIcon size={16} />
        </div>
        <span className="navbar-brand-name">Community Voting</span>
      </NavLink>

      <div className="navbar-actions">
        <NavLink
          to="/"
          end
          className={({ isActive }) =>
            `navbar-btn navbar-btn-outline ${isActive ? 'navbar-btn-solid' : ''}`
          }
        >
          <Users size={14} />
          <span>Voter View</span>
        </NavLink>

        <NavLink
          to="/admin"
          className={({ isActive }) =>
            `navbar-btn navbar-btn-outline ${isActive ? 'navbar-btn-solid' : ''}`
          }
        >
          <ShieldCheck size={14} />
          <span>Admin</span>
        </NavLink>


      </div>
    </header>
  );
}
