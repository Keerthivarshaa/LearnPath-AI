import React, { useState, useEffect } from 'react';
import api from '../services/api';
import { Compass, BookOpen, Clock, Target, PlayCircle, CheckCircle2, Lock, Sparkles, AlertCircle, ArrowRight, Loader2 } from 'lucide-react';
import { motion } from 'framer-motion';

const LearningRoadmap = ({ onStartAssessment }) => {
  const [roadmap, setRoadmap] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    fetchRoadmap();
  }, []);

  const fetchRoadmap = async () => {
    setLoading(true);
    setError('');
    try {
      const response = await api.get('/api/recommendation');
      setRoadmap(response.data);
    } catch (err) {
      console.error('Error fetching recommendation roadmap:', err);
      setError('Unable to load your personalized recommendation roadmap.');
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="roadmap-loader-screen">
        <Loader2 className="animate-spin text-cyan" size={40} />
        <p>Orchestrating learning milestones...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="glass-card roadmap-error-card fade-in">
        <AlertCircle size={40} className="error-icon" />
        <h3>Unable to load roadmap</h3>
        <p>{error}</p>
        <button onClick={fetchRoadmap} className="btn btn-secondary">
          Try Again
        </button>
      </div>
    );
  }

  // 1. Onboarding Mode
  if (!roadmap || roadmap.onboarding) {
    return (
      <div className="glass-card big-empty-card fade-in">
        <div className="card-gradient-top"></div>
        <Sparkles className="spark-decor" size={48} />
        <h2>Let's Orchestrate Your AI Learning Path</h2>
        <p className="onboarding-desc">
          Complete a quick diagnostic skill assessment first. Our engine will analyze your 
          strengths, tag your weak topics, and design a custom learning timeline matching your commitment.
        </p>
        <button onClick={onStartAssessment} className="btn btn-primary btn-onboard-cta">
          <span>Start Diagnostic Quiz</span>
          <ArrowRight size={15} />
        </button>
      </div>
    );
  }

  // 2. Normal Roadmap View
  return (
    <div className="learning-roadmap-layout fade-in">
      {/* Target summary banner */}
      <div className="glass-card roadmap-summary-banner">
        <div className="banner-badge">
          <Sparkles size={14} />
          <span>Personalized Syllabus Roadmap</span>
        </div>
        <h2>Target: {roadmap.certificationGoal}</h2>
        <p>Goal tier: <strong>{roadmap.currentLevel}</strong> • Commitment: <strong>{roadmap.weeklyStudyHours} Hours/Week</strong></p>

        <div className="roadmap-global-stats">
          <div className="stat-node">
            <span className="stat-label">Syllabus Progress</span>
            <div className="stat-progress-bar-container">
              <div className="progress-bar-fill" style={{ width: `${roadmap.completionPercentage}%` }}></div>
              <span className="progress-bar-text">{roadmap.completionPercentage}%</span>
            </div>
          </div>
          <div className="stat-node estimated-weeks-box">
            <Clock size={16} className="text-cyan" />
            <div>
              <span className="stat-label">Time Remaining</span>
              <h4>{roadmap.estimatedCompletionWeeks} {roadmap.estimatedCompletionWeeks === 1 ? 'Week' : 'Weeks'}</h4>
            </div>
          </div>
        </div>
      </div>

      <div className="roadmap-grid-layout">
        {/* Left Side: Roadmap Timeline */}
        <div className="roadmap-timeline-side">
          <h3 className="roadmap-side-title">Milestones Timeline</h3>
          <div className="roadmap-grid-timeline">
            <div className="timeline-line"></div>
            
            {roadmap.milestones?.map((milestone, idx) => {
              const status = milestone.status?.toUpperCase();
              
              return (
                <div key={idx} className={`timeline-node ${status?.toLowerCase()}`}>
                  <div className="node-icon-circle">
                    {status === 'COMPLETED' ? (
                      <CheckCircle2 size={18} />
                    ) : status === 'IN_PROGRESS' ? (
                      <PlayCircle size={18} />
                    ) : (
                      <Lock size={14} />
                    )}
                  </div>
                  
                  <div className="glass-card node-card">
                    <div className="node-card-header">
                      <span className="node-phase">PHASE {milestone.displayOrder} ({status.replace('_', ' ')})</span>
                      <span className="node-hours-badge">{milestone.estimatedHours}h</span>
                    </div>
                    <h3>{milestone.topic}</h3>
                    <p className="node-description">{milestone.category} • {milestone.difficulty}</p>
                    
                    {/* Active milestone resources */}
                    {status === 'IN_PROGRESS' && (
                      <div className="active-details-panel">
                        {milestone.prerequisites?.length > 0 && (
                          <div className="details-sub-row">
                            <strong>Prerequisites:</strong>
                            <div className="prereq-chips">
                              {milestone.prerequisites.map((p, i) => (
                                <span key={i} className="prereq-chip">{p}</span>
                              ))}
                            </div>
                          </div>
                        )}
                        {milestone.recommendedResources?.length > 0 && (
                          <div className="details-sub-row resources-sub-row">
                            <strong>Study Resources:</strong>
                            <ul className="resources-bullet-list">
                              {milestone.recommendedResources.map((res, i) => (
                                <li key={i}>{res}</li>
                              ))}
                            </ul>
                          </div>
                        )}
                      </div>
                    )}
                  </div>
                </div>
              );
            })}
          </div>
        </div>

        {/* Right Side: Priority topics & Study Plan */}
        <div className="roadmap-details-side">
          <div className="glass-card study-plan-card">
            <Target className="text-purple" size={20} />
            <h3>Daily Study Plan</h3>
            <p>{roadmap.dailyStudyPlan}</p>
          </div>

          <div className="glass-card priority-topics-card">
            <BookOpen className="text-cyan" size={20} />
            <h3>Syllabus Priorities</h3>
            <div className="priority-chips-box">
              {roadmap.priorityTopics?.map((topic, i) => (
                <span key={i} className={`priority-chip-item ${i === 0 ? 'top-priority' : ''}`}>
                  {i === 0 && <span className="top-priority-dot"></span>}
                  {topic}
                </span>
              ))}
            </div>
          </div>

          <div className="glass-card weekly-schedule-card">
            <Compass className="text-cyan" size={20} />
            <h3>Weekly Plan</h3>
            <div className="weekly-steps-list">
              {roadmap.weeklyPlan && Object.entries(roadmap.weeklyPlan).map(([week, desc], i) => (
                <div key={i} className="weekly-step-node">
                  <span className="step-week-tag">{week}</span>
                  <p>{desc}</p>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>

      <style>{`
        .learning-roadmap-layout {
          display: flex;
          flex-direction: column;
          gap: 2rem;
          max-width: 1000px;
          margin: 0 auto;
        }
        .roadmap-loader-screen {
          display: flex;
          flex-direction: column;
          align-items: center;
          justify-content: center;
          height: 300px;
          gap: 1rem;
          color: var(--text-secondary);
        }
        .roadmap-error-card {
          text-align: center;
          padding: 3rem;
          max-width: 450px;
          margin: 3rem auto;
          display: flex;
          flex-direction: column;
          align-items: center;
          gap: 1rem;
        }
        .error-icon {
          color: #ef4444;
        }
        
        .onboarding-desc {
          font-size: 0.95rem;
          color: var(--text-secondary);
          max-width: 500px;
          line-height: 1.6;
          margin-bottom: 0.5rem;
        }
        .btn-onboard-cta {
          margin-top: 1rem;
        }
        
        /* Summary Banner */
        .roadmap-summary-banner {
          background: linear-gradient(135deg, rgba(124,58,237,0.06) 0%, rgba(6,182,212,0.04) 100%);
          padding: 2.5rem;
          border-color: rgba(255,255,255,0.05);
        }
        .banner-badge {
          display: inline-flex;
          align-items: center;
          gap: 0.4rem;
          background: rgba(124,58,237,0.12);
          border: 1px solid rgba(124,58,237,0.25);
          color: #c084fc;
          font-size: 0.75rem;
          padding: 0.25rem 0.6rem;
          border-radius: 50px;
          font-weight: 600;
          margin-bottom: 0.75rem;
        }
        .roadmap-summary-banner h2 {
          font-size: 1.8rem;
          color: white;
        }
        .roadmap-summary-banner p {
          color: var(--text-secondary);
          font-size: 0.9rem;
          margin-top: 0.25rem;
        }
        
        .roadmap-global-stats {
          display: flex;
          align-items: center;
          justify-content: space-between;
          gap: 2rem;
          margin-top: 2rem;
          padding-top: 1.5rem;
          border-top: 1px solid rgba(255,255,255,0.05);
          flex-wrap: wrap;
        }
        .stat-node {
          display: flex;
          flex-direction: column;
          gap: 0.5rem;
          min-width: 200px;
        }
        .stat-label {
          font-size: 0.75rem;
          font-weight: 700;
          color: var(--text-muted);
          text-transform: uppercase;
          letter-spacing: 0.05em;
        }
        .stat-progress-bar-container {
          position: relative;
          height: 14px;
          background: rgba(255,255,255,0.05);
          border-radius: 50px;
          overflow: hidden;
          display: flex;
          align-items: center;
        }
        .progress-bar-fill {
          height: 100%;
          background: linear-gradient(90deg, var(--accent-purple) 0%, var(--accent-cyan) 100%);
          border-radius: 50px;
          transition: width 0.3s ease;
        }
        .progress-bar-text {
          position: absolute;
          right: 0.6rem;
          font-size: 0.65rem;
          font-weight: 800;
          color: white;
        }
        .estimated-weeks-box {
          flex-direction: row;
          align-items: center;
          gap: 0.75rem;
          min-width: 150px;
        }
        .estimated-weeks-box h4 {
          font-size: 1.25rem;
          color: white;
        }
        
        /* Grid timeline */
        .roadmap-grid-layout {
          display: grid;
          grid-template-columns: 1fr;
          gap: 2rem;
        }
        @media (min-width: 900px) {
          .roadmap-grid-layout {
            grid-template-columns: 1.6fr 1fr;
          }
        }
        
        .roadmap-side-title {
          font-size: 1.15rem;
          color: white;
          margin-bottom: 1.5rem;
        }
        
        .roadmap-timeline-side {
          display: flex;
          flex-direction: column;
        }
        
        .roadmap-details-side {
          display: flex;
          flex-direction: column;
          gap: 1.5rem;
        }
        
        /* Right sidebar widgets */
        .study-plan-card, .priority-topics-card, .weekly-schedule-card {
          padding: 1.75rem;
          background: rgba(19,27,46,0.35);
          display: flex;
          flex-direction: column;
          gap: 0.75rem;
        }
        .study-plan-card h3, .priority-topics-card h3, .weekly-schedule-card h3 {
          font-size: 0.95rem;
          color: white;
        }
        .study-plan-card p {
          font-size: 0.85rem;
          color: var(--text-secondary);
          line-height: 1.5;
        }
        
        .priority-chips-box {
          display: flex;
          flex-wrap: wrap;
          gap: 0.5rem;
        }
        .priority-chip-item {
          font-size: 0.75rem;
          font-weight: 600;
          background: rgba(255,255,255,0.03);
          border: 1px solid rgba(255,255,255,0.06);
          color: var(--text-secondary);
          padding: 0.3rem 0.65rem;
          border-radius: 50px;
          display: flex;
          align-items: center;
          gap: 0.35rem;
        }
        .top-priority {
          background: rgba(6,182,212,0.08);
          border-color: rgba(6,182,212,0.25);
          color: var(--accent-cyan);
        }
        .top-priority-dot {
          width: 5px;
          height: 5px;
          background: var(--accent-cyan);
          border-radius: 50%;
          box-shadow: 0 0 6px var(--accent-cyan);
        }
        
        .weekly-steps-list {
          display: flex;
          flex-direction: column;
          gap: 1rem;
        }
        .weekly-step-node {
          display: flex;
          flex-direction: column;
          gap: 0.2rem;
          padding-left: 0.75rem;
          border-left: 2px solid rgba(255,255,255,0.05);
        }
        .step-week-tag {
          font-size: 0.7rem;
          font-weight: 800;
          color: var(--accent-purple);
          text-transform: uppercase;
        }
        .weekly-step-node p {
          font-size: 0.8rem;
          color: var(--text-secondary);
          line-height: 1.4;
        }
        
        /* Active Details panel */
        .active-details-panel {
          margin-top: 1rem;
          padding-top: 1rem;
          border-top: 1px solid rgba(255,255,255,0.05);
          display: flex;
          flex-direction: column;
          gap: 0.75rem;
        }
        .details-sub-row {
          font-size: 0.8rem;
          display: flex;
          flex-direction: column;
          gap: 0.35rem;
        }
        .prereq-chips {
          display: flex;
          gap: 0.4rem;
        }
        .prereq-chip {
          background: rgba(255,255,255,0.03);
          border: 1px solid rgba(255,255,255,0.05);
          color: var(--text-muted);
          padding: 0.15rem 0.5rem;
          border-radius: 4px;
          font-size: 0.7rem;
        }
        .resources-bullet-list {
          list-style-type: none;
          padding-left: 0.75rem;
          display: flex;
          flex-direction: column;
          gap: 0.25rem;
        }
        .resources-bullet-list li {
          position: relative;
          color: var(--accent-cyan);
          font-weight: 500;
          font-size: 0.75rem;
        }
        .resources-bullet-list li::before {
          content: '•';
          position: absolute;
          left: -0.75rem;
          color: var(--text-muted);
        }
        .node-description {
          font-size: 0.8rem;
          color: var(--text-muted);
          margin-top: 0.2rem;
        }
        .node-card-header {
          display: flex;
          justify-content: space-between;
          align-items: center;
          width: 100%;
        }
        .node-hours-badge {
          font-size: 0.7rem;
          font-weight: 700;
          background: rgba(255,255,255,0.04);
          border: 1px solid rgba(255,255,255,0.08);
          color: var(--text-secondary);
          padding: 0.15rem 0.45rem;
          border-radius: 4px;
        }
      `}</style>
    </div>
  );
};

export default LearningRoadmap;
