# Simulador de Caixa Eletrônico em Python

> **AVISO:** este programa é uma **simulação acadêmica**. Ele não tem conexão com contas bancárias reais, não usa dados reais e não armazena informações permanentemente.

## 1. Identificação da disciplina

- **Curso:** Ciência da Computação, Universidade da Amazônia (UNAMA)
- **Disciplina:** Paradigmas de Programação
- **Atividade:** Atividade Avaliativa AV1 (Resolução de problema com paradigma imperativo)

## 2. Professor

Rodrigo Medeiros Costa

## 3. Identificação do aluno / integrantes

| Nome | Matrícula | Usuário no GitHub |
|------|-----------|-------------------|
| [PREENCHER] | [PREENCHER] | [PREENCHER] |
| [PREENCHER, se houver] | [PREENCHER] | [PREENCHER] |
| [PREENCHER, se houver] | [PREENCHER] | [PREENCHER] |

## 4. Descrição do problema

Um caixa eletrônico precisa permitir que o usuário consulte o saldo, deposite, saque e acompanhe as operações realizadas, sem nunca deixar o saldo negativo e sem aceitar entradas inválidas. O problema é implementar essa lógica de forma clara, usando o paradigma imperativo: uma sequência de instruções que altera o estado do programa (saldo e histórico) ao longo da execução.

## 5. Objetivo do simulador

Aplicar, em um problema de baixa complexidade, os conceitos do paradigma imperativo: sequência de instruções, variáveis, atribuições, decisões, repetições e funções, com validação de entradas e alteração explícita de estado.

## 6. Funcionalidades implementadas

1. **Consultar saldo:** mostra o saldo atual.
2. **Realizar depósito:** valida o valor e atualiza o saldo.
3. **Realizar saque:** valida o valor e verifica se há saldo suficiente antes de atualizar o saldo.
4. **Extrato:** lista as operações concluídas (tipo, valor e saldo após cada uma), o saldo inicial e o saldo atual.
5. **Sair:** encerra o laço principal e o programa.

## 7. Entradas, regras de negócio e resultados esperados

**Entradas**

- Opção do menu: `1`, `2`, `3`, `4` ou `5`.
- Valor monetário (depósito ou saque): número com vírgula ou ponto (ex.: `50`, `50,75`, `50.75`).

**Regras de negócio**

- Saldo inicial: **R$ 100,00** (constante `SALDO_INICIAL` em `main.py`).
- Depósitos e saques devem ter valor **maior que zero**.
- Saque maior que o saldo disponível é **recusado**, então o saldo nunca fica negativo.
- Entradas vazias, textos, opções inexistentes e valores negativos ou zero são **recusados**.
- Uma operação inválida **não altera** o saldo nem o histórico.
- Somente operações **concluídas** entram no histórico.
- Valores monetários usam `Decimal` (biblioteca padrão), evitando erros de ponto flutuante (como `0.1 + 0.2 = 0.30000000000000004`).
- **Casas decimais:** o programa aceita **no máximo duas casas decimais** (centavos). Valores com mais de duas casas (ex.: `10,555`) são **recusados**, não arredondados.
- Não há separador de milhar: digite `1000`, não `1.000`.

**Resultados esperados**

- Mensagens claras em português para cada situação (sucesso ou erro).
- O saldo exibido no extrato após cada operação corresponde ao saldo do sistema naquele momento.
- O programa permite várias operações seguidas, até o usuário escolher a opção 5.

## 8. Tecnologias e requisitos

- Python 3.8 ou superior (somente biblioteca padrão: `decimal`, `re`, `unittest`).
- Terminal (Prompt de Comando, PowerShell ou outro).
- Nenhuma biblioteca externa, banco de dados ou interface gráfica.

## 9. Como executar o programa (passo a passo)

1. Instale o Python 3 (https://www.python.org/downloads/). No Windows, marque **"Add Python to PATH"** durante a instalação.
2. Baixe ou clone este repositório.
3. Abra o terminal na pasta do projeto (`simulador-caixa-eletronico`).
4. Execute:

```bash
python main.py
```

No Windows, se `python` não funcionar, use `py main.py`.

## 10. Exemplos de utilização

Trecho de uma sessão real (saldo inicial R$ 100,00):

```text
Escolha uma opção (1-5): 2
Informe o valor do depósito: R$ 50
Depósito de R$ 50,00 realizado com sucesso.
Novo saldo: R$ 150,00

Escolha uma opção (1-5): 2
Informe o valor do depósito: R$ 0
O valor deve ser maior que zero.
Depósito não realizado. O saldo foi mantido.

Escolha uma opção (1-5): 3
Informe o valor do saque: R$ 30
Saque de R$ 30,00 realizado com sucesso.
Novo saldo: R$ 120,00

Escolha uma opção (1-5): 3
Informe o valor do saque: R$ 500
Saldo insuficiente. Saque não realizado.
Saldo disponível: R$ 120,00

Escolha uma opção (1-5): 4

----------------- EXTRATO -----------------
Saldo inicial: R$ 100,00
01. Depósito        R$ 50,00 | saldo após: R$ 150,00
02. Saque           R$ 30,00 | saldo após: R$ 120,00
-------------------------------------------
Saldo atual: R$ 120,00

Escolha uma opção (1-5): 5
Encerrando o simulador. Até logo!
```

## 11. O paradigma imperativo neste projeto

No paradigma imperativo, o programa é escrito como uma **sequência de comandos** que modificam o **estado** (dados em memória) passo a passo. Aqui, o estado é formado por duas variáveis em `main()`: `saldo` (um `Decimal`) e `historico` (uma lista). Cada operação concluída muda esse estado por atribuição, e o fluxo é controlado por decisões e repetições.

## 12. Onde estão os elementos imperativos no código

| Conceito | Exemplo em `main.py` |
|----------|----------------------|
| Sequência de instruções | Em `main()`: `saldo = SALDO_INICIAL`, depois `historico = []`, depois `continuar = True`, depois os `print` de aviso |
| Variáveis | `saldo`, `historico`, `continuar`, `opcao`, `valor` |
| Atribuição (mudança de estado) | `saldo = saldo + valor` (em `depositar`) e `saldo = saldo - valor` (em `sacar`) |
| Decisão | `if valor > saldo:` (em `sacar`); `if/elif/else` do menu em `main()` |
| Repetição | `while continuar:` (em `main()`) e `for operacao in historico:` (em `exibir_extrato`) |
| Funções | `exibir_menu`, `converter_valor`, `ler_valor`, `registrar_operacao`, `consultar_saldo`, `depositar`, `sacar`, `exibir_extrato`, `formatar_moeda`, `main` |
| Entrada e saída | `input(...)` e `print(...)` |
| Alteração de estado do histórico | `historico.append(operacao)` (em `registrar_operacao`) |

## 13. Como executar os testes

Os testes usam apenas a biblioteca padrão (`unittest`) e não dependem de serviços externos. Na pasta do projeto:

```bash
python -m unittest -v
```

Os testes cobrem: saldo inicial, depósito válido, depósito zero/negativo, saque válido, saque acima do saldo, saque negativo, texto no lugar de número, opção inválida no menu, extrato após várias operações, saldo correto no extrato e encerramento pela opção 5.

**Resultado dos testes na minha máquina:** [PREENCHER após executar]

## 14. Reflexão breve

Resumo (detalhes em [`docs/reflexao.md`](docs/reflexao.md)):

- **Decisões:** usar `Decimal` para dinheiro; recusar, e não arredondar, valores com mais de duas casas; manter `saldo` e `historico` como variáveis de `main()` passadas às funções.
- **Dificuldades e melhorias:** [PREENCHER com suas dificuldades reais]. Melhorias possíveis: salvar o histórico em arquivo, aceitar separador de milhar, criar limite de saque.

## 15. Contribuição dos integrantes

| Integrante | Contribuição |
|------------|--------------|
| [PREENCHER] | [PREENCHER] |
| [PREENCHER, se houver] | [PREENCHER] |
| [PREENCHER, se houver] | [PREENCHER] |

## 16. Vídeo de demonstração

Link do vídeo: **[PREENCHER após gravar e publicar o vídeo]**

(Instruções de gravação e publicação em [`video/README.md`](video/README.md).)

## 17. Limitações

- Os dados não são salvos: ao fechar o programa, saldo e histórico voltam ao estado inicial.
- Não há autenticação, transferências, PIX ou integração com serviços externos (fora do escopo da atividade).
- Não aceita separador de milhar nem notação científica.

## 18. Aviso

Este projeto é uma **simulação acadêmica** desenvolvida para a disciplina de Paradigmas de Programação. Não possui qualquer conexão com bancos ou contas reais.