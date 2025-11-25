# Bathroom
import pygame
import sys

def bathroom_page(username, pet_name, stats):
    pygame.init()

    # Window size
    WIDTH, HEIGHT = 1200, 700
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Bathroom Bathing Scene")

    # -----------------------------
    # Load sounds
    # -----------------------------
    try:
        splash_sound = pygame.mixer.Sound("water.mp3")
    except:
        splash_sound = None

    try:
        flush_sound = pygame.mixer.Sound("flush.mp3")
    except:
        flush_sound = None

    # ✅ NEW: shower loop sound
    try:
        shower_sound = pygame.mixer.Sound("shower.mp3")
    except:
        shower_sound = None

    # Load images
    bathroom_bg = pygame.image.load("bathroom.png").convert_alpha()
    bathtub_scene = pygame.image.load("bathtub.png").convert_alpha()
    chopper = pygame.image.load("pet2.png").convert()

    toilet_scene = pygame.image.load("toilet.png").convert_alpha()
    happy_after_pooping = pygame.image.load("toilet_happy.png").convert_alpha()

    chopper.set_colorkey((0, 0, 0))

    # Resize images
    bathroom_bg = pygame.transform.scale(bathroom_bg, (WIDTH, HEIGHT))
    bathtub_scene = pygame.transform.scale(bathtub_scene, (WIDTH, HEIGHT))
    toilet_scene = pygame.transform.scale(toilet_scene, (WIDTH, HEIGHT))
    happy_after_pooping = pygame.transform.scale(happy_after_pooping, (WIDTH, HEIGHT))

    chopper_width, chopper_height = 300, 275
    chopper = pygame.transform.scale(chopper, (chopper_width, chopper_height))
    chopper_x = (WIDTH - chopper_width) // 2
    chopper_y = (HEIGHT - chopper_height) // 2 + 150

    bathtub_rect = pygame.Rect(700, 400, 250, 200)
    toilet_rect = pygame.Rect(100, 400, 150, 150)

    house_rect = pygame.Rect(50, 500, 150, 150)

    # -----------------------------
    # Modes
    # -----------------------------
    bath_mode = False
    toilet_mode = False

    clock = pygame.time.Clock()

    def draw_scene():
        # Bathtub Open
        if bath_mode:
            screen.blit(bathtub_scene, (0, 0))

        # Toilet Open
        elif toilet_mode:
            screen.blit(toilet_scene, (0, 0))

        # Neutral Bathroom
        else:
            screen.blit(bathroom_bg, (0, 0))
            screen.blit(chopper, (chopper_x, chopper_y))

        # XP bar
        font = pygame.font.SysFont(None, 36)
        bar_width = 300
        bar_height = 25
        bar_x = WIDTH - bar_width - 50
        bar_y = 30

        pygame.draw.rect(screen, (180, 180, 180),
                         (bar_x, bar_y, bar_width, bar_height), border_radius=8)

        xp_ratio = min(stats["XP"] / (stats["Level"] * 100), 1)
        fill_width = int(bar_width * xp_ratio)
        pygame.draw.rect(screen, (0, 255, 0),
                         (bar_x, bar_y, fill_width, bar_height), border_radius=8)

        level_text = font.render(f"Level {stats['Level']}", True, (0, 0, 0))
        screen.blit(level_text, (bar_x, bar_y - 30))

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                return

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = pygame.mouse.get_pos()

                # Exit to main
                if house_rect.collidepoint(mouse_pos):

                    # ✅ STOP shower if leaving page
                    if shower_sound:
                        shower_sound.stop()

                    running = False
                    return

                # ✅ BATHTUB CLICK (TOGGLE)
                if bathtub_rect.collidepoint(mouse_pos):
                    toilet_mode = False  # turn off toilet

                    # Toggle bath mode
                    bath_mode = not bath_mode

                    if bath_mode:
                        # ✅ Start shower loop
                        if shower_sound:
                            shower_sound.play(-1)  # loop forever

                        # XP add
                        stats["XP"] += 5
                        xp_needed = stats["Level"] * 100
                        if stats["XP"] >= xp_needed:
                            stats["XP"] -= xp_needed
                            stats["Level"] += 1

                    else:
                        # ✅ Stop shower when exiting bathtub
                        if shower_sound:
                            shower_sound.stop()

                # ✅ TOILET CLICK (TOGGLE)
                if toilet_rect.collidepoint(mouse_pos):
                    bath_mode = False  # turn off bath

                    # ✅ Stop shower if toilet clicked
                    if shower_sound:
                        shower_sound.stop()

                    toilet_mode = not toilet_mode

                    if toilet_mode:
                        if flush_sound:
                            flush_sound.play()

                        # XP add
                        stats["XP"] += 5
                        xp_needed = stats["Level"] * 100
                        if stats["XP"] >= xp_needed:
                            stats["XP"] -= xp_needed
                            stats["Level"] += 1

        draw_scene()
        pygame.display.update()
        clock.tick(60)

    pygame.quit()
    sys.exit()
