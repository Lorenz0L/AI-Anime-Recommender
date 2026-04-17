const STEPS = [
  { label: 'We’re analyzing your query',      sub: 'Detecting mood, themes & audience' },
  { label: 'Searching for close matches',     sub: 'Finding titles that fit your vibe' },
  { label: 'Picking the best recommendations',sub: 'Ranking and writing explanations' },
  { label: 'Fetching community stats',        sub: 'Pulling ratings and discussion signals' },
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
