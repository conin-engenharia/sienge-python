"""
sienge.endpoints.bulk — Endpoints de Bulk Data (exportacao em massa).

ENDPOINTS BULK CONFIRMADOS (auditoria 2026-03-14):
  ✅ /income — parcelas a receber (startDate, endDate, selectionType=D)
  ✅ /outcome — parcelas a pagar (startDate, endDate, selectionType=D, correctionIndexerId, correctionDate)
  ✅ /bank-movement — movimentos caixa/banco (startDate, endDate) — 784 registros
  ✅ /purchase-quotations — cotacoes (startDate, endDate) — 75 itens
  ✅ /customer-extract-history — extrato cliente
  ✅ /customer-debt-balance — saldo devedor
  ✅ /defaulters-receivable-bills — inadimplentes
  ✅ /building/resources — insumos da obra
  ✅ /business-budget — orcamento empresarial
  ✅ /accountancy/accountBalance — saldos contabeis empresa
  ✅ /accountancy/accountCostCenterBalance — saldos contabeis CC
  ✅ /invoice-itens — itens notas fiscais
  ❌ /payable-bills — 404
  ❌ /building-cost-estimations — 404
  ❌ /cash-bank-movements — 404 (path correto: /bank-movement)
  ❌ /invoices — 404 (path correto: /invoice-itens)
"""

from __future__ import annotations

from .base import BaseEndpoints


class BulkEndpoints(BaseEndpoints):
    """Endpoints de Bulk Data para exportacao em massa."""

    def export_income(self, start_date: str, end_date: str, selection_type: str = "D") -> list[dict]:
        """Exporta parcelas a receber.

        Args:
            start_date: Data inicio (YYYY-MM-DD).
            end_date: Data fim (YYYY-MM-DD).
            selection_type: Tipo selecao — I(ssue), P(ay), D(ue), B(ill), C.

        Returns:
            Lista de dicts com dados.
        """
        data = self._get("/income", params={
            "startDate": start_date,
            "endDate": end_date,
            "selectionType": selection_type,
        }, is_bulk=True)
        result = data.get("data", data.get("results", data if isinstance(data, list) else []))
        return result if isinstance(result, list) else []

    def export_outcome(self, start_date: str, end_date: str, selection_type: str = "D",
                       correction_indexer_id: int = 1, correction_date: str = "") -> list[dict]:
        """Exporta parcelas a pagar.

        Args:
            start_date: Data inicio (YYYY-MM-DD).
            end_date: Data fim (YYYY-MM-DD).
            selection_type: Tipo selecao — I(ssue), P(ay), D(ue).
            correction_indexer_id: ID do indexador de correcao.
            correction_date: Data de correcao (YYYY-MM-DD).

        Returns:
            Lista de dicts.
        """
        if not correction_date:
            correction_date = end_date
        data = self._get("/outcome", params={
            "startDate": start_date,
            "endDate": end_date,
            "selectionType": selection_type,
            "correctionIndexerId": correction_indexer_id,
            "correctionDate": correction_date,
        }, is_bulk=True)
        result = data.get("data", data.get("results", data if isinstance(data, list) else []))
        return result if isinstance(result, list) else []

    def export_bank_movements(self, start_date: str, end_date: str) -> list[dict]:
        """Exporta movimentos de caixa e bancos.

        NOTA: Path correto e /bank-movement (NAO /cash-bank-movements).

        Args:
            start_date: Data inicio (YYYY-MM-DD).
            end_date: Data fim (YYYY-MM-DD).

        Returns:
            Lista de dicts com movimentos (784 na CONIN em 7 dias).
        """
        data = self._get("/bank-movement", params={
            "startDate": start_date,
            "endDate": end_date,
        }, is_bulk=True)
        result = data.get("data", data.get("results", data if isinstance(data, list) else []))
        return result if isinstance(result, list) else []

    def export_purchase_quotations(self, start_date: str, end_date: str) -> list[dict]:
        """Exporta cotacoes de precos em massa.

        Args:
            start_date: Data inicio (YYYY-MM-DD).
            end_date: Data fim (YYYY-MM-DD).

        Returns:
            Lista de dicts (75 na CONIN).
        """
        data = self._get("/purchase-quotations", params={
            "startDate": start_date,
            "endDate": end_date,
        }, is_bulk=True)
        result = data.get("data", data.get("results", data if isinstance(data, list) else []))
        return result if isinstance(result, list) else []

    def export_customer_extract(self, start_due_date: str, end_due_date: str) -> list[dict]:
        """Exporta historico de extrato de clientes.

        Args:
            start_due_date: Data inicio vencimento (YYYY-MM-DD).
            end_due_date: Data fim vencimento (YYYY-MM-DD).

        Returns:
            Lista de dicts.
        """
        data = self._get("/customer-extract-history", params={
            "startDueDate": start_due_date,
            "endDueDate": end_due_date,
        }, is_bulk=True)
        result = data.get("data", data.get("results", data if isinstance(data, list) else []))
        return result if isinstance(result, list) else []

    def export_customer_debt(self, start_due_date: str, end_due_date: str) -> list[dict]:
        """Exporta saldo devedor de clientes.

        Args:
            start_due_date: Data inicio vencimento (YYYY-MM-DD).
            end_due_date: Data fim vencimento (YYYY-MM-DD).

        Returns:
            Lista de dicts.
        """
        data = self._get("/customer-debt-balance", params={
            "startDueDate": start_due_date,
            "endDueDate": end_due_date,
        }, is_bulk=True)
        result = data.get("data", data.get("results", data if isinstance(data, list) else []))
        return result if isinstance(result, list) else []

    def export_defaulters(self, company_id: int) -> list[dict]:
        """Exporta titulos de inadimplentes.

        Args:
            company_id: ID da empresa (OBRIGATORIO).

        Returns:
            Lista de dicts.
        """
        data = self._get("/defaulters-receivable-bills", params={
            "companyId": company_id,
        }, is_bulk=True)
        result = data.get("data", data.get("results", data if isinstance(data, list) else []))
        return result if isinstance(result, list) else []

    def export_building_resources(self, building_id: int, start_date: str, end_date: str) -> list[dict]:
        """Exporta insumos de uma obra.

        Args:
            building_id: ID do empreendimento (OBRIGATORIO).
            start_date: Data inicio (YYYY-MM-DD).
            end_date: Data fim (YYYY-MM-DD).

        Returns:
            Lista de dicts.
        """
        data = self._get("/building/resources", params={
            "buildingId": building_id,
            "startDate": start_date,
            "endDate": end_date,
        }, is_bulk=True)
        result = data.get("data", data.get("results", data if isinstance(data, list) else []))
        return result if isinstance(result, list) else []

    def export_business_budget(self, start_date: str, end_date: str) -> list[dict]:
        """Exporta orcamento empresarial.

        Args:
            start_date: Data inicio (YYYY-MM-DD).
            end_date: Data fim (YYYY-MM-DD).

        Returns:
            Lista de dicts.
        """
        data = self._get("/business-budget", params={
            "startDate": start_date,
            "endDate": end_date,
        }, is_bulk=True)
        result = data.get("data", data.get("results", data if isinstance(data, list) else []))
        return result if isinstance(result, list) else []

    def export_account_balance(self, start_date: str, end_date: str) -> list[dict]:
        """Exporta saldos contabeis por empresa.

        Args:
            start_date: Data inicio (YYYY-MM-DD).
            end_date: Data fim (YYYY-MM-DD).

        Returns:
            Lista de dicts.
        """
        data = self._get("/accountancy/accountBalance", params={
            "startDate": start_date,
            "endDate": end_date,
        }, is_bulk=True)
        result = data.get("data", data.get("results", data if isinstance(data, list) else []))
        return result if isinstance(result, list) else []

    def export_account_cc_balance(self, start_date: str, end_date: str) -> list[dict]:
        """Exporta saldos contabeis por centro de custo.

        Args:
            start_date: Data inicio (YYYY-MM-DD).
            end_date: Data fim (YYYY-MM-DD).

        Returns:
            Lista de dicts.
        """
        data = self._get("/accountancy/accountCostCenterBalance", params={
            "startDate": start_date,
            "endDate": end_date,
        }, is_bulk=True)
        result = data.get("data", data.get("results", data if isinstance(data, list) else []))
        return result if isinstance(result, list) else []

    def export_invoice_items(self, company_id: int, start_date: str, end_date: str) -> list[dict]:
        """Exporta itens de notas fiscais.

        NOTA: Path correto e /invoice-itens (NAO /invoices).

        Args:
            company_id: ID da empresa (OBRIGATORIO).
            start_date: Data inicio (YYYY-MM-DD).
            end_date: Data fim (YYYY-MM-DD).

        Returns:
            Lista de dicts.
        """
        data = self._get("/invoice-itens", params={
            "companyId": company_id,
            "startDate": start_date,
            "endDate": end_date,
        }, is_bulk=True)
        result = data.get("data", data.get("results", data if isinstance(data, list) else []))
        return result if isinstance(result, list) else []

    def export(self, resource: str, params: dict | None = None) -> list[dict]:
        """Exporta qualquer recurso bulk generico.

        Args:
            resource: Nome do recurso (ex: "income", "bank-movement").
            params: Query params.

        Returns:
            Lista de dicts.
        """
        data = self._get(f"/{resource}", params=params, is_bulk=True)
        result = data.get("data", data.get("results", data if isinstance(data, list) else []))
        return result if isinstance(result, list) else []
