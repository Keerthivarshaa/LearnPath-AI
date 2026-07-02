import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { authService } from '../services/api';
import { User as UserIcon, Mail, Lock, Target, Clock, Award, AlertCircle } from 'lucide-react';

const Register = () => {
  const navigate = useNavigate();
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [certificationGoal, setCertificationGoal] = useState('AWS Certified Solutions Architect');
  const [studyHoursPerWeek, setStudyHoursPerWeek] = useState(10);
  const [currentLevel, setCurrentLevel] = useState('Beginner');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    // Name Validation
    if (!name || !name.trim()) {
      setError('Name is required');
      setLoading(false);
      return;
    }
    const cleanName = name.trim();
    if (cleanName.length < 2 || cleanName.length > 50) {
      setError('Name must be between 2 and 50 characters');
      setLoading(false);
      return;
    }

    // Password Validation
    if (password.length < 8) {
      setError('Password must be at least 8 characters long');
      setLoading(false);
      return;
    }
    const hasUppercase = /[A-Z]/.test(password);
    const hasLowercase = /[a-z]/.test(password);
    const hasDigit = /[0-9]/.test(password);
    if (!hasUppercase || !hasLowercase || !hasDigit) {
      setError('Password must contain at least one uppercase letter, one lowercase letter, and one digit');
      setLoading(false);
      return;
    }

    try {
      const data = await authService.register({
        name: cleanName,
        email,
        password,
        certificationGoal,
        studyHoursPerWeek: parseInt(studyHoursPerWeek),
        currentLevel
      });

      // Data contains { token, id, name, email, certificationGoal, studyHoursPerWeek, currentLevel }
      localStorage.setItem('token', data.token);
      localStorage.setItem('user', JSON.stringify({
        id: data.id,
        name: data.name,
        email: data.email,
        certificationGoal: data.certificationGoal,
        studyHoursPerWeek: data.studyHoursPerWeek,
        currentLevel: data.currentLevel
      }));

      navigate('/dashboard');
    } catch (err) {
      if (err.response && err.response.data) {
        setError(err.response.data.message || err.response.data || 'Failed to create account');
      } else {
        setError('Connection to backend failed. Please try again.');
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="auth-wrapper fade-in">
      <div className="glass-card auth-card register-card">
        <div className="auth-header">
          <h2>Create Account</h2>
          <p className="auth-subtitle">Initialize your personalized study roadmap</p>
        </div>

        {error && (
          <div className="alert alert-error">
            <AlertCircle size={18} />
            <span>{error}</span>
          </div>
        )}

        <form onSubmit={handleSubmit} className="auth-form">
          <div className="form-group">
            <label className="form-label" htmlFor="name">Full Name</label>
            <div className="input-with-icon">
              <UserIcon className="input-icon" size={18} />
              <input
                id="name"
                type="text"
                required
                className="form-input"
                placeholder="Jane Doe"
                value={name}
                onChange={(e) => setName(e.target.value)}
              />
            </div>
          </div>

          <div className="form-group">
            <label className="form-label" htmlFor="email">Email Address</label>
            <div className="input-with-icon">
              <Mail className="input-icon" size={18} />
              <input
                id="email"
                type="email"
                required
                className="form-input"
                placeholder="jane@example.com"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
              />
            </div>
          </div>

          <div className="form-group">
            <label className="form-label" htmlFor="password">Password</label>
            <div className="input-with-icon">
              <Lock className="input-icon" size={18} />
              <input
                id="password"
                type="password"
                required
                className="form-input"
                placeholder="••••••••"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
              />
            </div>
          </div>

          <div className="grid-2">
            <div className="form-group">
              <label className="form-label" htmlFor="certification">Target Goal</label>
              <div className="input-with-icon">
                <Target className="input-icon" size={18} />
                <select
                  id="certification"
                  className="form-input form-select"
                  value={certificationGoal}
                  onChange={(e) => setCertificationGoal(e.target.value)}
                >
                  <option value="AWS Certified Solutions Architect">AWS Solutions Architect</option>
                  <option value="Oracle Certified Professional Java SE 17">Oracle Java SE 17 Developer</option>
                  <option value="Google Associate Cloud Engineer">Google Cloud Associate</option>
                  <option value="Azure Fundamentals AZ-900">Microsoft Azure Fundamentals</option>
                  <option value="CompTIA Security+">CompTIA Security+</option>
                </select>
              </div>
            </div>

            <div className="form-group">
              <label className="form-label" htmlFor="hours">Hours / Week</label>
              <div className="input-with-icon">
                <Clock className="input-icon" size={18} />
                <input
                  id="hours"
                  type="number"
                  min="1"
                  max="60"
                  required
                  className="form-input"
                  value={studyHoursPerWeek}
                  onChange={(e) => setStudyHoursPerWeek(e.target.value)}
                />
              </div>
            </div>
          </div>

          <div className="form-group">
            <label className="form-label" htmlFor="level">Experience Level</label>
            <div className="input-with-icon">
              <Award className="input-icon" size={18} />
              <select
                id="level"
                className="form-input form-select"
                value={currentLevel}
                onChange={(e) => setCurrentLevel(e.target.value)}
              >
                <option value="Beginner">Beginner (No prior framework experience)</option>
                <option value="Intermediate">Intermediate (Some professional practice)</option>
                <option value="Advanced">Advanced (Experienced software engineer)</option>
              </select>
            </div>
          </div>

          <button 
            type="submit" 
            disabled={loading}
            className="btn btn-primary w-full auth-btn"
          >
            {loading ? 'Creating Account...' : 'Get Started Now'}
          </button>
        </form>

        <div className="auth-footer">
          <p>Already have an account? <Link to="/login" className="auth-link">Sign In</Link></p>
        </div>
      </div>

      <style>{`
        .register-card {
          max-width: 500px;
        }
      `}</style>
    </div>
  );
};

export default Register;
