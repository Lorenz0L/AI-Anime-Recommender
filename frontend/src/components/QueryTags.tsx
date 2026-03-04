import { QueryAnalysis } from '../api/client'

export const QueryTags = ({ analysis }: { analysis: QueryAnalysis }) => {
  const tags = [
    ...analysis.mood.map(([l]) => ({ label: l, type: 'mood' })),
    ...analysis.themes.map(([l]) => ({ label: l, type: 'theme' })),
    ...analysis.audience.map(([l]) => ({ label: l, type: 'audience' })),
  ]
  if (!tags.length) return null
  return (
    <div className="tags-row">
      <span className="tags-label">Groq detected →</span>
      {tags.map(({ label, type }) => (
        <span key={`${type}-${label}`} className={`tag tag-${type}`}>{label}</span>
      ))}
    </div>
  )
}
