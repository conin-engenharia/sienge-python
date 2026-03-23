#!/usr/bin/env python3
"""
Exemplo: Consultar obra no Sienge.

Uso:
    export SIENGE_SUBDOMAIN=sua-empresa
    export SIENGE_USERNAME=usuario-api
    export SIENGE_PASSWORD=senha-api

    python consultar_obra.py "Recofarma"
"""

import sys
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from sienge import SiengeClient, SiengeError


def main():
    client = SiengeClient.from_env()
    nome = sys.argv[1] if len(sys.argv) > 1 else ""

    if nome:
        print(f"Buscando obra: {nome}")
        obras = client.engenharia.search_obra(nome)
    else:
        print("Listando todas as obras...")
        obras = client.engenharia.list_obras(limit=20)

    if not obras:
        print("Nenhuma obra encontrada.")
        return

    for obra in obras:
        print(f"\n--- {obra.nome} (ID: {obra.id}) ---")
        print(f"  Tipo: {obra.tipo}")
        if obra.endereco:
            print(f"  Endereco: {obra.endereco}")


if __name__ == "__main__":
    try:
        main()
    except SiengeError as e:
        print(f"Erro Sienge: {e}")
        sys.exit(1)
