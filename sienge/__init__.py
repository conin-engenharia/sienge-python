"""
sienge — Cliente Python para a API REST do Sienge (ERP de construcao civil).

Primeiro wrapper Python do mundo para o Sienge.

Uso:
    from sienge import SiengeClient

    client = SiengeClient("conin", "usuario", "senha")

    # Engenharia
    obras = client.engenharia.list_obras()
    progresso = client.engenharia.get_progresso(123)

    # Financeiro
    titulos = client.financeiro.list_titulos()
    centros = client.financeiro.list_centros_custo()

    # Suprimentos
    pedidos = client.suprimentos.list_pedidos(building_id=123)

    # Credores
    fornecedores = client.credores.list_credores()

    # Contabilidade
    lancamentos = client.contabilidade.list_lancamentos(company_id=1)

    # Bulk (plano Ultimate)
    dados = client.bulk.export_income("2026-01-01")
"""

__version__ = "0.1.0"

from .client import SiengeClient
from .exceptions import (
    SiengeError,
    AuthError,
    NotFoundError,
    RateLimitError,
    MaintenanceError,
    ValidationError,
)

__all__ = [
    "SiengeClient",
    "SiengeError",
    "AuthError",
    "NotFoundError",
    "RateLimitError",
    "MaintenanceError",
    "ValidationError",
]
