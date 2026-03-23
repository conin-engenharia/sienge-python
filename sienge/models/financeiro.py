"""
sienge.models.financeiro — Dataclasses para Financeiro.
"""

from dataclasses import dataclass, field
from typing import Any


@dataclass
class CentroCusto:
    """Centro de custo (geralmente vinculado a uma obra)."""
    id: int
    nome: str = ""
    codigo: str = ""
    status: str = ""
    empresa_id: int | None = None
    cnpj: str = ""
    extras: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_api(cls, data: dict) -> "CentroCusto":
        return cls(
            id=data.get("id", 0),
            nome=data.get("name", ""),
            codigo=data.get("code", ""),
            status=data.get("status", ""),
            empresa_id=data.get("idCompany"),
            cnpj=data.get("cnpj", ""),
            extras={k: v for k, v in data.items() if k not in {
                "id", "name", "code", "status", "idCompany", "cnpj",
            }},
        )


@dataclass
class Titulo:
    """Titulo a pagar (bill) no Sienge."""
    id: int
    devedor_id: int | None = None
    credor_id: int | None = None
    documento_id: str = ""
    numero_documento: str = ""
    data_emissao: str | None = None
    num_parcelas: int = 0
    valor_total: float = 0.0
    notas: str = ""
    desconto: float = 0.0
    status: str = ""
    origem_id: int | None = None
    usuario_registro: str = ""
    links: list[dict] = field(default_factory=list)
    extras: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_api(cls, data: dict) -> "Titulo":
        return cls(
            id=data.get("id", 0),
            devedor_id=data.get("debtorId"),
            credor_id=data.get("creditorId"),
            documento_id=str(data.get("documentIdentificationId", "")),
            numero_documento=data.get("documentNumber", ""),
            data_emissao=data.get("issueDate"),
            num_parcelas=data.get("installmentsNumber", 0),
            valor_total=data.get("totalInvoiceAmount", 0.0),
            notas=data.get("notes", ""),
            desconto=data.get("discount", 0.0),
            status=data.get("status", ""),
            origem_id=data.get("originId"),
            usuario_registro=data.get("registeredBy", ""),
            links=data.get("links", []),
            extras={k: v for k, v in data.items() if k not in {
                "id", "debtorId", "creditorId", "documentIdentificationId",
                "documentNumber", "issueDate", "installmentsNumber",
                "totalInvoiceAmount", "notes", "discount", "status",
                "originId", "registeredBy", "links",
            }},
        )


@dataclass
class TituloInstallment:
    """Parcela de um titulo a pagar."""
    id: int
    numero_parcela: int = 0
    valor: float = 0.0
    data_vencimento: str | None = None
    data_pagamento: str | None = None
    status: str = ""
    extras: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_api(cls, data: dict) -> "TituloInstallment":
        return cls(
            id=data.get("id", 0),
            numero_parcela=data.get("installmentNumber", 0),
            valor=data.get("amount", data.get("value", 0.0)),
            data_vencimento=data.get("dueDate"),
            data_pagamento=data.get("paymentDate"),
            status=data.get("status", ""),
            extras={k: v for k, v in data.items() if k not in {
                "id", "installmentNumber", "amount", "value",
                "dueDate", "paymentDate", "status",
            }},
        )


@dataclass
class ContaContabil:
    """Conta contabil do plano de contas."""
    id: int
    numero_unico: str = ""
    nome: str = ""
    tipo: str = ""
    empresa_id: int | None = None
    extras: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_api(cls, data: dict) -> "ContaContabil":
        return cls(
            id=data.get("id", 0),
            numero_unico=data.get("uniqueNumber", ""),
            nome=data.get("name", ""),
            tipo=data.get("accountType", ""),
            empresa_id=data.get("companyId"),
            extras={k: v for k, v in data.items() if k not in {
                "id", "uniqueNumber", "name", "accountType", "companyId",
            }},
        )


@dataclass
class LancamentoContabil:
    """Lancamento contabil (accounting entry)."""
    id: int
    conta_debito_id: int | None = None
    conta_credito_id: int | None = None
    data: str | None = None
    valor: float = 0.0
    descricao: str = ""
    evento_id: int | None = None
    lote_id: int | None = None
    lote_tipo: str = ""
    empresa_id: int | None = None
    tipo: str = ""
    credor_codigo: str = ""
    cliente_codigo: str = ""
    documento_id: str = ""
    conciliado: bool = False
    origem: str = ""
    origem_descricao: str = ""
    extras: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_api(cls, data: dict) -> "LancamentoContabil":
        return cls(
            id=data.get("id", 0),
            conta_debito_id=data.get("debitAccountId"),
            conta_credito_id=data.get("creditAccountId"),
            data=data.get("date"),
            valor=data.get("amount", 0.0),
            descricao=data.get("description", ""),
            evento_id=data.get("eventId"),
            lote_id=data.get("entryBatchId"),
            lote_tipo=data.get("entryBatchType", ""),
            empresa_id=data.get("companyId"),
            tipo=data.get("entryType", ""),
            credor_codigo=str(data.get("creditorCode", "")),
            cliente_codigo=str(data.get("clientCode", "")),
            documento_id=str(data.get("documentId", "")),
            conciliado=data.get("conciliated", False),
            origem=data.get("origin", ""),
            origem_descricao=data.get("originDescription", ""),
            extras={k: v for k, v in data.items() if k not in {
                "id", "debitAccountId", "creditAccountId", "date", "amount",
                "description", "eventId", "entryBatchId", "entryBatchType",
                "companyId", "entryType", "creditorCode", "clientCode",
                "documentId", "conciliated", "origin", "originDescription",
            }},
        )
