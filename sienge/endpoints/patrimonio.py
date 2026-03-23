"""
sienge.endpoints.patrimonio — Endpoints de Patrimonio (ativos fixos, moveis, alugueis).
"""

from __future__ import annotations

from .base import BaseEndpoints
from ..utils import paginate


class PatrimonioEndpoints(BaseEndpoints):
    """Endpoints de Patrimonio: ativos fixos, moveis, alugueis de imoveis."""

    def list_ativos_fixos(self, limit: int | None = None) -> list[dict]:
        """Lista ativos fixos (patrimonio imobilizado).

        Args:
            limit: Limite de resultados.

        Returns:
            Lista de dicts com ativos fixos.
        """
        params: dict = {}
        if limit:
            params["limit"] = min(limit, 200)
        data = self._get("/patrimony/fixed", params=params)
        return data.get("results", data if isinstance(data, list) else [])

    def list_ativos_moveis(self, limit: int | None = None) -> list[dict]:
        """Lista ativos moveis (bens moveis).

        Args:
            limit: Limite de resultados.

        Returns:
            Lista de dicts com ativos moveis.
        """
        params: dict = {}
        if limit:
            params["limit"] = min(limit, 200)
        data = self._get("/patrimony/movable", params=params)
        return data.get("results", data if isinstance(data, list) else [])

    def list_alugueis(self, limit: int | None = None) -> list[dict]:
        """Lista alugueis de imoveis.

        Args:
            limit: Limite de resultados.

        Returns:
            Lista de dicts com alugueis.
        """
        params: dict = {}
        if limit:
            params["limit"] = min(limit, 200)
        data = self._get("/property-rental", params=params)
        return data.get("results", data if isinstance(data, list) else [])
