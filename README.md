<p align="center">
  <img src="assets/logo-conin.png" alt="CONIN Engenharia" width="400">
</p>

<h1 align="center">sienge-python</h1>

<p align="center">
  <strong>Primeiro cliente Python para a API REST do Sienge</strong> — o ERP mais usado na construcao civil brasileira.<br>
  <em>The first Python client for the Sienge REST API — Brazil's leading construction ERP.</em>
</p>

<p align="center">
  <a href="https://github.com/conin-engenharia/sienge-python/actions"><img src="https://github.com/conin-engenharia/sienge-python/actions/workflows/ci.yml/badge.svg" alt="CI"></a>
  <a href="https://github.com/conin-engenharia/sienge-python/blob/main/LICENSE"><img src="https://img.shields.io/github/license/conin-engenharia/sienge-python" alt="License"></a>
</p>

---

## O que e este projeto?

O Sienge e o sistema de gestao (ERP) mais utilizado por construtoras no Brasil. Ele gerencia obras, financeiro, compras, contabilidade e muito mais. O Sienge oferece uma **API** — uma forma de sistemas externos acessarem esses dados de forma automatizada.

Porem, ate hoje, nao existia uma biblioteca pronta em Python para consumir essa API. Cada empresa que precisava integrar com o Sienge tinha que escrever o codigo de conexao do zero.

O **sienge-python** resolve isso. E uma biblioteca que encapsula toda a comunicacao com a API do Sienge, permitindo que desenvolvedores acessem dados de obras, financeiro, compras e outros modulos com poucas linhas de codigo — sem se preocupar com autenticacao, paginacao, limites de requisicao ou tratamento de erros.

### Na pratica

**Sem esta biblioteca**, para listar os titulos a pagar de uma empresa, um desenvolvedor precisaria escrever ~50 linhas de codigo lidando com autenticacao HTTP, paginacao manual, controle de limite de requisicoes e tratamento de erros.

**Com esta biblioteca:**

```python
from sienge import SiengeClient

client = SiengeClient("sua-empresa", "usuario-api", "senha-api")
titulos = client.financeiro.list_titulos(start_date="2026-01-01")

for t in titulos:
    print(f"{t.numero_documento}: R$ {t.valor_total:,.2f}")
```

Toda a complexidade tecnica fica encapsulada — o desenvolvedor foca no que importa.

---

## Instalacao / Installation

```bash
pip install sienge-python
```

Ou direto do repositorio / Or from source:

```bash
pip install git+https://github.com/conin-engenharia/sienge-python.git
```

## Uso Rapido / Quick Start

```python
from sienge import SiengeClient

client = SiengeClient("sua-empresa", "usuario-api", "senha-api")

# Listar obras / List buildings
obras = client.engenharia.list_obras()
for obra in obras:
    print(f"{obra.nome} — {obra.tipo}")

# Titulos a pagar / Bills
titulos = client.financeiro.list_titulos(start_date="2026-01-01")
total = sum(t.valor_total for t in titulos)
print(f"Total a pagar: R$ {total:,.2f}")

# Centros de custo / Cost centers
centros = client.financeiro.search_centros_custo("Obra Centro")

# Pedidos de compra / Purchase orders
pedidos = client.suprimentos.list_pedidos(building_id=123)

# Fornecedores / Suppliers
fornecedores = client.credores.list_credores()

# Contabilidade / Accounting
lancamentos = client.contabilidade.list_lancamentos(company_id=1, start_date="2026-01-01")
```

### Via variaveis de ambiente / Environment variables

```bash
export SIENGE_SUBDOMAIN=sua-empresa
export SIENGE_USERNAME=usuario-api
export SIENGE_PASSWORD=senha-api
```

```python
from sienge import SiengeClient
client = SiengeClient.from_env()
```

## Modulos Disponiveis / Available Modules

| Modulo | Acesso | Funcionalidades |
|--------|--------|-----------------|
| **Engenharia** | `client.engenharia` | Obras, progresso, orcamento, diarios, canteiros, bases de custo |
| **Financeiro** | `client.financeiro` | Titulos, fluxo de caixa, contas bancarias, saldos, centros de custo, NF-e |
| **Suprimentos** | `client.suprimentos` | Pedidos de compra (CRUD), notas fiscais, contratos, estoque, cotacoes |
| **Comercial** | `client.comercial` | Clientes, contratos, unidades, mapa imobiliario, tipos de imovel |
| **Contabilidade** | `client.contabilidade` | Lancamentos, plano de contas, lotes, fechamento, empresas |
| **Credores** | `client.credores` | Fornecedores, info bancaria |
| **Patrimonio** | `client.patrimonio` | Ativos fixos, moveis, alugueis |
| **Webhooks** | `client.webhooks` | Cadastro e gerenciamento de notificacoes (10 eventos) |
| **Tabelas** | `client.tabelas` | Cidades, profissoes, marcas, unidades de medida, indexadores |
| **Bulk Data** | `client.bulk` | 12 endpoints de exportacao em massa (plano Ultimate) |

## Features

- **Type hints completos** — Dataclasses tipadas para todos os recursos
- **Rate limiting automatico** — 200 req/min REST, 20 req/min Bulk
- **Retry com backoff exponencial** — Resiliencia contra erros transientes
- **Paginacao automatica** — Iterators que buscam todas as paginas
- **Tratamento de erros** — Excecoes especificas: `AuthError`, `RateLimitError`, `NotFoundError`
- **Thread-safe** — Rate limiter com locks

## Excecoes / Exceptions

```python
from sienge import SiengeError, AuthError, RateLimitError, NotFoundError

try:
    obra = client.engenharia.get_obra(999)
except AuthError:
    print("Credenciais invalidas ou recurso nao liberado")
except NotFoundError:
    print("Obra nao encontrada")
except RateLimitError as e:
    print(f"Rate limit — retry em {e.retry_after}s")
except SiengeError as e:
    print(f"Erro: {e}")
```

## Paginacao Automatica / Auto-pagination

```python
# Itera sobre TODOS os centros de custo (3000+) automaticamente
for cc in client.financeiro.iter_centros_custo():
    print(f"{cc.codigo}: {cc.nome}")

# Ou limitar resultados
primeiros_50 = client.financeiro.list_centros_custo(limit=50)
```

## Pre-requisitos / Prerequisites

- Python 3.10+
- Conta de cliente **Data Center** do Sienge
- Usuario de API criado no painel Sienge (Menu > APIs e Conectores > Usuarios de API)
- Recursos necessarios liberados para o usuario (aba "Autorizacoes")

## Planos de API / API Plans

| Plano | Limite REST/dia | Limite Bulk/dia |
|-------|-----------------|-----------------|
| Free | 100 | 10 |
| Start | 1.000 | 100 |
| Essential | 5.000 | 500 |
| Enterprise | 10.000 | 1.000 |
| Ultimate | 75.000 | 7.500 |

## Contribuindo / Contributing

1. Fork o repositorio
2. Crie uma branch (`git checkout -b feature/minha-feature`)
3. Commit (`git commit -m 'Adiciona minha feature'`)
4. Push (`git push origin feature/minha-feature`)
5. Abra um Pull Request

## Licenca / License

MIT License — veja [LICENSE](LICENSE).

## Sobre / About

Desenvolvido pela [CONIN Engenharia](https://conin-ia.com.br) para automatizar operacoes de construcao civil com o Sienge.

*Built by CONIN Engenharia to automate construction operations with Sienge ERP.*
