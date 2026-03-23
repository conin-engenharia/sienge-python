#!/usr/bin/env python3
"""
Exemplo: Relatorio financeiro — titulos a pagar.

Uso:
    export SIENGE_SUBDOMAIN=sua-empresa
    export SIENGE_USERNAME=usuario-api
    export SIENGE_PASSWORD=senha-api

    python relatorio_financeiro.py [YYYY-MM-DD] [YYYY-MM-DD]
"""

import sys
from datetime import datetime, timedelta
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from sienge import SiengeClient, SiengeError
from sienge.utils import format_currency


def main():
    client = SiengeClient.from_env()

    end_date = sys.argv[2] if len(sys.argv) > 2 else datetime.now().strftime("%Y-%m-%d")
    start_date = sys.argv[1] if len(sys.argv) > 1 else (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")

    print(f"Relatorio Financeiro: {start_date} a {end_date}")
    print("=" * 50)

    titulos = client.financeiro.list_titulos(start_date=start_date, end_date=end_date)
    print(f"\nTitulos a pagar: {len(titulos)}")

    total = sum(t.valor_total for t in titulos)
    print(f"Valor total: {format_currency(total)}")

    # Agrupar por status
    por_status: dict[str, list] = {}
    for t in titulos:
        s = t.status or "?"
        por_status.setdefault(s, []).append(t)

    for status, grupo in sorted(por_status.items()):
        subtotal = sum(t.valor_total for t in grupo)
        print(f"  Status '{status}': {len(grupo)} titulos — {format_currency(subtotal)}")

    # Top 10 maiores
    print(f"\nTop 10 maiores titulos:")
    for t in sorted(titulos, key=lambda x: x.valor_total, reverse=True)[:10]:
        print(f"  {t.numero_documento}: {format_currency(t.valor_total)} (credor #{t.credor_id})")


if __name__ == "__main__":
    try:
        main()
    except SiengeError as e:
        print(f"Erro Sienge: {e}")
        sys.exit(1)
