from typing import List, Dict


def build_recommendation_prompt(user_query: str, analyzed_query: Dict, retrieved_anime: List[Dict]) -> str:
    moods = ", ".join(m[0] for m in analyzed_query.get("mood", [])) or "not specified"
    themes = ", ".join(t[0] for t in analyzed_query.get("themes", [])) or "not specified"
    audience = next((a[0] for a in analyzed_query.get("audience", [])), "general")

    candidates = ""
    for i, a in enumerate(retrieved_anime, 1):
        candidates += (
            f"\n[{i}] {a['title']} ({a.get('year', 'N/A')})\n"
            f"     Type: {a.get('type','?')} | Episodes: {a.get('episodes','?')} | MAL Score: {a.get('score','N/A')}\n"
            f"     Genres: {a.get('genres','Unknown')} | Themes: {a.get('themes','None')}\n"
            f"     Synopsis: {a.get('synopsis','No synopsis')}\n"
            f"     Similarity: {a.get('similarity_score', 0)}\n"
        )

    return f"""You are AniMind, an expert anime recommendation assistant.

USER REQUEST: "{user_query}"

DETECTED: Mood: {moods} | Themes: {themes} | Audience: {audience}

CANDIDATES:
{candidates}

Pick the 3 best matches. For each write a personalized explanation referencing their request, who would enjoy it, and one honest caveat.

Return ONLY this JSON:
{{
  "recommendations": [
    {{
      "title": "Exact title from candidates",
      "explanation": "2-3 sentences referencing their specific request",
      "best_for": "Type of viewer who will love this",
      "caveat": "One honest heads-up",
      "genres": ["genre1", "genre2"]
    }}
  ],
  "summary": "One friendly sentence summarizing what you found"
}}"""
