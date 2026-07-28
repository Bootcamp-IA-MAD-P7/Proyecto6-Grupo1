"""Small, local-only request controls for the prediction API."""

from __future__ import annotations

from collections import defaultdict, deque
from threading import Lock
from time import monotonic


class LocalRateLimiter:
    """Best-effort in-memory rate limiter for one local API process.

    Keys are retained only in process memory until their window expires. They
    must never be logged, persisted, or treated as an identity mechanism.
    """

    def __init__(self, requests_per_minute: int, window_seconds: float = 60.0) -> None:
        self.requests_per_minute = requests_per_minute
        self.window_seconds = window_seconds
        self._requests: dict[str, deque[float]] = defaultdict(deque)
        self._lock = Lock()

    def allow(self, temporary_client_key: str, now: float | None = None) -> bool:
        """Record and allow one request when the temporary window has capacity."""
        current_time = monotonic() if now is None else now
        cutoff = current_time - self.window_seconds

        with self._lock:
            self._discard_expired(cutoff)
            timestamps = self._requests[temporary_client_key]
            if len(timestamps) >= self.requests_per_minute:
                return False
            timestamps.append(current_time)
            return True

    def _discard_expired(self, cutoff: float) -> None:
        for key, timestamps in tuple(self._requests.items()):
            while timestamps and timestamps[0] <= cutoff:
                timestamps.popleft()
            if not timestamps:
                del self._requests[key]
