"""
sienge.endpoints.tabelas — Endpoints de Tabelas de Referencia (cidades, profissoes, unidades de medida, etc).
"""

from __future__ import annotations

from .base import BaseEndpoints
from ..utils import paginate


class TabelasEndpoints(BaseEndpoints):
    """Endpoints de Tabelas de Referencia: dados auxiliares e cadastros basicos."""

    def list_cidades(self, limit: int | None = None) -> list[dict]:
        """Lista cidades cadastradas.

        Args:
            limit: Limite de resultados (5.583 na CONIN).

        Returns:
            Lista de dicts com cidades.
        """
        def fetch(offset: int, lim: int) -> dict:
            return self._get("/cities", params={"offset": offset, "limit": lim})

        return list(paginate(fetch, max_results=limit))

    def list_estado_civil(self) -> list[dict]:
        """Lista estados civis.

        Returns:
            Lista de dicts com estados civis (4).
        """
        data = self._get("/civil-status")
        return data.get("results", data if isinstance(data, list) else [])

    def list_profissoes(self) -> list[dict]:
        """Lista profissoes cadastradas.

        Returns:
            Lista de dicts com profissoes (12).
        """
        data = self._get("/professions")
        return data.get("results", data if isinstance(data, list) else [])

    def list_marcas(self, limit: int | None = None) -> list[dict]:
        """Lista marcas/trademarks.

        Args:
            limit: Limite de resultados (258 na CONIN).

        Returns:
            Lista de dicts com marcas.
        """
        params: dict = {}
        if limit:
            params["limit"] = min(limit, 200)
        data = self._get("/trademarks", params=params)
        return data.get("results", data if isinstance(data, list) else [])

    def list_unidades_medida(self, limit: int | None = None) -> list[dict]:
        """Lista unidades de medida.

        Args:
            limit: Limite de resultados (67 na CONIN).

        Returns:
            Lista de dicts com unidades.
        """
        params: dict = {}
        if limit:
            params["limit"] = min(limit, 200)
        data = self._get("/units-of-measure", params=params)
        return data.get("results", data if isinstance(data, list) else [])

    def list_grupos_recurso(self, limit: int | None = None) -> list[dict]:
        """Lista grupos de recurso (insumos).

        Args:
            limit: Limite de resultados (81 na CONIN).

        Returns:
            Lista de dicts com grupos.
        """
        params: dict = {}
        if limit:
            params["limit"] = min(limit, 200)
        data = self._get("/resource-groups", params=params)
        return data.get("results", data if isinstance(data, list) else [])

    def list_grupos_servico(self, limit: int | None = None) -> list[dict]:
        """Lista grupos de servico (itens de obra).

        Args:
            limit: Limite de resultados (871 na CONIN).

        Returns:
            Lista de dicts com grupos.
        """
        def fetch(offset: int, lim: int) -> dict:
            return self._get("/work-item-groups", params={"offset": offset, "limit": lim})

        return list(paginate(fetch, max_results=limit))

    def list_indexadores(self) -> list[dict]:
        """Lista indexadores de correcao monetaria (IGPM, IPCA, etc).

        Returns:
            Lista de dicts com indexadores (3 na CONIN).
        """
        data = self._get("/indexers")
        return data.get("results", data if isinstance(data, list) else [])

    def list_condicoes_pagamento(self) -> list[dict]:
        """Lista condicoes/tipos de pagamento.

        Returns:
            Lista de dicts com condicoes (8 na CONIN).
        """
        data = self._get("/payment-condition-types")
        return data.get("results", data if isinstance(data, list) else [])
