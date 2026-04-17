import { SearchBar } from './components/SearchBar'
import { AnimeCard } from './components/AnimeCard'
import { QueryTags } from './components/QueryTags'
import { LoadingState } from './components/LoadingState'
import { useRecommendations } from './hooks/useRecommendations'

export default function App() {
  const { data, loading, error, search, reset } = useRecommendations()
  const handleSearch = (q: string) => { reset(); search(q) }

  return (
    <div className="app">
      <div className="bg-grid" />
      <div className="bg-glow" />

      <header className="header">
        <div className="logo">
          <div className="logo-mark">AM</div>
          <div>
            <div className="logo-name">AniMind</div>
            <div className="logo-sub">AI Anime Recommender</div>
          </div>
        </div>
        <div className="pills">
          <span className="pill">Personalized picks</span>
          <span className="pill">Mood-aware</span>
          <span className="pill">Community stats</span>
        </div>
      </header>

      <main className="main">
        <section className="hero">
          <h1 className="hero-h">
            Describe what you're craving.<br />
            <span className="hero-accent">We'll find it.</span>
          </h1>
          <p className="hero-p">
            Skip the genre tags. Describe a feeling, a vibe, a story.
          </p>
        </section>

        <SearchBar onSearch={handleSearch} loading={loading} />

        <section className="results">
          {loading && <LoadingState />}

          {error && (
            <div className="err-state">
              <div className="err-icon">⚠</div>
              <p className="err-title">Something went wrong</p>
              <p className="err-msg">{error}</p>
            </div>
          )}

          {data && !loading && (
            <>
              {data.summary && <p className="summary">{data.summary}</p>}
              <QueryTags analysis={data.analysis} />
              <div className="cards">
                {data.recommendations.map((rec, i) => (
                  <AnimeCard key={rec.title} rec={rec} index={i} />
                ))}
              </div>
            </>
          )}

          {!data && !loading && !error && (
            <div className="empty">
              <div className="empty-icon">◎</div>
              <p>Your recommendations appear here</p>
              <p className="empty-sub">Try: "sad romance" or "action with great fight scenes"</p>
            </div>
          )}
        </section>
      </main>

      <footer className="foot">
        Built by us · Anime data updates live
      </footer>
    </div>
  )
}
