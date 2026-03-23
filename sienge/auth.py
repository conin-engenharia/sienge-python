"""
sienge.auth — Autenticacao HTTP Basic Auth para a API Sienge.
"""

from requests.auth import HTTPBasicAuth


class SiengeAuth:
    """Gerencia credenciais e autenticacao para a API Sienge."""

    def __init__(self, username: str, password: str):
        if not username or not password:
            raise ValueError("Username e password sao obrigatorios para autenticacao no Sienge.")
        self._username = username
        self._password = password

    def get_auth(self) -> HTTPBasicAuth:
        """Retorna objeto HTTPBasicAuth para uso com requests."""
        return HTTPBasicAuth(self._username, self._password)

    @property
    def username(self) -> str:
        return self._username
