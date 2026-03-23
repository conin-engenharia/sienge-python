"""
sienge.exceptions — Excecoes customizadas para o cliente Sienge.
"""


class SiengeError(Exception):
    """Erro base para operacoes do Sienge."""

    def __init__(self, message: str, status_code: int | None = None, response_body: str = ""):
        self.status_code = status_code
        self.response_body = response_body
        super().__init__(message)


class AuthError(SiengeError):
    """Credenciais invalidas ou recurso nao autorizado (401)."""
    pass


class NotFoundError(SiengeError):
    """Recurso ou endpoint nao encontrado (404)."""
    pass


class RateLimitError(SiengeError):
    """Limite de requisicoes atingido (429)."""

    def __init__(self, message: str = "Rate limit atingido", retry_after: int = 60, **kwargs):
        self.retry_after = retry_after
        super().__init__(message, status_code=429, **kwargs)


class MaintenanceError(SiengeError):
    """Sienge em manutencao (503). Horario: 00:00-06:30 UTC."""
    pass


class ValidationError(SiengeError):
    """Parametros invalidos (400)."""
    pass
