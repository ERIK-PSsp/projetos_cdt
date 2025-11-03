import pygame
import random
import time
import os

# --- Configurações Iniciais e Pygame ---

pygame.init()

# Define o tamanho da tela
LARGURA_TELA = 800
ALTURA_TELA = 650
JANELA = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
pygame.display.set_caption("Jogo da Memória (Flip Card)")

# Cores
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
CINZA_FUNDO = (20, 20, 30)

# Fonte para o placar e mensagens
FONTE = pygame.font.Font(None, 40)

# --- Configurações das Cartas ---

TAMANHO_CARTA = 100
ESPACAMENTO = 20
CARTAS_POR_LINHA = 5  # 10 cartas no total (2 linhas de 5)
NUM_PARES = 5

# Caminho para os recursos (MUDE SE NECESSÁRIO)
PASTA_IMAGENS = "assets"
VERSO_NOME = "versus_flip.png" # Nome do arquivo da imagem de fundo da carta

# Nomes dos arquivos das imagens da frente (5 imagens, que formarão 5 pares)
# NOTA: Adapte estes nomes para as 5 imagens que você colocar na pasta 'assets'
NOMES_IMAGENS_FRENTE = [f"frente_{i}.png" for i in range(1, NUM_PARES + 1)] 

# --- Funções de Carregamento de Recursos ---

def carregar_imagem(nome_arquivo):
    """Carrega e dimensiona uma imagem da pasta 'assets'."""
    caminho = os.path.join(PASTA_IMAGENS, nome_arquivo)
    try:
        imagem = pygame.image.load(caminho).convert_alpha()
        return pygame.transform.scale(imagem, (TAMANHO_CARTA, TAMANHO_CARTA))
    except pygame.error as e:
        print(f"ERRO: Não foi possível carregar a imagem '{nome_arquivo}'. Certifique-se de que a pasta 'assets' e o arquivo existem.")
        print(f"Detalhe do Erro: {e}")
        pygame.quit()
        exit()

def carregar_recursos():
    """Carrega o verso e todas as imagens da frente."""
    
    # 1. Carregar o Verso
    verso_img = carregar_imagem(VERSO_NOME)

    # 2. Carregar as Imagens da Frente
    imagens_frente = []
    for nome in NOMES_IMAGENS_FRENTE:
        imagem_surface = carregar_imagem(nome)
        # Armazenamos a imagem e seu ID (o nome do arquivo)
        imagens_frente.append((imagem_surface, nome)) 

    # 3. Criar a lista final de todas as cartas (5 pares) e embaralhar
    todas_imagens = imagens_frente * 2 
    random.shuffle(todas_imagens)
    
    return verso_img, todas_imagens


# --- Classe Carta (Card) ---

class Carta:
    def __init__(self, imagem_e_id, x, y, verso_img):
        # O ID é o nome do arquivo, usado para checar a correspondência
        self.imagem_frente = imagem_e_id[0]
        self.id_par = imagem_e_id[1] 
        self.imagem_verso = verso_img
        
        # Cria o retângulo para detecção de clique e posicionamento
        self.rect = pygame.Rect(x, y, TAMANHO_CARTA, TAMANHO_CARTA)
        
        self.virada = False      # Indica se a carta está virada para cima
        self.encontrada = False  # Indica se o par já foi feito

    def desenhar(self, janela):
        """Desenha a face (frente) ou o verso da carta na tela."""
        if self.encontrada or self.virada:
            janela.blit(self.imagem_frente, self.rect)
        else:
            janela.blit(self.imagem_verso, self.rect)
            
    def clicar(self, pos):
        """Verifica se o clique ocorreu no espaço da carta."""
        return self.rect.collidepoint(pos)


# --- Lógica do Layout e Criação de Cartas ---

def criar_cartas(todas_imagens, verso_img):
    """Cria e posiciona as 10 cartas na grade 5x2."""
    cartas = []
    
    # Calcular margem para centralizar a grade
    largura_grade = CARTAS_POR_LINHA * TAMANHO_CARTA + (CARTAS_POR_LINHA - 1) * ESPACAMENTO
    margem_x = (LARGURA_TELA - largura_grade) // 2
    margem_y = 100 # Começa a grade 100px abaixo do topo (espaço para o placar)
    
    for i, img_e_id in enumerate(todas_imagens):
        linha = i // CARTAS_POR_LINHA
        coluna = i % CARTAS_POR_LINHA
        
        # Cálculo da posição (x, y)
        x = margem_x + coluna * (TAMANHO_CARTA + ESPACAMENTO)
        y = margem_y + linha * (TAMANHO_CARTA + ESPACAMENTO)
        
        cartas.append(Carta(img_e_id, x, y, verso_img))
        
    return cartas


# --- Função Principal do Jogo ---

def game_loop():
    # Carrega todos os recursos
    verso_img, todas_imagens = carregar_recursos()
    cartas = criar_cartas(todas_imagens, verso_img)

    # Variáveis de Estado do Jogo
    rodando = True
    cartas_viradas = []       # Armazena as 1 ou 2 cartas viradas atualmente
    pontuacao = 0
    aguardando_verificacao = False # Sinaliza que 2 cartas estão viradas e o jogo deve pausar
    tempo_ultima_virada = 0
    
    RELOGIO = pygame.time.Clock()

    while rodando:
        # --- 1. Processamento de Eventos (Cliques) ---
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False
            
            if evento.type == pygame.MOUSEBUTTONDOWN and not aguardando_verificacao:
                pos_clique = evento.pos
                
                for carta in cartas:
                    # Se a carta foi clicada, não está virada e não foi encontrada
                    if carta.clicar(pos_clique) and not carta.virada and not carta.encontrada:
                        carta.virada = True
                        cartas_viradas.append(carta)
                        
                        # Se 2 cartas foram viradas, prepare para verificar o par
                        if len(cartas_viradas) == 2:
                            aguardando_verificacao = True
                            tempo_ultima_virada = time.time() # Inicia o timer

        # --- 2. Lógica de Checagem de Par (Executa após um pequeno delay) ---
        if aguardando_verificacao and time.time() - tempo_ultima_virada > 1.0: # Delay de 1 segundo
            carta1, carta2 = cartas_viradas
            
            if carta1.id_par == carta2.id_par:
                # É um par! Marca como encontrado
                carta1.encontrada = True
                carta2.encontrada = True
                pontuacao += 10
            else:
                # Não é um par! Vira as cartas de volta
                carta1.virada = False
                carta2.virada = False
                
            cartas_viradas = []               # Limpa a lista de viradas
            aguardando_verificacao = False    # Libera o clique

        # --- 3. Checagem de Fim de Jogo ---
        if all(carta.encontrada for carta in cartas):
            # Desenha a mensagem de vitória
            JANELA.fill(CINZA_FUNDO)
            texto_fim = FONTE.render("VOCÊ VENCEU!", True, BRANCO)
            texto_ponto = FONTE.render(f"Pontuação Final: {pontuacao}", True, BRANCO)
            
            JANELA.blit(texto_fim, (LARGURA_TELA // 2 - texto_fim.get_width() // 2, ALTURA_TELA // 2 - 50))
            JANELA.blit(texto_ponto, (LARGURA_TELA // 2 - texto_ponto.get_width() // 2, ALTURA_TELA // 2 + 10))
            pygame.display.flip()
            
            time.sleep(3) # Pausa antes de fechar
            rodando = False

        # --- 4. Desenho na Tela ---
        JANELA.fill(CINZA_FUNDO)
        
        # Desenhar Placar
        texto_placar = FONTE.render(f"Pontuação: {pontuacao}", True, BRANCO)
        JANELA.blit(texto_placar, (LARGURA_TELA // 2 - texto_placar.get_width() // 2, 30))

        # Desenhar Cartas
        for carta in cartas:
            carta.desenhar(JANELA) 

        pygame.display.flip()
        RELOGIO.tick(60)

    pygame.quit()

if __name__ == "__main__":
    # IMPORTANTE: Instruções para o usuário configurar antes de rodar!
    print("--- INSTRUÇÕES PARA RODAR ---")
    print(f"1. Crie uma pasta chamada '{PASTA_IMAGENS}' no mesmo local do script.")
    print(f"2. Coloque o arquivo do verso da carta: '{VERSO_NOME}'.")
    print(f"3. Coloque as 5 imagens da frente: {NOMES_IMAGENS_FRENTE}")
    print("-----------------------------")
    game_loop()