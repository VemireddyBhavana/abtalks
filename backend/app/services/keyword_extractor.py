import re
from typing import List, Set


class KeywordExtractor:
    """
    Extracts technical concepts, frameworks, tools, algorithms, and APIs from candidate answers.
    """

    KNOWN_TECH_TERMS = {
        "react", "fastapi", "axios", "pydantic", "uvicorn", "vite", "tailwind",
        "mcp", "rag", "embeddings", "vector", "asgi", "wsgi", "hooks", "routing",
        "interceptors", "concurrency", "docker", "vercel", "render", "context",
        "sliding window", "system prompt", "react agent", "cosine similarity"
    }

    @classmethod
    def extract_keywords(cls, text: str) -> List[str]:
        text_lower = text.lower()
        found: Set[str] = set()

        for term in cls.KNOWN_TECH_TERMS:
            if term in text_lower:
                found.add(term)

        # Regex fallback for capitalized technical words
        words = re.findall(r"\b[A-Z][a-zA-Z0-9]{2,}\b", text)
        for w in words:
            found.add(w)

        return sorted(list(found))
