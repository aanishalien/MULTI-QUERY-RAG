import re
from typing import List
from anthropic import Anthropic
import ast
from dotenv import load_dotenv
import os

load_dotenv()

client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

class QueryExpander:
    def __init__(self, n_queries: int = 4):
        self.n_queries = n_queries
    
    def expand(self, query: str) -> List[str]:
        prompt = f""" 
You are an expert query expander. Given the input query, generate {self.n_queries} diverse and relevant search queries that capture different aspects of the original query. Each query should be concise and focused.

Original Query: "{query}"

Generate {self.n_queries - 1} alternative search queries
that have the same meaning but use different wording.

Return ONLY a Python list of strings.
"""
        
        response = client.messages.create(
            model="claude-3-haiku-20240307",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.4,
            max_tokens=300
        )

        raw_text = response.content[0].text.strip()
        
        try:
            # Extract first Python-style list from text
            match = re.search(r"\[[\s\S]*\]", raw_text)
            if not match:
                raise ValueError("No list found in response")

            expanded = ast.literal_eval(match.group())

            if not isinstance(expanded, list):
                raise ValueError("Parsed result is not a list")

            return expanded

        except Exception as e:
            raise ValueError(f"Failed to parse response: {raw_text}") from e
        