import React from 'react';
import { motion } from 'framer-motion';

const StatCard = ({ icon: Icon, label, value, gradientClass }) => {
  return (
    <motion.div
      className={`glass-card matrix-card ${gradientClass}`}
      whileHover={{ y: -4, borderSecondary: 'rgba(255, 255, 255, 0.2)' }}
      transition={{ type: 'spring', stiffness: 300, damping: 20 }}
    >
      <div className="matrix-icon">
        <Icon size={20} />
      </div>
      <div className="matrix-info">
        <span className="matrix-label">{label}</span>
        <h4 className="matrix-value">{value}</h4>
      </div>
    </motion.div>
  );
};

export default StatCard;
