# -*- coding: utf-8 -*-

# Importando as bibliotecas necessárias.
import pygame
import random
from os import path

# Estabelece a pasta que contem as figuras.
img_dir = path.join(path.dirname(__file__), 'img')

# Dados gerais do jogo.
WIDTH = 480 # Largura da tela
HEIGHT = 600 # Altura da tela
FPS = 60 # Frames por segundo

# Define algumas variáveis com as cores básicas
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

#classe jogador que representa a nave
class Player(pygame.sprite.Sprite):
        
    #Construtor da classe pau (Sprite)
    def __init__(self):
        
        # Construtor da classe pai (Sprite).
        pygame.sprite.Sprite.__init__(self)
       
        #carregando a imagem de fundo
        player_img = pygame.image.load(path.join(img_dir, "playerShip1_orange.png")).convert()
        self.image = player_img
        
        #diminuindo o tamanho da imagem
        self.image = pygame.transform.scale(player_img, (50,38))
        
        #deixando transparente
        self.image.set_colorkey(BLACK)
        
        #detalhes sobre o posicionamento
        self.rect = self.image.get_rect()
        
        #centraliza embaixo da tela
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
        
        #velocidade da nave
        self.speedx = 0
                
    #metodo que atualiza a posicao da navinha
    def update(self):
        self.rect.x += self.speedx
        
        #mantem dentro da tela
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

class Mob(pygame.sprite.Sprite):
    
    def __init__(self):
        
        pygame.sprite.Sprite.__init__(self)
        
        mob_img = pygame.image.load(path.join(img_dir, "meteorBrown_med1.png")).convert()
        
        self.image = mob_img

        self.image.set_colorkey(BLACK)
        
        self.image = pygame.transform.scale(mob_img, (50, 38))
        
        self.rect = self.image.get_rect()
        
        self.rect.y = random.randrange(-100,-40)
        self.rect.x = random.randrange(0, WIDTH)
        
        self.speedx = random.randrange(-3,3)
        self.speedy = random.randrange(2,9)
        
    def update(self):
        
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        
        if self.rect.top > HEIGHT + 10 or self.rect.left < -50 or self.rect.right > WIDTH + 50:
            
            self.rect.y = random.randrange(-100,-40)
            self.rect.x = random.randrange(0, WIDTH)
        
            self.speedx = random.randrange(-3,3)
            self.speedy = random.randrange(2,9)



# Inicialização do Pygame.
pygame.init()
pygame.mixer.init()

# Tamanho da tela.
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Nome do jogo
pygame.display.set_caption("Super navinha")

#variavel para o ajuste de velocidade
clock = pygame.time.Clock()

# Carrega o fundo do jogo
background = pygame.image.load(path.join(img_dir, 'starfield.png')).convert()
background_rect = background.get_rect()

player = Player()

mob = Mob()
#cria um grupo de sprites e adiciona a nave
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

mobs = pygame.sprite.Group()
for i in range(0,8):
    mob = Mob()
    all_sprites.add(mob)
    mobs.add(mob)
    
# Comando para evitar travamentos.
try:
    
    # Loop principal.
    running = True
    while running:
        
        #ajusta a velocidade do jogo
        clock.tick(FPS)
        
        # Processa os eventos (mouse, teclado, botão, etc).
        for event in pygame.event.get():
            
            # Verifica se foi fechado
            if event.type == pygame.QUIT:
                running = False
    
            #verifica se apertou alguma tecla    
            if event.type == pygame.KEYDOWN:
                #depende da tecla, altera a velocidade
                if event.key == pygame.K_LEFT:
                    player.speedx = -8
                if event.key == pygame.K_RIGHT:
                    player.speedx = 8
                   
            #verifica se soltou alguma tecla
            if event.type == pygame.KEYUP:
                #dependendo da tecla, altera a velocidade
                if event.key == pygame.K_LEFT:
                    player.speedx = 0
                if event.key == pygame.K_RIGHT:
                    player.speedx = 0
            
        #depois de processar os eventos
        #atualiza a acao de cada sprite
        all_sprites.update()
        # A cada loop, redesenha o fundo e os sprites
        screen.fill(BLACK)
        screen.blit(background, background_rect)
        all_sprites.draw(screen)
        
        # Depois de desenhar tudo, inverte o display.
        pygame.display.flip()
        
finally:
    pygame.quit()
