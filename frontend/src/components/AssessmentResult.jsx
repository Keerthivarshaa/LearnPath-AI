import React from 'react';
import { CheckCircle2, AlertTriangle, HelpCircle, Sparkles, BookOpen, RefreshCw, XCircle } from 'lucide-react';
import { motion } from 'framer-motion';

const AssessmentResult = ({ result, onRetake }) => {
  if (!result) return null;

  const scorePercentage = Math.round((result.score / result.totalQuestions) * 100);

  // Compute recommendations
  const getRecommendation = (percent) => {
    if (percent >= 80) return "Advanced Track: You have solid fundamentals. Start building complex architectures and microservices.";
    if (percent >= 50) return "Intermediate Track: Focus on strengthening your weak topics. Deepen database and networking fundamentals.";
    return "Foundation Track: Build core syntax skills first. Work on baseline system parameters and basic deployments.";
  };

  return (
    <div className="assessment-result-container fade-in">
      <div className="glass-card result-summary-card">
        <div className="result-glow"></div>
        <div className="result-circular-gauge">
          <svg width="120" height="120" viewBox="0 0 120 120">
            <circle cx="60" cy="60" r="50" className="circle-back" />
            <motion.circle
              cx="60"
              cy="60"
              r="50"
              className="circle-front"
              strokeDasharray="314.16"
              initial={{ strokeDashoffset: 314.16 }}
              animate={{ strokeDashoffset: 314.16 - (314.16 * scorePercentage) / 100 }}
              transition={{ duration: 1.2, ease: 'easeOut' }}
              stroke={scorePercentage >= 70 ? '#10b981' : scorePercentage >= 40 ? '#eab308' : '#ef4444'}
            />
          </svg>
          <div className="gauge-text">
            <span className="gauge-num">{scorePercentage}%</span>
            <span className="gauge-label">Score</span>
          </div>
        </div>

        <div className="result-info-side">
          <div className="result-badge-top">
            <Sparkles size={14} />
            <span>Diagnostic Complete</span>
          </div>
          <h2>You scored {result.score} / {result.totalQuestions}</h2>
          <p className="recommendation-text">{getRecommendation(scorePercentage)}</p>
          
          <button onClick={onRetake} className="btn btn-secondary btn-retake">
            <RefreshCw size={15} />
            <span>Retake Assessment</span>
          </button>
        </div>
      </div>

      <div className="grid-2 topics-grid">
        {/* Strong Topics */}
        <div className="glass-card topics-panel strong-topics-panel">
          <div className="panel-header">
            <CheckCircle2 className="text-emerald" size={20} />
            <h3>Strong Core Topics</h3>
          </div>
          {result.strongTopics?.length > 0 ? (
            <ul className="topics-list">
              {result.strongTopics.map((topic, i) => (
                <li key={i} className="topic-item">
                  <span className="topic-dot dot-strong"></span>
                  <span>{topic}</span>
                </li>
              ))}
            </ul>
          ) : (
            <p className="empty-topics-text">No strong topics identified yet. Keep practicing!</p>
          )}
        </div>

        {/* Weak Topics */}
        <div className="glass-card topics-panel weak-topics-panel">
          <div className="panel-header">
            <AlertTriangle className="text-amber" size={20} />
            <h3>Topics to Improve</h3>
          </div>
          {result.weakTopics?.length > 0 ? (
            <ul className="topics-list">
              {result.weakTopics.map((topic, i) => (
                <li key={i} className="topic-item">
                  <span className="topic-dot dot-weak"></span>
                  <span>{topic}</span>
                </li>
              ))}
            </ul>
          ) : (
            <p className="empty-topics-text">Amazing! No weak topics identified.</p>
          )}
        </div>
      </div>

      {/* Answers Explanations Review List */}
      <h3 className="section-title">Question-by-Question Review</h3>
      <div className="answers-review-list">
        {result.answers?.map((ans, idx) => (
          <div key={idx} className={`glass-card review-item-card ${ans.isCorrect ? 'correct-border' : 'incorrect-border'}`}>
            <div className="review-card-header">
              <span className="review-num">Question {idx + 1}</span>
              <div className="review-status-badge">
                {ans.isCorrect ? (
                  <span className="status-correct"><CheckCircle2 size={14} /> Correct</span>
                ) : (
                  <span className="status-incorrect"><XCircle size={14} /> Incorrect</span>
                )}
              </div>
            </div>

            <h4 className="review-question-text">{ans.questionText}</h4>

            <div className="review-options-summary">
              {ans.correctOptionId === ans.selectedOptionId ? (
                <div className="option-summary-box correct-answer-choice">
                  <span className="choice-label">Your Choice (Correct):</span>
                  <p>Option successfully matched key parameter.</p>
                </div>
              ) : (
                <>
                  <div className="option-summary-box incorrect-answer-choice">
                    <span className="choice-label">Your Choice:</span>
                    <p>{ans.selectedOptionId ? "Selected incorrect option" : "No answer selected"}</p>
                  </div>
                  <div className="option-summary-box correct-answer-target">
                    <span className="choice-label">Correct Answer:</span>
                    <p>Refer to correct choice requirements.</p>
                  </div>
                </>
              )}
            </div>

            {ans.correctExplanation && (
              <div className="explanation-panel">
                <BookOpen size={16} className="explanation-icon" />
                <div className="explanation-content">
                  <h5>Explanation</h5>
                  <p>{ans.correctExplanation}</p>
                </div>
              </div>
            )}
          </div>
        ))}
      </div>

      <style>{`
        .assessment-result-container {
          display: flex;
          flex-direction: column;
          gap: 2rem;
        }
        .result-summary-card {
          position: relative;
          display: flex;
          align-items: center;
          gap: 2.5rem;
          padding: 2.5rem;
          background: linear-gradient(135deg, rgba(16,185,129,0.06) 0%, rgba(6,182,212,0.03) 100%);
          overflow: hidden;
        }
        .result-glow {
          position: absolute;
          top: -20%;
          right: -10%;
          width: 250px;
          height: 250px;
          background: radial-gradient(circle, var(--accent-cyan-glow) 0%, transparent 70%);
          filter: blur(40px);
          pointer-events: none;
        }
        .result-circular-gauge {
          position: relative;
          width: 120px;
          height: 120px;
          flex-shrink: 0;
        }
        .circle-back {
          stroke: rgba(255,255,255,0.03);
          stroke-width: 8;
          fill: none;
        }
        .circle-front {
          stroke-width: 8;
          stroke-linecap: round;
          fill: none;
          transform: rotate(-90deg);
          transform-origin: 50% 50%;
        }
        .gauge-text {
          position: absolute;
          top: 50%;
          left: 50%;
          transform: translate(-50%, -50%);
          display: flex;
          flex-direction: column;
          align-items: center;
        }
        .gauge-num {
          font-family: var(--font-display);
          font-size: 1.8rem;
          font-weight: 800;
          color: white;
        }
        .gauge-label {
          font-size: 0.65rem;
          text-transform: uppercase;
          color: var(--text-muted);
          letter-spacing: 0.05em;
        }
        .result-info-side {
          display: flex;
          flex-direction: column;
          gap: 0.5rem;
          z-index: 1;
        }
        .result-badge-top {
          display: inline-flex;
          align-items: center;
          gap: 0.4rem;
          background: rgba(16,185,129,0.15);
          border: 1px solid rgba(16,185,129,0.25);
          color: #34d399;
          font-size: 0.75rem;
          padding: 0.25rem 0.60rem;
          border-radius: 50px;
          font-weight: 600;
          width: fit-content;
        }
        .result-info-side h2 {
          font-size: 1.8rem;
          color: white;
        }
        .recommendation-text {
          color: var(--text-secondary);
          font-size: 0.95rem;
          line-height: 1.5;
          max-width: 600px;
        }
        .btn-retake {
          margin-top: 1rem;
          width: fit-content;
          font-size: 0.85rem;
          padding: 0.5rem 1rem;
        }
        .topics-grid {
          margin-top: 1rem;
        }
        .topics-panel {
          padding: 1.75rem;
          background: rgba(19, 27, 46, 0.4);
        }
        .panel-header {
          display: flex;
          align-items: center;
          gap: 0.75rem;
          margin-bottom: 1.5rem;
          padding-bottom: 0.75rem;
          border-bottom: 1px solid rgba(255,255,255,0.05);
        }
        .panel-header h3 {
          font-size: 1rem;
          color: white;
        }
        .text-emerald { color: #10b981; }
        .text-amber { color: #f59e0b; }
        .topics-list {
          list-style: none;
          display: flex;
          flex-direction: column;
          gap: 0.75rem;
        }
        .topic-item {
          display: flex;
          align-items: center;
          gap: 0.75rem;
          font-size: 0.9rem;
          color: var(--text-secondary);
        }
        .topic-dot {
          width: 6px;
          height: 6px;
          border-radius: 50%;
        }
        .dot-strong { background: #10b981; box-shadow: 0 0 8px #10b981; }
        .dot-weak { background: #f59e0b; box-shadow: 0 0 8px #f59e0b; }
        .empty-topics-text {
          font-size: 0.85rem;
          color: var(--text-muted);
        }
        .section-title {
          font-size: 1.2rem;
          color: white;
          margin-top: 1.5rem;
          margin-bottom: 0.5rem;
        }
        .answers-review-list {
          display: flex;
          flex-direction: column;
          gap: 1.5rem;
        }
        .review-item-card {
          padding: 2rem;
          background: rgba(19, 27, 46, 0.3);
          border-left: 4px solid transparent;
        }
        .correct-border { border-left-color: #10b981; }
        .incorrect-border { border-left-color: #ef4444; }
        .review-card-header {
          display: flex;
          justify-content: space-between;
          align-items: center;
          margin-bottom: 1rem;
        }
        .review-num {
          font-size: 0.75rem;
          font-weight: 700;
          color: var(--text-muted);
          text-transform: uppercase;
        }
        .review-status-badge {
          font-size: 0.8rem;
          font-weight: 600;
        }
        .status-correct {
          color: #10b981;
          display: flex;
          align-items: center;
          gap: 0.35rem;
        }
        .status-incorrect {
          color: #ef4444;
          display: flex;
          align-items: center;
          gap: 0.35rem;
        }
        .review-question-text {
          font-size: 1.05rem;
          color: white;
          margin-bottom: 1.5rem;
        }
        .review-options-summary {
          display: flex;
          flex-direction: column;
          gap: 0.75rem;
          margin-bottom: 1.5rem;
        }
        .option-summary-box {
          padding: 0.85rem 1.25rem;
          border-radius: var(--radius-sm);
          font-size: 0.9rem;
        }
        .choice-label {
          font-size: 0.7rem;
          font-weight: 700;
          text-transform: uppercase;
          display: block;
          margin-bottom: 0.2rem;
        }
        .correct-answer-choice {
          background: rgba(16,185,129,0.06);
          border: 1px solid rgba(16,185,129,0.15);
          color: #a7f3d0;
        }
        .incorrect-answer-choice {
          background: rgba(239,68,68,0.06);
          border: 1px solid rgba(239,68,68,0.15);
          color: #fca5a5;
        }
        .correct-answer-target {
          background: rgba(255,255,255,0.03);
          border: 1px solid rgba(255,255,255,0.06);
          color: var(--text-secondary);
        }
        .explanation-panel {
          display: flex;
          gap: 0.75rem;
          background: rgba(6,182,212,0.05);
          border: 1px solid rgba(6,182,212,0.15);
          padding: 1.15rem;
          border-radius: var(--radius-sm);
        }
        .explanation-icon {
          color: var(--accent-cyan);
          flex-shrink: 0;
          margin-top: 0.15rem;
        }
        .explanation-content h5 {
          font-size: 0.8rem;
          color: var(--accent-cyan);
          text-transform: uppercase;
          margin-bottom: 0.25rem;
        }
        .explanation-content p {
          font-size: 0.85rem;
          color: var(--text-secondary);
          line-height: 1.4;
        }
      `}</style>
    </div>
  );
};

export default AssessmentResult;
