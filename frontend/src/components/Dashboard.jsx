import { useState, useEffect } from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { statsService, applicationService } from '../services/api';
import './Dashboard.css';

export default function Dashboard() {
  const [stats, setStats] = useState(null);
  const [applications, setApplications] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      setLoading(true);
      const [statsData, appsData] = await Promise.all([
        statsService.getStats(),
        applicationService.getAll(),
      ]);
      setStats(statsData);
      setApplications(appsData);
      setError(null);
    } catch (err) {
      setError('Failed to load dashboard data');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleStatusChange = async (id, newStatus) => {
    try {
      await applicationService.updateStatus(id, newStatus);
      fetchData();
    } catch (err) {
      setError('Failed to update application status');
      console.error(err);
    }
  };

  const handleDelete = async (id) => {
    if (window.confirm('Are you sure you want to delete this application?')) {
      try {
        await applicationService.delete(id);
        fetchData();
      } catch (err) {
        setError('Failed to delete application');
        console.error(err);
      }
    }
  };

  if (loading) {
    return <div className="dashboard-loading">Loading dashboard...</div>;
  }

  if (error) {
    return (
      <div className="dashboard-error">
        <p>{error}</p>
        <button onClick={fetchData}>Retry</button>
      </div>
    );
  }

  // Prepare chart data
  const chartData = stats?.by_status
    ? Object.entries(stats.by_status).map(([status, count]) => ({
        status,
        count,
      }))
    : [];

  return (
    <div className="dashboard">
      {/* Stats Cards */}
      <div className="stats-grid">
        <div className="stat-card total">
          <div className="stat-label">Total Applications</div>
          <div className="stat-value">{stats?.total_applications || 0}</div>
        </div>
        <div className="stat-card interview">
          <div className="stat-label">Interviews</div>
          <div className="stat-value">{stats?.interviews || 0}</div>
        </div>
        <div className="stat-card offer">
          <div className="stat-label">Offers</div>
          <div className="stat-value">{stats?.offers || 0}</div>
        </div>
        <div className="stat-card rejected">
          <div className="stat-label">Rejected</div>
          <div className="stat-value">{stats?.rejected || 0}</div>
        </div>
      </div>

      {/* Chart */}
      {chartData.length > 0 && (
        <div className="chart-container">
          <h2>Applications by Status</h2>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={chartData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#e0e0e0" />
              <XAxis dataKey="status" />
              <YAxis />
              <Tooltip
                contentStyle={{ backgroundColor: '#f9f9f9', border: '1px solid #ccc' }}
              />
              <Bar dataKey="count" fill="#007bff" radius={[8, 8, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>
      )}

      {/* Applications List */}
      <div className="applications-section">
        <h2>Recent Applications</h2>
        {applications.length === 0 ? (
          <div className="empty-state">
            <p>No applications yet. Start by adding your first application!</p>
          </div>
        ) : (
          <div className="applications-list">
            {applications.map((app) => (
              <div key={app.id} className="application-card">
                <div className="app-header">
                  <div className="app-info">
                    <h3>{app.company}</h3>
                    <p className="app-role">{app.role}</p>
                    <p className="app-date">
                      Applied: {new Date(app.application_date).toLocaleDateString()}
                    </p>
                  </div>
                  <div className="app-actions">
                    <select
                      value={app.status}
                      onChange={(e) => handleStatusChange(app.id, e.target.value)}
                      className="status-select"
                    >
                      <option value="Applied">Applied</option>
                      <option value="Interview">Interview</option>
                      <option value="Rejected">Rejected</option>
                      <option value="Offer">Offer</option>
                    </select>
                    <button
                      onClick={() => handleDelete(app.id)}
                      className="delete-btn"
                    >
                      Delete
                    </button>
                  </div>
                </div>
                <div className={`status-badge status-${app.status.toLowerCase()}`}>
                  {app.status}
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
