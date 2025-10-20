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

nome_arquivo = "meus_desejos.txt"
desejos = []

try:
    with open(nome_arquivo, 'r', encoding='utf-8') as arquivo:
        for linha in arquivo:
            desejos.append(linha.strip())
    print(f"Meus desejos foram carregados do arquivo '{nome_arquivo}'!\n") 
except FileNotFoundError: 
    print("Parece que é a sua primeira vez! Vamos criar a sua lista de desejos.\n")
except Exception as e:
    print(f"Ocorreu um erro ao carregar os seus desejos: {e}")

# def salvar_desejos(lista_de_desejos):
#     try: