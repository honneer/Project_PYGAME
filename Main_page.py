import pygame
import sys
import math
import subprocess
from pygame import mixer
from Kitchen import kitchen_page
from Bathroom import bathroom_page
from Bedroom import bedroom_page

# ================= MAIN PAGE =================
def main_page(username, pet_name, stats):
    pygame.init()
    mixer.init()

    # Play background music on loop
    mixer.music.load("morning.mp3")
    mixer.music.play(-1)

    WIDTH, HEIGHT = 1200, 700
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Tiny Tails: Lawn Area")

    # Background
    bg_img = pygame.image.load("mainpage.jpg").convert()
    bg_img = pygame.transform.smoothscale(bg_img, (WIDTH, HEIGHT))

    # Two pet images (eyes open & eyes closed)
    pet_open = pygame.image.load("pet2.png").convert()
    pet_open.set_colorkey((0, 0, 0))
    pet_open = pygame.transform.scale(pet_open, (300, 300))

    pet_closed = pygame.image.load("pet_closed.png").convert()
    pet_closed.set_colorkey((0, 0, 0))
    pet_closed = pygame.transform.scale(pet_closed, (300, 300))

    # Start with open eyes
    pet_img = pet_open
    pet_rect = pet_img.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 150))

    # Colors
    BLUE = (70, 130, 180)
    XP_BG = (180, 180, 180)
    XP_FILL = (100, 200, 250)

    # Buttons (cx, cy, radius)
    buttons = [
        (190, HEIGHT - 80, 40),
        (420, HEIGHT - 80, 40),
        (650, HEIGHT - 80, 40),
        (880, HEIGHT - 80, 40)
    ]

    # Load icons
    kitchen_icon = pygame.image.load("burger.png").convert_alpha()
    bathroom_icon = pygame.image.load("bath.png").convert_alpha()
    bedroom_icon = pygame.image.load("bedd.png").convert_alpha()
    gaming_icon = pygame.image.load("console.png").convert_alpha()
    icons = [
        pygame.transform.smoothscale(kitchen_icon, (70, 70)),
        pygame.transform.smoothscale(bathroom_icon, (70, 70)),
        pygame.transform.smoothscale(bedroom_icon, (70, 70)),
        pygame.transform.smoothscale(gaming_icon, (70, 70))
    ]

    labels = ["Kitchen", "Bathroom", "Bedroom", "Gaming Room"]

    # XP / Level System
    stats.setdefault("XP", 0)
    stats.setdefault("Level", 1)

    font = pygame.font.SysFont(None, 36)
    clock = pygame.time.Clock()

    # Timer for blinking
    blink_timer = 0
    blink_interval = 1500  # milliseconds
    eyes_open = True

    running = True
    while running:
        dt = clock.tick(60)
        blink_timer += dt

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                mixer.music.stop()
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                for i, (cx, cy, r) in enumerate(buttons):
                    if math.hypot(mouse_x - cx, mouse_y - cy) <= r:
                        mixer.music.stop()
                        if labels[i] == "Kitchen":
                            kitchen_page(username, pet_name, stats)
                        elif labels[i] == "Bathroom":
                            bathroom_page(username, pet_name, stats)
                        elif labels[i] == "Bedroom":
                            bedroom_page(username, pet_name, stats)
                        elif labels[i] == "Gaming Room":
                            # close this window and open the game
                            pygame.quit()
                            subprocess.Popen(["python", "gameCPT.py"])
                            sys.exit()

        # Blink eyes every 1.5 sec
        if blink_timer >= blink_interval:
            eyes_open = not eyes_open
            pet_img = pet_open if eyes_open else pet_closed
            blink_timer = 0

        # Draw
        screen.blit(bg_img, (0, 0))
        screen.blit(pet_img, pet_rect)

        # Buttons
        for i, (cx, cy, r) in enumerate(buttons):
            pygame.draw.circle(screen, BLUE, (cx, cy), r)
            icon_rect = icons[i].get_rect(center=(cx, cy))
            screen.blit(icons[i], icon_rect)

        # XP Bar
        xp_bar_width = 400
        xp_bar_height = 20
        xp_x = WIDTH // 2 - xp_bar_width // 2
        xp_y = 30
        pygame.draw.rect(screen, XP_BG, (xp_x, xp_y, xp_bar_width, xp_bar_height), border_radius=10)

        xp_needed = stats["Level"] * 100
        xp_fill = min(1.0, stats["XP"] / xp_needed)
        fill_width = int(xp_fill * xp_bar_width)
        pygame.draw.rect(screen, XP_FILL, (xp_x, xp_y, fill_width, xp_bar_height), border_radius=10)

        xp_text = font.render(f"XP: {stats['XP']} / {xp_needed}", True, (0, 0, 0))
        lvl_text = font.render(f"Level {stats['Level']}", True, (0, 0, 0))
        screen.blit(xp_text, (xp_x, xp_y + xp_bar_height + 5))
        screen.blit(lvl_text, (xp_x + xp_bar_width + 20, xp_y - 5))

        # Level up check
        if stats["XP"] >= xp_needed:
            stats["XP"] -= xp_needed
            stats["Level"] += 1
            print(f"{pet_name} leveled up! Now Level {stats['Level']}")

        pygame.display.flip()


if __name__ == "__main__":
    username = "Player1"
    pet_name = "Chopper"
    stats = {}
    main_page(username, pet_name, stats)
