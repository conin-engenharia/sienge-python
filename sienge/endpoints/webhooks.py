"""
sienge.endpoints.webhooks — Endpoints de Webhooks (gerenciar notificacoes).

Eventos suportados:
    CUSTOMER_CREATED, CUSTOMER_UPDATED, CUSTOMER_REMOVED,
    CUSTOMER_DISABLED, CUSTOMER_ENABLED,
    SALES_CONTRACT_CREATED, SALES_CONTRACT_UPDATED, SALES_CONTRACT_REMOVED,
    SALES_CONTRACT_ISSUED, SALES_CONTRACT_CANCELED
"""

from __future__ import annotations

from .base import BaseEndpoints


class WebhooksEndpoints(BaseEndpoints):
    """Endpoints de Webhooks: cadastro e gerenciamento de notificacoes."""

    def list_hooks(self) -> list[dict]:
        """Lista webhooks registrados.

        Returns:
            Lista de dicts com webhooks.
        """
        data = self._get("/hooks")
        return data.get("results", data if isinstance(data, list) else [])

    def create_hook(self, event_type: str, url: str) -> dict:
        """Registra um novo webhook.

        Args:
            event_type: Tipo de evento (ex: "CUSTOMER_CREATED").
            url: URL de callback.

        Returns:
            Resposta da API com ID do webhook criado.
        """
        return self._post("/hooks", json_body={
            "eventType": event_type,
            "url": url,
        })

    def delete_hook(self, hook_id: int) -> dict:
        """Remove um webhook registrado.

        Args:
            hook_id: ID do webhook.

        Returns:
            Resposta da API.
        """
        return self._delete(f"/hooks/{hook_id}")
