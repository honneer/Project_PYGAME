# Bathroom
import pygame
import sys

def bathroom_page(username, pet_name, stats):
    pygame.init()

    # Window size
    WIDTH, HEIGHT = 1200, 700
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Bathroom")

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

    try:
        shower_sound = pygame.mixer.Sound("shower.mp3")
    except:
        shower_sound = None

    # -----------------------------
    # Load images
    # -----------------------------
    bathroom_bg = pygame.image.load("bathroom.png").convert_alpha()
    bathtub_scene = pygame.image.load("bathtub.png").convert_alpha()
    toilet_scene = pygame.image.load("toilet.jpg").convert_alpha()
    happy_after_pooping = pygame.image.load("toilet_happy.png").convert_alpha()

    # 🩵 Pet (Chopper) blinking images
    chopper_open = pygame.image.load("pet2.png").convert_alpha()
    chopper_close = pygame.image.load("pet_closed.png").convert_alpha()

    # Resize everything
    bathroom_bg = pygame.transform.scale(bathroom_bg, (WIDTH, HEIGHT))
    bathtub_scene = pygame.transform.scale(bathtub_scene, (WIDTH, HEIGHT))
    toilet_scene = pygame.transform.scale(toilet_scene, (WIDTH, HEIGHT))
    happy_after_pooping = pygame.transform.scale(happy_after_pooping, (WIDTH, HEIGHT))

    chopper_width, chopper_height = 315, 330
    chopper_open = pygame.transform.scale(chopper_open, (chopper_width, chopper_height))
    chopper_close = pygame.transform.scale(chopper_close, (chopper_width, chopper_height))

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

    # Blinking setup
    blink_interval = 1000  # milliseconds
    last_blink_time = pygame.time.get_ticks()
    pet_eye_open = True

    clock = pygame.time.Clock()

    def draw_scene():
        """Draw everything depending on mode."""
        # 🛁 Bathtub scene
        if bath_mode:
            screen.blit(bathtub_scene, (0, 0))

        # 🚽 Toilet scene
        elif toilet_mode:
            screen.blit(toilet_scene, (0, 0))

        # 🚿 Neutral bathroom with blinking chopper
        else:
            screen.blit(bathroom_bg, (0, 0))
            if pet_eye_open:
                screen.blit(chopper_open, (chopper_x, chopper_y))
            else:
                screen.blit(chopper_close, (chopper_x, chopper_y))

        # XP Bar
        font = pygame.font.SysFont(None, 36)
        bar_width = 300
        bar_height = 25
        bar_x = WIDTH - bar_width - 50
        bar_y = 30
        pygame.draw.rect(screen, (180, 180, 180), (bar_x, bar_y, bar_width, bar_height), border_radius=8)

        xp_ratio = min(stats["XP"] / (stats["Level"] * 100), 1)
        fill_width = int(bar_width * xp_ratio)
        pygame.draw.rect(screen, (0, 255, 0), (bar_x, bar_y, fill_width, bar_height), border_radius=8)

        level_text = font.render(f"Level {stats['Level']}", True, (0, 0, 0))
        screen.blit(level_text, (bar_x, bar_y - 30))

    # -----------------------------
    # Main Loop
    # -----------------------------
    running = True
    while running:
        current_time = pygame.time.get_ticks()

        # Update blink if neutral mode only
        if not bath_mode and not toilet_mode:
            if current_time - last_blink_time >= blink_interval:
                pet_eye_open = not pet_eye_open
                last_blink_time = current_time

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                return

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = pygame.mouse.get_pos()

                # 🏠 Exit to main page
                if house_rect.collidepoint(mouse_pos):
                    if shower_sound:
                        shower_sound.stop()
                    running = False
                    return

                # 🛁 Bathtub click toggle
                if bathtub_rect.collidepoint(mouse_pos):
                    toilet_mode = False  # disable toilet mode
                    bath_mode = not bath_mode

                    if bath_mode:
                        if shower_sound:
                            shower_sound.play(-1)
                        # Add XP
                        stats["XP"] += 5
                        xp_needed = stats["Level"] * 100
                        if stats["XP"] >= xp_needed:
                            stats["XP"] -= xp_needed
                            stats["Level"] += 1
                    else:
                        if shower_sound:
                            shower_sound.stop()

                # 🚽 Toilet click toggle
                if toilet_rect.collidepoint(mouse_pos):
                    bath_mode = False
                    if shower_sound:
                        shower_sound.stop()

                    toilet_mode = not toilet_mode

                    if toilet_mode:
                        if flush_sound:
                            flush_sound.play()
                        # Add XP
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
