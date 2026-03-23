"""
sienge.endpoints.contabilidade — Endpoints de Contabilidade (lancamentos, plano de contas, lotes, empresas).
"""

from __future__ import annotations

from datetime import datetime, timedelta
from typing import Iterator

from .base import BaseEndpoints
from ..models.financeiro import ContaContabil, LancamentoContabil
from ..utils import paginate


class ContabilidadeEndpoints(BaseEndpoints):
    """Endpoints de Contabilidade: lancamentos, plano de contas, lotes, empresas."""

    # ── Lancamentos (/accountancy/entries) ───────────────────────────

    def list_lancamentos(
        self,
        company_id: int,
        start_date: str | None = None,
        end_date: str | None = None,
        limit: int | None = None,
    ) -> list[LancamentoContabil]:
        """Lista lancamentos contabeis.

        Args:
            company_id: ID da empresa (OBRIGATORIO).
            start_date: Data inicio (YYYY-MM-DD). Default: 30 dias atras.
            end_date: Data fim (YYYY-MM-DD). Default: hoje.
            limit: Limite de resultados (None = todos).

        Returns:
            Lista de LancamentoContabil.
        """
        return list(self.iter_lancamentos(company_id, start_date, end_date, max_results=limit))

    def iter_lancamentos(
        self,
        company_id: int,
        start_date: str | None = None,
        end_date: str | None = None,
        max_results: int | None = None,
    ) -> Iterator[LancamentoContabil]:
        """Itera sobre lancamentos contabeis com paginacao automatica.

        Args:
            company_id: ID da empresa (OBRIGATORIO).
            start_date: Data inicio (YYYY-MM-DD).
            end_date: Data fim (YYYY-MM-DD).
            max_results: Limite total.

        Yields:
            LancamentoContabil.
        """
        if not start_date:
            start_date = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
        if not end_date:
            end_date = datetime.now().strftime("%Y-%m-%d")

        def fetch(offset: int, limit: int) -> dict:
            return self._get("/accountancy/entries", params={
                "companyId": company_id,
                "startDate": start_date,
                "endDate": end_date,
                "offset": offset,
                "limit": limit,
            })

        for item in paginate(fetch, max_results=max_results):
            yield LancamentoContabil.from_api(item)

    # ── Plano de Contas (/accountancy/accounts) ──────────────────────

    def list_plano_contas(self, limit: int | None = None) -> list[ContaContabil]:
        """Lista contas do plano de contas.

        Args:
            limit: Limite de resultados (None = todas, 8.235 na CONIN).

        Returns:
            Lista de ContaContabil.
        """
        return list(self.iter_plano_contas(max_results=limit))

    def iter_plano_contas(self, max_results: int | None = None) -> Iterator[ContaContabil]:
        """Itera sobre contas do plano de contas.

        Yields:
            ContaContabil.
        """
        def fetch(offset: int, limit: int) -> dict:
            return self._get("/accountancy/accounts", params={"offset": offset, "limit": limit})

        for item in paginate(fetch, max_results=max_results):
            yield ContaContabil.from_api(item)

    # ── Lotes Contabeis (/batch) ─────────────────────────────────────

    def list_lotes(
        self,
        company_id: int,
        start_date: str | None = None,
        end_date: str | None = None,
        limit: int | None = None,
    ) -> list[dict]:
        """Lista lotes contabeis.

        Args:
            company_id: ID da empresa (OBRIGATORIO).
            start_date: Data inicio (YYYY-MM-DD). Default: 30 dias atras.
            end_date: Data fim (YYYY-MM-DD). Default: hoje.
            limit: Limite de resultados.

        Returns:
            Lista de dicts com lotes.
        """
        if not start_date:
            start_date = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
        if not end_date:
            end_date = datetime.now().strftime("%Y-%m-%d")

        params: dict = {
            "companyId": company_id,
            "startDate": start_date,
            "endDate": end_date,
        }
        if limit:
            params["limit"] = min(limit, 200)
        data = self._get("/batch", params=params)
        return data.get("results", data if isinstance(data, list) else [])

    # ── Fechamento Contabil (/closingaccountancy) ────────────────────

    def get_fechamento(self, month_year: str) -> dict:
        """Busca status de fechamento contabil de um periodo.

        NOTA: Path correto e /closingaccountancy (NAO /accountancy/closing).

        Args:
            month_year: Periodo no formato YYYY-MM (OBRIGATORIO).

        Returns:
            Dict com dados do fechamento.
        """
        return self._get("/closingaccountancy", params={"monthYear": month_year})

    # ── Empresas (/companies) ────────────────────────────────────────

    def list_empresas(self, limit: int | None = None) -> list[dict]:
        """Lista empresas cadastradas no Sienge.

        Args:
            limit: Limite de resultados.

        Returns:
            Lista de dicts com empresas (10 na CONIN).
        """
        params: dict = {}
        if limit:
            params["limit"] = min(limit, 200)
        data = self._get("/companies", params=params)
        return data.get("results", data if isinstance(data, list) else [])
