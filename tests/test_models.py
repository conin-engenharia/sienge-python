"""
Testes para os models do Sienge.
"""

import pytest
from sienge.models.obra import Obra, ObraProgresso
from sienge.models.financeiro import CentroCusto, Titulo, TituloInstallment, ContaContabil, LancamentoContabil
from sienge.models.suprimentos import PedidoCompra, SolicitacaoCompra
from sienge.models.comercial import Cliente, Contrato, Unidade
from sienge.models.credores import Credor


class TestObra:
    def test_from_api_basic(self):
        data = {"id": 1, "name": "Recofarma", "type": "Em andamento"}
        obra = Obra.from_api(data)
        assert obra.id == 1
        assert obra.nome == "Recofarma"
        assert obra.tipo == "Em andamento"

    def test_from_api_full(self):
        data = {
            "id": 42,
            "name": "VDP",
            "type": "Ativa",
            "address": "Rua A, 123",
            "cnpj": "12.345.678/0001-99",
            "commercialName": "VDP Comercial",
            "creationDate": "2025-06-01",
            "extraField": "valor_extra",
        }
        obra = Obra.from_api(data)
        assert obra.id == 42
        assert obra.endereco == "Rua A, 123"
        assert obra.nome_comercial == "VDP Comercial"
        assert obra.extras["extraField"] == "valor_extra"


class TestObraProgresso:
    def test_from_api(self):
        data = {"percentage": 72.5, "planned": 75.0, "executed": 72.5, "deviation": -2.5}
        prog = ObraProgresso.from_api(123, data)
        assert prog.building_id == 123
        assert prog.percentual == 72.5
        assert prog.desvio == -2.5


class TestCentroCusto:
    def test_from_api(self):
        data = {"id": 100, "name": "CC Recofarma", "code": "001", "status": "Ativo", "idCompany": 1}
        cc = CentroCusto.from_api(data)
        assert cc.id == 100
        assert cc.nome == "CC Recofarma"
        assert cc.empresa_id == 1


class TestTitulo:
    def test_from_api(self):
        data = {
            "id": 186856,
            "creditorId": 42,
            "documentNumber": "TX PHP-2381",
            "totalInvoiceAmount": 133.03,
            "status": "S",
            "issueDate": "2026-01-15",
            "installmentsNumber": 1,
        }
        titulo = Titulo.from_api(data)
        assert titulo.id == 186856
        assert titulo.valor_total == 133.03
        assert titulo.credor_id == 42
        assert titulo.num_parcelas == 1


class TestTituloInstallment:
    def test_from_api(self):
        data = {"id": 1, "installmentNumber": 1, "amount": 500.00, "dueDate": "2026-03-15", "status": "P"}
        parcela = TituloInstallment.from_api(data)
        assert parcela.valor == 500.00
        assert parcela.data_vencimento == "2026-03-15"


class TestContaContabil:
    def test_from_api(self):
        data = {"id": 5, "uniqueNumber": "1.1.01", "name": "Caixa Geral", "accountType": "A", "companyId": 1}
        conta = ContaContabil.from_api(data)
        assert conta.numero_unico == "1.1.01"
        assert conta.nome == "Caixa Geral"


class TestLancamentoContabil:
    def test_from_api(self):
        data = {
            "id": 999,
            "debitAccountId": 10,
            "creditAccountId": 20,
            "date": "2026-02-28",
            "amount": 1500.00,
            "description": "Pagamento fornecedor",
            "companyId": 1,
        }
        lanc = LancamentoContabil.from_api(data)
        assert lanc.valor == 1500.00
        assert lanc.conta_debito_id == 10


class TestPedidoCompra:
    def test_from_api(self):
        data = {
            "id": 50,
            "formattedPurchaseOrderId": "PC-001",
            "supplierId": 10,
            "status": "Aprovado",
            "authorized": True,
        }
        pedido = PedidoCompra.from_api(data)
        assert pedido.numero_formatado == "PC-001"
        assert pedido.fornecedor_id == 10
        assert pedido.autorizado is True


class TestSolicitacaoCompra:
    def test_from_api(self):
        data = {
            "id": 30,
            "number": "SC-010",
            "requester": "Joao",
            "buildingId": 1,
            "status": "Pendente",
        }
        sol = SolicitacaoCompra.from_api(data)
        assert sol.solicitante == "Joao"
        assert sol.obra_id == 1


class TestCliente:
    def test_from_api(self):
        data = {"id": 1, "name": "Petrobras", "cpfCnpj": "33.000.167/0001-01", "type": "PJ"}
        cli = Cliente.from_api(data)
        assert cli.nome == "Petrobras"
        assert cli.tipo == "PJ"


class TestContrato:
    def test_from_api(self):
        data = {"id": 5, "number": "CT-001", "clientId": 1, "buildingId": 42, "value": 1200000.00}
        contrato = Contrato.from_api(data)
        assert contrato.valor == 1200000.00


class TestUnidade:
    def test_from_api(self):
        data = {"id": 10, "name": "Apt 101", "buildingId": 42, "block": "A", "floor": "1", "area": 85.5}
        unidade = Unidade.from_api(data)
        assert unidade.bloco == "A"
        assert unidade.area == 85.5


class TestCredor:
    def test_from_api(self):
        data = {"id": 100, "name": "Cimento Nassara", "cpfCnpj": "12.345.678/0001-99", "active": True}
        credor = Credor.from_api(data)
        assert credor.nome == "Cimento Nassara"
        assert credor.ativo is True


# ── Testes de Imports dos novos modulos ──────────────────────────────

class TestNewModuleImports:
    def test_import_patrimonio(self):
        from sienge.endpoints.patrimonio import PatrimonioEndpoints
        assert PatrimonioEndpoints is not None

    def test_import_webhooks(self):
        from sienge.endpoints.webhooks import WebhooksEndpoints
        assert WebhooksEndpoints is not None

    def test_import_tabelas(self):
        from sienge.endpoints.tabelas import TabelasEndpoints
        assert TabelasEndpoints is not None

    def test_client_has_new_modules(self):
        from sienge.client import SiengeClient
        # Verifica que os atributos existem no __init__
        import inspect
        src = inspect.getsource(SiengeClient.__init__)
        assert "patrimonio" in src
        assert "webhooks" in src
        assert "tabelas" in src


class TestNewEndpointMethods:
    """Verifica que os novos metodos existem nos modulos."""

    def test_financeiro_novos_metodos(self):
        from sienge.endpoints.financeiro import FinanceiroEndpoints
        assert hasattr(FinanceiroEndpoints, "list_titulos_por_alteracao")
        assert hasattr(FinanceiroEndpoints, "import_nfe")
        assert hasattr(FinanceiroEndpoints, "get_cash_flow")
        assert hasattr(FinanceiroEndpoints, "list_contas_bancarias")
        assert hasattr(FinanceiroEndpoints, "get_saldos_contas")

    def test_contabilidade_novos_metodos(self):
        from sienge.endpoints.contabilidade import ContabilidadeEndpoints
        assert hasattr(ContabilidadeEndpoints, "list_plano_contas")
        assert hasattr(ContabilidadeEndpoints, "iter_plano_contas")
        assert hasattr(ContabilidadeEndpoints, "list_lotes")
        assert hasattr(ContabilidadeEndpoints, "get_fechamento")
        assert hasattr(ContabilidadeEndpoints, "list_empresas")

    def test_engenharia_novos_metodos(self):
        from sienge.endpoints.engenharia import EngenhariaEndpoints
        assert hasattr(EngenhariaEndpoints, "list_tipos_evento_diario")
        assert hasattr(EngenhariaEndpoints, "list_progresso_obra")
        assert hasattr(EngenhariaEndpoints, "list_canteiros")
        assert hasattr(EngenhariaEndpoints, "list_bases_custo")

    def test_suprimentos_novos_metodos(self):
        from sienge.endpoints.suprimentos import SuprimentosEndpoints
        assert hasattr(SuprimentosEndpoints, "create_pedido")
        assert hasattr(SuprimentosEndpoints, "update_item_status")

    def test_comercial_novos_metodos(self):
        from sienge.endpoints.comercial import ComercialEndpoints
        assert hasattr(ComercialEndpoints, "list_tipos_cliente")
        assert hasattr(ComercialEndpoints, "list_caracteristicas_unidades")
        assert hasattr(ComercialEndpoints, "list_situacoes_unidades")
        assert hasattr(ComercialEndpoints, "list_tipos_imovel")
        assert hasattr(ComercialEndpoints, "get_mapa_imobiliario")

    def test_bulk_novos_metodos(self):
        from sienge.endpoints.bulk import BulkEndpoints
        assert hasattr(BulkEndpoints, "export_customer_extract")
        assert hasattr(BulkEndpoints, "export_customer_debt")
        assert hasattr(BulkEndpoints, "export_defaulters")
        assert hasattr(BulkEndpoints, "export_building_resources")
        assert hasattr(BulkEndpoints, "export_business_budget")
        assert hasattr(BulkEndpoints, "export_account_balance")
        assert hasattr(BulkEndpoints, "export_account_cc_balance")
        assert hasattr(BulkEndpoints, "export_invoice_items")

    def test_patrimonio_metodos(self):
        from sienge.endpoints.patrimonio import PatrimonioEndpoints
        assert hasattr(PatrimonioEndpoints, "list_ativos_fixos")
        assert hasattr(PatrimonioEndpoints, "list_ativos_moveis")
        assert hasattr(PatrimonioEndpoints, "list_alugueis")

    def test_webhooks_metodos(self):
        from sienge.endpoints.webhooks import WebhooksEndpoints
        assert hasattr(WebhooksEndpoints, "list_hooks")
        assert hasattr(WebhooksEndpoints, "create_hook")
        assert hasattr(WebhooksEndpoints, "delete_hook")

    def test_tabelas_metodos(self):
        from sienge.endpoints.tabelas import TabelasEndpoints
        assert hasattr(TabelasEndpoints, "list_cidades")
        assert hasattr(TabelasEndpoints, "list_estado_civil")
        assert hasattr(TabelasEndpoints, "list_profissoes")
        assert hasattr(TabelasEndpoints, "list_marcas")
        assert hasattr(TabelasEndpoints, "list_unidades_medida")
        assert hasattr(TabelasEndpoints, "list_grupos_recurso")
        assert hasattr(TabelasEndpoints, "list_grupos_servico")
        assert hasattr(TabelasEndpoints, "list_indexadores")
        assert hasattr(TabelasEndpoints, "list_condicoes_pagamento")

    def test_base_has_patch(self):
        from sienge.endpoints.base import BaseEndpoints
        assert hasattr(BaseEndpoints, "_patch")
