import { useState } from 'react';
import { aiService } from '../services/api';
import './AITip.css';

export default function AITip() {
  const [jobDescription, setJobDescription] = useState('');
  const [bulletPoints, setBulletPoints] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleGenerateTip = async () => {
    if (!jobDescription.trim()) {
      setError('Please paste a job description');
      return;
    }

    try {
      setLoading(true);
      setError(null);
      const response = await aiService.generateTip(jobDescription);
      setBulletPoints(response.bullet_points);
    } catch (err) {
      setError('Failed to generate resume tips. Please try again.');
      console.error(err);
      setBulletPoints(null);
    } finally {
      setLoading(false);
    }
  };

  const handleCopy = (text) => {
    navigator.clipboard.writeText(text);
    alert('Copied to clipboard!');
  };

  const handleClear = () => {
    setJobDescription('');
    setBulletPoints(null);
    setError(null);
  };

  return (
    <div className="ai-tip-container">
      <div className="ai-card">
        <div className="ai-header">
          <h2>✨ AI Resume Tip Generator</h2>
          <p>Paste a job description to get tailored resume bullet points</p>
        </div>

        <div className="ai-content">
          {/* Input Section */}
          <div className="input-section">
            <label htmlFor="job-desc">Job Description *</label>
            <textarea
              id="job-desc"
              placeholder="Paste the full job description here..."
              value={jobDescription}
              onChange={(e) => setJobDescription(e.target.value)}
              disabled={loading}
              rows="10"
            />

            {error && <div className="ai-error">{error}</div>}

            <div className="button-group">
              <button
                onClick={handleGenerateTip}
                className="generate-btn"
                disabled={loading || !jobDescription.trim()}
              >
                {loading ? '⏳ Generating...' : '🚀 Generate Resume Tips'}
              </button>
              <button
                onClick={handleClear}
                className="clear-btn"
                disabled={loading}
              >
                Clear
              </button>
            </div>
          </div>

          {/* Output Section */}
          {bulletPoints && (
            <div className="output-section">
              <h3>📝 Your Resume Bullet Points</h3>
              <p className="output-subtitle">
                Copy these to your resume for this specific role:
              </p>
              <div className="bullet-points">
                {bulletPoints.map((point, index) => (
                  point && (
                    <div key={index} className="bullet-point">
                      <div className="bullet-number">{index + 1}</div>
                      <div className="bullet-content">
                        <p>{point}</p>
                        <button
                          onClick={() => handleCopy(point)}
                          className="copy-btn"
                          title="Copy to clipboard"
                        >
                          📋 Copy
                        </button>
                      </div>
                    </div>
                  )
                ))}
              </div>
            </div>
          )}

          {!bulletPoints && !loading && jobDescription && (
            <div className="placeholder">
              <p>Click "Generate Resume Tips" to create AI-powered bullet points</p>
            </div>
          )}
        </div>

        <div className="ai-tips">
          <h3>💡 How to Use</h3>
          <ol>
            <li>Find a job posting on LinkedIn, Indeed, or similar</li>
            <li>Copy the entire job description</li>
            <li>Paste it in the textarea above</li>
            <li>Click "Generate Resume Tips"</li>
            <li>Copy the bullet points and add them to your resume</li>
          </ol>
        </div>
      </div>
    </div>
  );
}
