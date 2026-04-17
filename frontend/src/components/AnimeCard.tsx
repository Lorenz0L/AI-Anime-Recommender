import { useState } from 'react'
import { Recommendation } from '../api/client'
import { SentimentBadge } from './SentimentBadge'

export const AnimeCard = ({ rec, index }: { rec: Recommendation; index: number }) => {
  const [open, setOpen] = useState(false)

  return (
    <article className="card" style={{ animationDelay: `${index * 110}ms` }}>
      <div className="card-top">
        <span className="card-rank">#{index + 1}</span>
        {rec.image_url && (
          <img
            className="card-cover"
            src={rec.image_url}
            alt={`${rec.title} cover`}
            loading="lazy"
          />
        )}
        <div className="card-head">
          <h2 className="card-title">{rec.title}</h2>
          <div className="card-genres">
            {rec.genres?.map(g => <span key={g} className="gpill">{g}</span>)}
          </div>
        </div>
      </div>

      <p className="card-explain">{rec.explanation}</p>

      <div className="card-meta">
        <div className="meta-box">
          <span className="meta-lbl">Best for</span>
          <span className="meta-val">{rec.best_for}</span>
        </div>
        <div className="meta-box meta-warn">
          <span className="meta-lbl">⚠ Heads up</span>
          <span className="meta-val">{rec.caveat}</span>
        </div>
      </div>

      <div className="card-foot">
        <SentimentBadge s={rec.sentiment} />
        {rec.sentiment?.mal_url && (
          <a href={rec.sentiment.mal_url} target="_blank" rel="noreferrer" className="mal-link">
            View details ↗
          </a>
        )}
        {rec.sentiment?.sample_comments?.length > 0 && (
          <button className="stats-btn" onClick={() => setOpen(!open)}>
            {open ? 'Hide' : 'Show'} stats
          </button>
        )}
      </div>

      {open && (
        <div className="stats-panel">
          {rec.sentiment.sample_comments.map((c, i) => (
            <div key={i} className="stat-row">✦ {c}</div>
          ))}
        </div>
      )}
    </article>
  )
}
