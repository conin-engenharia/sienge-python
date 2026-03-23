"""
sienge.rate_limiter — Controle de rate limit para a API Sienge.

Limites:
  - REST: 200 req/min por subdominio
  - BULK: 20 req/min por subdominio
"""

import threading
import time
from collections import deque


class RateLimiter:
    """Rate limiter baseado em janela deslizante (sliding window)."""

    def __init__(self, max_requests: int, window_seconds: float = 60.0):
        self._max_requests = max_requests
        self._window = window_seconds
        self._timestamps: deque[float] = deque()
        self._lock = threading.Lock()

    def acquire(self) -> float:
        """Bloqueia ate que uma requisicao possa ser feita.

        Returns:
            Tempo de espera em segundos (0 se nao precisou esperar).
        """
        total_wait = 0.0
        with self._lock:
            now = time.monotonic()
            # Remove timestamps fora da janela
            cutoff = now - self._window
            while self._timestamps and self._timestamps[0] < cutoff:
                self._timestamps.popleft()

            if len(self._timestamps) >= self._max_requests:
                # Precisa esperar ate o timestamp mais antigo sair da janela
                wait_until = self._timestamps[0] + self._window
                wait_time = wait_until - now
                if wait_time > 0:
                    total_wait = wait_time

        if total_wait > 0:
            time.sleep(total_wait)

        with self._lock:
            self._timestamps.append(time.monotonic())

        return total_wait

    @property
    def remaining(self) -> int:
        """Requisicoes restantes na janela atual."""
        with self._lock:
            now = time.monotonic()
            cutoff = now - self._window
            while self._timestamps and self._timestamps[0] < cutoff:
                self._timestamps.popleft()
            return max(0, self._max_requests - len(self._timestamps))


# Instancias globais por tipo de API
_rest_limiter = None
_bulk_limiter = None
_lock = threading.Lock()


def get_rest_limiter() -> RateLimiter:
    """Retorna o rate limiter para REST API (200 req/min)."""
    global _rest_limiter
    with _lock:
        if _rest_limiter is None:
            _rest_limiter = RateLimiter(max_requests=195, window_seconds=60.0)  # margem de 5
        return _rest_limiter


def get_bulk_limiter() -> RateLimiter:
    """Retorna o rate limiter para Bulk API (20 req/min)."""
    global _bulk_limiter
    with _lock:
        if _bulk_limiter is None:
            _bulk_limiter = RateLimiter(max_requests=18, window_seconds=60.0)  # margem de 2
        return _bulk_limiter
