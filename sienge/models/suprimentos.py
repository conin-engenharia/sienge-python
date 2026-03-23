"""
sienge.models.suprimentos — Dataclasses para Suprimentos (pedidos de compra).

Campos reais da API /purchase-orders:
id, formattedPurchaseOrderId, status, consistent, authorized,
disapproved, deliveryLate, supplierId, buildingId
"""

from dataclasses import dataclass, field
from typing import Any


@dataclass
class PedidoCompra:
    """Pedido de compra no Sienge. Mapeado de GET /purchase-orders."""
    id: int
    numero_formatado: str = ""
    status: str = ""
    consistente: str = ""
    autorizado: bool = False
    reprovado: bool = False
    entrega_atrasada: bool = False
    fornecedor_id: int | None = None
    building_id: int | None = None  # referencia centro de custo
    extras: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_api(cls, data: dict) -> "PedidoCompra":
        return cls(
            id=data.get("id", 0),
            numero_formatado=data.get("formattedPurchaseOrderId", str(data.get("number", ""))),
            status=data.get("status", ""),
            consistente=data.get("consistent", ""),
            autorizado=data.get("authorized", False),
            reprovado=data.get("disapproved", False),
            entrega_atrasada=data.get("deliveryLate", False),
            fornecedor_id=data.get("supplierId"),
            building_id=data.get("buildingId"),
            extras={k: v for k, v in data.items() if k not in {
                "id", "formattedPurchaseOrderId", "number", "status",
                "consistent", "authorized", "disapproved", "deliveryLate",
                "supplierId", "buildingId",
            }},
        )


@dataclass
class ItemPedido:
    """Item de um pedido de compra."""
    id: int
    descricao: str = ""
    quantidade: float = 0.0
    unidade: str = ""
    valor_unitario: float = 0.0
    valor_total: float = 0.0
    insumo_id: int | None = None
    extras: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_api(cls, data: dict) -> "ItemPedido":
        return cls(
            id=data.get("id", 0),
            descricao=data.get("description", data.get("resourceDescription", "")),
            quantidade=data.get("quantity", 0.0),
            unidade=data.get("unit", data.get("measurementUnit", "")),
            valor_unitario=data.get("unitPrice", data.get("unitValue", 0.0)),
            valor_total=data.get("totalPrice", data.get("totalValue", 0.0)),
            insumo_id=data.get("resourceId"),
            extras={k: v for k, v in data.items() if k not in {
                "id", "description", "resourceDescription", "quantity",
                "unit", "measurementUnit", "unitPrice", "unitValue",
                "totalPrice", "totalValue", "resourceId",
            }},
        )


@dataclass
class ItemSolicitacao:
    """Item de uma solicitacao de compra."""
    id: int
    descricao: str = ""
    quantidade: float = 0.0
    unidade: str = ""
    insumo_id: int | None = None
    extras: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_api(cls, data: dict) -> "ItemSolicitacao":
        return cls(
            id=data.get("id", 0),
            descricao=data.get("description", data.get("resourceDescription", "")),
            quantidade=data.get("quantity", 0.0),
            unidade=data.get("unit", data.get("measurementUnit", "")),
            insumo_id=data.get("resourceId"),
            extras={k: v for k, v in data.items() if k not in {
                "id", "description", "resourceDescription", "quantity",
                "unit", "measurementUnit", "resourceId",
            }},
        )


@dataclass
class SolicitacaoCompra:
    """Solicitacao de compra no Sienge.

    NOTA: GET /purchase-requests retorna 405 na CONIN (nao disponivel).
    """
    id: int
    numero: str = ""
    data: str | None = None
    solicitante: str = ""
    obra_id: int | None = None
    centro_custo_id: int | None = None
    status: str = ""
    observacao: str = ""
    itens: list[ItemSolicitacao] = field(default_factory=list)
    extras: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_api(cls, data: dict) -> "SolicitacaoCompra":
        itens_raw = data.get("items", [])
        return cls(
            id=data.get("id", 0),
            numero=str(data.get("number", data.get("requestNumber", ""))),
            data=data.get("date", data.get("requestDate")),
            solicitante=data.get("requester", data.get("requestedBy", "")),
            obra_id=data.get("buildingId"),
            centro_custo_id=data.get("costCenterId"),
            status=data.get("status", ""),
            observacao=data.get("observation", data.get("notes", "")),
            itens=[ItemSolicitacao.from_api(i) for i in itens_raw] if itens_raw else [],
            extras={k: v for k, v in data.items() if k not in {
                "id", "number", "requestNumber", "date", "requestDate",
                "requester", "requestedBy", "buildingId", "costCenterId",
                "status", "observation", "notes", "items",
            }},
        )
