import pygame
from pygame.locals import *


#A PRÓPRIA VIDA!
#Mas de maneira séria, é basicamente toda célula do jogo.
class Life(pygame.sprite.Sprite):

        def __init__(self, x, y, numera):
            pygame.sprite.Sprite.__init__(self)
            self.vivo = 0
            self.numera = numera
            self.image = pygame.Surface((18,12))
            self.image.fill((50, 50, 50))
            self.alive = False
            self.rect = self.image.get_rect(center=(x,y))

        #Atualizar se está vivo ou morto
        def update(self):
 
            if self.alive == False:
                self.image.fill((180,180,180))
                self.alive = True

            elif self.alive == True:
                self.image.fill((50, 50, 50))
                self.alive = False

        #Feito para loop de verificação
        def check(self, sprites):
            num = self.numera
            vivos = 0
            
            for linha in range(-1,2):
                if num[0]+linha not in range(40):
                    continue       
                for cell in range(-1,2):
                    if num[1]+cell not in range(40):
                        continue
                    if linha == 0 and cell == 0:
                        continue
                    ver = sprites[num[0]+linha].sprites()[num[1]+cell].alive
                    if ver == True:
                        vivos += 1
            self.vivo = vivos                            
        def commit(self):
            vivos = self.vivo
            if vivos == 3 and self.alive == False:
                    self.alive = True
                    self.image.fill((180,180,180))
            elif vivos <= 1 and self.alive == True:
                self.alive = False
                self.image.fill((50, 50, 50))
            elif vivos <= 3 and self.alive == True:
                pass
            elif vivos > 3 and self.alive == True:
                self.alive = False
                self.image.fill((50, 50, 50))    
#O jogo em si
def main():
    # Fazendo a Tela e inicializando o Relógio
    pygame.init()
    screen = pygame.display.set_mode((800,600))
    pygame.display.set_caption('O jogo da vida')
    clock = pygame.time.Clock()

    # Fazendo o Background junto das linhas
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((50, 50, 50))
    width = 20
    height = 15
    while width <= 800:
        pygame.draw.lines(background,(180,180,180),True,((width,0), (width,600)))
        width += 20
    while height <= 600:
        pygame.draw.lines(background,(180,180,180),True,((0,height), (800,height)))
        height += 15


    #Inserindo cada célula no seu devido local
    #Posição Inicial
    positionx = 10
    positiony = 8.5

    #Cada linha é agrupada por um grupo de Sprites
    line = pygame.sprite.Group()

    #A lista onde cada linha vai ficar
    allsprites = []

    #Populando a lista
    for linha in range(40):
        for unid in range(40):
            life = Life(positionx,positiony,[linha,unid])
            line.add(life)
            if positionx <= 800:
                positionx += 20
        else:
            allsprites.append(line)
            line = pygame.sprite.Group()
        positionx = 10
        positiony += 15  
        

    # Renderizando tudo
    screen.blit(background, (0, 0))
    for line in allsprites:
        pygame.sprite.RenderPlain((line)).draw(background)
    pygame.display.flip()
    
    # O loop após a inicialização
    #Declarando varíaveis para uso no loop
    activeSim = False
    tick = 1
    while True:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == QUIT:
                return
            #Código para mudar se cada célula está viva ou morta
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if activeSim == False:
                    #Após pegar a posição do mouse...
                    pos = pygame.mouse.get_pos()
                    x , y = pos
                    #É feito um cálculo dos incrementos, na qual é utilizado no indice
                    x = x // 20
                    y = y // 15
                #Pegando a célula da lista, e mandando ela atualizar
                allsprites[y].sprites()[x].update()
                #Fazendo o jogo renderizar aquele quadrado
                pygame.sprite.RenderPlain(allsprites[y])
            
            #Lendo o input do teclado    
            elif event.type == pygame.KEYDOWN:
                #Lendo o Espaço para começar e parar o jogo
                if event.key == pygame.K_SPACE:
                    if activeSim == False:
                        activeSim = True
                    elif activeSim == True:
                        activeSim = False
                #Lendo os números para acelerar/desacelerar o jogo
                if event.key == pygame.K_1:
                    tick = 1
                if event.key == pygame.K_2:
                    tick = 3
                if event.key == pygame.K_3:
                    tick = 5
                if event.key == pygame.K_4:
                    tick = 10

        #A simulação do jogo            
        if activeSim:                        
            clock.tick(tick)
            for linha in allsprites:
                for cell in linha:
                    cell.check(allsprites)
                        
            for linha in allsprites:
                for cell in linha:
                    cell.commit()
            for line in allsprites:    
                pygame.sprite.RenderPlain((line)).draw(background)
            pygame.display.flip()  
                       
 
                        
        #No final tudo, sendo renderizado novamente, por segurança.
        screen.blit(background, (0, 0))
        for line in allsprites:
            pygame.sprite.RenderPlain((line)).draw(background)
        pygame.display.flip()   


if __name__ == '__main__': main()