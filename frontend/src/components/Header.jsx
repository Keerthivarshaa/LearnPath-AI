import React from 'react';
import { motion } from 'framer-motion';
import { ChevronRight, LogOut, Calendar } from 'lucide-react';

const Header = ({ activeTab, handleLogout }) => {
  const tabNames = {
    overview: 'Overview',
    path: 'Learning Path',
    assessment: 'Assessment',
    progress: 'Progress',
    settings: 'Settings',
  };

  return (
    <header className="saas-header">
      <div className="header-breadcrumbs">
        <span className="breadcrumb-main">LearnPath AI</span>
        <ChevronRight size={14} className="breadcrumb-sep" />
        <span className="breadcrumb-sub font-display">
          {tabNames[activeTab] || 'Console'}
        </span>
      </div>

      <div className="header-actions">
        <div className="header-date">
          <Calendar size={14} />
          <span>
            {new Date().toLocaleDateString('en-US', {
              month: 'short',
              day: 'numeric',
              year: 'numeric',
            })}
          </span>
        </div>

        <motion.button
          onClick={handleLogout}
          className="btn-header-logout"
          title="Log Out Session"
          whileHover={{ y: -1 }}
          whileTap={{ scale: 0.97 }}
        >
          <LogOut size={16} />
          <span>Sign Out</span>
        </motion.button>
      </div>
    </header>
  );
};

export default Header;
