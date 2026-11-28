"""Process-local store for opt-in staff login tokens."""

import re
import secrets
from threading import Lock
from time import monotonic

COOKIE_NAME = "__Host-omai_remember_session"
TTL_SECONDS = 24 * 60 * 60
_TOKEN_FORMAT = re.compile(r"[A-Za-z0-9_-]{43}")


class RememberedSessions:
    def __init__(self, ttl_seconds=TTL_SECONDS, capacity=256, clock=monotonic):
        self._ttl_seconds = ttl_seconds
        self._capacity = capacity
        self._clock = clock
        self._expires_at = {}
        self._lock = Lock()

    def issue(self):
        with self._lock:
            now = self._clock()
            # Equal lifetimes keep entries ordered by expiry, oldest first.
            while self._expires_at:
                oldest = next(iter(self._expires_at))
                if self._expires_at[oldest] > now and len(self._expires_at) < self._capacity:
                    break
                del self._expires_at[oldest]
            token = secrets.token_urlsafe(32)
            self._expires_at[token] = now + self._ttl_seconds
            return token

    def is_valid(self, token):
        if not isinstance(token, str) or not _TOKEN_FORMAT.fullmatch(token):
            return False
        with self._lock:
            expires_at = self._expires_at.get(token)
            if expires_at is None:
                return False
            if self._clock() >= expires_at:
                del self._expires_at[token]
                return False
            return True

    def revoke(self, token):
        with self._lock:
            self._expires_at.pop(token, None)
