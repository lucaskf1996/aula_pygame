# -*- coding: utf-8 -*-

# Importando as bibliotecas necessárias.
import pygame
import random
from os import path
import time

# Estabelece a pasta que contem as figuras, sons e fontes
img_dir = path.join(path.dirname(__file__), 'img')
snd_dir = path.join(path.dirname(__file__), "snd")
fnt_dir = path.join(path.dirname(__file__), "font")

# Dados gerais do jogo.
WIDTH = 700 # Largura da tela
HEIGHT = 900 # Altura da tela
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
        
    #Construtor da classe(Sprite)
    def __init__(self, player_img):
        
        # Construtor da classe pai (Sprite).
        pygame.sprite.Sprite.__init__(self)
       
        #carregando a imagem de fundo
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
        self.speedy = 0
        
        #Melhora a colisao estabelecendo um raio de um circulo
        self.radius = 25
        
        
    #metodo que atualiza a posicao da navinha
    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        
        #mantem dentro da tela
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.y > HEIGHT-50:
            self.rect.y = HEIGHT-50
        if self.rect.y < 30:
            self.rect.y = 30







class Mob(pygame.sprite.Sprite):
    
    def __init__(self, mob_img):
        
        pygame.sprite.Sprite.__init__(self)
        
        self.image = mob_img

        self.image.set_colorkey(BLACK)
        
        self.image = pygame.transform.scale(mob_img, (50, 38))
        
        self.rect = self.image.get_rect()
        
        velocidade_max_x = 5
        velocidade_min_x = -5

        self.rect.y = random.randrange(-100,-40)
        self.rect.x = random.randrange(0, WIDTH)
        
        #quanto mais proximo de WIDTH mais eu retiro e quanto mais longe menos eu retiro
        velocidade_max_x = velocidade_max_x - velocidade_max_x * self.rect.x/WIDTH
        velocidade_min_x = velocidade_min_x - velocidade_min_x * (1 - self.rect.x/WIDTH)

        self.speedx = random.uniform(velocidade_min_x, velocidade_max_x) #max 3 para x = 0 eh bom 
        self.speedy = random.randrange(5,9)
        
        self.radius = int(self.rect.width * 0.7 / 2)
        
    def update(self):
        
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        
        if self.rect.top > HEIGHT + 10 or self.rect.left < -50 or self.rect.right > WIDTH + 50:
            
            self.rect.y = random.randrange(-100,-40)
            self.rect.x = random.randrange(0, WIDTH)
                       
            velocidade_max_x = 5
            velocidade_min_x = -5
            velocidade_max_x = velocidade_max_x - velocidade_max_x * self.rect.x/WIDTH
            velocidade_min_x = velocidade_min_x - velocidade_min_x * (1 - self.rect.x/WIDTH)

            self.speedx = random.uniform(velocidade_min_x, velocidade_max_x)
            self.speedy = random.randrange(5,9)

class Laser(pygame.sprite.Sprite):
    
    def __init__(self, laser_img, pos_x, pos_y):
        
        pygame.sprite.Sprite.__init__(self)
        
        self.image = laser_img
        
        self.rect = self.image.get_rect()
        
        self.image.set_colorkey(BLACK)

        self.rect.x = pos_x
        self.rect.y = pos_y
        
        self.image = pygame.transform.scale(laser_img, (10, 30))
        
    def update(self):
        
        #Velocidade do laser
        self.rect.y -= 10
        if self.rect.bottom < 0:
            self.kill()

class Explosion(pygame.sprite.Sprite):
    
    #construtor
    def __init__(self, center, explosion_anim):
        
        pygame.sprite.Sprite.__init__(self)
        
        #carrega a animacao
        self.explosion_anim = explosion_anim
        
        #inicia o processo de animacao colocando a primeira imagem na tela
        self.frame = 0
        self.image = self.explosion_anim[self.frame]
        self.rect = self.image.get_rect()
        self.rect.center = center
        
        #guarda o tick da primeira imagem
        self.last_update = pygame.time.get_ticks()
        
        #controle de ticks de animacao: troca de umagem a cada self.fram_ticks milisegundos
        self.frame_ticks = 50
        
    def update(self):
        
        #verifica o frame atual
        now = pygame.time.get_ticks()
        
        #verifica quantos ticks se passaram desde a ultima mudanca de fram
        elapsed_ticks = now - self.last_update
        
        #se ja esta na hora de mudar de imagem
        if elapsed_ticks > self.frame_ticks:
            
            #marca o tick da nova imagem
            self.last_update = now
            
            #avanca um quadro
            self.frame +=1
            
            #verifica se ja chegou no final da animacao
            if self.frame == len(self.explosion_anim):
                
                #se sim, finaliza a animacao
                self.kill()
            
            else:
                #se ainda nao chegou ao fim da explosao, troca de imagem
                center = self.rect.center
                self.image = self.explosion_anim[self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center

def load_assets(img_dir, snd_dir):
    assets = {}
    assets["player_img"] = pygame.image.load(path.join(img_dir, "playerShip1_orange.png")).convert()
    assets["mob_img"] = pygame.image.load(path.join(img_dir, "meteorBrown_med1.png")).convert()
    assets["laser_img"] = pygame.image.load(path.join(img_dir, "laserRed16.png")).convert()
    assets["background"] = pygame.image.load(path.join(img_dir, 'starfield.png')).convert()
    assets["boom_sound"] = pygame.mixer.Sound(path.join(snd_dir, "expl3.wav"))
    assets["laser_hit"] = pygame.mixer.Sound(path.join(snd_dir, "expl6.wav"))
    assets["laser_pew"] = pygame.mixer.Sound(path.join(snd_dir, "pew.wav"))
    explosion_anim=[]
    for i in range(9):
        filename = 'regularExplosion0{}.png'.format(i)
        img = pygame.image.load(path.join(img_dir, filename)).convert()
        img = pygame.transform.scale(img, (32, 32))
        img.set_colorkey(BLACK)
        explosion_anim.append(img)
    assets["explosion_anim"] = explosion_anim
    assets["score_font"] = pygame.font.Font(path.join(fnt_dir, "PressStart2P.ttf"), 28)
    return assets
    

# Inicialização do Pygame.
pygame.init()
pygame.mixer.init()

# Tamanho da tela.
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Nome do jogo
pygame.display.set_caption("Super navinha")

#carrega todos os assets de uma vez só e guarda em um dicionario
assets = load_assets(img_dir, snd_dir)

player = Player(assets["player_img"])
mob = Mob(assets["mob_img"])
laser = Laser(assets["laser_img"], player.rect.x, player.rect.y)


#variavel para o ajuste de velocidade
clock = pygame.time.Clock()

# Carrega o fundo do jogo
background = assets["background"]
background = pygame.transform.scale(background, (WIDTH, HEIGHT))
background_rect = background.get_rect()

#Carrega os sons do Jogo
pygame.mixer.music.load(path.join(snd_dir, 'narutao.wav'))
pygame.mixer.music.set_volume(1)
boom_sound = assets["boom_sound"]
laser_hit = assets["laser_hit"]
laser_pew = assets["laser_pew"]

player = Player(assets["player_img"]) 

#carrega a fonte para desenhar o score
score_font = assets["score_font"]
#cria um grupo de sprites e adiciona a nave
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

mobs = pygame.sprite.Group()
for i in range(0,15):
    mob = Mob(assets["mob_img"])
    all_sprites.add(mob)
    mobs.add(mob)

lista_laser = pygame.sprite.Group()

#Flags dos botoes
right_key=0
left_key=0
down_key=0
up_key=0


# Comando para evitar travamentos.
try:
    #Inicia a musica
    pygame.mixer.music.play(loops=-1)

    score = 0

    PLAYING = 0
    EXPLODING = 1
    DONE = 2

    vidas = 0

    state = PLAYING
    # Loop principal.
    while state != DONE:
        #ajusta a velocidade do jogo
        clock.tick(FPS)
        
        if state == PLAYING:
            # Processa os eventos (mouse, teclado, botão, etc).
            for event in pygame.event.get():
            
                # Verifica se foi fechado
                if event.type == pygame.QUIT:
                    state = DONE
            
            
                #verifica se apertou alguma tecla    
                if event.type == pygame.KEYDOWN:
                    #depende da tecla, altera a velocidade
                    if event.key == pygame.K_LEFT:
                        player.speedx = -8
                        left_key = 1
                    if event.key == pygame.K_RIGHT:
                        right_key = 1
                        player.speedx = 8
                    if event.key == pygame.K_DOWN:
                        down_key = 1
                        player.speedy = 3
                    if event.key == pygame.K_UP:
                        up_key = 1
                        player.speedy = -3
                    if event.key == pygame.K_SPACE:
                        #Atira
                        laser = Laser(assets["laser_img"], player.rect.x + 20, player.rect.y)
                    
                        laser_pew.play()
                    
                        #adiciona laser pra lista de laser
                        all_sprites.add(laser)
                        lista_laser.add(laser)
                   
                #verifica se soltou alguma tecla
                if event.type == pygame.KEYUP:
                
                    #dependendo da tecla, altera a velocidade
                    if event.key == pygame.K_LEFT:
                        left_key = 0
                        player.speedx = 0
                        if right_key == 1:
                            player.speedx = 8
                    if event.key == pygame.K_RIGHT:
                        right_key = 0
                        player.speedx = 0
                        if left_key == 1:
                            player.speedx = -8
                    if event.key == pygame.K_UP:
                        up_key = 0
                        player.speedy = 0
                        if down_key == 1:
                            player.speedx = 3
                    if event.key == pygame.K_DOWN:
                        down_key = 0
                        player.speedy = 0
                        if up_key == 1:
                            player.speedx = -3

        #depois de processar os eventos
        #atualiza a acao de cada sprite
        all_sprites.update()
        
        if state == PLAYING:

            #verifica se houve colisao entre nave e meteroro
            hits1 = pygame.sprite.spritecollide(player, mobs, False, pygame.sprite.collide_circle)
            if hits1:
            
                #toca som de colisao
                boom_sound.play()
                player.kill()
                explosao = Explosion(player.rect.center, assets["explosion_anim"])
                all_sprites.add(explosao)
                state = EXPLODING
                explosion_tick = pygame.time.get_ticks()
                explosion_duration = explosao.frame_ticks * len(explosao.explosion_anim) + 400
            
            
            hits2 = pygame.sprite.groupcollide(lista_laser, mobs, True, True)
        
            for hit in hits2:
            
                mob = Mob(assets["mob_img" ])
                mobs.add(mob)
                all_sprites.add(mob)
                laser_hit.play()
 
                explosao = Explosion(hit.rect.center, assets["explosion_anim"])
                all_sprites.add(explosao)

                score += 100
        
        elif state == EXPLODING:
            now = pygame.time.get_ticks()
            if now - explosion_tick > explosion_duration:
                vidas += 1
                if vidas > 2:
                    state = DONE
                else:
                    player = Player(assets["player_img"])
                    all_sprites.add(player)
                    state = PLAYING
                

        # A cada loop, redesenha o fundo e os sprites
        
        screen.fill(BLACK)
        screen.blit(background, background_rect)
        all_sprites.draw(screen)
        
        #desenha o score
        text_surface = score_font.render("{:08d}".format(score), True, YELLOW)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (WIDTH / 2, 10)
        screen.blit(text_surface, text_rect)
        # Depois de desenhar tudo, inverte o display.
        pygame.display.flip()
        
finally:

    pygame.quit()