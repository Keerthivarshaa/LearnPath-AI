import React from 'react';
import { motion } from 'framer-motion';

const ProgressCard = ({ progressData }) => {
  const percentage = progressData ? Math.round(progressData.completionPercentage) : 0;
  
  // Circumference for r=55 is 2 * PI * 55 = 345.57
  const strokeOffset = 345.5 - (345.5 * percentage) / 100;
  
  const completedCount = progressData ? progressData.completedMilestones.length : 0;
  const completedTopicsCount = progressData ? progressData.completedTopics.length : 0;

  return (
    <div className="glass-card widget-panel">
      <div className="widget-header">
        <h3>Milestone Tracker</h3>
        <span className="widget-subtitle">Syllabus Completion Gauge</span>
      </div>

      <div className="circular-progress-showcase">
        <div className="svg-wrapper">
          <svg width="140" height="140" viewBox="0 0 140 140">
            <circle cx="70" cy="70" r="55" className="circle-back" />
            <motion.circle
              cx="70"
              cy="70"
              r="55"
              className="circle-front"
              strokeDasharray="345.5"
              initial={{ strokeDashoffset: 345.5 }}
              animate={{ strokeDashoffset: strokeOffset }}
              transition={{ duration: 1, ease: 'easeOut' }}
            />
          </svg>
          <div className="inner-percentage">
            <span className="percent-num">{percentage}%</span>
            <span className="percent-label">Done</span>
          </div>
        </div>
        <div className="progress-details">
          <div className="detail-item">
            <span className="dot dot-completed"></span>
            <span>Completed Milestones: {completedCount}</span>
          </div>
          <div className="detail-item">
            <span className="dot dot-pending"></span>
            <span>Completed Topics: {completedTopicsCount}</span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ProgressCard;
