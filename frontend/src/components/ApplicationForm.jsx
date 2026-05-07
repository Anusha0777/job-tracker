import { useState } from 'react';
import { applicationService } from '../services/api';
import './ApplicationForm.css';

export default function ApplicationForm({ onSuccess }) {
  const [company, setCompany] = useState('');
  const [role, setRole] = useState('');
  const [applicationDate, setApplicationDate] = useState(
    new Date().toISOString().split('T')[0]
  );
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!company.trim() || !role.trim()) {
      setError('Company and role are required');
      return;
    }

    try {
      setLoading(true);
      setError(null);

      await applicationService.create(
        company.trim(),
        role.trim(),
        new Date(applicationDate).toISOString()
      );

      setSuccess(true);
      setCompany('');
      setRole('');
      setApplicationDate(new Date().toISOString().split('T')[0]);

      setTimeout(() => {
        setSuccess(false);
        if (onSuccess) onSuccess();
      }, 1500);
    } catch (err) {
      setError('Failed to add application. Please try again.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="form-container">
      <div className="form-card">
        <h2>Add Job Application</h2>
        <p className="form-subtitle">Track a new job application</p>

        {error && <div className="form-error">{error}</div>}
        {success && (
          <div className="form-success">✓ Application added successfully!</div>
        )}

        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label htmlFor="company">Company Name *</label>
            <input
              id="company"
              type="text"
              placeholder="e.g., Google, Microsoft, Startup Inc"
              value={company}
              onChange={(e) => setCompany(e.target.value)}
              disabled={loading}
              required
            />
          </div>

          <div className="form-group">
            <label htmlFor="role">Job Role *</label>
            <input
              id="role"
              type="text"
              placeholder="e.g., Senior Software Engineer, Product Manager"
              value={role}
              onChange={(e) => setRole(e.target.value)}
              disabled={loading}
              required
            />
          </div>

          <div className="form-group">
            <label htmlFor="date">Application Date</label>
            <input
              id="date"
              type="date"
              value={applicationDate}
              onChange={(e) => setApplicationDate(e.target.value)}
              disabled={loading}
            />
          </div>

          <button
            type="submit"
            className="submit-btn"
            disabled={loading}
          >
            {loading ? 'Adding...' : 'Add Application'}
          </button>
        </form>

        <div className="form-tips">
          <h3>💡 Tips</h3>
          <ul>
            <li>Use "AI Resume Tip" to get tailored resume bullet points for the role</li>
            <li>You can update the status of your applications from the Dashboard</li>
            <li>Track interviews, rejections, and offers in one place</li>
          </ul>
        </div>
      </div>
    </div>
  );
}
