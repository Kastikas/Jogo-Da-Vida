import pygame
from pygame.locals import *


#A PRÓPRIA VIDA!
#Mas de maneira séria, é basicamente toda célula do jogo.
class Life(pygame.sprite.Sprite):

        def __init__(self, cpx, cpy, num):
            pygame.sprite.Sprite.__init__(self)
            self.nb = 0
            self.num = num
            self.image = pygame.Surface((13,13))
            self.image.fill((50, 50, 50))
            self.alive = False
            self.rect = self.image.get_rect(topleft=(cpx,cpy))

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
            num = self.num
            nb = 0

            for line in range(-1,2):
                c_line = 0
                if num[0]+line == -1:
                    c_line = 39
                elif num[0]+line == 40:
                    c_line = 0
                else:
                    c_line = num[0]+line      
                for cell in range(-1,2):
                    c_cell = 0
                    if num[1]+cell == -1:
                        c_cell = 59
                    elif num[1]+cell == 60:
                        c_cell = 0
                    elif line == 0 and cell == 0:
                        continue
                    else:
                        c_cell = num[1]+cell
                    ver = sprites[c_line].sprites()[c_cell].alive
                    if ver == True:
                        nb += 1
            self.nb = nb                            
        def commit(self):
            nb = self.nb
            if nb == 3 and self.alive == False:
                    self.alive = True
                    self.image.fill((180,180,180))
            elif nb <= 1 and self.alive == True:
                self.alive = False
                self.image.fill((50, 50, 50))
            elif nb <= 3 and self.alive == True:
                pass
            elif nb > 3 and self.alive == True:
                self.alive = False
                self.image.fill((50, 50, 50))    
#O jogo em si
def main():
    # Fazendo a Tela e inicializando o Relógio
    pygame.init()
    screen = pygame.display.set_mode((900,600))
    pygame.display.set_caption('O jogo da vida')
    clock = pygame.time.Clock()

    # Fazendo o Background junto das linhas
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((50, 50, 50))
    width = 15
    height = 15
    while width <= 900:
        pygame.draw.lines(background,(180,180,180),True,((width,0), (width,600)))
        width += 15
    while height <= 600:
        pygame.draw.lines(background,(180,180,180),True,((0,height), (900,height)))
        height += 15


    #Inserindo cada célula no seu devido local
    #Posição Inicial
    px = 1
    py = 1

    #Cada linha é agrupada por um grupo de Sprites
    sline = pygame.sprite.Group()

    #A lista onde cada linha vai ficar
    allsprites = []

    #Populando a lista
    for line in range(40):
        for unid in range(60):
            life = Life(px,py,[line,unid])
            sline.add(life)
            if px <= 900:
                px += 15
        else:
            allsprites.append(sline)
            sline = pygame.sprite.Group()
        px = 1
        py += 15  
        

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
                    apx , apy = pos
                    #É feito um cálculo dos incrementos, na qual é utilizado no indice
                    apx = apx // 15
                    apy = apy // 15
                #Pegando a célula da lista, e mandando ela atualizar
                allsprites[apy].sprites()[apx].update()
                #Fazendo o jogo renderizar aquele quadrado
                pygame.sprite.RenderPlain(allsprites[apy])
            
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
            for line in allsprites:
                for cell in line:
                    cell.check(allsprites)
                        
            for line in allsprites:
                for cell in line:
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