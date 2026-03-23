#!/usr/bin/env python3
"""
Exemplo: Listar pedidos de compra de uma obra.

Uso:
    export SIENGE_SUBDOMAIN=sua-empresa
    export SIENGE_USERNAME=usuario-api
    export SIENGE_PASSWORD=senha-api

    python pedido_compra.py [building_id]
"""

import sys
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from sienge import SiengeClient, SiengeError


def main():
    client = SiengeClient.from_env()

    building_id = int(sys.argv[1]) if len(sys.argv) > 1 else None

    if building_id:
        print(f"Pedidos de compra da obra #{building_id}")
    else:
        print("Todos os pedidos de compra")
    print("=" * 50)

    pedidos = client.suprimentos.list_pedidos(building_id=building_id, limit=50)

    if not pedidos:
        print("Nenhum pedido encontrado.")
        return

    for p in pedidos:
        print(f"\nPedido {p.numero_formatado} (ID: {p.id})")
        print(f"  Fornecedor ID: {p.fornecedor_id}")
        print(f"  Status: {p.status}")
        print(f"  Autorizado: {p.autorizado}")

    print(f"\n{'=' * 50}")
    print(f"Total: {len(pedidos)} pedidos")


if __name__ == "__main__":
    try:
        main()
    except SiengeError as e:
        print(f"Erro Sienge: {e}")
        sys.exit(1)
