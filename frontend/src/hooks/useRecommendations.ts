import { useState } from 'react'
import { getRecommendations, RecommendResponse } from '../api/client'

export const useRecommendations = () => {
  const [data, setData] = useState<RecommendResponse | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const search = async (query: string) => {
    setLoading(true)
    setError(null)
    setData(null)
    try {
      setData(await getRecommendations(query))
    } catch (e: any) {
      setError(e?.response?.data?.detail || e?.message || 'Something went wrong. Is the backend running?')
    } finally {
      setLoading(false)
    }
  }

  return {
    data,
    loading,
    error,
    search,
    reset: () => { setData(null); setError(null) }
  }
}
