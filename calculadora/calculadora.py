# --- Documentação do Código ---
# Este programa é uma calculadora aprimorada que permite realizar múltiplas operações
# sequencialmente. Ele demonstra o uso de funções para modularizar o código,
# loops para repetição e manipulação de fluxos de decisão.

def adicionar(x, y):
    """Realiza a operação de adição."""
    return x + y

def subtrair(x, y):
    """Realiza a operação de subtração."""
    return x - y

def multiplicar(x, y):
    """Realiza a operação de multiplicação."""
    return x * y

def dividir(x, y):
    """Realiza a operação de divisão, com tratamento para divisão por zero."""
    if y == 0:
        return "Erro: Não é possível dividir por zero!"
    else:
        return x / y

def calculadora_avancada():
    """
    Função principal da calculadora avançada.
    Gerencia o fluxo de operações, entradas e saídas.
    """
    print("--- Calculadora Avançada em Python ---")
    
    # Variável para controlar se a calculadora deve continuar executando
    continuar_calculando = True
    resultado_anterior = None # Armazena o resultado da operação anterior

    while continuar_calculando:
        # Se houver um resultado anterior, pergunta se o usuário quer usá-lo
        if resultado_anterior is not None:
            print(f"\nResultado anterior: {resultado_anterior}")
            usar_anterior = input("Deseja usar o resultado anterior como primeiro número? (s/n): ").lower()
            if usar_anterior == 's':
                num1 = resultado_anterior
            else:
                while True:
                    try:
                        num1 = float(input("Digite o primeiro número: "))
                        break
                    except ValueError:
                        print("Entrada inválida. Por favor, digite apenas números.")
        else:
            # Se não há resultado anterior, pede o primeiro número normalmente
            while True:
                try:
                    num1 = float(input("Digite o primeiro número: "))
                    break
                except ValueError:
                    print("Entrada inválida. Por favor, digite apenas números.")

        print("\nEscolha a operação:")
        print("1. Adição      (+)")
        print("2. Subtração   (-)")
        print("3. Multiplicação(*)")
        print("4. Divisão     (/)")
        print("--------------------")

        # Loop para garantir uma escolha de operação válida
        while True:
            escolha = input("Digite o número da operação (1/2/3/4): ")
            if escolha in ('1', '2', '3', '4'):
                break
            else:
                print("Opção inválida. Por favor, digite 1, 2, 3 ou 4.")

        # Pede o segundo número para a operação atual
        while True:
            try:
                num2 = float(input("Digite o segundo número: "))
                break
            except ValueError:
                print("Entrada inválida. Por favor, digite apenas números.")

        # Realiza a operação e exibe o resultado
        if escolha == '1':
            resultado = adicionar(num1, num2)
            print(f"{num1} + {num2} = {resultado}")
        elif escolha == '2':
            resultado = subtrair(num1, num2)
            print(f"{num1} - {num2} = {resultado}")
        elif escolha == '3':
            resultado = multiplicar(num1, num2)
            print(f"{num1} * {num2} = {resultado}")
        elif escolha == '4':
            resultado = dividir(num1, num2)
            # O tratamento de erro para divisão por zero já está na função dividir()
            if isinstance(resultado, str) and "Erro" in resultado:
                print(resultado)
                resultado_anterior = None # Não armazena erro como resultado anterior
            else:
                print(f"{num1} / {num2} = {resultado}")
        
        # Armazena o resultado para a próxima iteração, se não for um erro
        if not (isinstance(resultado, str) and "Erro" in resultado):
            resultado_anterior = resultado
        else:
            resultado_anterior = None # Reseta se houve erro

        # Pergunta ao usuário se deseja continuar
        while True:
            proxima_acao = input("\nDeseja fazer outra operação?\nDigite 'c' para continuar com o resultado,\n'n' para iniciar um novo cálculo, ou 's' para sair: ").lower()
            if proxima_acao == 's':
                continuar_calculando = False
                print("Obrigado por usar a calculadora! Até mais!")
                break
            elif proxima_acao == 'n':
                resultado_anterior = None # Reseta o resultado para um novo cálculo
                break
            elif proxima_acao == 'c':
                if resultado_anterior is None:
                    print("Não há um resultado anterior para continuar. Iniciando um novo cálculo.")
                    resultado_anterior = None # Garante que não use um None
                    break
                else:
                    break # Continua o loop com o resultado anterior já setado
            else:
                print("Opção inválida. Digite 'c', 'n' ou 's'.")

# Chama a função principal para iniciar a calculadora
calculadora_avancada()