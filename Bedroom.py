# Bedroom
import pygame
import sys
from pygame import mixer

def bedroom_page(username, pet_name, stats):
    pygame.init()
    mixer.init()

    WIDTH, HEIGHT = 1200, 700
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Bedroom")

    # ---------------------------------
    # Load images
    # ---------------------------------
    day_img = pygame.image.load("day_bedroom.png")
    night_img = pygame.image.load("night_bedroom.png")

    # Scale them to fit window
    day_img = pygame.transform.scale(day_img, (WIDTH, HEIGHT))
    night_img = pygame.transform.scale(night_img, (WIDTH, HEIGHT))

    # Clickable areas
    lamp_rect = pygame.Rect(150, 400, 120, 150)   # Lamp area
    house_rect = pygame.Rect(50, 500, 150, 150)   # House area

    # ---------------------------------
    # Load sounds
    # ---------------------------------
    try:
        night_music = pygame.mixer.Sound("night.mp3")
    except:
        night_music = None

    is_night = False
    transitioning = False
    fade_alpha = 0
    fade_speed = 5  # Higher = faster transition

    clock = pygame.time.Clock()
    running = True

    while running:
        dt = clock.tick(60)  # Limit to 60 FPS, get delta time
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # Stop music when quitting
                if night_music:
                    night_music.stop()
                running = False
                return

            if event.type == pygame.MOUSEBUTTONDOWN:
                # Click house → return to main page
                if house_rect.collidepoint(event.pos):
                    # Stop music when leaving
                    if night_music:
                        night_music.stop()
                    running = False
                    return

                # Click lamp → toggle day/night & increase XP
                if lamp_rect.collidepoint(event.pos) and not transitioning:
                    transitioning = True
                    fade_alpha = 0
                    is_night = not is_night

                    # Play or stop music depending on night/day
                    if is_night:
                        if night_music:
                            night_music.play(-1)  # Loop forever
                    else:
                        if night_music:
                            night_music.stop()

                    # --- Activity XP reward ---
                    stats["XP"] += 5
                    xp_needed = stats["Level"] * 100
                    if stats["XP"] >= xp_needed:
                        stats["XP"] -= xp_needed
                        stats["Level"] += 1

        # ---------------------------------
        # Scene transition logic
        # ---------------------------------
        if not transitioning:
            if is_night:
                screen.blit(night_img, (0, 0))
            else:
                screen.blit(day_img, (0, 0))
        else:
            # Show previous + fading into new
            if is_night:
                screen.blit(day_img, (0, 0))
                fade_surface = night_img.copy()
            else:
                screen.blit(night_img, (0, 0))
                fade_surface = day_img.copy()

            fade_surface.set_alpha(fade_alpha)
            screen.blit(fade_surface, (0, 0))

            fade_alpha += fade_speed * (dt / 16)  # Frame-rate independent
            if fade_alpha >= 255:
                transitioning = False

        # ---------------------------------
        # Draw XP bar
        # ---------------------------------
        font = pygame.font.SysFont(None, 36)
        bar_width = 300
        bar_height = 25
        bar_x = WIDTH - bar_width - 50
        bar_y = 30

        pygame.draw.rect(screen, (180, 180, 180), (bar_x, bar_y, bar_width, bar_height), border_radius=8)

        xp_ratio = min(stats["XP"] / (stats["Level"] * 100), 1)  # Prevent overflow
        fill_width = int(bar_width * xp_ratio)
        pygame.draw.rect(screen, (0, 255, 0), (bar_x, bar_y, fill_width, bar_height), border_radius=8)

        level_text = font.render(f"Level {stats['Level']}", True, (0, 0, 0))
        screen.blit(level_text, (bar_x, bar_y - 30))

        # ---------------------------------
        # Debug: show clickable areas (optional)
        # ---------------------------------
        # pygame.draw.rect(screen, (255, 0, 0), lamp_rect, 2)
        # pygame.draw.rect(screen, (0, 0, 255), house_rect, 2)

        pygame.display.flip()

    pygame.quit()
    sys.exit()
