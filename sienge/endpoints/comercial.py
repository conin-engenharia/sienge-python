"""
sienge.endpoints.comercial — Endpoints Comerciais (clientes, contratos, unidades).
"""

from __future__ import annotations

from typing import Iterator

from .base import BaseEndpoints
from ..models.comercial import Cliente, Unidade
from ..utils import paginate


class ComercialEndpoints(BaseEndpoints):
    """Endpoints Comerciais: clientes, contratos de venda, unidades."""

    # ── Clientes ───────────────────────────────────────────────────────

    def list_clientes(self, limit: int | None = None) -> list[Cliente]:
        """Lista clientes.

        Args:
            limit: Limite de resultados (None = todos).

        Returns:
            Lista de Cliente.
        """
        return list(self.iter_clientes(max_results=limit))

    def iter_clientes(self, max_results: int | None = None) -> Iterator[Cliente]:
        """Itera sobre clientes com paginacao.

        Yields:
            Cliente.
        """
        def fetch(offset: int, limit: int) -> dict:
            return self._get("/customers", params={"offset": offset, "limit": limit})

        for item in paginate(fetch, max_results=max_results):
            yield Cliente.from_api(item)

    def get_cliente(self, client_id: int) -> Cliente:
        """Busca um cliente pelo ID.

        Args:
            client_id: ID do cliente.

        Returns:
            Cliente.
        """
        data = self._get(f"/customers/{client_id}")
        return Cliente.from_api(data)

    def search_clientes(self, nome: str) -> list[Cliente]:
        """Busca clientes pelo nome.

        Args:
            nome: Nome ou parte do nome.

        Returns:
            Lista de Cliente.
        """
        data = self._get("/customers", params={"name": nome})
        results = data.get("results", data if isinstance(data, list) else [])
        return [Cliente.from_api(r) for r in results]

    # ── Contratos de Venda (/sales-contracts) ───────────────────────────

    def list_contratos_venda(
        self,
        limit: int | None = None,
    ) -> list[dict]:
        """Lista contratos de venda.

        NOTA: /contracts NAO EXISTE. Usar /sales-contracts.
        Para contratos de suprimentos, usar SuprimentosEndpoints.

        Args:
            limit: Limite de resultados.

        Returns:
            Lista de dicts com contratos.
        """
        params: dict = {}
        if limit:
            params["limit"] = min(limit, 200)

        data = self._get("/sales-contracts", params=params)
        results = data.get("results", data if isinstance(data, list) else [])
        return results

    def get_contrato_venda(self, contract_id: int) -> dict:
        """Busca um contrato de venda pelo ID.

        Args:
            contract_id: ID do contrato.

        Returns:
            Dict com dados do contrato.
        """
        return self._get(f"/sales-contracts/{contract_id}")

    # ── Contas a Receber (/accounts-receivable) ──────────────────────

    def list_titulos_receber(
        self,
        customer_id: int,
        company_id: int | None = None,
        cost_center_id: int | None = None,
        limit: int | None = None,
    ) -> list[dict]:
        """Lista titulos a receber de um cliente.

        NOTA: /receivable-bills NAO EXISTE.
        Endpoint correto: /accounts-receivable/receivable-bills

        Args:
            customer_id: ID do cliente (OBRIGATORIO).
            company_id: ID da empresa (opcional).
            cost_center_id: ID do centro de custo (opcional).
            limit: Limite de resultados.

        Returns:
            Lista de dicts com titulos a receber.
        """
        params: dict = {"customerId": customer_id}
        if company_id:
            params["companyId"] = company_id
        if cost_center_id:
            params["costCenterId"] = cost_center_id
        if limit:
            params["limit"] = min(limit, 200)

        data = self._get("/accounts-receivable/receivable-bills", params=params)
        results = data.get("results", data if isinstance(data, list) else [])
        return results

    # ── Unidades ───────────────────────────────────────────────────────

    def list_unidades(
        self,
        building_id: int | None = None,
        limit: int | None = None,
    ) -> list[Unidade]:
        """Lista unidades imobiliarias.

        Args:
            building_id: Filtrar por obra.
            limit: Limite de resultados.

        Returns:
            Lista de Unidade.
        """
        params: dict = {}
        if building_id:
            params["buildingId"] = building_id
        if limit:
            params["limit"] = min(limit, 200)

        data = self._get("/units", params=params)
        results = data.get("results", data if isinstance(data, list) else [])
        return [Unidade.from_api(r) for r in results]

    def get_unidade(self, unit_id: int) -> Unidade:
        """Busca uma unidade pelo ID.

        Args:
            unit_id: ID da unidade.

        Returns:
            Unidade.
        """
        data = self._get(f"/units/{unit_id}")
        return Unidade.from_api(data)

    # ── Tipos de Cliente (/customer-types) ───────────────────────────

    def list_tipos_cliente(self) -> list[dict]:
        """Lista tipos de cliente cadastrados.

        Returns:
            Lista de dicts com tipos de cliente.
        """
        data = self._get("/customer-types")
        return data.get("results", data if isinstance(data, list) else [])

    # ── Unidades — Detalhes Imobiliarios ─────────────────────────────

    def list_caracteristicas_unidades(self) -> list[dict]:
        """Lista caracteristicas de unidades imobiliarias.

        Returns:
            Lista de dicts com caracteristicas.
        """
        data = self._get("/units/characteristics")
        return data.get("results", data if isinstance(data, list) else [])

    def list_situacoes_unidades(self) -> list[dict]:
        """Lista situacoes possiveis de unidades.

        Returns:
            Lista de dicts com situacoes.
        """
        data = self._get("/units/situations")
        return data.get("results", data if isinstance(data, list) else [])

    def list_tipos_imovel(self) -> list[dict]:
        """Lista tipos de imovel.

        Returns:
            Lista de dicts com tipos (4 na CONIN).
        """
        data = self._get("/property-types")
        return data.get("results", data if isinstance(data, list) else [])

    def get_mapa_imobiliario(
        self,
        cost_center_id: int,
        start_date: str,
        end_date: str,
    ) -> list[dict]:
        """Busca mapa imobiliario (quadro de areas).

        Args:
            cost_center_id: ID do centro de custo (OBRIGATORIO).
            start_date: Data inicio (YYYY-MM-DD).
            end_date: Data fim (YYYY-MM-DD).

        Returns:
            Lista de dicts com dados do mapa.
        """
        data = self._get("/real-estate-map", params={
            "costCentersId": cost_center_id,
            "startDate": start_date,
            "endDate": end_date,
        })
        return data.get("results", data if isinstance(data, list) else [])
