import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "1"
import pygame
from pygame.locals import QUIT
# A PRÓPRIA VIDA!
# Mas de maneira séria, é basicamente toda célula do jogo.

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 600
PLAY_SCREEN_WIDTH = SCREEN_WIDTH - 300
SQUARE_SIZE = 13
BOX_SIZE = SQUARE_SIZE+2
AMOUNT_OF_CELLS = PLAY_SCREEN_WIDTH // BOX_SIZE
AMOUNT_OF_LINES = SCREEN_HEIGHT // BOX_SIZE


class Life(pygame.sprite.Sprite):

    def __init__(self, cpx, cpy, num):
        pygame.sprite.Sprite.__init__(self)
        self.nb = 0
        self.num = num
        self.image = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE))
        self.image.fill((50, 50, 50))
        self.alive = False
        self.rect = self.image.get_rect(topleft=(cpx, cpy))

        # Atualizar se está vivo ou morto
    def revive(self):
        if self.alive is False:
            self.image.fill((180, 180, 180))
            self.alive = True

        elif self.alive is True:
            self.image.fill((50, 50, 50))
            self.alive = False
    # Feito para loop de verificação

    def check(self, sprites):
        num = self.num
        nb = 0

        for line in range(-1, 2):
            c_line = 0
            if num[0]+line == -1:
                c_line = AMOUNT_OF_LINES-1
            elif num[0]+line == AMOUNT_OF_LINES:
                c_line = 0
            else:
                c_line = num[0]+line
            for cell in range(-1, 2):
                c_cell = 0
                if num[1]+cell == -1:
                    c_cell = AMOUNT_OF_CELLS-1
                elif num[1]+cell == AMOUNT_OF_CELLS:
                    c_cell = 0
                elif line == 0 and cell == 0:
                    continue
                else:
                    c_cell = num[1]+cell
                ver = sprites[c_line].sprites()[c_cell].alive
                if ver is True:
                    nb += 1
            self.nb = nb

    def commit(self):
        nb = self.nb
        if nb == 3 and self.alive is False:
            self.alive = True
            self.image.fill((180, 180, 180))
        elif nb <= 1 and self.alive is True:
            self.alive = False
            self.image.fill((50, 50, 50))
        elif nb <= 3 and self.alive is True:
            pass
        elif nb > 3 and self.alive is True:
            self.alive = False
            self.image.fill((50, 50, 50))
# O jogo em si


def main():
    # Fazendo a Tela e inicializando o Relógio
    pygame.init()
    pygame.font.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('O jogo da vida')
    clock = pygame.time.Clock()

    # Fazendo o Background junto das linhas
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((50, 50, 50))
    width_incre = BOX_SIZE
    height_incre = BOX_SIZE
    while width_incre <= PLAY_SCREEN_WIDTH:
        pygame.draw.lines(background, (180, 180, 180), True,
                          ((width_incre, 0), (width_incre, SCREEN_HEIGHT)))
        width_incre += BOX_SIZE
    while height_incre <= SCREEN_HEIGHT:
        pygame.draw.lines(background, (180, 180, 180), True, ((0, height_incre),
                          (PLAY_SCREEN_WIDTH, height_incre)))
        height_incre += BOX_SIZE

    # Drawing a Rect for GUI
    pygame.draw.rect(background, (0, 0, 0), (948, 98, 204, 54))
    box = background.subsurface((950, 100, 200, 50))
    box.fill((250, 0, 0))
    box.blit(pygame.font.SysFont('hack', 12).render('Not active', False, (0, 0, 0)), (65, 18))

    # Inserindo cada célula no seu devido local
    # Posição Inicial
    px = 1
    py = 1

    # Cada linha é agrupada por um grupo de Sprites
    sline = pygame.sprite.Group()

    # A lista onde cada linha vai ficar
    allsprites = pygame.sprite.RenderPlain()
    indexBox = []

    # Populando a lista
    for line in range(AMOUNT_OF_LINES):
        for unid in range(AMOUNT_OF_CELLS):
            life = Life(px, py, [line, unid])
            sline.add(life)
            if px <= PLAY_SCREEN_WIDTH:
                px += BOX_SIZE
        else:
            indexBox.append(sline)
            allsprites.add(sline)
            sline = pygame.sprite.Group()
        px = 1
        py += BOX_SIZE

    # Renderizando tudo
    screen.blit(background, (0, 0))
    pygame.display.flip()

    # O loop após a inicialização
    # Declarando varíaveis para uso no loop
    activeSim = False
    tick = 1

    while True:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == QUIT:
                return
            # Código para mudar se cada célula está viva ou morta
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if activeSim is False:
                    # Após pegar a posição do mouse...
                    pos = pygame.mouse.get_pos()
                    apx, apy = pos
                    # É feito um cálculo dos incrementos, na qual é utilizado no indice
                    apx = apx // BOX_SIZE
                    apy = apy // BOX_SIZE
                # Pegando a célula da lista, e mandando ela atualizar
                indexBox[apy].sprites()[apx].revive()

            # Lendo o input do teclado
            elif event.type == pygame.KEYDOWN:
                # Lendo o Espaço para começar e parar o jogo
                if event.key == pygame.K_SPACE:
                    if activeSim is False:
                        activeSim = True
                    elif activeSim is True:
                        activeSim = False
                # Lendo os números para acelerar/desacelerar o jogo
                if event.key == pygame.K_1:
                    tick = 1
                if event.key == pygame.K_2:
                    tick = 3
                if event.key == pygame.K_3:
                    tick = 5
                if event.key == pygame.K_4:
                    tick = 10
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()

        # A simulação do jogo
        if activeSim:
            clock.tick(tick)
            for line in indexBox:
                for cell in line:
                    cell.check(indexBox)

            for line in indexBox:
                for cell in line:
                    cell.commit()
            allsprites.update()
            pygame.display.flip()

        # No final tudo, sendo renderizado novamente, por segurança.
        screen.blit(background, (0, 0))
        allsprites.draw(background)
        pygame.display.flip()


if __name__ == '__main__':
    main()
