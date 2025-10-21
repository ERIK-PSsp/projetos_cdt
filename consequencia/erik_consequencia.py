'''
primicias

descobrir os 'desejos'
montar uma lista
criar um arquivo para salvar os 'desejos'
salvar os 'desejos' no arquivo
carregar os 'desejos' do arquivo
identificar erros ao carregar os 'desejos'


'''

print ("✨ Minha lista de desejos para o futuro ✨\n")

NOME_ARQUIVO = "meus_desejos.txt"
desejos = []

try:
    with open(NOME_ARQUIVO, 'r', encoding='utf-8') as arquivo:
        for linha in arquivo:
            desejos.append(linha.strip())
    print(f"Meus desejos foram carregados do arquivo '{NOME_ARQUIVO}'!\n") 
except FileNotFoundError: 
    print("Parece que é a sua primeira vez! Vamos criar a sua lista de desejos.\n")
except Exception as e:
    print(f"Ocorreu um erro ao carregar os seus desejos: {e}")

def salvar_desejos(lista_de_desejos):
    try:
        with open(NOME_ARQUIVO, 'w', encoding='utf-8') as arquivo:
            for desejo in lista_de_desejos:
                arquivo.write(desejo + "\n")
        print(f"Seus desejos foram salvos com sucesso!")
    except Exception as e:
        print(f"Ocorreu um erro ao salvar os seus desejos: {e}")
while True:
    print("\n--- O que você gostaria de fazer?---")
    print("1. Adicionar um novo desejo")
    print("2. Ver minha lista de desejos")
    print("3. Sair")
    
    opcao = input("1, 2 ou 3? ")
    
    if opcao == '1':
        novo_desejo = input("Qual é o seu novo desejo?")
        if novo_desejo.strip() == "":
            desejos.append(novo_desejo.strip())
            salvar_desejos(desejos)
        else:
            print("Desejo não pode ser vazio! Tente novamente.")
            
            
    elif opcao == '2':
        print("\n--- Minha Lista de Desejos ---")
        if not desejos:
            print("Sua lista de desejos está vazia.")
        else:
            for i, desejo in enumerate(desejos):
                print(f"{i + 1}. {desejo}")
            print("-----------------------------")
            
    elif opcao == '3':
        print("Até mais! Que seus desejos sejam realizados!")
        break
    else:
        print("Opção inválida! Por favor, escolha 1, 2 ou 3.")
        
        