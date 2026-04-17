import axios from 'axios'

const api = axios.create({ baseURL: '/api' })

export interface SentimentData {
  score: number | null
  label: 'positive' | 'mixed' | 'negative' | 'unknown'
  mal_score: number | null
  members: number
  popularity_rank: number | null
  post_count: number
  sample_comments: string[]
  mal_url: string
}

export interface Recommendation {
  title: string
  image_url?: string
  explanation: string
  best_for: string
  caveat: string
  genres: string[]
  sentiment: SentimentData
}

export interface QueryAnalysis {
  mood: [string, number][]
  themes: [string, number][]
  audience: [string, number][]
  enriched_query: string
}

export interface RecommendResponse {
  query: string
  analysis: QueryAnalysis
  recommendations: Recommendation[]
  summary: string
}

export const getRecommendations = (query: string) =>
  api.post<RecommendResponse>('/recommend', { query }).then(r => r.data)
