import React, { useState, useEffect, useRef } from 'react';
import api from '../services/api';
import { Send, Loader2, Sparkles, MessageSquare, Copy, Check, ArrowRight, User } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

const AITutor = ({ onProgressUpdated }) => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [suggestions, setSuggestions] = useState([]);
  const [copiedId, setCopiedId] = useState(null);
  
  const chatEndRef = useRef(null);

  useEffect(() => {
    fetchChatHistoryAndSuggestions();
  }, []);

  useEffect(() => {
    scrollToBottom();
  }, [messages, loading]);

  const fetchChatHistoryAndSuggestions = async () => {
    try {
      const historyRes = await api.get('/api/tutor/history');
      setMessages(historyRes.data);

      const suggestionsRes = await api.get('/api/tutor/suggestions');
      setSuggestions(suggestionsRes.data);
    } catch (err) {
      console.error('Error loading AI Tutor context:', err);
    }
  };

  const scrollToBottom = () => {
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const handleSendMessage = async (textToSend) => {
    if (!textToSend.trim()) return;
    setInput('');
    setLoading(true);

    // Append user message immediately
    const userMsg = { role: 'USER', content: textToSend, timestamp: new Date().toISOString() };
    setMessages(prev => [...prev, userMsg]);

    try {
      const res = await api.post('/api/tutor/chat', { message: textToSend });
      
      // Simulated delay for high-fidelity typing feel
      setTimeout(() => {
        const botMsg = { role: 'ASSISTANT', content: res.data.response, timestamp: new Date().toISOString() };
        setMessages(prev => [...prev, botMsg]);
        setSuggestions(res.data.suggestedQuestions);
        setLoading(false);
        
        // Notify parent dashboard to update progress (rewards +10 XP)
        if (onProgressUpdated) onProgressUpdated();
      }, 1200);

    } catch (err) {
      console.error('Error sending message:', err);
      setLoading(false);
      const errMsg = { role: 'ASSISTANT', content: '⚠️ Sorry, I encountered an error connecting to the AI brain. Please try again.', timestamp: new Date().toISOString() };
      setMessages(prev => [...prev, errMsg]);
    }
  };

  const handleCopyCode = (codeText, blockIdx) => {
    navigator.clipboard.writeText(codeText);
    setCopiedId(blockIdx);
    setTimeout(() => setCopiedId(null), 2000);
  };

  // Helper to parse rule-based markdown dynamically
  const parseMarkdown = (text) => {
    if (!text) return null;
    const lines = text.split('\n');
    const elements = [];
    
    let inCodeBlock = false;
    let codeLanguage = '';
    let codeBuffer = [];
    let inTable = false;
    let tableRows = [];

    lines.forEach((line, idx) => {
      // 1. Code block toggles
      if (line.startsWith('```')) {
        if (inCodeBlock) {
          // Close block
          const fullCode = codeBuffer.join('\n');
          const currentLang = codeLanguage;
          const currentIdx = idx;
          elements.push(
            <div key={`code-${idx}`} className="code-block-wrapper">
              <div className="code-header">
                <span>{currentLang || 'code'}</span>
                <button 
                  onClick={() => handleCopyCode(fullCode, currentIdx)} 
                  className="btn-copy"
                  type="button"
                >
                  {copiedId === currentIdx ? <Check size={12} className="text-green" /> : <Copy size={12} />}
                  <span>{copiedId === currentIdx ? 'Copied' : 'Copy'}</span>
                </button>
              </div>
              <pre className="code-content">
                <code>{fullCode}</code>
              </pre>
            </div>
          );
          codeBuffer = [];
          inCodeBlock = false;
        } else {
          // Open block
          codeLanguage = line.slice(3).trim();
          inCodeBlock = true;
        }
        return;
      }

      if (inCodeBlock) {
        codeBuffer.push(line);
        return;
      }

      // 2. Table parsing
      if (line.startsWith('|') && line.endsWith('|')) {
        inTable = true;
        tableRows.push(line);
        return;
      } else if (inTable) {
        // Table ended, compile it
        elements.push(renderParsedTable(tableRows, idx));
        tableRows = [];
        inTable = false;
      }

      // 3. Header formatting
      if (line.startsWith('#### ')) {
        elements.push(<h4 key={idx} className="md-h4">{formatBold(line.slice(5))}</h4>);
        return;
      }
      if (line.startsWith('### ')) {
        elements.push(<h3 key={idx} className="md-h3">{formatBold(line.slice(4))}</h3>);
        return;
      }
      if (line.startsWith('## ')) {
        elements.push(<h2 key={idx} className="md-h2">{formatBold(line.slice(3))}</h2>);
        return;
      }

      // 4. Bullet lists
      if (line.startsWith('- ') || line.startsWith('* ')) {
        elements.push(<li key={idx} className="md-li">{formatBold(line.slice(2))}</li>);
        return;
      }

      // 5. Normal paragraphs
      if (line.trim()) {
        elements.push(<p key={idx} className="md-p">{formatBold(line)}</p>);
      }
    });

    // Cleanup lingering buffers
    if (inTable && tableRows.length > 0) {
      elements.push(renderParsedTable(tableRows, 999));
    }

    return elements;
  };

  const formatBold = (str) => {
    const parts = str.split('**');
    return parts.map((part, i) => i % 2 === 1 ? <strong key={i} className="md-strong">{part}</strong> : part);
  };

  const renderParsedTable = (rows, key) => {
    // Exclude separator rows like |---|---|
    const parsedRows = rows.filter(r => !r.includes('---'));
    if (parsedRows.length === 0) return null;

    const headerCols = parsedRows[0].split('|').map(s => s.trim()).filter(Boolean);
    const bodyRows = parsedRows.slice(1).map(row => row.split('|').map(s => s.trim()).filter(Boolean));

    return (
      <div key={`table-${key}`} className="table-responsive-wrapper">
        <table className="md-table">
          <thead>
            <tr>
              {headerCols.map((h, i) => <th key={i}>{h}</th>)}
            </tr>
          </thead>
          <tbody>
            {bodyRows.map((cols, i) => (
              <tr key={i}>
                {cols.map((cell, j) => <td key={j}>{cell}</td>)}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    );
  };

  return (
    <div className="ai-tutor-container fade-in">
      <div className="tutor-header-bar glass-card">
        <div className="tutor-meta">
          <Sparkles className="spark-icon animate-pulse" size={20} />
          <div>
            <h3>AI Personal Tutor</h3>
            <span className="subtitle">Contextual learning prepared for your syllabus</span>
          </div>
        </div>
      </div>

      <div className="chat-window-frame glass-card">
        {/* Messages list */}
        <div className="messages-viewport">
          {messages.length === 0 ? (
            <div className="chat-welcome-shimmer">
              <MessageSquare className="tutor-welcome-icon" size={40} />
              <h4>Hi, I'm your LearnPath Prep Assistant!</h4>
              <p>Ask me to explain IAM policies, VPC NAT setups, JVM optimizations, or test you with a practice question.</p>
            </div>
          ) : (
            messages.map((msg, idx) => (
              <div key={idx} className={`message-row ${msg.role.toLowerCase()}`}>
                <div className="message-avatar-circle">
                  {msg.role === 'ASSISTANT' ? <Sparkles size={14} /> : <User size={14} />}
                </div>
                <div className="message-bubble">
                  {msg.role === 'ASSISTANT' ? parseMarkdown(msg.content) : <p>{msg.content}</p>}
                </div>
              </div>
            ))
          )}

          {/* Typing Indicator */}
          {loading && (
            <div className="message-row assistant typing">
              <div className="message-avatar-circle">
                <Sparkles size={14} className="animate-spin-slow" />
              </div>
              <div className="message-bubble typing-bubble">
                <span className="dot dot-1"></span>
                <span className="dot dot-2"></span>
                <span className="dot dot-3"></span>
              </div>
            </div>
          )}
          
          <div ref={chatEndRef} />
        </div>

        {/* Suggestions footer */}
        {suggestions.length > 0 && !loading && (
          <div className="chat-suggestions-box">
            <span className="suggestions-label">Suggested Prompts:</span>
            <div className="suggestions-list-pills">
              {suggestions.map((sug, i) => (
                <button 
                  key={i} 
                  onClick={() => handleSendMessage(sug)} 
                  className="suggestion-pill"
                  type="button"
                >
                  <span>{sug}</span>
                  <ArrowRight size={10} />
                </button>
              ))}
            </div>
          </div>
        )}

        {/* User Input form */}
        <form onSubmit={(e) => { e.preventDefault(); handleSendMessage(input); }} className="chat-input-form">
          <input
            type="text"
            className="chat-text-input"
            placeholder="Ask your tutor anything..."
            value={input}
            onChange={(e) => setInput(e.target.value)}
            disabled={loading}
          />
          <button 
            type="submit" 
            className="btn btn-primary btn-chat-send" 
            disabled={loading || !input.trim()}
          >
            {loading ? <Loader2 className="animate-spin" size={16} /> : <Send size={15} />}
          </button>
        </form>
      </div>
    </div>
  );
};

export default AITutor;
