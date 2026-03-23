"""
sienge.models.obra — Dataclasses para Engenharia (empreendimentos).

No Sienge, "obras" sao empreendimentos (GET /enterprises).
Campos reais da API: id, name, commercialName, cnpj, type, adress, creationDate
"""

from dataclasses import dataclass, field
from typing import Any


@dataclass
class Obra:
    """Representa um empreendimento (obra/projeto) no Sienge.

    Mapeado de GET /enterprises.
    """
    id: int
    nome: str = ""
    nome_comercial: str = ""
    cnpj: str = ""
    tipo: str = ""
    endereco: str = ""
    data_criacao: str | None = None
    extras: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_api(cls, data: dict) -> "Obra":
        """Cria instancia a partir da resposta da API /enterprises."""
        return cls(
            id=data.get("id", 0),
            nome=data.get("name", data.get("nome", "")),
            nome_comercial=data.get("commercialName", "") or "",
            cnpj=data.get("cnpj", "") or "",
            tipo=data.get("type", data.get("tipo", "")),
            endereco=data.get("adress", data.get("address", data.get("endereco", ""))) or "",
            data_criacao=data.get("creationDate", data.get("dataCriacao")),
            extras={k: v for k, v in data.items() if k not in {
                "id", "name", "nome", "commercialName", "cnpj",
                "type", "tipo", "adress", "address", "endereco",
                "creationDate", "dataCriacao",
            }},
        )


@dataclass
class ObraProgresso:
    """Progresso de execucao de uma obra.

    NOTA: O endpoint /buildings/{id}/progress NAO EXISTE na API Sienge.
    Este model e mantido para futuro uso caso o Sienge adicione o endpoint.
    """
    building_id: int
    percentual: float = 0.0
    previsto: float = 0.0
    executado: float = 0.0
    desvio: float = 0.0
    data_referencia: str | None = None
    extras: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_api(cls, building_id: int, data: dict) -> "ObraProgresso":
        """Cria instancia a partir da resposta da API."""
        return cls(
            building_id=building_id,
            percentual=data.get("percentage", data.get("percentual", 0.0)),
            previsto=data.get("planned", data.get("previsto", 0.0)),
            executado=data.get("executed", data.get("executado", 0.0)),
            desvio=data.get("deviation", data.get("desvio", 0.0)),
            data_referencia=data.get("referenceDate", data.get("dataReferencia")),
            extras={k: v for k, v in data.items() if k not in {
                "percentage", "percentual", "planned", "previsto",
                "executed", "executado", "deviation", "desvio",
                "referenceDate", "dataReferencia",
            }},
        )
