import React, { useState, useEffect, useRef } from 'react';
import api from '../services/api';
import QuestionCard from '../components/QuestionCard';
import AssessmentResult from '../components/AssessmentResult';
import { Sparkles, Play, Clock, ChevronLeft, ChevronRight, CheckCircle2, ShieldAlert, Loader2, BookOpen } from 'lucide-react';
import { motion } from 'framer-motion';

const Assessment = ({ onAssessmentComplete }) => {
  const [latestResult, setLatestResult] = useState(null);
  const [questions, setQuestions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [quizStarted, setQuizStarted] = useState(false);
  const [currentIdx, setCurrentIdx] = useState(0);
  const [selectedAnswers, setSelectedAnswers] = useState({});
  const [timeLeft, setTimeLeft] = useState(300); // 5 minutes in seconds

  const timerRef = useRef(null);

  useEffect(() => {
    fetchLatestResult();
  }, []);

  // Timer Countdown Logic
  useEffect(() => {
    if (quizStarted && timeLeft > 0) {
      timerRef.current = setInterval(() => {
        setTimeLeft((prev) => prev - 1);
      }, 1000);
    } else if (timeLeft === 0 && quizStarted) {
      clearInterval(timerRef.current);
      handleSubmitQuiz(); // Auto submit
    }

    return () => clearInterval(timerRef.current);
  }, [quizStarted, timeLeft]);

  const fetchLatestResult = async () => {
    setLoading(true);
    try {
      const response = await api.get('/api/assessment/result');
      if (response.status === 200 && response.data) {
        setLatestResult(response.data);
      }
    } catch (err) {
      // 404 indicates no test has been taken yet, which is expected
      console.log('No previous assessment result found.');
    } finally {
      setLoading(false);
    }
  };

  const startQuiz = async () => {
    setLoading(true);
    try {
      const response = await api.get('/api/assessment/questions');
      setQuestions(response.data);
      setSelectedAnswers({});
      setCurrentIdx(0);
      setTimeLeft(300);
      setQuizStarted(true);
      setLatestResult(null);
    } catch (err) {
      console.error('Error fetching questions:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleSelectOption = (questionId, optionId) => {
    setSelectedAnswers((prev) => ({
      ...prev,
      [questionId]: optionId,
    }));
  };

  const handleNext = () => {
    if (currentIdx < questions.length - 1) {
      setCurrentIdx(currentIdx + 1);
    }
  };

  const handlePrev = () => {
    if (currentIdx > 0) {
      setCurrentIdx(currentIdx - 1);
    }
  };

  const handleSubmitQuiz = async () => {
    clearInterval(timerRef.current);
    setSubmitting(true);
    try {
      const response = await api.post('/api/assessment/submit', {
        answers: selectedAnswers,
      });
      setLatestResult(response.data);
      setQuizStarted(false);
      if (onAssessmentComplete) onAssessmentComplete();
    } catch (err) {
      console.error('Error submitting assessment:', err);
    } finally {
      setSubmitting(false);
    }
  };

  const handleRetake = () => {
    setLatestResult(null);
    setQuizStarted(false);
  };

  // Helper to format remaining time
  const formatTime = (seconds) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins}:${secs < 10 ? '0' : ''}${secs}`;
  };

  if (loading) {
    return (
      <div className="quiz-loader-screen">
        <Loader2 className="animate-spin text-cyan" size={40} />
        <p>Loading assessment panel...</p>
      </div>
    );
  }

  // 1. Render Test Result Screen if complete
  if (latestResult && !quizStarted) {
    return (
      <div className="assessment-page-frame">
        <div className="section-intro">
          <h1>Assessment Results</h1>
          <p className="subtitle">Review your diagnostic scores and personalized skill categorizations.</p>
        </div>
        <AssessmentResult result={latestResult} onRetake={handleRetake} />
      </div>
    );
  }

  // 2. Render Quiz Interface when started
  if (quizStarted && questions.length > 0) {
    const activeQuestion = questions[currentIdx];
    const isLastQuestion = currentIdx === questions.length - 1;
    const progressPercent = Math.round(((currentIdx + 1) / questions.length) * 100);

    return (
      <div className="assessment-page-frame quiz-active-layout">
        {/* Quiz Progress & Timer Header */}
        <div className="quiz-status-header glass-card">
          <div className="status-progress-side">
            <span className="quiz-progress-text">Progress: {progressPercent}%</span>
            <div className="quiz-progress-bar-bg">
              <div className="quiz-progress-bar-fill" style={{ width: `${progressPercent}%` }}></div>
            </div>
          </div>
          <div className="status-timer-side">
            <Clock size={16} className="timer-icon" />
            <span className="timer-countdown">{formatTime(timeLeft)}</span>
          </div>
        </div>

        {/* Current Question Card */}
        <QuestionCard
          question={activeQuestion}
          questionIndex={currentIdx}
          totalQuestions={questions.length}
          selectedOptionId={selectedAnswers[activeQuestion.id]}
          onSelectOption={handleSelectOption}
        />

        {/* Quiz Action Navigation Footer */}
        <div className="quiz-navigation-footer">
          <button onClick={handlePrev} disabled={currentIdx === 0} className="btn btn-secondary nav-btn-left">
            <ChevronLeft size={16} />
            <span>Previous</span>
          </button>

          {isLastQuestion ? (
            <button 
              onClick={handleSubmitQuiz} 
              disabled={submitting}
              className="btn btn-primary btn-submit-quiz"
            >
              {submitting ? (
                <>
                  <Loader2 className="animate-spin" size={16} />
                  <span>Grading Answers...</span>
                </>
              ) : (
                <>
                  <CheckCircle2 size={16} />
                  <span>Submit Assessment</span>
                </>
              )}
            </button>
          ) : (
            <button onClick={handleNext} className="btn btn-secondary nav-btn-right">
              <span>Next</span>
              <ChevronRight size={16} />
            </button>
          )}
        </div>
      </div>
    );
  }

  // 3. Render Quiz Welcome / Start Screen
  return (
    <div className="assessment-page-frame welcome-screen-layout fade-in">
      <div className="glass-card start-assessment-card">
        <div className="card-top-decoration"></div>
        <Sparkles className="welcome-spark animate-bounce" size={48} />
        <h2>Diagnostic Skill Assessment</h2>
        <p className="welcome-desc">
          Evaluate your architectural, programming, and database design capabilities before 
          generating your customized AI learning path.
        </p>

        <div className="assessment-rules-grid">
          <div className="rule-item">
            <Clock className="rule-icon text-cyan" size={18} />
            <div>
              <h4>5 Minutes Limit</h4>
              <p>The quiz has a global timer and auto-submits when time expires.</p>
            </div>
          </div>
          <div className="rule-item">
            <BookOpen className="rule-icon text-purple" size={18} />
            <div>
              <h4>Topic-based Grading</h4>
              <p>Dynamic sorting automatically maps your strong vs. weak learning topics.</p>
            </div>
          </div>
        </div>

        <button onClick={startQuiz} className="btn btn-primary btn-start-now">
          <Play size={15} />
          <span>Start Assessment</span>
        </button>
      </div>

      <style>{`
        .assessment-page-frame {
          max-width: 800px;
          margin: 0 auto;
          display: flex;
          flex-direction: column;
          gap: 1.5rem;
        }
        .section-intro {
          margin-bottom: 0.5rem;
        }
        .section-intro h1 {
          font-size: 1.8rem;
          color: white;
        }
        .section-intro .subtitle {
          color: var(--text-secondary);
          font-size: 0.95rem;
          margin-top: 0.25rem;
        }
        .quiz-loader-screen {
          display: flex;
          flex-direction: column;
          align-items: center;
          justify-content: center;
          height: 300px;
          gap: 1rem;
          color: var(--text-secondary);
          font-size: 0.95rem;
        }
        .text-cyan { color: var(--accent-cyan); }
        .text-purple { color: var(--accent-purple); }
        
        /* Welcome / Start layout */
        .start-assessment-card {
          position: relative;
          text-align: center;
          padding: 4rem 2.5rem;
          display: flex;
          flex-direction: column;
          align-items: center;
          gap: 1.5rem;
          overflow: hidden;
          background: rgba(19, 27, 46, 0.45);
        }
        .card-top-decoration {
          position: absolute;
          top: 0;
          left: 0;
          width: 100%;
          height: 4px;
          background: linear-gradient(90deg, var(--accent-purple) 0%, var(--accent-cyan) 100%);
        }
        .welcome-spark {
          color: var(--accent-cyan);
          filter: drop-shadow(0 0 10px var(--accent-cyan-glow));
        }
        .start-assessment-card h2 {
          font-size: 1.8rem;
          color: white;
        }
        .welcome-desc {
          font-size: 0.95rem;
          color: var(--text-secondary);
          max-width: 520px;
          line-height: 1.6;
        }
        .assessment-rules-grid {
          display: grid;
          grid-template-columns: 1fr;
          gap: 1.5rem;
          width: 100%;
          max-width: 520px;
          margin-top: 1rem;
          text-align: left;
        }
        @media (min-width: 600px) {
          .assessment-rules-grid {
            grid-template-columns: 1fr 1fr;
          }
        }
        .rule-item {
          display: flex;
          gap: 1rem;
          padding: 1.25rem;
          background: rgba(0,0,0,0.15);
          border: 1px solid rgba(255,255,255,0.05);
          border-radius: var(--radius-sm);
        }
        .rule-icon {
          flex-shrink: 0;
          margin-top: 0.15rem;
        }
        .rule-item h4 {
          font-size: 0.9rem;
          color: white;
          margin-bottom: 0.15rem;
        }
        .rule-item p {
          font-size: 0.75rem;
          color: var(--text-muted);
          line-height: 1.4;
        }
        .btn-start-now {
          margin-top: 1rem;
          font-size: 1rem;
          padding: 0.85rem 2rem;
        }

        /* Quiz Active Layout */
        .quiz-status-header {
          display: flex;
          justify-content: space-between;
          align-items: center;
          padding: 1.25rem 2rem;
          background: rgba(19, 27, 46, 0.5);
          border-color: rgba(255,255,255,0.05);
        }
        .status-progress-side {
          display: flex;
          flex-direction: column;
          gap: 0.5rem;
          width: 60%;
        }
        .quiz-progress-text {
          font-size: 0.75rem;
          font-weight: 700;
          color: var(--text-secondary);
        }
        .quiz-progress-bar-bg {
          height: 6px;
          background: rgba(255,255,255,0.05);
          border-radius: 10px;
          overflow: hidden;
          width: 100%;
        }
        .quiz-progress-bar-fill {
          height: 100%;
          background: linear-gradient(90deg, var(--accent-purple) 0%, var(--accent-cyan) 100%);
          border-radius: 10px;
          transition: width 0.3s ease;
        }
        .status-timer-side {
          display: flex;
          align-items: center;
          gap: 0.5rem;
          background: rgba(239,68,68,0.1);
          border: 1px solid rgba(239,68,68,0.25);
          color: #fca5a5;
          padding: 0.4rem 0.85rem;
          border-radius: 50px;
        }
        .timer-icon {
          animation: pulse 1.5s infinite ease-in-out;
        }
        .timer-countdown {
          font-family: var(--font-display);
          font-weight: 700;
          font-size: 1rem;
        }
        .quiz-navigation-footer {
          display: flex;
          justify-content: space-between;
          align-items: center;
          margin-top: 1rem;
        }
        .btn-submit-quiz {
          box-shadow: 0 4px 14px 0 rgba(16,185,129,0.3);
          background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        }
        .btn-submit-quiz:hover {
          box-shadow: 0 6px 20px 0 rgba(16,185,129,0.5);
        }
      `}</style>
    </div>
  );
};

export default Assessment;
