"""
sienge.endpoints.suprimentos — Endpoints de Suprimentos.

ENDPOINTS REAIS (auditoria 2026-03-14):
  ✅ GET /purchase-orders — 55.482 pedidos
  ✅ GET /purchase-invoices — 52.987 notas fiscais
  ✅ GET /supply-contracts/all — 187 contratos
  ✅ GET /supply-contracts/measurements/all — 371 medicoes
  ✅ GET /supply-contracts/addenda — 18 aditivos
  ✅ GET /stock-inventories/{ccId}/items — estoque por CC
  ✅ GET /stock-reservations — reservas
  ✅ GET /purchase-quotations/all/negotiations — 58 cotacoes
  ❌ GET /purchase-requests — 405 (GET nao funciona, POST sim)
  ❌ GET /stock — 404 (path errado)
  ❌ GET /contracts — 404 (path errado)
"""

from __future__ import annotations

from datetime import datetime, timedelta
from typing import Iterator

from .base import BaseEndpoints
from ..models.suprimentos import PedidoCompra
from ..utils import paginate


class SuprimentosEndpoints(BaseEndpoints):
    """Endpoints de Suprimentos: pedidos de compra."""

    # ── Pedidos de Compra (/purchase-orders) ───────────────────────────

    def list_pedidos(
        self,
        building_id: int | None = None,
        supplier_id: int | None = None,
        status: str | None = None,
        limit: int | None = None,
    ) -> list[PedidoCompra]:
        """Lista pedidos de compra.

        Args:
            building_id: Filtrar por obra (centro de custo).
            supplier_id: Filtrar por fornecedor.
            status: Filtrar por status (ex: "PENDING", "COMPLETED").
            limit: Limite de resultados.

        Returns:
            Lista de PedidoCompra.
        """
        return list(self.iter_pedidos(building_id, supplier_id, status, max_results=limit))

    def iter_pedidos(
        self,
        building_id: int | None = None,
        supplier_id: int | None = None,
        status: str | None = None,
        max_results: int | None = None,
    ) -> Iterator[PedidoCompra]:
        """Itera sobre pedidos de compra com paginacao.

        Yields:
            PedidoCompra.
        """
        def fetch(offset: int, limit: int) -> dict:
            params: dict = {"offset": offset, "limit": limit}
            if building_id:
                params["buildingId"] = building_id
            if supplier_id:
                params["supplierId"] = supplier_id
            if status:
                params["status"] = status
            return self._get("/purchase-orders", params=params)

        for item in paginate(fetch, max_results=max_results):
            yield PedidoCompra.from_api(item)

    def get_pedido(self, order_id: int) -> PedidoCompra:
        """Busca um pedido de compra pelo ID.

        Args:
            order_id: ID do pedido.

        Returns:
            PedidoCompra.
        """
        data = self._get(f"/purchase-orders/{order_id}")
        return PedidoCompra.from_api(data)

    def get_pedido_itens(self, order_id: int) -> list[dict]:
        """Lista itens de um pedido de compra.

        Args:
            order_id: ID do pedido.

        Returns:
            Lista de dicts com itens.
        """
        data = self._get(f"/purchase-orders/{order_id}/items")
        return data.get("results", data if isinstance(data, list) else [])

    # ── Notas Fiscais de Compra (/purchase-invoices) ─────────────────

    def list_notas_fiscais(
        self,
        limit: int | None = None,
    ) -> list[dict]:
        """Lista notas fiscais de compra.

        Args:
            limit: Limite de resultados.

        Returns:
            Lista de dicts com notas fiscais (52.987 na CONIN).
        """
        params: dict = {}
        if limit:
            params["limit"] = min(limit, 200)
        data = self._get("/purchase-invoices", params=params)
        return data.get("results", data if isinstance(data, list) else [])

    def get_nota_fiscal(self, sequential_number: int) -> dict:
        """Busca nota fiscal de compra por numero sequencial.

        Args:
            sequential_number: Numero sequencial da NF.

        Returns:
            Dict com dados da nota fiscal.
        """
        return self._get(f"/purchase-invoices/{sequential_number}")

    def get_nota_fiscal_itens(self, sequential_number: int) -> list[dict]:
        """Lista itens de uma nota fiscal de compra.

        Args:
            sequential_number: Numero sequencial da NF.

        Returns:
            Lista de dicts com itens.
        """
        data = self._get(f"/purchase-invoices/{sequential_number}/items")
        return data.get("results", data if isinstance(data, list) else [])

    # ── Contratos de Suprimentos (/supply-contracts) ─────────────────

    def list_contratos_suprimentos(
        self,
        limit: int | None = None,
    ) -> list[dict]:
        """Lista contratos de suprimentos.

        NOTA: /contracts NAO EXISTE. Path correto: /supply-contracts/all

        Args:
            limit: Limite de resultados.

        Returns:
            Lista de dicts com contratos (187 na CONIN).
        """
        params: dict = {}
        if limit:
            params["limit"] = min(limit, 200)
        data = self._get("/supply-contracts/all", params=params)
        return data.get("results", data if isinstance(data, list) else [])

    def list_medicoes_contrato(
        self,
        limit: int | None = None,
    ) -> list[dict]:
        """Lista medicoes de contratos.

        Args:
            limit: Limite de resultados.

        Returns:
            Lista de dicts com medicoes (371 na CONIN).
        """
        params: dict = {}
        if limit:
            params["limit"] = min(limit, 200)
        data = self._get("/supply-contracts/measurements/all", params=params)
        return data.get("results", data if isinstance(data, list) else [])

    def list_aditivos_contrato(self) -> list[dict]:
        """Lista aditivos de contratos.

        Returns:
            Lista de dicts com aditivos (18 na CONIN).
        """
        data = self._get("/supply-contracts/addenda")
        return data.get("results", data if isinstance(data, list) else [])

    # ── Estoque (/stock-inventories) ─────────────────────────────────

    def list_estoque(self, cost_center_id: int) -> list[dict]:
        """Lista itens em estoque de um centro de custo.

        NOTA: /stock NAO EXISTE. Path correto: /stock-inventories/{ccId}/items

        Args:
            cost_center_id: ID do centro de custo.

        Returns:
            Lista de dicts com itens de estoque.
        """
        data = self._get(f"/stock-inventories/{cost_center_id}/items")
        return data.get("results", data if isinstance(data, list) else [])

    def list_reservas_estoque(self) -> list[dict]:
        """Lista reservas de estoque.

        Returns:
            Lista de dicts com reservas.
        """
        data = self._get("/stock-reservations")
        return data.get("results", data if isinstance(data, list) else [])

    # ── Cotacoes de Precos (/purchase-quotations) ────────────────────

    def list_cotacoes(
        self,
        start_date: str | None = None,
        end_date: str | None = None,
        limit: int | None = None,
    ) -> list[dict]:
        """Lista cotacoes de precos com negociacoes.

        NOTA: GET /purchase-quotations retorna 405.
        Path correto: /purchase-quotations/all/negotiations

        Args:
            start_date: Data inicio (YYYY-MM-DD). Obrigatorio se sem quotationNumber.
            end_date: Data fim (YYYY-MM-DD). Obrigatorio se sem quotationNumber.
            limit: Limite de resultados.

        Returns:
            Lista de dicts com cotacoes (58 na CONIN).
        """
        if not start_date:
            start_date = (datetime.now() - timedelta(days=90)).strftime("%Y-%m-%d")
        if not end_date:
            end_date = datetime.now().strftime("%Y-%m-%d")

        params: dict = {"startDate": start_date, "endDate": end_date}
        if limit:
            params["limit"] = min(limit, 200)
        data = self._get("/purchase-quotations/all/negotiations", params=params)
        return data.get("results", data if isinstance(data, list) else [])

    # ── Criar Pedido de Compra (POST /purchase-orders) ───────────────

    def create_pedido(self, pedido_data: dict) -> dict:
        """Cria um pedido de compra.

        Args:
            pedido_data: Dict com dados do pedido conforme API.

        Returns:
            Resposta da API.
        """
        return self._post("/purchase-orders", json_body=pedido_data)

    # ── Autorizar/Rejeitar Item (PATCH) ──────────────────────────────

    def update_item_status(self, order_id: int, item_id: int, status: str) -> dict:
        """Autoriza ou rejeita um item de pedido de compra.

        Args:
            order_id: ID do pedido.
            item_id: ID do item.
            status: Novo status (ex: "AUTHORIZED", "REJECTED").

        Returns:
            Resposta da API.
        """
        return self._patch(
            f"/purchase-orders/{order_id}/items/{item_id}/status",
            json_body={"status": status},
        )
