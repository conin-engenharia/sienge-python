"""
sienge.models.credores — Dataclasses para Credores (fornecedores).

Campos reais da API /creditors:
id, name, tradeName, cpf, cnpj, supplier, broker, employee, active, stateRegistrationNumber
"""

from dataclasses import dataclass, field
from typing import Any


@dataclass
class Credor:
    """Credor/fornecedor no Sienge. Mapeado de GET /creditors."""
    id: int
    nome: str = ""
    nome_fantasia: str = ""
    cpf: str = ""
    cnpj: str = ""
    fornecedor: bool = False
    corretor: bool = False
    funcionario: bool = False
    ativo: bool = True
    inscricao_estadual: str = ""
    extras: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_api(cls, data: dict) -> "Credor":
        return cls(
            id=data.get("id", data.get("code", 0)),
            nome=data.get("name", ""),
            nome_fantasia=data.get("tradeName", "") or "",
            cpf=data.get("cpf", "") or "",
            cnpj=data.get("cnpj", "") or "",
            fornecedor=data.get("supplier", "N") == "S",
            corretor=data.get("broker", "N") == "S",
            funcionario=data.get("employee", "N") == "S",
            ativo=data.get("active", True),
            inscricao_estadual=data.get("stateRegistrationNumber", "") or "",
            extras={k: v for k, v in data.items() if k not in {
                "id", "code", "name", "tradeName", "cpf", "cnpj",
                "supplier", "broker", "employee", "active",
                "stateRegistrationNumber",
            }},
        )

    @property
    def documento(self) -> str:
        """Retorna CPF ou CNPJ (o que estiver preenchido)."""
        return self.cnpj or self.cpf or ""
