"""Testes automatizados simples (biblioteca padrão unittest) para main.py."""

import io
import unittest
from contextlib import redirect_stdout
from decimal import Decimal
from unittest.mock import patch

import main


def executar(entradas):
    """Roda main.main() com entradas simuladas e devolve o texto impresso."""
    saida = io.StringIO()
    with patch("builtins.input", side_effect=entradas):
        with redirect_stdout(saida):
            main.main()
    return saida.getvalue()


def rodar_funcao(funcao, entradas, *args):
    """Roda uma função isolada com entradas simuladas; devolve (retorno, texto)."""
    saida = io.StringIO()
    with patch("builtins.input", side_effect=entradas):
        with redirect_stdout(saida):
            retorno = funcao(*args)
    return retorno, saida.getvalue()


class TestConversaoDeValores(unittest.TestCase):
    def test_aceita_ponto_e_virgula(self):
        self.assertEqual(main.converter_valor("50,75")[0], Decimal("50.75"))
        self.assertEqual(main.converter_valor("50.75")[0], Decimal("50.75"))

    def test_recusa_texto_vazio_e_letras(self):
        self.assertIsNone(main.converter_valor("")[0])
        self.assertIsNone(main.converter_valor("   ")[0])
        self.assertIsNone(main.converter_valor("abc")[0])
        self.assertIsNone(main.converter_valor("NaN")[0])

    def test_recusa_mais_de_duas_casas(self):
        valor, erro = main.converter_valor("10,555")
        self.assertIsNone(valor)
        self.assertIsNotNone(erro)


class TestOperacoes(unittest.TestCase):
    def test_deposito_valido(self):
        historico = []
        saldo, _ = rodar_funcao(main.depositar, ["50"], Decimal("100.00"), historico)
        self.assertEqual(saldo, Decimal("150.00"))
        self.assertEqual(len(historico), 1)
        self.assertEqual(historico[0]["saldo_apos"], Decimal("150.00"))

    def test_deposito_zero_e_negativo(self):
        for entrada in ["0", "-10"]:
            historico = []
            saldo, _ = rodar_funcao(main.depositar, [entrada], Decimal("100.00"), historico)
            self.assertEqual(saldo, Decimal("100.00"))
            self.assertEqual(historico, [])

    def test_saque_valido(self):
        historico = []
        saldo, _ = rodar_funcao(main.sacar, ["30,50"], Decimal("100.00"), historico)
        self.assertEqual(saldo, Decimal("69.50"))
        self.assertEqual(historico[0]["tipo"], "Saque")

    def test_saque_maior_que_saldo(self):
        historico = []
        saldo, texto = rodar_funcao(main.sacar, ["500"], Decimal("100.00"), historico)
        self.assertEqual(saldo, Decimal("100.00"))
        self.assertEqual(historico, [])
        self.assertIn("Saldo insuficiente", texto)

    def test_saque_igual_ao_saldo_deixa_zero(self):
        historico = []
        saldo, _ = rodar_funcao(main.sacar, ["100"], Decimal("100.00"), historico)
        self.assertEqual(saldo, Decimal("0.00"))

    def test_saque_negativo_e_texto(self):
        for entrada in ["-5", "abc", ""]:
            historico = []
            saldo, _ = rodar_funcao(main.sacar, [entrada], Decimal("100.00"), historico)
            self.assertEqual(saldo, Decimal("100.00"))
            self.assertEqual(historico, [])

    def test_soma_de_centavos_sem_erro_de_ponto_flutuante(self):
        historico = []
        saldo = Decimal("0.00")
        saldo, _ = rodar_funcao(main.depositar, ["0,10"], saldo, historico)
        saldo, _ = rodar_funcao(main.depositar, ["0,20"], saldo, historico)
        self.assertEqual(saldo, Decimal("0.30"))


class TestFluxoDoMenu(unittest.TestCase):
    def test_consultar_saldo_inicial_e_sair(self):
        texto = executar(["1", "5"])
        self.assertIn("R$ 100,00", texto)
        self.assertIn("Encerrando", texto)

    def test_opcao_inexistente_e_vazia(self):
        texto = executar(["9", "", "abc", "5"])
        self.assertEqual(texto.count("Opção inválida"), 3)

    def test_varias_operacoes_e_extrato(self):
        # depósito 50 -> 150; saque 30 -> 120; saque 500 (recusado); extrato; sair
        texto = executar(["2", "50", "3", "30", "3", "500", "4", "5"])
        self.assertIn("Depósito", texto)
        self.assertIn("saldo após: R$ 150,00", texto)
        self.assertIn("saldo após: R$ 120,00", texto)
        self.assertIn("Saldo atual: R$ 120,00", texto)
        self.assertIn("Saldo insuficiente", texto)

    def test_extrato_vazio(self):
        texto = executar(["4", "5"])
        self.assertIn("Nenhuma operação realizada ainda.", texto)


class TestFormatacao(unittest.TestCase):
    def test_formato_brasileiro(self):
        self.assertEqual(main.formatar_moeda(Decimal("1234.5")), "R$ 1.234,50")
        self.assertEqual(main.formatar_moeda(Decimal("0")), "R$ 0,00")


if __name__ == "__main__":
    unittest.main()