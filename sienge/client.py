"""
sienge.client — Cliente principal para a API REST do Sienge.

Uso:
    from sienge import SiengeClient

    client = SiengeClient("conin", "usuario", "senha")
    obras = client.engenharia.list_obras()
    titulos = client.financeiro.list_titulos()
"""

import logging
import os

import requests

from .auth import SiengeAuth
from .rate_limiter import get_rest_limiter, get_bulk_limiter, RateLimiter
from .endpoints.engenharia import EngenhariaEndpoints
from .endpoints.financeiro import FinanceiroEndpoints
from .endpoints.suprimentos import SuprimentosEndpoints
from .endpoints.comercial import ComercialEndpoints
from .endpoints.contabilidade import ContabilidadeEndpoints
from .endpoints.credores import CredoresEndpoints
from .endpoints.bulk import BulkEndpoints
from .endpoints.patrimonio import PatrimonioEndpoints
from .endpoints.webhooks import WebhooksEndpoints
from .endpoints.tabelas import TabelasEndpoints

logger = logging.getLogger("sienge")

DEFAULT_TIMEOUT = 30
DEFAULT_MAX_RETRIES = 3


class SiengeClient:
    """Cliente para a API REST do Sienge.

    Uso basico:
        client = SiengeClient("conin", "usuario", "senha")
        obras = client.engenharia.list_obras()

    Ou via variaveis de ambiente:
        # Defina SIENGE_SUBDOMAIN, SIENGE_USERNAME, SIENGE_PASSWORD
        client = SiengeClient.from_env()

    Args:
        subdomain: Subdominio da empresa no Sienge (ex: "conin").
        username: Usuario de API (criado no painel Sienge).
        password: Senha do usuario de API.
        timeout: Timeout em segundos para cada requisicao.
        max_retries: Numero maximo de retentativas em erro transiente.
    """

    def __init__(
        self,
        subdomain: str,
        username: str,
        password: str,
        timeout: int = DEFAULT_TIMEOUT,
        max_retries: int = DEFAULT_MAX_RETRIES,
    ):
        self._subdomain = subdomain
        self._auth = SiengeAuth(username, password)
        self._timeout = timeout
        self._max_retries = max_retries

        # URLs
        self._base_url = f"https://api.sienge.com.br/{subdomain}/public/api/v1"
        self._bulk_url = f"https://api.sienge.com.br/{subdomain}/public/api/bulk-data/v1"

        # Session com auth persistente
        self._session = requests.Session()
        self._session.auth = self._auth.get_auth()
        self._session.headers.update({"Accept": "application/json"})

        # Rate limiters
        self._rest_limiter: RateLimiter = get_rest_limiter()
        self._bulk_limiter: RateLimiter = get_bulk_limiter()

        # Endpoint groups
        self.engenharia = EngenhariaEndpoints(self)
        self.financeiro = FinanceiroEndpoints(self)
        self.suprimentos = SuprimentosEndpoints(self)
        self.comercial = ComercialEndpoints(self)
        self.contabilidade = ContabilidadeEndpoints(self)
        self.credores = CredoresEndpoints(self)
        self.bulk = BulkEndpoints(self)
        self.patrimonio = PatrimonioEndpoints(self)
        self.webhooks = WebhooksEndpoints(self)
        self.tabelas = TabelasEndpoints(self)

        logger.info("SiengeClient inicializado para '%s' (user: %s)", subdomain, username)

    @classmethod
    def from_env(
        cls,
        subdomain_var: str = "SIENGE_SUBDOMAIN",
        username_var: str = "SIENGE_USERNAME",
        password_var: str = "SIENGE_PASSWORD",
        **kwargs,
    ) -> "SiengeClient":
        """Cria cliente a partir de variaveis de ambiente.

        Args:
            subdomain_var: Nome da env var para subdominio.
            username_var: Nome da env var para usuario.
            password_var: Nome da env var para senha.
            **kwargs: Argumentos extras passados ao construtor.

        Returns:
            SiengeClient configurado.

        Raises:
            ValueError: Se variaveis de ambiente estao faltando.
        """
        subdomain = os.getenv(subdomain_var, "")
        username = os.getenv(username_var, "")
        password = os.getenv(password_var, "")

        if not subdomain:
            raise ValueError(f"Variavel de ambiente '{subdomain_var}' nao definida.")
        if not username:
            raise ValueError(f"Variavel de ambiente '{username_var}' nao definida.")
        if not password:
            raise ValueError(f"Variavel de ambiente '{password_var}' nao definida.")

        return cls(subdomain, username, password, **kwargs)

    @property
    def subdomain(self) -> str:
        """Subdominio da empresa no Sienge."""
        return self._subdomain

    @property
    def base_url(self) -> str:
        """URL base da API REST."""
        return self._base_url

    @property
    def bulk_url(self) -> str:
        """URL base da API Bulk."""
        return self._bulk_url

    def __repr__(self) -> str:
        return f"SiengeClient(subdomain='{self._subdomain}', user='{self._auth.username}')"
