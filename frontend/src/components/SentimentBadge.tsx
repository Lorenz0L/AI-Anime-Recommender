import { SentimentData } from '../api/client'

export const SentimentBadge = ({ s }: { s: SentimentData }) => {
  if (!s || s.label === 'unknown') return <span className="badge badge-unknown">No MAL data</span>
  const cfg = {
    positive: { symbol: '↑', text: 'Well received', cls: 'badge-pos' },
    mixed:    { symbol: '~', text: 'Mixed reviews', cls: 'badge-mix' },
    negative: { symbol: '↓', text: 'Divisive',      cls: 'badge-neg' },
  }[s.label] ?? { symbol: '~', text: 'Mixed', cls: 'badge-mix' }

  return (
    <div className={`badge ${cfg.cls}`}>
      <span>{cfg.symbol}</span>
      <span>{cfg.text}</span>
      {s.mal_score && <strong>{s.mal_score}/10</strong>}
      {s.members > 0 && <span className="badge-members">{(s.members / 1000).toFixed(0)}k members</span>}
    </div>
  )
}
