"""
sienge.models — Dataclasses tipadas para os recursos da API Sienge.
"""

from .obra import Obra, ObraProgresso
from .financeiro import Titulo, TituloInstallment, CentroCusto, ContaContabil, LancamentoContabil
from .suprimentos import PedidoCompra, ItemPedido, SolicitacaoCompra, ItemSolicitacao
from .comercial import Cliente, Contrato, Unidade
from .credores import Credor

__all__ = [
    "Obra", "ObraProgresso",
    "Titulo", "TituloInstallment", "CentroCusto", "ContaContabil", "LancamentoContabil",
    "PedidoCompra", "ItemPedido", "SolicitacaoCompra", "ItemSolicitacao",
    "Cliente", "Contrato", "Unidade",
    "Credor",
]
