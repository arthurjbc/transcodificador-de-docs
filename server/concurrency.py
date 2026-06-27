import threading
from contextlib import contextmanager


class ConversionManager:
    def __init__(self, max_concurrent):
        self.max_concurrent = max_concurrent
        self._semaphore = threading.BoundedSemaphore(max_concurrent)
        self._lock = threading.Lock()
        self.active = 0
        self.peak = 0
        self.total = 0
        self.failed = 0
        self.bytes_in = 0
        self.bytes_out = 0

    @contextmanager
    def slot(self):
        """Reserva uma vaga de conversão; bloqueia se o limite foi atingido."""
        self._semaphore.acquire()
        with self._lock:
            self.active += 1
            self.peak = max(self.peak, self.active)
        try:
            yield
        finally:
            with self._lock:
                self.active -= 1
            self._semaphore.release()

    def record_success(self, in_size, out_size):
        with self._lock:
            self.total += 1
            self.bytes_in += in_size
            self.bytes_out += out_size

    def record_failure(self):
        with self._lock:
            self.failed += 1

    def snapshot(self):
        with self._lock:
            return {
                "active": self.active,
                "peak": self.peak,
                "total": self.total,
                "failed": self.failed,
                "bytes_in": self.bytes_in,
                "bytes_out": self.bytes_out,
            }
