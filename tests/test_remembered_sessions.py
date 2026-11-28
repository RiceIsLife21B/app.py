import unittest

from remembered_sessions import RememberedSessions


class RememberedSessionsTests(unittest.TestCase):
    def setUp(self):
        self.now = 100.0
        self.sessions = RememberedSessions(ttl_seconds=10, capacity=2, clock=lambda: self.now)

    def test_only_issued_tokens_are_valid(self):
        token = self.sessions.issue()
        self.assertTrue(self.sessions.is_valid(token))
        self.assertFalse(self.sessions.is_valid(None))
        self.assertFalse(self.sessions.is_valid("a" * 43))
        self.assertFalse(self.sessions.is_valid("invalid"))
        self.assertFalse(RememberedSessions().is_valid(token))

    def test_expiration_is_absolute(self):
        token = self.sessions.issue()
        self.now += 9
        self.assertTrue(self.sessions.is_valid(token))
        self.now += 1
        self.assertFalse(self.sessions.is_valid(token))

    def test_revocation_is_idempotent(self):
        token = self.sessions.issue()
        self.sessions.revoke(token)
        self.sessions.revoke(token)
        self.sessions.revoke(None)
        self.assertFalse(self.sessions.is_valid(token))

    def test_capacity_evicts_the_oldest_token(self):
        oldest = self.sessions.issue()
        second = self.sessions.issue()
        newest = self.sessions.issue()
        self.assertFalse(self.sessions.is_valid(oldest))
        self.assertTrue(self.sessions.is_valid(second))
        self.assertTrue(self.sessions.is_valid(newest))
