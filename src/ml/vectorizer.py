"""Configurable TF-IDF vectorizer wrapper."""

from __future__ import annotations

from sklearn.feature_extraction.text import TfidfVectorizer

DEFAULT_CONFIG = {
    "max_features": 8000,
    "stop_words": "english",
    "min_df": 3,
    "max_df": 0.8,
    "ngram_range": (1, 2),
    "sublinear_tf": True,
}


class VectorizerConfig:
    """Wraps TfidfVectorizer with dict-based configuration."""

    def __init__(self, config: dict | None = None):
        merged = {**DEFAULT_CONFIG, **(config or {})}
        self._ngram_range = tuple(merged.pop("ngram_range", (1, 2)))
        self.config = merged
        self._vectorizer = TfidfVectorizer(
            **merged, ngram_range=self._ngram_range
        )

    def fit_transform(self, texts: list[str]):
        return self._vectorizer.fit_transform(texts)

    def transform(self, texts: list[str]):
        return self._vectorizer.transform(texts)

    @property
    def vectorizer(self) -> TfidfVectorizer:
        return self._vectorizer

    @property
    def feature_names(self) -> list[str]:
        return self._vectorizer.get_feature_names_out().tolist()

    def get_config(self) -> dict:
        return {
            **self.config,
            "ngram_range": list(self._ngram_range),
            "vectorizer": "TfidfVectorizer",
        }
