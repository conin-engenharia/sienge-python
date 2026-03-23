"""
sienge.endpoints.engenharia — Endpoints de Engenharia (empreendimentos, centros de custo como obras).

IMPORTANTE: O Sienge NAO tem endpoint /buildings.
- "Obras" no Sienge sao representadas como /enterprises (empreendimentos)
- Centros de custo (/cost-centers) tambem representam obras
- Pedidos de compra (/purchase-orders) referenciam buildingId = centro de custo
"""

from __future__ import annotations

from typing import Iterator

from .base import BaseEndpoints
from ..models.obra import Obra
from ..utils import paginate


class EngenhariaEndpoints(BaseEndpoints):
    """Endpoints de Engenharia: empreendimentos (obras), centros de custo."""

    # ── Empreendimentos (/enterprises) ─────────────────────────────────
    # Este e o conceito de "obra" no Sienge

    def list_obras(self, limit: int | None = None) -> list[Obra]:
        """Lista empreendimentos (obras/projetos).

        No Sienge, obras sao "enterprises" (empreendimentos).
        Retornados via GET /enterprises.

        Args:
            limit: Limite de resultados (None = todos via paginacao).

        Returns:
            Lista de Obra.
        """
        return list(self.iter_obras(max_results=limit))

    def iter_obras(self, max_results: int | None = None) -> Iterator[Obra]:
        """Itera sobre empreendimentos com paginacao automatica.

        Yields:
            Obra.
        """
        def fetch(offset: int, limit: int) -> dict:
            return self._get("/enterprises", params={"offset": offset, "limit": limit})

        for item in paginate(fetch, max_results=max_results):
            yield Obra.from_api(item)

    def get_obra(self, enterprise_id: int) -> Obra:
        """Busca um empreendimento pelo ID.

        Args:
            enterprise_id: ID do empreendimento no Sienge.

        Returns:
            Obra.
        """
        data = self._get(f"/enterprises/{enterprise_id}")
        return Obra.from_api(data)

    def search_obra(self, nome: str) -> list[Obra]:
        """Busca empreendimentos pelo nome.

        Filtra localmente pois /enterprises nao tem parametro de busca por nome.

        Args:
            nome: Nome ou parte do nome.

        Returns:
            Lista de Obra encontradas.
        """
        nome_lower = nome.lower()
        results = []
        for obra in self.iter_obras():
            if nome_lower in obra.nome.lower():
                results.append(obra)
            if len(results) >= 50:  # limite de seguranca
                break
        return results

    # ── Orcamentos de Obra (/building-cost-estimations) ──────────────

    def list_orcamento_planilhas(self, building_id: int) -> list[dict]:
        """Lista planilhas do orcamento de uma obra.

        Args:
            building_id: ID do empreendimento.

        Returns:
            Lista de dicts com planilhas.
        """
        data = self._get(f"/building-cost-estimations/{building_id}/sheets")
        return data.get("results", data if isinstance(data, list) else [])

    def list_orcamento_insumos(self, building_id: int, limit: int | None = None) -> list[dict]:
        """Lista insumos do orcamento de uma obra.

        Args:
            building_id: ID do empreendimento.
            limit: Limite de resultados.

        Returns:
            Lista de dicts com insumos (631 para building_id=1 na CONIN).
        """
        params: dict = {}
        if limit:
            params["limit"] = min(limit, 200)
        data = self._get(f"/building-cost-estimations/{building_id}/resources", params=params)
        return data.get("results", data if isinstance(data, list) else [])

    # ── Diario de Obra (/construction-daily-report) ──────────────────

    def list_diarios_obra(self, limit: int | None = None) -> list[dict]:
        """Lista diarios de obra.

        NOTA: Path correto e /construction-daily-report (singular).
        /construction-daily-reports (plural) retorna 404.

        Args:
            limit: Limite de resultados.

        Returns:
            Lista de dicts com diarios.
        """
        params: dict = {}
        if limit:
            params["limit"] = min(limit, 200)
        data = self._get("/construction-daily-report", params=params)
        return data.get("results", data if isinstance(data, list) else [])

    # ── Calendario de Obra (/building-projects/{id}/calendar) ────────

    def get_calendario_obra(self, building_id: int) -> dict:
        """Busca calendario de uma obra.

        NOTA: /building-calendar NAO EXISTE.
        Path correto: /building-projects/{buildingId}/calendar

        Args:
            building_id: ID do empreendimento.

        Returns:
            Dict com configuracao do calendario.
        """
        return self._get(f"/building-projects/{building_id}/calendar")

    # ── Tipos de Evento de Diario (/construction-daily-report/event-type) ──

    def list_tipos_evento_diario(self) -> list[dict]:
        """Lista tipos de evento para diario de obra.

        Returns:
            Lista de dicts com tipos de evento.
        """
        data = self._get("/construction-daily-report/event-type")
        return data.get("results", data if isinstance(data, list) else [])

    # ── Progresso de Obra (/building-projects/progress-logs) ─────────

    def list_progresso_obra(self, limit: int | None = None) -> list[dict]:
        """Lista logs de progresso de obras.

        Args:
            limit: Limite de resultados.

        Returns:
            Lista de dicts com logs de progresso.
        """
        params: dict = {}
        if limit:
            params["limit"] = min(limit, 200)
        data = self._get("/building-projects/progress-logs", params=params)
        return data.get("results", data if isinstance(data, list) else [])

    # ── Canteiros de Obra (/sites) ───────────────────────────────────

    def list_canteiros(self, building_id: int) -> list[dict]:
        """Lista canteiros de obra.

        Args:
            building_id: ID do empreendimento (OBRIGATORIO).

        Returns:
            Lista de dicts com canteiros.
        """
        data = self._get("/sites", params={"buildingId": building_id})
        return data.get("results", data if isinstance(data, list) else [])

    # ── Bases de Custo (/cost-databases) ─────────────────────────────

    def list_bases_custo(self) -> list[dict]:
        """Lista bases de referencia de custo (SINAPI, SICRO, etc).

        Returns:
            Lista de dicts com bases de custo (2 na CONIN).
        """
        data = self._get("/cost-databases")
        return data.get("results", data if isinstance(data, list) else [])
