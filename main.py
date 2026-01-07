import numpy as np
import pygame
import math

pygame.init()
pygame.display.set_caption("Omnibus")
WIDTH, HEIGHT = 800, 600
SCALE = WIDTH // 6
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
font = pygame.Font("assets/FiraCodeNerdFont-Bold.ttf", WIDTH // 30)
point_radius = WIDTH // 100
trayectory_width = point_radius // 4
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
    pygame.draw.aacircle(screen, color, (x, y), point_radius)


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
# mininum distance to add point to trayectory (for efficiency)
minimum_distance = 2
# minimum points to consider trayectory
minimum_points = 20

show_permutations = False
permutations_text = ""

hide_permutations_event = pygame.USEREVENT + 1


def single_permutation(initial_roots, final_roots, index) -> int:
    initial = initial_roots[index]

    # check if similar root
    for i, root in enumerate(final_roots):
        if abs(initial - root) < 0.1:
            return i + 1

    return None


def get_permutations(initial_roots, final_roots) -> str:
    # compare roots
    permutations_text = "\nPermutations:\n"
    assert len(initial_roots) == len(final_roots)
    for i in range(len(initial_roots)):
        permutation = single_permutation(initial_roots, final_roots, i)
        if not permutation:
            permutations_text += f"La raiz {i + 1} no ha permutado"
            continue
        permutations_text += f"{i + 1} -> {permutation}\n"

    return permutations_text


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
                # hide results if want new trayectory
                if show_permutations:
                    show_permutations = False

                root_buffer.clear()
                mouse_buffer.clear()
                creating_trayectory = True
        elif event.type == hide_permutations_event:
            show_permutations = False

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == pygame.BUTTON_LEFT:
                creating_trayectory = False

                # if valid trayectory
                if math.dist(mouse_buffer[0], mouse_buffer[-1]) < 5 and len(mouse_buffer) >= minimum_points:
                    initial_roots = [pixel_to_complex(*points[0]) for points in root_buffer]
                    final_roots = [pixel_to_complex(*points[-1]) for points in root_buffer]

                    permutations_text = get_permutations(initial_roots, final_roots)
                    show_permutations = True
                    pygame.time.set_timer(hide_permutations_event, 5000)

    px, py = pygame.mouse.get_pos()
    alpha = pixel_to_complex(px, py)

    coefs = [1, 0, 0, 0, -1, alpha]
    roots = np.roots(coefs)

    if creating_trayectory:
        mouse_point = (px, py)
        # add mouse point if not the same
        if len(mouse_buffer) < 2 or math.dist(mouse_point, mouse_buffer[-1]) > minimum_distance:
            mouse_buffer.append((px, py))

        points = [complex_to_pixel(z) for z in roots]
        for point in points:
            if len(root_buffer) < len(roots):
                root_buffer.append([point,])
            else:
                # find the list with the closest final point
                closest_list = min(root_buffer, key=lambda buffer_list: math.dist(buffer_list[-1], point))

                # only add if point is not the same
                if len(closest_list) < 2 or math.dist(point, closest_list[-1]) > minimum_distance:
                    closest_list.append(point)

    # RENDER
    screen.fill(WHITE)
    for point in singular_points:
        plot_complex(point, RED)
    for root in roots:
        plot_complex(complex(root), BLACK)
    if creating_trayectory:
        # show root trayectories
        if len(root_buffer) > 0:
            for points in root_buffer:
                if len(points) >= 2:
                    pygame.draw.lines(surface=screen, color=RED, closed=False, points=points, width=trayectory_width)

        # show mouse trayectory
        if len(mouse_buffer) >= 2:
            pygame.draw.lines(surface=screen, color=BLUE, closed=False, points=mouse_buffer, width=trayectory_width)

    if show_permutations:
        permutations_surface = font.render(permutations_text, True, BLACK)
        tam_x, tam_y = permutations_surface.get_size()
        x = (WIDTH - tam_x) // 2
        y = (HEIGHT - tam_y) // 2
        screen.blit(permutations_surface, (x, y))

    screen.blit(text, (tx, ty))

    pygame.display.flip()
