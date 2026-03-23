"""
sienge.models.comercial — Dataclasses para Comercial (clientes, contratos, unidades).
"""

from dataclasses import dataclass, field
from typing import Any


@dataclass
class Cliente:
    """Cliente no Sienge."""
    id: int
    nome: str = ""
    cpf_cnpj: str = ""
    email: str = ""
    telefone: str = ""
    endereco: str = ""
    cidade: str = ""
    estado: str = ""
    tipo: str = ""  # PF ou PJ
    extras: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_api(cls, data: dict) -> "Cliente":
        return cls(
            id=data.get("id", 0),
            nome=data.get("name", ""),
            cpf_cnpj=data.get("cpfCnpj", data.get("document", "")),
            email=data.get("email", ""),
            telefone=data.get("phone", data.get("telephone", "")),
            endereco=data.get("address", ""),
            cidade=data.get("city", ""),
            estado=data.get("state", ""),
            tipo=data.get("type", data.get("personType", "")),
            extras={k: v for k, v in data.items() if k not in {
                "id", "name", "cpfCnpj", "document", "email",
                "phone", "telephone", "address", "city", "state",
                "type", "personType",
            }},
        )


@dataclass
class Contrato:
    """Contrato de venda no Sienge."""
    id: int
    numero: str = ""
    cliente_id: int | None = None
    obra_id: int | None = None
    unidade_id: int | None = None
    valor: float = 0.0
    data_contrato: str | None = None
    status: str = ""
    extras: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_api(cls, data: dict) -> "Contrato":
        return cls(
            id=data.get("id", 0),
            numero=str(data.get("number", data.get("contractNumber", ""))),
            cliente_id=data.get("clientId", data.get("customerId")),
            obra_id=data.get("buildingId"),
            unidade_id=data.get("unitId"),
            valor=data.get("value", data.get("totalAmount", 0.0)),
            data_contrato=data.get("contractDate", data.get("date")),
            status=data.get("status", ""),
            extras={k: v for k, v in data.items() if k not in {
                "id", "number", "contractNumber", "clientId", "customerId",
                "buildingId", "unitId", "value", "totalAmount",
                "contractDate", "date", "status",
            }},
        )


@dataclass
class Unidade:
    """Unidade imobiliaria no Sienge."""
    id: int
    nome: str = ""
    obra_id: int | None = None
    bloco: str = ""
    andar: str = ""
    tipo: str = ""
    area: float = 0.0
    status: str = ""
    extras: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_api(cls, data: dict) -> "Unidade":
        return cls(
            id=data.get("id", 0),
            nome=data.get("name", ""),
            obra_id=data.get("buildingId"),
            bloco=data.get("block", data.get("tower", "")),
            andar=data.get("floor", ""),
            tipo=data.get("type", data.get("unitType", "")),
            area=data.get("area", data.get("privateArea", 0.0)),
            status=data.get("status", ""),
            extras={k: v for k, v in data.items() if k not in {
                "id", "name", "buildingId", "block", "tower",
                "floor", "type", "unitType", "area", "privateArea", "status",
            }},
        )
