"""
sienge.endpoints.credores — Endpoints de Credores (fornecedores).
"""

from __future__ import annotations

from typing import Iterator

from .base import BaseEndpoints
from ..models.credores import Credor
from ..utils import paginate


class CredoresEndpoints(BaseEndpoints):
    """Endpoints de Credores/Fornecedores."""

    def list_credores(self, limit: int | None = None) -> list[Credor]:
        """Lista credores/fornecedores.

        Args:
            limit: Limite de resultados (None = todos).

        Returns:
            Lista de Credor.
        """
        return list(self.iter_credores(max_results=limit))

    def iter_credores(self, max_results: int | None = None) -> Iterator[Credor]:
        """Itera sobre credores com paginacao.

        Yields:
            Credor.
        """
        def fetch(offset: int, limit: int) -> dict:
            return self._get("/creditors", params={"offset": offset, "limit": limit})

        for item in paginate(fetch, max_results=max_results):
            yield Credor.from_api(item)

    def get_credor(self, creditor_id: int) -> Credor:
        """Busca um credor pelo ID.

        Args:
            creditor_id: ID do credor.

        Returns:
            Credor.
        """
        data = self._get(f"/creditors/{creditor_id}")
        return Credor.from_api(data)

    def search_credores(self, nome: str) -> list[Credor]:
        """Busca credores pelo nome.

        Args:
            nome: Nome ou parte do nome.

        Returns:
            Lista de Credor.
        """
        data = self._get("/creditors", params={"name": nome})
        results = data.get("results", data if isinstance(data, list) else [])
        return [Credor.from_api(r) for r in results]

    def get_info_bancaria(self, creditor_id: int) -> list[dict]:
        """Lista informacoes bancarias de um credor.

        Args:
            creditor_id: ID do credor.

        Returns:
            Lista de dicts com dados bancarios.
        """
        data = self._get(f"/creditors/{creditor_id}/bank-accounts")
        return data.get("results", data if isinstance(data, list) else [])
