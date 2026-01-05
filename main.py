import numpy as np
import pygame
import math

pygame.init()
pygame.display.set_caption("Omnibus")
WIDTH, HEIGHT = 800, 600
SCALE = WIDTH // 4
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
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


# TODO: compute singular points
# def compute_singular_points(coefs: list[complex]) -> list[complex]:
#     derivative = np.polyder(coefs)


alpha = 0 + 0j
coefs = [1, 0, 0, 0, -1, alpha]
roots = np.roots(coefs)
singular_points = [
    4 / (5 * np.power(5, 1 / 4)) + 0j,
    -(4 / (5 * np.power(5, 1 / 4))) + 0j,
    4 / (5 * np.power(5, 1 / 4)) * 1j,
    -(4 / (5 * np.power(5, 1 / 4)) * 1j)
]

# almacena los puntos de las trayectorias de los puntos cuando se mantiene el raton
initial_roots = []
root_buffer = []
mouse_buffer = []
creating_trayectory = False


def single_permutation(initial_roots, final_roots, index) -> int:
    initial = initial_roots[index]

    # check if similar root
    for i, root in enumerate(final_roots):
        if abs(initial - root) < 0.1:
            return i + 1

    return None


def check_permutations(initial_roots, final_roots):
    # compare roots
    assert len(initial_roots) == len(final_roots)
    print("\nPermutations:")
    for i in range(len(initial_roots)):
        permutation = single_permutation(initial_roots, final_roots, i)
        if not permutation:
            print(f"La raiz {i + 1} no ha permutado")
            continue
        print(f"{i + 1} -> {permutation}")


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
                root_buffer.clear()
                mouse_buffer.clear()
                creating_trayectory = True

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == pygame.BUTTON_LEFT:
                creating_trayectory = False

                initial_roots = [pixel_to_complex(*points[0]) for points in root_buffer]
                final_roots = [pixel_to_complex(*points[-1]) for points in root_buffer]

                check_permutations(initial_roots, final_roots)

    px, py = pygame.mouse.get_pos()
    alpha = pixel_to_complex(px, py)

    coefs = [1, 0, 0, 0, -1, alpha]
    roots = np.roots(coefs)

    if creating_trayectory:
        mouse_point = (px, py)
        # add mouse point if not the same
        if len(mouse_buffer) < 2 or math.dist(mouse_point, mouse_buffer[-1]) > 0.1:
            mouse_buffer.append((px, py))

        points = [complex_to_pixel(z) for z in roots]
        for point in points:
            if len(root_buffer) < len(roots):
                root_buffer.append([point,])
            else:
                # find the list with the closest final point
                closest_list = min(root_buffer, key=lambda buffer_list: math.dist(buffer_list[-1], point))

                # only add if point is not the same
                if len(closest_list) < 2 or math.dist(point, closest_list[-1]) > 0.1:
                    closest_list.append(point)

    # RENDER
    screen.fill(WHITE)
    for point in singular_points:
        plot_complex(point, RED)
    for root in roots:
        plot_complex(complex(root), BLACK)
    if len(root_buffer) > 0 and creating_trayectory:
        # show root trayectories
        for points in root_buffer:
            if len(points) >= 2:
                pygame.draw.lines(surface=screen, color=RED, closed=False, points=points, width=5)
        # show mouse trayectory
        if len(mouse_buffer) >= 2:
            pygame.draw.lines(surface=screen, color=BLUE, closed=False, points=mouse_buffer, width=5)

    screen.blit(text, (tx, ty))

    pygame.display.flip()
