"""
sienge.endpoints.base — Classe base para grupos de endpoints.
"""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any

import requests

from ..exceptions import (
    AuthError,
    MaintenanceError,
    NotFoundError,
    RateLimitError,
    SiengeError,
    ValidationError,
)
from ..rate_limiter import RateLimiter
from ..utils import retry_with_backoff

if TYPE_CHECKING:
    from ..client import SiengeClient

logger = logging.getLogger("sienge")


class BaseEndpoints:
    """Classe base que fornece metodos HTTP autenticados e com rate limiting."""

    def __init__(self, client: "SiengeClient"):
        self._client = client

    @property
    def _base_url(self) -> str:
        return self._client._base_url

    @property
    def _bulk_url(self) -> str:
        return self._client._bulk_url

    @property
    def _session(self) -> requests.Session:
        return self._client._session

    @property
    def _rest_limiter(self) -> RateLimiter:
        return self._client._rest_limiter

    @property
    def _bulk_limiter(self) -> RateLimiter:
        return self._client._bulk_limiter

    @property
    def _timeout(self) -> int:
        return self._client._timeout

    @property
    def _max_retries(self) -> int:
        return self._client._max_retries

    def _request(
        self,
        method: str,
        path: str,
        params: dict[str, Any] | None = None,
        json_body: dict[str, Any] | None = None,
        is_bulk: bool = False,
    ) -> dict:
        """Faz requisicao autenticada com rate limiting e retry.

        Args:
            method: HTTP method (GET, POST, PUT, DELETE).
            path: Path relativo (ex: "/bills").
            params: Query parameters.
            json_body: Body JSON para POST/PUT.
            is_bulk: Se True, usa bulk URL e bulk rate limiter.

        Returns:
            Resposta JSON como dict.

        Raises:
            SiengeError: Em caso de erro.
        """
        base = self._bulk_url if is_bulk else self._base_url
        url = f"{base}{path}"
        limiter = self._bulk_limiter if is_bulk else self._rest_limiter

        def _do_request() -> dict:
            limiter.acquire()
            resp = self._session.request(
                method=method,
                url=url,
                params=params,
                json=json_body,
                timeout=self._timeout,
            )
            return self._handle_response(resp, method, url)

        return retry_with_backoff(
            _do_request,
            max_retries=self._max_retries,
            retryable_exceptions=(
                RateLimitError, MaintenanceError,
                requests.exceptions.ConnectionError,
                requests.exceptions.Timeout,
            ),
        )

    def _handle_response(self, resp: requests.Response, method: str, url: str) -> dict:
        """Trata status codes da resposta."""
        if resp.status_code == 200:
            if not resp.content:
                return {}
            try:
                return resp.json()
            except ValueError:
                return {"_raw": resp.text}

        if resp.status_code == 201:
            try:
                return resp.json()
            except ValueError:
                return {"_created": True}

        if resp.status_code == 204:
            return {"_no_content": True}

        body = resp.text[:500] if resp.text else ""

        if resp.status_code == 400:
            raise ValidationError(
                f"Parametros invalidos: {body}",
                status_code=400,
                response_body=body,
            )

        if resp.status_code == 401:
            raise AuthError(
                f"Nao autorizado. Verifique credenciais ou libere o recurso no painel Sienge. "
                f"URL: {url}",
                status_code=401,
                response_body=body,
            )

        if resp.status_code == 404:
            raise NotFoundError(
                f"Recurso nao encontrado: {url}",
                status_code=404,
                response_body=body,
            )

        if resp.status_code == 429:
            raise RateLimitError(
                f"Rate limit atingido para {url}",
                retry_after=60,
                response_body=body,
            )

        if resp.status_code == 503:
            raise MaintenanceError(
                f"Sienge em manutencao (00:00-06:30 UTC). URL: {url}",
                status_code=503,
                response_body=body,
            )

        raise SiengeError(
            f"Erro HTTP {resp.status_code} em {method} {url}: {body}",
            status_code=resp.status_code,
            response_body=body,
        )

    def _get(self, path: str, params: dict[str, Any] | None = None, is_bulk: bool = False) -> dict:
        return self._request("GET", path, params=params, is_bulk=is_bulk)

    def _post(self, path: str, json_body: dict[str, Any] | None = None, params: dict[str, Any] | None = None) -> dict:
        return self._request("POST", path, params=params, json_body=json_body)

    def _put(self, path: str, json_body: dict[str, Any] | None = None) -> dict:
        return self._request("PUT", path, json_body=json_body)

    def _patch(self, path: str, json_body: dict[str, Any] | None = None) -> dict:
        return self._request("PATCH", path, json_body=json_body)

    def _delete(self, path: str) -> dict:
        return self._request("DELETE", path)
