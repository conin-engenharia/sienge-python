"""
sienge.utils — Utilitarios: paginacao automatica, retry, formatacao.
"""

import logging
import time
from typing import Any, Callable, Iterator, TypeVar

from .exceptions import RateLimitError, MaintenanceError, SiengeError

logger = logging.getLogger("sienge")

T = TypeVar("T")

# Limite maximo por pagina da API Sienge
MAX_PAGE_SIZE = 200


def retry_with_backoff(
    func: Callable[..., T],
    max_retries: int = 3,
    base_delay: float = 1.0,
    max_delay: float = 60.0,
    retryable_exceptions: tuple = (RateLimitError, MaintenanceError, ConnectionError, TimeoutError),
) -> T:
    """Executa func com retry e backoff exponencial.

    Args:
        func: Callable sem argumentos a executar.
        max_retries: Numero maximo de tentativas.
        base_delay: Delay base em segundos.
        max_delay: Delay maximo em segundos.
        retryable_exceptions: Excecoes que disparam retry.

    Returns:
        Resultado de func().

    Raises:
        A excecao original apos esgotar tentativas.
    """
    last_exc = None
    for attempt in range(max_retries + 1):
        try:
            return func()
        except retryable_exceptions as e:
            last_exc = e
            if attempt == max_retries:
                raise
            # Se RateLimitError, usa retry_after como delay
            if isinstance(e, RateLimitError) and e.retry_after:
                delay = min(e.retry_after, max_delay)
            else:
                delay = min(base_delay * (2 ** attempt), max_delay)
            logger.warning(
                "Tentativa %d/%d falhou (%s). Retentando em %.1fs...",
                attempt + 1, max_retries + 1, type(e).__name__, delay,
            )
            time.sleep(delay)
    raise last_exc  # type: ignore[misc]


def paginate(
    fetch_page: Callable[[int, int], dict],
    limit_per_page: int = 200,
    max_results: int | None = None,
) -> Iterator[dict]:
    """Itera automaticamente sobre resultados paginados da API Sienge.

    A API retorna: {"resultSetMetadata": {"count": N, "offset": O, "limit": L}, "results": [...]}

    Args:
        fetch_page: Callable(offset, limit) que retorna a resposta JSON da API.
        limit_per_page: Itens por pagina (max 200).
        max_results: Limite total de resultados (None = todos).

    Yields:
        Cada item individual dos resultados.
    """
    offset = 0
    page_size = min(limit_per_page, MAX_PAGE_SIZE)
    yielded = 0

    while True:
        data = fetch_page(offset, page_size)

        results = data.get("results", [])
        if not results:
            break

        for item in results:
            yield item
            yielded += 1
            if max_results and yielded >= max_results:
                return

        # Verifica se ha mais paginas
        metadata = data.get("resultSetMetadata", {})
        total = metadata.get("count", 0)

        offset += len(results)
        if offset >= total:
            break


def format_currency(value: float | int | None, symbol: str = "R$") -> str:
    """Formata valor monetario no padrao brasileiro."""
    if value is None:
        return f"{symbol} 0,00"
    formatted = f"{value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    return f"{symbol} {formatted}"


def parse_sienge_date(date_str: str | None) -> str | None:
    """Normaliza datas do Sienge para YYYY-MM-DD."""
    if not date_str:
        return None
    # Sienge retorna YYYY-MM-DD normalmente
    return date_str[:10] if len(date_str) >= 10 else date_str
