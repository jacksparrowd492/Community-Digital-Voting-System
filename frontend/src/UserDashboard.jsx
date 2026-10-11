import React, { useState, useEffect } from 'react';
import {
  getProposals,
  getProposalDetail,
  castVote,
  revokeVote,
} from './api';
import {
  Clock,
  CheckCircle2,
  XCircle,
  RotateCcw,
  RefreshCw,
  ChevronRight,
} from 'lucide-react';

/* ── helpers ── */
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

function formatCountdown(deadlineStr, status) {
  if (status !== 'active') return { text: statusLabel(status), urgent: false };
  const diff = new Date(deadlineStr) - new Date();
  if (diff <= 0) return { text: 'Expired', urgent: true };
  const days  = Math.floor(diff / (1000 * 60 * 60 * 24));
  const hours = Math.floor((diff / (1000 * 60 * 60)) % 24);
  const mins  = Math.floor((diff / 1000 / 60) % 60);
  const text  = days > 0
    ? `Closes in ${days}d ${hours}h`
    : `Closes in ${hours}h ${mins}m`;
  return { text, urgent: diff < 1000 * 60 * 60 };
}

function pct(part, total) {
  return total ? Math.round((part / total) * 100) : 0;
}

/* ── per-proposal vote form ──
   Rendered with key={proposal.id}, so each proposal gets its own empty
   voter-name state that resets whenever another proposal is opened. */
function VoteForm({ proposal, myVote, onVote, onRevoke }) {
  const [voterName, setVoterName] = useState('');
  const [submitting, setSubmitting] = useState(false);
  const isActive = proposal.status === 'active';

  const submit = async (choice) => {
    setSubmitting(true);
    const ok = await onVote(proposal.id, voterName.trim(), choice);
    setSubmitting(false);
    // Only clear on success so a failed attempt can be corrected
    if (ok) setVoterName('');
  };

  return (
    <div className="vote-form-card">
      <div className="vote-form-title">Your vote</div>

      <label htmlFor={`voter-name-input-${proposal.id}`} className="form-label-light">
        Your name
      </label>
      <input
        id={`voter-name-input-${proposal.id}`}
        className="form-input-light"
        placeholder="e.g. Priya Sharma"
        autoComplete="off"
        value={voterName}
        onChange={e => setVoterName(e.target.value)}
      />
      <div className="form-help-light">
        One vote per name on each proposal. Names are case-sensitive.
      </div>

      {myVote && (
        <div className="voted-banner">
          <div className="voted-banner-info">
            <CheckCircle2 size={15} />
            {myVote.voterName} voted <strong style={{ marginLeft:3 }}>{myVote.vote.toUpperCase()}</strong>
          </div>
          {isActive && (
            <button
              className="btn-revoke"
              onClick={() => onRevoke(proposal.id)}
              id={`revoke-btn-${proposal.id}`}
            >
              <RotateCcw size={12} style={{ marginRight:3 }} />
              Revoke
            </button>
          )}
        </div>
      )}

      {isActive ? (
        voterName.trim() ? (
          <div className="vote-btns-row">
            <button
              className="vote-btn-light yes"
              onClick={() => submit('yes')}
              disabled={submitting}
              id={`vote-yes-${proposal.id}`}
            >
              <CheckCircle2 size={14} /> Yes
            </button>
            <button
              className="vote-btn-light no"
              onClick={() => submit('no')}
              disabled={submitting}
              id={`vote-no-${proposal.id}`}
            >
              <XCircle size={14} /> No
            </button>
            <button
              className="vote-btn-light abstain"
              onClick={() => submit('abstain')}
              disabled={submitting}
              id={`vote-abstain-${proposal.id}`}
            >
              Abstain
            </button>
          </div>
        ) : (
          <p className="text-muted" style={{ fontSize:13 }}>Enter your name to vote.</p>
        )
      ) : (
        <p className="text-muted" style={{ fontSize:13 }}>Voting is closed for this proposal.</p>
      )}
    </div>
  );
}

export default function UserDashboard({ showToast }) {
  const [proposals, setProposals] = useState([]);
  const [loading, setLoading]     = useState(true);
  const [filter, setFilter]       = useState('all');
  const [selected, setSelected]   = useState(null); // proposal object

  const [userVotes, setUserVotes] = useState(() => {
    // Drop the votes cached against the proposals from before the reseed
    localStorage.removeItem('voting_user_votes');
    // Voter names are no longer persisted; clear any previously saved one
    localStorage.removeItem('voting_voter_name');
    try { return JSON.parse(localStorage.getItem('voting_user_votes_v2')) || {}; }
    catch { return {}; }
  });

  const [, setTicker] = useState(0);
  useEffect(() => {
    const t = setInterval(() => setTicker(n => n + 1), 1000);
    return () => clearInterval(t);
  }, []);

  const recordVote = (proposalId, data) => {
    const u = { ...userVotes, [proposalId]: data };
    setUserVotes(u);
    localStorage.setItem('voting_user_votes_v2', JSON.stringify(u));
  };

  const removeVote = (proposalId) => {
    const u = { ...userVotes };
    delete u[proposalId];
    setUserVotes(u);
    localStorage.setItem('voting_user_votes_v2', JSON.stringify(u));
  };

  /* fetch */
  const fetchProposals = async () => {
    try {
      setLoading(true);
      const list = await getProposals(filter === 'all' ? undefined : filter);
      const detailed = await Promise.all(
        list.map(async (p) => {
          try { return await getProposalDetail(p.id); }
          catch { return { ...p, vote_counts: { yes:0, no:0, abstain:0, total:0 } }; }
        })
      );
      setProposals(detailed);
      // keep selected in sync
      setSelected(prev =>
        prev ? (detailed.find(p => p.id === prev.id) || null) : null
      );
    } catch (err) {
      showToast(err.response?.data?.detail || 'Failed to load proposals', 'error');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => { fetchProposals(); }, [filter]);

  /* auto-select first */
  useEffect(() => {
    if (!selected && proposals.length > 0) setSelected(proposals[0]);
  }, [proposals]);

  /* vote */
  /* returns true on success so the form knows whether to clear its input */
  const handleVote = async (proposalId, voterName, choice) => {
    if (!voterName) {
      showToast('Enter your name before voting', 'error');
      return false;
    }
    let res;
    try {
      res = await castVote(proposalId, { voter_name: voterName, vote: choice });
    } catch (err) {
      showToast(err.response?.data?.detail || 'Failed to cast vote', 'error');
      return false;
    }
    recordVote(proposalId, { voteId: res.id, vote: res.vote, voterName: res.voter_name });
    showToast(`Voted "${choice}" successfully!`);
    await refreshProposal(proposalId);
    return true;
  };

  /* reload one proposal's counts without stealing focus if the user moved on */
  const refreshProposal = async (proposalId) => {
    try {
      const updated = await getProposalDetail(proposalId);
      setProposals(prev => prev.map(p => p.id === proposalId ? updated : p));
      setSelected(prev => prev?.id === proposalId ? updated : prev);
    } catch {
      /* counts refresh on the next list reload */
    }
  };

  /* revoke */
  const handleRevoke = async (proposalId) => {
    const uv = userVotes[proposalId];
    if (!uv?.voteId) { showToast('No vote to revoke', 'error'); return; }
    try {
      await revokeVote(uv.voteId);
      removeVote(proposalId);
      showToast('Vote revoked. You may vote again.');
      await refreshProposal(proposalId);
    } catch (err) {
      showToast(err.response?.data?.detail || 'Failed to revoke vote', 'error');
    }
  };

  /* ── render ── */
  const FILTERS = ['all', 'active', 'expired', 'closed'];
  const FILTER_LABELS = { all: 'All', active: 'Open', expired: 'Expired', closed: 'Closed' };

  return (
    <div className="app-shell">
      {/* ── Left Sidebar ── */}
      <aside className="sidebar">
        <div className="sidebar-header">
          <div style={{ display:'flex', alignItems:'center', justifyContent:'space-between', marginBottom:'0.75rem' }}>
            <h2 className="sidebar-title">Proposals</h2>
            <button
              className="btn btn-outline"
              onClick={fetchProposals}
              disabled={loading}
              style={{ padding:'0.3rem 0.6rem', fontSize:'12px' }}
              title="Refresh"
              id="refresh-proposals-btn"
            >
              <RefreshCw size={13} className={loading ? 'animate-spin' : ''} />
            </button>
          </div>

          <div className="filter-tabs" role="tablist">
            {FILTERS.map(f => (
              <button
                key={f}
                id={`filter-tab-${f}`}
                role="tab"
                aria-selected={filter === f}
                className={`filter-tab ${filter === f ? 'active' : ''}`}
                onClick={() => setFilter(f)}
              >
                {FILTER_LABELS[f]}
              </button>
            ))}
          </div>
        </div>

        <div className="sidebar-list">
          {loading && proposals.length === 0 && (
            <div className="empty-state"><p>Loading…</p></div>
          )}
          {!loading && proposals.length === 0 && (
            <div className="empty-state">
              <h3>No proposals</h3>
              <p>Nothing matches this filter.</p>
            </div>
          )}
          {proposals.map(p => {
            const counts   = p.vote_counts || { yes:0, no:0, abstain:0, total:0 };
            const cd       = formatCountdown(p.deadline, p.status);
            const yPct     = pct(counts.yes, counts.total);
            const nPct     = pct(counts.no,  counts.total);
            const aPct     = pct(counts.abstain, counts.total);
            const isEmpty  = counts.total === 0;

            return (
              <div
                key={p.id}
                className={`sidebar-item ${selected?.id === p.id ? 'selected' : ''}`}
                onClick={() => setSelected(p)}
                id={`sidebar-item-${p.id}`}
                role="button"
                tabIndex={0}
                onKeyDown={e => e.key === 'Enter' && setSelected(p)}
              >
                <div className="sidebar-item-top">
                  <span className="sidebar-item-title">{p.title}</span>
                  <span className={statusClass(p.status)}>{statusLabel(p.status)}</span>
                </div>
                <div className="sidebar-item-meta">
                  <span style={{ color: cd.urgent ? 'var(--red)' : undefined }}>
                    {cd.text}
                  </span>
                </div>
                <div className="mini-bar">
                  {isEmpty
                    ? <div className="mini-bar-empty" />
                    : <>
                        <div className="mini-bar-yes"     style={{ width:`${yPct}%` }} />
                        <div className="mini-bar-no"      style={{ width:`${nPct}%` }} />
                        <div className="mini-bar-abstain" style={{ width:`${aPct}%` }} />
                      </>
                  }
                </div>
                <div className="sidebar-item-votes">
                  {counts.total === 0 ? 'No votes yet' : `${counts.total} vote${counts.total !== 1 ? 's' : ''}`}
                </div>
              </div>
            );
          })}
        </div>
      </aside>

      {/* ── Detail Panel ── */}
      <main className="detail-panel">
        {!selected ? (
          <div className="detail-placeholder">
            <div style={{ textAlign:'center' }}>
              <ChevronRight size={36} style={{ opacity:0.3, margin:'0 auto 0.5rem' }} />
              <p>Select a proposal to view details</p>
            </div>
          </div>
        ) : (() => {
          const p      = selected;
          const counts = p.vote_counts || { yes:0, no:0, abstain:0, total:0 };
          const cd     = formatCountdown(p.deadline, p.status);
          const yPct = pct(counts.yes, counts.total);
          const nPct = pct(counts.no,  counts.total);
          const aPct = pct(counts.abstain, counts.total);
          const isEmpty = counts.total === 0;

          return (
            <>
              {/* Main info card */}
              <div className="detail-card">
                <div className="detail-status-row">
                  <span className={statusClass(p.status)}>{statusLabel(p.status)}</span>
                </div>

                <h1 className="detail-title">{p.title}</h1>

                <div className="detail-meta">
                  <span>
                    Closes in{' '}
                    <strong style={{ color: cd.urgent ? 'var(--red)' : undefined }}>
                      {cd.text.replace('Closes in ', '')}
                    </strong>
                    {' '}({new Date(p.deadline).toLocaleString()})
                  </span>
                  <span>Proposed {new Date(p.created_at).toLocaleString()}</span>
                </div>

                <p className="detail-desc">{p.description}</p>

                {/* Results */}
                <div className="results-section">
                  <div className="results-title">Current results</div>

                  <div className="big-bar">
                    {isEmpty
                      ? null
                      : <>
                          <div className="big-bar-yes"     style={{ width:`${yPct}%` }} />
                          <div className="big-bar-no"      style={{ width:`${nPct}%` }} />
                          <div className="big-bar-abstain" style={{ width:`${aPct}%` }} />
                        </>
                    }
                  </div>

                  <div className="bar-legend">
                    <div className="bar-legend-item yes">
                      <div className="bar-legend-label">Yes</div>
                      <div className="bar-legend-value">
                        {counts.yes}
                        <span className="bar-legend-pct">{yPct}%</span>
                      </div>
                    </div>
                    <div className="bar-legend-item no">
                      <div className="bar-legend-label">No</div>
                      <div className="bar-legend-value">
                        {counts.no}
                        <span className="bar-legend-pct">{nPct}%</span>
                      </div>
                    </div>
                    <div className="bar-legend-item abstain">
                      <div className="bar-legend-label">Abstain</div>
                      <div className="bar-legend-value">
                        {counts.abstain}
                        <span className="bar-legend-pct">{aPct}%</span>
                      </div>
                    </div>
                    <div className="bar-legend-item total">
                      <div className="bar-legend-label">Total</div>
                      <div className="bar-legend-value">{counts.total}</div>
                    </div>
                  </div>
                </div>
              </div>

              {/* Voting card: keyed by proposal ID so the name input resets per proposal */}
              <VoteForm
                key={p.id}
                proposal={p}
                myVote={userVotes[p.id]}
                onVote={handleVote}
                onRevoke={handleRevoke}
              />
            </>
          );
        })()}
      </main>
    </div>
  );
}
