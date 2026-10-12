"""
Simulador de Caixa Eletrônico (Conta Bancária) - Atividade AV1
Disciplina: Paradigmas de Programação
Professor: Rodrigo Medeiros Costa

AVISO: este programa é uma SIMULAÇÃO ACADÊMICA. Ele não tem conexão com
contas bancárias reais, não usa dados reais e não guarda nada em disco.

Paradigma: imperativo. O programa é uma sequência de instruções que altera
o estado (as variáveis `saldo` e `historico`) por meio de atribuições,
decisões (if/elif/else), repetição (while) e funções.

Regras principais:
- Saldo inicial: R$ 100,00 (constante SALDO_INICIAL).
- Valores monetários usam Decimal (evita erros de ponto flutuante).
- Valores com mais de duas casas decimais são RECUSADOS (não são arredondados).
- Depósito e saque exigem valor maior que zero.
- Saque maior que o saldo é recusado, então o saldo nunca fica negativo.
- Operação inválida não altera o saldo nem o histórico.
"""

import re
from decimal import Decimal

# Saldo com que a simulação começa (documentado também no README).
SALDO_INICIAL = Decimal("100.00")

# Menor unidade monetária: dois dígitos depois da vírgula (centavos).
CENTAVO = Decimal("0.01")

# Aceita sinal opcional, dígitos e, opcionalmente, vírgula ou ponto com dígitos.
PADRAO_VALOR = re.compile(r"^[+-]?[0-9]+([.,][0-9]+)?$")


def formatar_moeda(valor):
    """Converte um Decimal em texto no formato brasileiro, ex.: R$ 1.234,56."""
    texto = f"{valor:,.2f}"  # formato americano: 1,234.56
    texto = texto.replace(",", "X").replace(".", ",").replace("X", ".")
    return "R$ " + texto


def exibir_menu():
    """Mostra as opções disponíveis ao usuário."""
    print()
    print("=" * 40)
    print("      CAIXA ELETRÔNICO (SIMULAÇÃO)")
    print("=" * 40)
    print("1 - Consultar saldo")
    print("2 - Realizar depósito")
    print("3 - Realizar saque")
    print("4 - Extrato")
    print("5 - Sair")
    print("-" * 40)


def converter_valor(texto):
    """
    Tenta converter um texto em Decimal com duas casas decimais.
    Retorna (valor, None) se der certo ou (None, mensagem_de_erro) se falhar.
    """
    texto = texto.strip()

    if texto == "":
        return None, "Entrada vazia. Digite um valor, por exemplo 50 ou 50,75."

    if not PADRAO_VALOR.match(texto):
        return None, "Valor inválido. Use apenas números, por exemplo 50 ou 50,75."

    texto = texto.replace(",", ".")  # aceita vírgula como separador decimal

    if "." in texto:
        casas_decimais = len(texto.split(".")[1])
        if casas_decimais > 2:
            return None, "Use no máximo duas casas decimais (centavos)."

    valor = Decimal(texto).quantize(CENTAVO)
    return valor, None


def ler_valor(rotulo):
    """
    Pede um valor ao usuário e valida.
    Retorna um Decimal positivo ou None se a entrada for inválida.
    """
    texto = input(f"Informe o valor do {rotulo}: R$ ")
    valor, erro = converter_valor(texto)

    if erro is not None:
        print(erro)
        return None

    if valor <= 0:
        print("O valor deve ser maior que zero.")
        return None

    return valor


def registrar_operacao(historico, tipo, valor, saldo_apos):
    """Acrescenta uma operação concluída ao histórico (altera a lista)."""
    operacao = {"tipo": tipo, "valor": valor, "saldo_apos": saldo_apos}
    historico.append(operacao)


def consultar_saldo(saldo):
    """Mostra o saldo atual."""
    print(f"Saldo atual: {formatar_moeda(saldo)}")


def depositar(saldo, historico):
    """Realiza um depósito e retorna o novo saldo."""
    valor = ler_valor("depósito")

    if valor is None:
        print("Depósito não realizado. O saldo foi mantido.")
        return saldo

    saldo = saldo + valor  # atribuição: o estado do programa muda aqui
    registrar_operacao(historico, "Depósito", valor, saldo)
    print(f"Depósito de {formatar_moeda(valor)} realizado com sucesso.")
    print(f"Novo saldo: {formatar_moeda(saldo)}")
    return saldo


def sacar(saldo, historico):
    """Realiza um saque (se houver saldo suficiente) e retorna o novo saldo."""
    valor = ler_valor("saque")

    if valor is None:
        print("Saque não realizado. O saldo foi mantido.")
        return saldo

    if valor > saldo:
        print("Saldo insuficiente. Saque não realizado.")
        print(f"Saldo disponível: {formatar_moeda(saldo)}")
        return saldo

    saldo = saldo - valor  # só chega aqui se o saque for válido
    registrar_operacao(historico, "Saque", valor, saldo)
    print(f"Saque de {formatar_moeda(valor)} realizado com sucesso.")
    print(f"Novo saldo: {formatar_moeda(saldo)}")
    return saldo


def exibir_extrato(historico, saldo):
    """Mostra todas as operações concluídas e o saldo após cada uma."""
    print()
    print("----------------- EXTRATO -----------------")
    print(f"Saldo inicial: {formatar_moeda(SALDO_INICIAL)}")

    if len(historico) == 0:
        print("Nenhuma operação realizada ainda.")
    else:
        numero = 1
        for operacao in historico:
            print(
                f"{numero:02d}. {operacao['tipo']:<9} "
                f"{formatar_moeda(operacao['valor']):>14} | "
                f"saldo após: {formatar_moeda(operacao['saldo_apos'])}"
            )
            numero = numero + 1

    print("-------------------------------------------")
    print(f"Saldo atual: {formatar_moeda(saldo)}")


def main():
    """Função principal: controla o fluxo do programa com um laço while."""
    saldo = SALDO_INICIAL  # estado inicial
    historico = []         # lista vazia de operações
    continuar = True

    print("AVISO: esta é uma simulação acadêmica, sem conexão com contas reais.")
    print(f"Saldo inicial da simulação: {formatar_moeda(saldo)}")

    while continuar:
        exibir_menu()
        opcao = input("Escolha uma opção (1-5): ").strip()

        if opcao == "1":
            consultar_saldo(saldo)
        elif opcao == "2":
            saldo = depositar(saldo, historico)
        elif opcao == "3":
            saldo = sacar(saldo, historico)
        elif opcao == "4":
            exibir_extrato(historico, saldo)
        elif opcao == "5":
            print("Encerrando o simulador. Até logo!")
            continuar = False  # faz o laço terminar
        else:
            print("Opção inválida. Digite um número de 1 a 5.")


if __name__ == "__main__":
    main()