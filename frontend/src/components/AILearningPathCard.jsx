import React from 'react';
import { motion } from 'framer-motion';
import { Compass, ChevronRight, Lock } from 'lucide-react';

const AILearningPathCard = ({ roadmapData, onStartAssessment }) => {
  const hasRoadmap = roadmapData && !roadmapData.onboarding;
  
  // Find in-progress and locked milestones to show
  const activeMilestone = hasRoadmap 
    ? roadmapData.milestones.find(m => m.status === 'IN_PROGRESS') 
    : null;
    
  const nextLockedMilestone = hasRoadmap 
    ? roadmapData.milestones.find(m => m.status === 'LOCKED') 
    : null;

  return (
    <div className="glass-card widget-panel">
      <div className="widget-header">
        <h3>Continuous Learning Node</h3>
        <span className="widget-subtitle">Next Course Modules</span>
      </div>

      {!hasRoadmap ? (
        <div className="empty-shimmer-state">
          <Compass className="empty-compass animate-pulse" size={32} />
          <p>No active roadmap modules loaded. Connect diagnostic logs to display your path.</p>
          <motion.button 
            onClick={onStartAssessment} 
            className="btn btn-secondary btn-sm"
            whileHover={{ scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
            type="button"
          >
            Go to Assessment
          </motion.button>
        </div>
      ) : (
        <div className="roadmap-quick-list">
          {activeMilestone && (
            <motion.div 
              className="quick-list-item active"
              whileHover={{ x: 4 }}
            >
              <div className="item-num">
                {activeMilestone.displayOrder < 10 ? `0${activeMilestone.displayOrder}` : activeMilestone.displayOrder}
              </div>
              <div className="item-text">
                <h4>{activeMilestone.topic}</h4>
                <p>{activeMilestone.category} • {activeMilestone.difficulty}</p>
              </div>
              <ChevronRight size={16} className="item-arrow" />
            </motion.div>
          )}
          
          {nextLockedMilestone && (
            <div className="quick-list-item locked">
              <Lock size={16} className="item-lock" />
              <div className="item-text">
                <h4>{nextLockedMilestone.topic}</h4>
                <p>{nextLockedMilestone.category} • {nextLockedMilestone.difficulty}</p>
              </div>
            </div>
          )}

          {!activeMilestone && !nextLockedMilestone && (
            <p className="completion-cheer-text">🎉 You have completed all recommended milestones for this goal!</p>
          )}
        </div>
      )}
      <style>{`
        .completion-cheer-text {
          font-size: 0.85rem;
          color: var(--text-secondary);
          text-align: center;
          padding: 1.5rem 0;
        }
      `}</style>
    </div>
  );
};

export default AILearningPathCard;
