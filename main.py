import numpy as np
import pygame

pygame.init()
pygame.display.set_caption("Omnibus")
WIDTH, HEIGHT = 800, 600
SCALE = WIDTH // 4
BLACK = (0, 0, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
font = pygame.Font("/usr/share/fonts/TTF/FiraCodeNerdFont-Bold.ttf", WIDTH // 20)
screen = pygame.display.set_mode((WIDTH, HEIGHT))

text = font.render("x⁵ - x + α = 0", True, BLACK)

text_size = text.get_size()
tx = WIDTH // 2 - text_size[0] // 2
ty = text_size[1] * 2


def complex_to_pixel(n: complex):
    x = n.real
    y = n.imag

    x = x * SCALE + WIDTH // 2
    y = y * SCALE + HEIGHT // 2

    return x, y


def pixel_to_complex(px: int, py: int):
    x = (px - WIDTH // 2) / SCALE
    y = (py - HEIGHT // 2) / SCALE

    return complex(x, y)


def plot_complex(n: complex, color: tuple[int, int, int]):
    global screen

    x, y = complex_to_pixel(n)
    pygame.draw.aacircle(screen, color, (x, y), 10)


def compute_singular_points(coefs: list[complex]) -> list[complex]:
    derivative = np.polyder(coefs)


alpha = 0 + 0j
coefs = [1, 0, 0, 0, -1, alpha]
roots = np.roots(coefs)
singular_points = [
    4 / (5 * np.power(5, 1 / 4)) + 0j,
    -(4 / (5 * np.power(5, 1 / 4))) + 0j,
    4 / (5 * np.power(5, 1 / 4)) * 1j,
    -(4 / (5 * np.power(5, 1 / 4)) * 1j)
]

compute_singular_points(coefs)

# almacena los puntos de las trayectorias de los puntos cuando se mantiene el raton
buffer = []
creating_trayectory = False

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                pygame.quit()
                exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == pygame.BUTTON_LEFT:
                buffer.clear()
                creating_trayectory = True
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == pygame.BUTTON_LEFT:
                creating_trayectory = False

    px, py = pygame.mouse.get_pos()
    alpha = pixel_to_complex(px, py)

    coefs = [1, 0, 0, 0, -1, alpha]
    roots = np.roots(coefs)

    if creating_trayectory:
        buffer.append((px, py))
        buffer += [complex_to_pixel(z) for z in roots]

    # RENDER
    screen.fill(WHITE)
    for point in singular_points:
        plot_complex(point, RED)
    for root in roots:
        plot_complex(complex(root), BLACK)
    if len(buffer) > 0 and creating_trayectory:
        for point in buffer:
            pygame.draw.aacircle(screen, RED, point, 1)

    screen.blit(text, (tx, ty))

    pygame.display.flip()
