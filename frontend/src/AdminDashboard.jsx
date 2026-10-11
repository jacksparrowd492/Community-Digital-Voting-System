import React, { useState, useEffect } from 'react';
import {
  getProposals,
  getProposalDetail,
  createProposal,
  closeProposal,
} from './api';
import {
  PlusCircle,
  Lock,
  Layers,
  Activity,
  CheckCircle2,
  AlertTriangle,
  RefreshCw,
  Key,
  X,
  ChevronDown,
  ChevronUp,
} from 'lucide-react';

function statusLabel(s) {
  if (s === 'active') return 'Open';
  if (s === 'closed') return 'Closed';
  return 'Expired';
}

function statusClass(s) {
  if (s === 'active') return 'badge badge-open';
  if (s === 'closed') return 'badge badge-closed';
  return 'badge badge-expired';
}

function pct(part, total) {
  return total ? Math.round((part / total) * 100) : 0;
}

export default function AdminDashboard({ showToast, showCreate, onCreateClose }) {
  const [proposals, setProposals]   = useState([]);
  const [loading, setLoading]       = useState(true);
  const [adminToken, setAdminToken] = useState(
    () => localStorage.getItem('voting_admin_token') || 'karthi123'
  );
  const [adminOpen, setAdminOpen]   = useState(false);

  // Create form
  const [newTitle, setNewTitle]             = useState('');
  const [newDescription, setNewDescription] = useState('');
  const [newDeadlineHours, setNewHours]     = useState('48');
  const [submitting, setSubmitting]         = useState(false);

  const handleTokenChange = (v) => {
    setAdminToken(v);
    localStorage.setItem('voting_admin_token', v);
  };

  const fetchProposals = async () => {
    try {
      setLoading(true);
      const list = await getProposals();
      const detailed = await Promise.all(
        list.map(async (p) => {
          try { return await getProposalDetail(p.id); }
          catch { return { ...p, vote_counts: { yes:0, no:0, abstain:0, total:0 } }; }
        })
      );
      setProposals(detailed);
    } catch (err) {
      showToast(err.response?.data?.detail || 'Failed to load proposals', 'error');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => { fetchProposals(); }, []);

  // Open create modal when navbar button clicked
  useEffect(() => {
    if (showCreate) {
      // modal is inline; scroll to top
      window.scrollTo(0, 0);
    }
  }, [showCreate]);

  /* Create proposal */
  const handleCreate = async (e) => {
    e.preventDefault();
    if (!newTitle.trim() || !newDescription.trim()) {
      showToast('Title and description are required', 'error');
      return;
    }
    setSubmitting(true);
    try {
      const hours    = parseInt(newDeadlineHours, 10) || 48;
      const deadline = new Date(Date.now() + hours * 60 * 60 * 1000).toISOString();
      await createProposal({ title: newTitle.trim(), description: newDescription.trim(), deadline });
      showToast('Proposal published!');
      setNewTitle('');
      setNewDescription('');
      setNewHours('48');
      onCreateClose?.();
      fetchProposals();
    } catch (err) {
      showToast(err.response?.data?.detail || 'Failed to create proposal', 'error');
    } finally {
      setSubmitting(false);
    }
  };

  /* Close proposal */
  const handleClose = async (id) => {
    if (!window.confirm(`Close Proposal #${id}?`)) return;
    try {
      await closeProposal(id, adminToken);
      showToast(`Proposal #${id} closed.`);
      fetchProposals();
    } catch (err) {
      showToast(err.response?.data?.detail || 'Failed to close. Check admin token.', 'error');
    }
  };

  /* Metrics */
  const total       = proposals.length;
  const activeCount = proposals.filter(p => p.status === 'active').length;
  const closedCount = proposals.filter(p => p.status === 'closed').length;
  const expiredCount= proposals.filter(p => p.status === 'expired').length;
  const totalVotes  = proposals.reduce((s, p) => s + (p.vote_counts?.total || 0), 0);

  return (
    <div className="admin-page">
      {/* Header */}
      <div className="admin-page-header">
        <h1 className="admin-page-title">Administrator Console</h1>
        <div className="admin-page-actions">
          <button
            className="btn btn-outline"
            onClick={fetchProposals}
            disabled={loading}
            id="admin-refresh-btn"
          >
            <RefreshCw size={14} className={loading ? 'animate-spin' : ''} />
            Refresh
          </button>
          <button
            className="btn btn-navy"
            onClick={() => document.getElementById('create-section')?.scrollIntoView({ behavior:'smooth' })}
            id="admin-new-btn"
          >
            <PlusCircle size={14} />
            New Proposal
          </button>
        </div>
      </div>

      {/* Metrics */}
      <div className="metrics-row">
        {[
          { num: total,       lbl: 'Total',        color: undefined },
          { num: activeCount, lbl: 'Active',        color: 'var(--green)' },
          { num: closedCount, lbl: 'Closed',        color: 'var(--red)' },
          { num: expiredCount,lbl: 'Expired',       color: 'var(--amber)' },
          { num: totalVotes,  lbl: 'Total Votes',   color: undefined },
        ].map(({ num, lbl, color }) => (
          <div className="metric-box" key={lbl}>
            <div className="metric-num" style={{ color }}>{num}</div>
            <div className="metric-lbl">{lbl}</div>
          </div>
        ))}
      </div>

      {/* Create proposal card */}
      <div className="admin-card" id="create-section">
        <div className="admin-card-title">
          <PlusCircle size={17} style={{ color:'var(--navy)' }} />
          Create New Proposal
        </div>
        <form onSubmit={handleCreate}>
          <div className="form-grid-title-hours">
            <div className="form-group">
              <label className="form-label" htmlFor="new-title">Title *</label>
              <input
                id="new-title"
                className="form-input"
                placeholder="e.g. Expand community center broadband"
                value={newTitle}
                onChange={e => setNewTitle(e.target.value)}
                maxLength={200}
                required
              />
            </div>
            <div className="form-group">
              <label className="form-label" htmlFor="new-hours">Voting window (hours) *</label>
              <input
                id="new-hours"
                type="number"
                min="1"
                max="720"
                className="form-input"
                value={newDeadlineHours}
                onChange={e => setNewHours(e.target.value)}
                required
              />
              <div className="form-help">Default: 48 h (2 days)</div>
            </div>
          </div>

          <div className="form-group">
            <label className="form-label" htmlFor="new-desc">Description *</label>
            <textarea
              id="new-desc"
              className="form-textarea"
              rows={3}
              placeholder="Outline objectives, scope, cost, and community impact…"
              value={newDescription}
              onChange={e => setNewDescription(e.target.value)}
              required
            />
          </div>

          <div className="form-actions">
            <button type="submit" className="btn btn-navy" disabled={submitting} id="submit-proposal-btn">
              <PlusCircle size={14} />
              {submitting ? 'Publishing…' : 'Publish Proposal'}
            </button>
          </div>
        </form>
      </div>

      {/* Admin token collapsible */}
      <div className="admin-collapse">
        <button
          className="admin-collapse-trigger"
          onClick={() => setAdminOpen(o => !o)}
          id="admin-token-toggle"
        >
          <Key size={15} />
          Admin Token
          {adminOpen ? <ChevronUp size={14} /> : <ChevronDown size={14} />}
        </button>
        {adminOpen && (
          <div className="admin-collapse-body">
            <div className="form-group" style={{ maxWidth:340 }}>
              <label className="form-label" htmlFor="admin-token-input">
                X-Admin-Token header value
              </label>
              <input
                id="admin-token-input"
                type="password"
                className="form-input"
                value={adminToken}
                onChange={e => handleTokenChange(e.target.value)}
                placeholder="karthi123"
              />
              <div className="form-help">
                Sent as <code>X-Admin-Token</code> when closing proposals.
                Development default: <code>karthi123</code>. Set <code>ADMIN_TOKEN</code> on the
                server for any real deployment.
              </div>
            </div>
          </div>
        )}
      </div>

      {/* Proposals table */}
      <div className="admin-card">
        <div className="admin-card-title">
          <Layers size={17} />
          Proposal Monitoring
        </div>

        {loading && proposals.length === 0 ? (
          <div className="empty-state"><p>Loading…</p></div>
        ) : proposals.length === 0 ? (
          <div className="empty-state"><h3>No proposals yet</h3><p>Create one above.</p></div>
        ) : (
          <table className="admin-table admin-table-responsive">
            <thead>
              <tr>
                <th>#</th>
                <th>Title</th>
                <th>Status</th>
                <th>Deadline</th>
                <th>Votes</th>
                <th style={{ width:80 }}>Yes</th>
                <th style={{ width:80 }}>No</th>
                <th style={{ width:80 }}>Abstain</th>
                <th>Action</th>
              </tr>
            </thead>
            <tbody>
              {proposals.map(p => {
                const c      = p.vote_counts || { yes:0, no:0, abstain:0, total:0 };
                const isActive = p.status === 'active';
                return (
                  <tr key={p.id}>
                    <td className="cell-id" style={{ color:'var(--text-muted)', fontWeight:500 }}>#{p.id}</td>
                    <td className="cell-title" style={{ fontWeight:600 }}>{p.title}</td>
                    <td className="cell-status"><span className={statusClass(p.status)}>{statusLabel(p.status)}</span></td>
                    <td data-label="Deadline" style={{ color:'var(--text-secondary)', fontSize:12 }}>
                      {new Date(p.deadline).toLocaleDateString()}
                    </td>
                    <td data-label="Votes" style={{ fontWeight:600 }}>{c.total}</td>
                    <td data-label="Yes" className="text-green">{c.yes} ({pct(c.yes,c.total)}%)</td>
                    <td data-label="No" className="text-red">{c.no} ({pct(c.no,c.total)}%)</td>
                    <td data-label="Abstain" style={{ color:'var(--gray)' }}>{c.abstain} ({pct(c.abstain,c.total)}%)</td>
                    <td className="cell-action">
                      {isActive ? (
                        <button
                          className="btn btn-danger btn-sm"
                          onClick={() => handleClose(p.id)}
                          id={`close-btn-${p.id}`}
                        >
                          <Lock size={12} />
                          Close
                        </button>
                      ) : (
                        <span className="cell-action-none" style={{ fontSize:12, color:'var(--text-muted)' }}>—</span>
                      )}
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        )}
      </div>
    </div>
  );
}
