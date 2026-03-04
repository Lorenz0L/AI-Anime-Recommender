import { useState, KeyboardEvent } from 'react'

const EXAMPLES = [
  'dark psychological thriller, morally grey protagonist',
  'relaxing slice of life with beautiful animation',
  'epic fantasy with deep world building',
]

export const SearchBar = ({ onSearch, loading }: { onSearch: (q: string) => void; loading: boolean }) => {
  const [query, setQuery] = useState('')
  const submit = () => { if (query.trim() && !loading) onSearch(query.trim()) }
  const onKey = (e: KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); submit() }
  }

  return (
    <div className="search-wrap">
      <div className={`search-box${loading ? ' disabled' : ''}`}>
        <textarea
          className="search-input"
          value={query}
          onChange={e => setQuery(e.target.value)}
          onKeyDown={onKey}
          placeholder='Describe what you want... e.g. "something dark and mind-bending"'
          rows={2}
          disabled={loading}
        />
        <button className="search-btn" onClick={submit} disabled={loading || !query.trim()}>
          {loading
            ? <div className="spin" />
            : <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.35-4.35"/></svg>
          }
        </button>
      </div>
      <div className="examples">
        <span className="ex-label">Try →</span>
        {EXAMPLES.map(ex => (
          <button key={ex} className="ex-chip" disabled={loading}
            onClick={() => { setQuery(ex); onSearch(ex) }}>
            {ex}
          </button>
        ))}
      </div>
    </div>
  )
}
