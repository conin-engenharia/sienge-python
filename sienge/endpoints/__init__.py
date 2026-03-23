"""
sienge.endpoints — Modulos de endpoints agrupados por area funcional.
"""

from .engenharia import EngenhariaEndpoints
from .financeiro import FinanceiroEndpoints
from .suprimentos import SuprimentosEndpoints
from .comercial import ComercialEndpoints
from .contabilidade import ContabilidadeEndpoints
from .credores import CredoresEndpoints
from .bulk import BulkEndpoints
from .patrimonio import PatrimonioEndpoints
from .webhooks import WebhooksEndpoints
from .tabelas import TabelasEndpoints

__all__ = [
    "EngenhariaEndpoints",
    "FinanceiroEndpoints",
    "SuprimentosEndpoints",
    "ComercialEndpoints",
    "ContabilidadeEndpoints",
    "CredoresEndpoints",
    "BulkEndpoints",
    "PatrimonioEndpoints",
    "WebhooksEndpoints",
    "TabelasEndpoints",
]
