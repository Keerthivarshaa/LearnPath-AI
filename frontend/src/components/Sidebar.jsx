import React from 'react';
import { motion } from 'framer-motion';
import { LayoutDashboard, Compass, BookOpen, BarChart3, Settings, MessageSquare } from 'lucide-react';

const Sidebar = ({ activeTab, setActiveTab, user, sidebarOpen, roadmapGenerated }) => {
  const initials = user?.name
    ? user.name
        .split(' ')
        .map((n) => n[0])
        .join('')
        .toUpperCase()
        .substring(0, 2)
    : 'US';

  const menuItems = [
    { id: 'overview', label: 'Overview', icon: LayoutDashboard },
    { id: 'path', label: 'Learning Path', icon: Compass, badge: roadmapGenerated ? 'Active' : null },
    { id: 'tutor', label: 'AI Tutor', icon: MessageSquare },
    { id: 'assessment', label: 'Assessment', icon: BookOpen },
    { id: 'progress', label: 'Progress', icon: BarChart3 },
    { id: 'settings', label: 'Settings', icon: Settings },
  ];

  return (
    <aside className={`saas-sidebar ${sidebarOpen ? 'open' : 'closed'}`}>
      <div className="sidebar-logo">
        <Compass className="logo-icon animate-spin-slow" />
        <span className="logo-text">
          LearnPath <span className="logo-highlight">AI</span>
        </span>
      </div>

      <nav className="sidebar-links">
        {menuItems.map((item) => {
          const Icon = item.icon;
          return (
            <motion.button
              key={item.id}
              onClick={() => setActiveTab(item.id)}
              className={`sidebar-link ${activeTab === item.id ? 'active' : ''}`}
              whileHover={{ x: 4 }}
              whileTap={{ scale: 0.98 }}
              type="button"
            >
              <Icon size={18} />
              <span>{item.label}</span>
              {item.badge && <span className="badge-new">{item.badge}</span>}
            </motion.button>
          );
        })}
      </nav>

      <div className="sidebar-footer">
        <div className="user-avatar-circle">{initials}</div>
        <div className="user-meta">
          <span className="user-meta-name">{user?.name || 'Developer'}</span>
          <span className="user-meta-role">Developer</span>
        </div>
      </div>
    </aside>
  );
};

export default Sidebar;
