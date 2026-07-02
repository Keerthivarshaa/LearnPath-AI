import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { motion, AnimatePresence } from 'framer-motion';
import api from '../services/api';

// Import modular SaaS components
import Sidebar from '../components/Sidebar';
import Header from '../components/Header';
import StatCard from '../components/StatCard';
import ProgressCard from '../components/ProgressCard';
import AILearningPathCard from '../components/AILearningPathCard';
import Assessment from './Assessment';
import LearningRoadmap from './LearningRoadmap';
import AITutor from './AITutor';

import { 
  Clock, Target, Shield, AlertCircle, Plus, RefreshCw, Award, Bell, CheckCircle2, Flame, Trophy, Lock, Sparkles
} from 'lucide-react';

const Dashboard = () => {
  const navigate = useNavigate();
  const [user, setUser] = useState(null);
  const [roadmapData, setRoadmapData] = useState(null);
  const [progressData, setProgressData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [activeTab, setActiveTab] = useState('overview');
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const [reloadTrigger, setReloadTrigger] = useState(0);
  const [toasts, setToasts] = useState([]);

  // Time logging states
  const [newLogHours, setNewLogHours] = useState('');
  const [newLogTopic, setNewLogTopic] = useState('');

  // Settings states
  const [settingsGoal, setSettingsGoal] = useState('');
  const [settingsHours, setSettingsHours] = useState(10);
  const [settingsLevel, setSettingsLevel] = useState('Beginner');
  const [settingsSuccess, setSettingsSuccess] = useState('');

  // Achievements template list
  const achievementsList = [
    { key: 'First Assessment', title: 'First Assessment', desc: 'Completed your first diagnostic test', xp: 150, icon: Target },
    { key: 'First Study Session', title: 'First Study Session', desc: 'Logged your first learning session', xp: 50, icon: Clock },
    { key: '7-Day Streak', title: '7-Day Streak', desc: 'Maintained a 7-day study streak', xp: 150, icon: Flame },
    { key: '30-Day Streak', title: '30-Day Streak', desc: 'Maintained a 30-day study streak', xp: 300, icon: Trophy },
    { key: 'Level 5', title: 'Level 5 Prep Master', desc: 'Reached preparation Level 5', xp: 250, icon: Award },
    { key: '1000 XP', title: '1000 XP Club', desc: 'Accumulated 1000 total experience points', xp: 100, icon: Sparkles }
  ];

  useEffect(() => {
    fetchUserProfileRoadmapAndProgress();
  }, [navigate, reloadTrigger]);

  const fetchUserProfileRoadmapAndProgress = async () => {
    try {
      const profileRes = await api.get('/api/user/me');
      setUser(profileRes.data);
      
      // Initialize settings states
      setSettingsGoal(profileRes.data.certificationGoal);
      setSettingsHours(profileRes.data.studyHoursPerWeek);
      setSettingsLevel(profileRes.data.currentLevel);

      // Fetch dynamic roadmap recommendation
      const roadmapRes = await api.get('/api/recommendation');
      setRoadmapData(roadmapRes.data);

      // Fetch dynamic progress
      const progressRes = await api.get('/api/progress');
      setProgressData(progressRes.data);

      // Trigger toasts for backend notifications
      if (progressRes.data.notifications && progressRes.data.notifications.length > 0) {
        progressRes.data.notifications.forEach((notif, idx) => {
          setTimeout(() => {
            setToasts(prev => [...prev, { id: Date.now() + idx, message: notif }]);
          }, idx * 800);
        });
      }
    } catch (err) {
      console.error('Error fetching dashboard states:', err);
      setError('Failed to load user profile. Please log in again.');
      if (err.response && err.response.status === 401) {
        localStorage.removeItem('token');
        localStorage.removeItem('user');
        navigate('/login');
      }
    } finally {
      setLoading(false);
    }
  };

  const handleLogout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    navigate('/login');
  };

  // Handle study log submission
  const handleAddLog = async (e) => {
    e.preventDefault();
    if (!newLogHours || !newLogTopic) return;
    try {
      const res = await api.post('/api/progress/study-log', {
        hours: parseFloat(newLogHours),
        topic: newLogTopic
      });
      setProgressData(res.data);

      // Refetch recommendation roadmap so milestones updates are synced
      const roadmapRes = await api.get('/api/recommendation');
      setRoadmapData(roadmapRes.data);
      
      // Show newly received toasts if any
      if (res.data.notifications && res.data.notifications.length > 0) {
        res.data.notifications.forEach((notif, idx) => {
          setTimeout(() => {
            setToasts(prev => [...prev, { id: Date.now() + idx, message: notif }]);
          }, idx * 800);
        });
      }

      setNewLogHours('');
      setNewLogTopic('');
    } catch (err) {
      console.error('Error logging study hours:', err);
    }
  };

  // Update profile settings mock
  const handleSaveSettings = (e) => {
    e.preventDefault();
    setSettingsSuccess('');
    
    // Update local user state to reflect settings change
    setUser(prev => ({
      ...prev,
      certificationGoal: settingsGoal,
      studyHoursPerWeek: parseInt(settingsHours),
      currentLevel: settingsLevel
    }));
    
    setSettingsSuccess('Settings updated successfully!');
    setTimeout(() => setSettingsSuccess(''), 3000);
  };

  const triggerAssessmentReload = () => {
    setReloadTrigger(prev => prev + 1);
  };

  const removeToast = (id) => {
    setToasts(prev => prev.filter(t => t.id !== id));
  };

  if (loading) {
    return (
      <div className="skeleton-container container fade-in">
        <div className="skeleton-sidebar"></div>
        <div className="skeleton-content">
          <div className="skeleton-header"></div>
          <div className="skeleton-hero"></div>
          <div className="skeleton-cards">
            <div className="skeleton-card"></div>
            <div className="skeleton-card"></div>
            <div className="skeleton-card"></div>
          </div>
        </div>
      </div>
    );
  }

  if (error || !user) {
    return (
      <div className="dashboard-error-wrapper fade-in">
        <div className="glass-card error-card">
          <AlertCircle size={40} className="error-icon" />
          <h2>Unable to Connect</h2>
          <p>{error || 'An unexpected authentication error occurred.'}</p>
          <button onClick={() => navigate('/login')} className="btn btn-primary">
            Go to Sign In
          </button>
        </div>
      </div>
    );
  }

  const isRoadmapOrchestrated = roadmapData && !roadmapData.onboarding;

  return (
    <div className="saas-dashboard-container">
      {/* Dynamic Toasts Center */}
      <div className="toast-notifications-hub">
        <AnimatePresence>
          {toasts.map((toast) => (
            <motion.div
              key={toast.id}
              initial={{ opacity: 0, x: 50, y: -20 }}
              animate={{ opacity: 1, x: 0, y: 0 }}
              exit={{ opacity: 0, x: 50 }}
              className="glass-card toast-alert-node"
            >
              <div className="toast-alert-content">
                <Bell size={16} className="text-cyan animate-pulse" />
                <span>{toast.message}</span>
              </div>
              <button onClick={() => removeToast(toast.id)} className="toast-close-btn">&times;</button>
            </motion.div>
          ))}
        </AnimatePresence>
      </div>

      {/* Sidebar Navigation */}
      <Sidebar 
        activeTab={activeTab} 
        setActiveTab={setActiveTab} 
        user={user} 
        sidebarOpen={sidebarOpen} 
        roadmapGenerated={isRoadmapOrchestrated}
      />

      {/* Main Content Dashboard Frame */}
      <main className="saas-main">
        {/* Top Header Navigation */}
        <Header activeTab={activeTab} handleLogout={handleLogout} />

        {/* Tab Views Frame */}
        <div className="saas-content">
          <AnimatePresence mode="wait">
            {activeTab === 'overview' && (
              <motion.div
                key="overview"
                initial={{ opacity: 0, y: 15 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -15 }}
                transition={{ duration: 0.25 }}
                className="overview-tab-content"
              >
                {/* Modern Welcoming Card */}
                <div className="glass-card hero-welcome-card">
                  <div className="hero-glow"></div>
                  <div className="hero-text-side">
                    <span className="hero-small-tag">PERSONAL DEVELOPMENT CONSOLE</span>
                    <h1>Welcome back, {user.name}!</h1>
                    <p>
                      Your customized curriculum prep console is active. Finish your diagnostic test, 
                      compile your roadmap milestones, and optimize study times.
                    </p>
                    {!isRoadmapOrchestrated && (
                      <button 
                        onClick={() => setActiveTab('assessment')} 
                        className="btn btn-primary hero-cta-btn"
                      >
                        <span>Start Diagnostic Assessment</span>
                      </button>
                    )}
                  </div>
                  <div className="hero-badge-side">
                    <div className="badge-hexagon">
                      <RefreshCw size={32} className="hexagon-spark animate-spin-slow" />
                    </div>
                  </div>
                </div>

                {/* Profile Stats Matrix Grid */}
                <section className="stats-matrix grid-3">
                  <StatCard 
                    icon={Target} 
                    label="Goal Roadmap" 
                    value={user.certificationGoal} 
                    gradientClass="purple-gradient"
                  />
                  <StatCard 
                    icon={Flame} 
                    label="Preparation Streak" 
                    value={progressData ? `${progressData.currentStreak} Days Active` : '0 Days Active'} 
                    gradientClass="cyan-gradient"
                  />
                  <StatCard 
                    icon={Award} 
                    label="XP Level Rating" 
                    value={progressData ? `Level ${progressData.level} (${progressData.xp} XP)` : 'Level 1'} 
                    gradientClass="gold-gradient"
                  />
                </section>

                {/* Bottom Overview Split Section */}
                <div className="grid-2 bottom-split-panel">
                  {/* Left Side: Circular Progress Widget */}
                  <ProgressCard progressData={progressData} />

                  {/* Right Side: Continue Learning Module List */}
                  <AILearningPathCard 
                    roadmapData={roadmapData} 
                    onStartAssessment={() => setActiveTab('assessment')}
                  />
                </div>
              </motion.div>
            )}

            {/* Learning Path Tab View */}
            {activeTab === 'path' && (
              <motion.div
                key="path"
                initial={{ opacity: 0, y: 15 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -15 }}
                transition={{ duration: 0.25 }}
                className="path-tab-content"
              >
                <LearningRoadmap 
                  key={reloadTrigger} 
                  onStartAssessment={() => setActiveTab('assessment')} 
                />
              </motion.div>
            )}

            {/* AI Tutor Tab View */}
            {activeTab === 'tutor' && (
              <motion.div
                key="tutor"
                initial={{ opacity: 0, y: 15 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -15 }}
                transition={{ duration: 0.25 }}
                className="tutor-tab-content"
              >
                <AITutor onProgressUpdated={triggerAssessmentReload} />
              </motion.div>
            )}

            {/* Assessment Tab View */}
            {activeTab === 'assessment' && (
              <motion.div
                key="assessment"
                initial={{ opacity: 0, y: 15 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -15 }}
                transition={{ duration: 0.25 }}
                className="assessment-tab-content"
              >
                <Assessment onAssessmentComplete={triggerAssessmentReload} />
              </motion.div>
            )}

            {/* Progress Tab View */}
            {activeTab === 'progress' && (
              <motion.div
                key="progress"
                initial={{ opacity: 0, y: 15 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -15 }}
                transition={{ duration: 0.25 }}
                className="progress-tab-content grid-2"
              >
                {/* Hour Logging Form */}
                <div className="glass-card tracker-widget">
                  <div className="widget-header">
                    <h3>Study Time Tracker</h3>
                    <span className="widget-subtitle">Log your preparation sessions (+50 XP/h)</span>
                  </div>

                  <form onSubmit={handleAddLog} className="log-form">
                    <div className="form-group">
                      <label className="form-label" htmlFor="logHours">Hours Spent</label>
                      <input
                        id="logHours"
                        type="number"
                        step="0.5"
                        min="0.5"
                        max="24"
                        required
                        className="form-input"
                        placeholder="e.g. 2.5"
                        value={newLogHours}
                        onChange={(e) => setNewLogHours(e.target.value)}
                      />
                    </div>
                    
                    <div className="form-group">
                      <label className="form-label" htmlFor="logTopic">Topic Covered</label>
                      <select
                        id="logTopic"
                        required
                        className="form-input form-select"
                        value={newLogTopic}
                        onChange={(e) => setNewLogTopic(e.target.value)}
                      >
                        <option value="">Select study topic...</option>
                        {/* AWS */}
                        <option value="EC2 Instance Models">AWS EC2 Instance Models</option>
                        <option value="IAM Security">AWS IAM Security</option>
                        <option value="RDS Scalability">AWS RDS Scalability</option>
                        <option value="VPC Networking">AWS VPC Networking</option>
                        {/* Java */}
                        <option value="Garbage Collection">Java Garbage Collection</option>
                        <option value="Pattern Matching">Java Pattern Matching</option>
                        <option value="JDBC Pools">Java JDBC Connection Pools</option>
                        {/* Security+ */}
                        <option value="Cryptography">Security Cryptography</option>
                        <option value="Network Security">Security Network Security</option>
                        {/* Azure */}
                        <option value="Azure Storage">Azure Storage Solutions</option>
                        <option value="Azure Regions">Azure Regions & High Availability</option>
                        <option value="Azure Governance">Azure Management & Governance</option>
                      </select>
                    </div>

                    <button type="submit" className="btn btn-primary w-full">
                      <Plus size={16} />
                      <span>Log Study Session</span>
                    </button>
                  </form>
                </div>

                {/* Achievements List widget */}
                <div className="glass-card tracker-widget achievements-panel">
                  <div className="widget-header">
                    <h3>Unlocked Badges</h3>
                    <span className="widget-subtitle">Preparational milestone awards</span>
                  </div>

                  <div className="achievements-grid-list">
                    {achievementsList.map((ach) => {
                      const isUnlocked = progressData?.unlockedAchievements?.includes(ach.key);
                      const IconComponent = ach.icon;

                      return (
                        <div key={ach.key} className={`achievement-item-box ${isUnlocked ? 'unlocked' : 'locked'}`}>
                          <div className="achievement-icon-circle">
                            {isUnlocked ? <IconComponent size={18} /> : <Lock size={14} />}
                          </div>
                          <div className="achievement-info">
                            <h4>{ach.title}</h4>
                            <p>{ach.desc} (+{ach.xp} XP)</p>
                          </div>
                        </div>
                      );
                    })}
                  </div>
                </div>
              </motion.div>
            )}

            {/* Settings Tab View */}
            {activeTab === 'settings' && (
              <motion.div
                key="settings"
                initial={{ opacity: 0, y: 15 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -15 }}
                transition={{ duration: 0.25 }}
                className="settings-tab-content"
              >
                <div className="glass-card settings-card">
                  <div className="widget-header">
                    <h3>Preferences & Core Goal</h3>
                    <span className="widget-subtitle">Manage roadmap settings & difficulty rating</span>
                  </div>

                  {settingsSuccess && (
                    <div className="alert alert-success">
                      <CheckCircle2 size={18} />
                      <span>{settingsSuccess}</span>
                    </div>
                  )}

                  <form onSubmit={handleSaveSettings} className="settings-form">
                    <div className="form-group">
                      <label className="form-label" htmlFor="setGoal">Certification Target Goal</label>
                      <select
                        id="setGoal"
                        className="form-input form-select"
                        value={settingsGoal}
                        onChange={(e) => setSettingsGoal(e.target.value)}
                      >
                        <option value="AWS Certified Solutions Architect">AWS Solutions Architect</option>
                        <option value="Oracle Certified Professional Java SE 17">Oracle Java SE 17 Developer</option>
                        <option value="Google Associate Cloud Engineer">Google Cloud Associate</option>
                        <option value="Azure Fundamentals AZ-900">Microsoft Azure Fundamentals</option>
                        <option value="CompTIA Security+">CompTIA Security+</option>
                      </select>
                    </div>

                    <div className="form-group">
                      <label className="form-label" htmlFor="setHours">Weekly Hour Target</label>
                      <input
                        id="setHours"
                        type="number"
                        min="1"
                        max="60"
                        className="form-input"
                        value={settingsHours}
                        onChange={(e) => setSettingsHours(e.target.value)}
                      />
                    </div>

                    <div className="form-group">
                      <label className="form-label" htmlFor="setLevel">Current Rating Tier</label>
                      <select
                        id="setLevel"
                        className="form-input form-select"
                        value={settingsLevel}
                        onChange={(e) => setSettingsLevel(e.target.value)}
                      >
                        <option value="Beginner">Beginner (Basic Syntax / No cloud history)</option>
                        <option value="Intermediate">Intermediate (Some framework projects)</option>
                        <option value="Advanced">Advanced (Experienced Architect)</option>
                      </select>
                    </div>

                    <button type="submit" className="btn btn-primary">
                      Save Changes
                    </button>
                  </form>
                </div>
              </motion.div>
            )}
          </AnimatePresence>
        </div>
      </main>
    </div>
  );
};

export default Dashboard;
