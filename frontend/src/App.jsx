import { useState } from 'react';
import Dashboard from './components/Dashboard';
import ApplicationForm from './components/ApplicationForm';
import AITip from './components/AITip';
import './App.css';

export default function App() {
  const [activeTab, setActiveTab] = useState('dashboard');
  const [refreshTrigger, setRefreshTrigger] = useState(0);

  const handleApplicationAdded = () => {
    setRefreshTrigger(prev => prev + 1);
    setActiveTab('dashboard');
  };

  return (
    <div className="app-container">
      <header className="app-header">
        <h1>📋 AI Job Application Tracker</h1>
        <p>Track your job search and get AI-powered resume tips</p>
      </header>

      <nav className="nav-tabs">
        <button
          className={`nav-tab ${activeTab === 'dashboard' ? 'active' : ''}`}
          onClick={() => setActiveTab('dashboard')}
        >
          Dashboard
        </button>
        <button
          className={`nav-tab ${activeTab === 'add-application' ? 'active' : ''}`}
          onClick={() => setActiveTab('add-application')}
        >
          Add Application
        </button>
        <button
          className={`nav-tab ${activeTab === 'ai-tip' ? 'active' : ''}`}
          onClick={() => setActiveTab('ai-tip')}
        >
          AI Resume Tip
        </button>
      </nav>

      <main className="app-content">
        {activeTab === 'dashboard' && (
          <Dashboard key={refreshTrigger} />
        )}
        {activeTab === 'add-application' && (
          <ApplicationForm onSuccess={handleApplicationAdded} />
        )}
        {activeTab === 'ai-tip' && (
          <AITip />
        )}
      </main>

      <footer className="app-footer">
        <p>Built with React, FastAPI & Google Gemini API</p>
      </footer>
    </div>
  );
}
