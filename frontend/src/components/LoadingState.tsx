const STEPS = [
  { label: 'Groq is analyzing your query',    sub: 'Detecting mood, themes & audience' },
  { label: 'Searching the anime database',     sub: 'Semantic vector search (ChromaDB)' },
  { label: 'Groq is picking the best matches', sub: 'Re-ranking & writing explanations' },
  { label: 'Fetching live community stats',    sub: 'MyAnimeList scores via Jikan API' },
]

export const LoadingState = () => (
  <div className="loading">
    <div className="orb" />
    <p className="loading-title">AniMind is thinking...</p>
    <div className="steps">
      {STEPS.map((s, i) => (
        <div key={i} className="step" style={{ animationDelay: `${i * 0.65}s` }}>
          <div className="step-dot" style={{ animationDelay: `${i * 0.65}s` }} />
          <div>
            <div className="step-label">{s.label}</div>
            <div className="step-sub">{s.sub}</div>
          </div>
        </div>
      ))}
    </div>
  </div>
)
