try:
    from pgzero.actor import Actor
    from pgzero.keyboard import keyboard
    from pgzero.screen import Screen
except ImportError:
    pass  # PgZero injeta esses nomes em tempo de execução

# from pgzero.gui import *
import random

WIDTH = 600
HEIGHT = 200

JOGAR = 1
ENCERRAR = 0
estado_jogo = JOGAR

pontuacao = 0

# Atores
trex = Actor("trex1", pos=(50, 160))
trex.vy = 0

solo = Actor("ground2", topleft=(0, 180))
solo.vel = -4

fim_de_jogo = Actor("gameover", center=(300, 100))
reiniciar = Actor("restart", center=(300, 140))

nuvens = []
obstaculos = []


def draw():
    screen.clear()
    screen.fill((255, 255, 255))

    solo.draw()
    for n in nuvens:
        n.draw()
    for o in obstaculos:
        o.draw()
    trex.draw()

    if estado_jogo == ENCERRAR:
        fim_de_jogo.draw()
        reiniciar.draw()

    screen.draw.text(f"Pontuação: {pontuacao}",
                     (500, 20), color="black", fontsize=24)


def update():
    global estado_jogo, pontuacao

    if estado_jogo == JOGAR:
        movimentar_solo()
        gravidade()
        controlar_trex()
        gerar_nuvens()
        gerar_obstaculos()
        pontuar()
        detectar_colisao()
    elif estado_jogo == ENCERRAR:
        solo.vel = 0
        for n in nuvens:
            n.x += 0
        for o in obstaculos:
            o.x += 0


def movimentar_solo():
    solo.x += solo.vel
    if solo.right < WIDTH:
        solo.left = 0


def gravidade():
    trex.vy += 0.8
    trex.y += trex.vy
    if trex.y >= 160:
        trex.y = 160
        trex.vy = 0


def controlar_trex():
    if keyboard.space and trex.y >= 160:
        trex.vy = -12


def gerar_nuvens():
    if random.randint(0, 60) == 0:
        n = Actor("cloud", pos=(WIDTH, random.randint(40, 100)))
        n.vel = -2
        nuvens.append(n)

    for nuvem in list(nuvens):
        nuvem.x += nuvem.vel
        if nuvem.right < 0:
            nuvens.remove(nuvem)


def gerar_obstaculos():
    if random.randint(0, 60) == 0:
        img = f"obstacle{random.randint(1, 6)}"
        o = Actor(img, pos=(WIDTH, 165))
        o.vel = -(4 + pontuacao // 100)
        obstaculos.append(o)

    for obs in list(obstaculos):
        obs.x += obs.vel
        if obs.right < 0:
            obstaculos.remove(obs)


def detectar_colisao():
    global estado_jogo
    for obs in obstaculos:
        if trex.colliderect(obs):
            estado_jogo = ENCERRAR


def pontuar():
    global pontuacao
    pontuacao += 1


def on_mouse_down(pos):
    if estado_jogo == ENCERRAR and reiniciar.collidepoint(pos):
        reiniciar_jogo()


def reiniciar_jogo():
    global estado_jogo, pontuacao
    trex.y = 160
    trex.vy = 0
    solo.vel = -4
    nuvens.clear()
    obstaculos.clear()
    pontuacao = 0
    estado_jogo = JOGAR
