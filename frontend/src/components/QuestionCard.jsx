import React from 'react';
import { HelpCircle } from 'lucide-react';

const QuestionCard = ({ question, questionIndex, totalQuestions, selectedOptionId, onSelectOption }) => {
  if (!question) return null;

  // Capitalize difficulty level for display
  const difficultyDisplay = question.difficulty 
    ? question.difficulty.charAt(0) + question.difficulty.slice(1).toLowerCase() 
    : 'Beginner';

  // Get color class for difficulty
  const getDifficultyClass = (diff) => {
    switch (diff?.toUpperCase()) {
      case 'ADVANCED': return 'diff-advanced';
      case 'INTERMEDIATE': return 'diff-intermediate';
      default: return 'diff-beginner';
    }
  };

  return (
    <div className="glass-card quiz-card-panel fade-in">
      <div className="quiz-card-header">
        <div className="quiz-meta-left">
          <span className="quiz-number-tag">Question {questionIndex + 1} of {totalQuestions}</span>
          <span className="quiz-category-tag">{question.category || 'General'}</span>
        </div>
        <span className={`quiz-diff-badge ${getDifficultyClass(question.difficulty)}`}>
          {difficultyDisplay}
        </span>
      </div>

      <div className="quiz-question-box">
        <HelpCircle size={20} className="question-icon" />
        <h3 className="quiz-question-text">{question.text}</h3>
      </div>

      <div className="quiz-options-list">
        {question.options?.map((option, idx) => {
          const optionLetter = String.fromCharCode(65 + idx);
          const isSelected = selectedOptionId === option.id;

          return (
            <button
              key={option.id}
              onClick={() => onSelectOption(question.id, option.id)}
              className={`quiz-option-btn ${isSelected ? 'selected' : ''}`}
              type="button"
            >
              <span className="option-indicator">{optionLetter}</span>
              <span className="option-text">{option.text}</span>
            </button>
          );
        })}
      </div>

      <style>{`
        .quiz-card-panel {
          padding: 2.5rem;
          margin-top: 1.5rem;
          border-color: rgba(255,255,255,0.05);
        }
        .quiz-card-header {
          display: flex;
          justify-content: space-between;
          align-items: center;
          margin-bottom: 2rem;
          padding-bottom: 1rem;
          border-bottom: 1px solid rgba(255,255,255,0.05);
        }
        .quiz-meta-left {
          display: flex;
          align-items: center;
          gap: 1rem;
        }
        .quiz-number-tag {
          font-size: 0.75rem;
          font-weight: 700;
          color: var(--accent-cyan);
          text-transform: uppercase;
          letter-spacing: 0.05em;
        }
        .quiz-category-tag {
          font-size: 0.75rem;
          font-weight: 600;
          background: rgba(124,58,237,0.12);
          border: 1px solid rgba(124,58,237,0.25);
          color: #c084fc;
          padding: 0.2rem 0.6rem;
          border-radius: 4px;
        }
        .quiz-diff-badge {
          font-size: 0.75rem;
          font-weight: 700;
          padding: 0.2rem 0.6rem;
          border-radius: 4px;
        }
        .diff-beginner {
          background: rgba(16,185,129,0.12);
          border: 1px solid rgba(16,185,129,0.25);
          color: #a7f3d0;
        }
        .diff-intermediate {
          background: rgba(234,179,8,0.12);
          border: 1px solid rgba(234,179,8,0.25);
          color: #fef08a;
        }
        .diff-advanced {
          background: rgba(239,68,68,0.12);
          border: 1px solid rgba(239,68,68,0.25);
          color: #fca5a5;
        }
        .quiz-question-box {
          display: flex;
          align-items: flex-start;
          gap: 1rem;
          margin-bottom: 2rem;
        }
        .question-icon {
          color: var(--accent-cyan);
          margin-top: 0.15rem;
          flex-shrink: 0;
        }
        .quiz-question-text {
          font-size: 1.15rem;
          font-weight: 600;
          color: white;
          line-height: 1.5;
        }
        .quiz-options-list {
          display: flex;
          flex-direction: column;
          gap: 1rem;
        }
        .quiz-option-btn {
          display: flex;
          align-items: center;
          gap: 1rem;
          padding: 1.15rem 1.5rem;
          background: rgba(0, 0, 0, 0.15);
          border: 1px solid rgba(255,255,255,0.06);
          border-radius: var(--radius-sm);
          color: var(--text-secondary);
          font-family: var(--font-sans);
          cursor: pointer;
          text-align: left;
          width: 100%;
          transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
        }
        .quiz-option-btn:hover {
          color: white;
          background: rgba(255,255,255,0.02);
          border-color: rgba(255,255,255,0.15);
          transform: translateX(4px);
        }
        .quiz-option-btn.selected {
          border-color: var(--accent-cyan);
          background: rgba(6,182,212,0.05);
          color: white;
          box-shadow: 0 0 15px rgba(6,182,212,0.08);
        }
        .option-indicator {
          font-weight: 800;
          color: var(--text-muted);
          background: rgba(255,255,255,0.02);
          border: 1px solid rgba(255,255,255,0.08);
          width: 28px;
          height: 28px;
          border-radius: 6px;
          display: flex;
          align-items: center;
          justify-content: center;
          font-size: 0.8rem;
          flex-shrink: 0;
          transition: all 0.2s ease;
        }
        .quiz-option-btn.selected .option-indicator {
          background: var(--accent-cyan);
          color: black;
          border-color: var(--accent-cyan);
          box-shadow: 0 0 8px var(--accent-cyan-glow);
        }
        .option-text {
          font-size: 0.95rem;
          font-weight: 500;
          line-height: 1.4;
        }
      `}</style>
    </div>
  );
};

export default QuestionCard;
