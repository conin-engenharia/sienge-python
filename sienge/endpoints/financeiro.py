"""
sienge.endpoints.financeiro — Endpoints Financeiros (titulos, centros de custo, contas).
"""

from __future__ import annotations

import re
from datetime import datetime, timedelta
from typing import Iterator

from .base import BaseEndpoints
from ..models.financeiro import CentroCusto, ContaContabil, Titulo, TituloInstallment
from ..utils import paginate

_SAFE_SEARCH = re.compile(r"[^\w\s\-.]", re.UNICODE)


class FinanceiroEndpoints(BaseEndpoints):
    """Endpoints Financeiros: titulos a pagar/receber, centros de custo, contas contabeis."""

    # ── Titulos a Pagar (Bills) ────────────────────────────────────────

    def list_titulos(
        self,
        start_date: str | None = None,
        end_date: str | None = None,
        status: str | None = None,
        limit: int | None = None,
    ) -> list[Titulo]:
        """Lista titulos a pagar.

        Args:
            start_date: Data inicio (YYYY-MM-DD). Default: 30 dias atras.
            end_date: Data fim (YYYY-MM-DD). Default: hoje.
            status: Filtro de status (ex: "S" aberto, "P" pago).
            limit: Limite de resultados (None = todos via paginacao).

        Returns:
            Lista de Titulo.
        """
        return list(self.iter_titulos(start_date, end_date, status, max_results=limit))

    def iter_titulos(
        self,
        start_date: str | None = None,
        end_date: str | None = None,
        status: str | None = None,
        max_results: int | None = None,
    ) -> Iterator[Titulo]:
        """Itera sobre titulos com paginacao automatica.

        Args:
            start_date: Data inicio (YYYY-MM-DD). Default: 30 dias atras.
            end_date: Data fim (YYYY-MM-DD). Default: hoje.
            status: Filtro de status.
            max_results: Limite total.

        Yields:
            Titulo.
        """
        if not start_date:
            start_date = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
        if not end_date:
            end_date = datetime.now().strftime("%Y-%m-%d")

        def fetch(offset: int, limit: int) -> dict:
            params = {
                "startDate": start_date,
                "endDate": end_date,
                "offset": offset,
                "limit": limit,
            }
            if status:
                params["status"] = status
            return self._get("/bills", params=params)

        for item in paginate(fetch, max_results=max_results):
            yield Titulo.from_api(item)

    def get_titulo(self, bill_id: int) -> Titulo:
        """Busca um titulo pelo ID.

        Args:
            bill_id: ID do titulo.

        Returns:
            Titulo.
        """
        data = self._get(f"/bills/{bill_id}")
        return Titulo.from_api(data)

    def get_parcelas(self, bill_id: int) -> list[TituloInstallment]:
        """Lista parcelas de um titulo.

        Args:
            bill_id: ID do titulo.

        Returns:
            Lista de TituloInstallment.
        """
        data = self._get(f"/bills/{bill_id}/installments")
        results = data.get("results", data if isinstance(data, list) else [])
        return [TituloInstallment.from_api(r) for r in results]

    def get_impostos(self, bill_id: int) -> list[dict]:
        """Lista impostos de um titulo.

        Args:
            bill_id: ID do titulo.

        Returns:
            Lista de dicts com impostos.
        """
        data = self._get(f"/bills/{bill_id}/taxes")
        return data.get("results", data if isinstance(data, list) else [])

    # ── Titulos a Pagar — Criacao (/bills POST) ────────────────────────

    def create_titulo(self, titulo_data: dict) -> dict:
        """Cria um titulo a pagar.

        NOTA: /payable-bills NAO EXISTE como endpoint REST.
        Usar /bills com POST.

        Args:
            titulo_data: Dict com dados do titulo conforme API.

        Returns:
            Resposta da API.
        """
        return self._post("/bills", json_body=titulo_data)

    # ── Extrato de Contas (/accounts-statements) ─────────────────────

    def list_accounts_statements(
        self,
        start_date: str | None = None,
        end_date: str | None = None,
        limit: int | None = None,
    ) -> list[dict]:
        """Lista movimentacoes financeiras (extrato de contas).

        Args:
            start_date: Data inicio (YYYY-MM-DD). Default: 30 dias atras.
            end_date: Data fim (YYYY-MM-DD). Default: hoje.
            limit: Limite de resultados.

        Returns:
            Lista de dicts com movimentacoes.
        """
        if not start_date:
            start_date = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
        if not end_date:
            end_date = datetime.now().strftime("%Y-%m-%d")

        params: dict = {"startDate": start_date, "endDate": end_date}
        if limit:
            params["limit"] = min(limit, 200)

        data = self._get("/accounts-statements", params=params)
        return data.get("results", data if isinstance(data, list) else [])

    # ── Balancete de Verificacao (/trial-balance) ────────────────────

    def get_trial_balance(
        self,
        company_id: int,
        initial_period: str,
        final_period: str,
    ) -> list[dict]:
        """Busca dados do balancete de verificacao.

        Args:
            company_id: ID da empresa (OBRIGATORIO).
            initial_period: Periodo inicial (YYYY-MM-DD).
            final_period: Periodo final (YYYY-MM-DD).

        Returns:
            Lista de dicts com dados do balancete.
        """
        data = self._get("/trial-balance", params={
            "companyId": company_id,
            "initialPeriod": initial_period,
            "finalPeriod": final_period,
        })
        return data.get("results", data if isinstance(data, list) else [])

    # ── Centros de Custo ───────────────────────────────────────────────

    def list_centros_custo(self, limit: int | None = None) -> list[CentroCusto]:
        """Lista todos os centros de custo.

        Args:
            limit: Limite de resultados (None = todos).

        Returns:
            Lista de CentroCusto.
        """
        return list(self.iter_centros_custo(max_results=limit))

    def iter_centros_custo(self, max_results: int | None = None) -> Iterator[CentroCusto]:
        """Itera sobre centros de custo com paginacao automatica.

        Yields:
            CentroCusto.
        """
        def fetch(offset: int, limit: int) -> dict:
            return self._get("/cost-centers", params={"offset": offset, "limit": limit})

        for item in paginate(fetch, max_results=max_results):
            yield CentroCusto.from_api(item)

    def search_centros_custo(self, nome: str) -> list[CentroCusto]:
        """Busca centros de custo pelo nome.

        Args:
            nome: Nome ou parte do nome.

        Returns:
            Lista de CentroCusto.
        """
        safe = _SAFE_SEARCH.sub("", nome)
        data = self._get("/cost-centers", params={"filter": f"name like '%{safe}%'"})
        results = data.get("results", data if isinstance(data, list) else [])
        return [CentroCusto.from_api(r) for r in results]

    # ── Contas Contabeis ───────────────────────────────────────────────

    def list_contas_contabeis(self, limit: int | None = None) -> list[ContaContabil]:
        """Lista contas contabeis.

        Args:
            limit: Limite de resultados (None = todas).

        Returns:
            Lista de ContaContabil.
        """
        return list(self.iter_contas_contabeis(max_results=limit))

    def iter_contas_contabeis(self, max_results: int | None = None) -> Iterator[ContaContabil]:
        """Itera sobre contas contabeis.

        Yields:
            ContaContabil.
        """
        def fetch(offset: int, limit: int) -> dict:
            return self._get("/accountancy/accounts", params={"offset": offset, "limit": limit})

        for item in paginate(fetch, max_results=max_results):
            yield ContaContabil.from_api(item)

    # ── Plano Financeiro ───────────────────────────────────────────────

    def list_categorias_pagamento(self) -> list[dict]:
        """Lista categorias do plano financeiro.

        Returns:
            Lista de dicts com categorias.
        """
        data = self._get("/payment-categories")
        return data.get("results", data if isinstance(data, list) else [])

    def get_categoria_pagamento(self, category_id: int) -> dict:
        """Busca uma categoria pelo ID.

        Args:
            category_id: ID da categoria.

        Returns:
            Dict com dados da categoria.
        """
        return self._get(f"/payment-categories/{category_id}")

    # ── Titulos por Data de Alteracao (/bills/by-change-date) ─────────

    def list_titulos_por_alteracao(
        self,
        start_date: str | None = None,
        end_date: str | None = None,
        limit: int | None = None,
    ) -> list[Titulo]:
        """Lista titulos filtrados por data de alteracao.

        Args:
            start_date: Data inicio (YYYY-MM-DD). Default: 30 dias atras.
            end_date: Data fim (YYYY-MM-DD). Default: hoje.
            limit: Limite de resultados.

        Returns:
            Lista de Titulo.
        """
        if not start_date:
            start_date = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
        if not end_date:
            end_date = datetime.now().strftime("%Y-%m-%d")

        def fetch(offset: int, lim: int) -> dict:
            return self._get("/bills/by-change-date", params={
                "startDate": start_date,
                "endDate": end_date,
                "offset": offset,
                "limit": lim,
            })

        results = list(paginate(fetch, max_results=limit))
        return [Titulo.from_api(r) for r in results]

    # ── Importar NF-e (/eletronic-invoice-bills POST) ────────────────

    def import_nfe(self, nfe_xml: str) -> dict:
        """Importa titulo a partir de XML de NF-e.

        Args:
            nfe_xml: Conteudo XML da NF-e.

        Returns:
            Resposta da API.
        """
        return self._post("/eletronic-invoice-bills", json_body={"xml": nfe_xml})

    # ── Fluxo de Caixa (/cash-flow) ─────────────────────────────────

    def get_cash_flow(self) -> list[dict]:
        """Busca projecao de fluxo de caixa (real/projetado/comprometido).

        Returns:
            Lista de dicts com dados do fluxo.
        """
        data = self._get("/cash-flow")
        return data.get("results", data if isinstance(data, list) else [])

    # ── Contas Bancarias (/checking-accounts) ────────────────────────

    def list_contas_bancarias(self, limit: int | None = None) -> list[dict]:
        """Lista contas bancarias (contas correntes).

        Args:
            limit: Limite de resultados.

        Returns:
            Lista de dicts com contas bancarias (63 na CONIN).
        """
        params: dict = {}
        if limit:
            params["limit"] = min(limit, 200)
        data = self._get("/checking-accounts", params=params)
        return data.get("results", data if isinstance(data, list) else [])

    # ── Saldos de Contas (/accounts-balances) ────────────────────────

    def get_saldos_contas(self, balance_date: str) -> list[dict]:
        """Busca saldos de contas em uma data especifica.

        Args:
            balance_date: Data do saldo (YYYY-MM-DD, OBRIGATORIO).

        Returns:
            Lista de dicts com saldos.
        """
        data = self._get("/accounts-balances", params={"balanceDate": balance_date})
        return data.get("results", data if isinstance(data, list) else [])
