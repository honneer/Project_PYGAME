# Kitchen
import warnings
warnings.filterwarnings('ignore', category=UserWarning, module='distutils')

from Sql_db import feed_pet, play_game, print_pet_stats
import pygame
import sys
import os

def remove_near_white(surface, threshold=30):
    surface = surface.convert_alpha()
    w, h = surface.get_size()
    for x in range(w):
        for y in range(h):
            r, g, b, a = surface.get_at((x, y))
            if r > 255 - threshold and g > 255 - threshold and b > 255 - threshold:
                surface.set_at((x, y), (255, 255, 255, 0))
    return surface

def remove_near_black(surface, threshold=30):
    surface = surface.convert_alpha()
    w, h = surface.get_size()
    for x in range(w):
        for y in range(h):
            r, g, b, a = surface.get_at((x, y))
            if r < threshold and g < threshold and b < threshold:
                surface.set_at((x, y), (0, 0, 0, 0))
    return surface

def kitchen_page(username, pet_name, stats):
    pygame.init()
    pygame.mixer.init()

    WIDTH, HEIGHT = 1200, 700
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Kitchen")

    clock = pygame.time.Clock()

    # Image paths
    bg_path = "kitchen.png"
    fridge_open_path = "opendoor.png"
    pet_open_path = "pet2.png"
    pet_close_path = "pet_closed.png"

    food_paths = {
        "burger": "burger.png",
        "icecream": "icecream.jpg",
        "cake": "cake.jpg",
        "watermelon": "watermelon.jpg"
    }

    munch_sound_path = "munch.mp3"

    # ✅ Check files exist
    missing_files = [path for path in [bg_path, pet_open_path, pet_close_path, fridge_open_path, munch_sound_path] + list(food_paths.values()) if not os.path.isfile(path)]
    if missing_files:
        print("Missing files:", missing_files)
        return

    # Load images
    bg_closed = pygame.image.load(bg_path).convert()
    bg_open = pygame.image.load(fridge_open_path).convert()

    pet_open_img = pygame.image.load(pet_open_path).convert_alpha()
    pet_close_img = pygame.image.load(pet_close_path).convert_alpha()
    pet_open_img = pygame.transform.smoothscale(pet_open_img, (300, 300))
    pet_close_img = pygame.transform.smoothscale(pet_close_img, (300, 300))
    pet_rect = pet_open_img.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 150))

    bg_closed = pygame.transform.smoothscale(bg_closed, (WIDTH, HEIGHT))
    bg_open = pygame.transform.smoothscale(bg_open, (WIDTH, HEIGHT))

    fridge_rect = pygame.Rect(1000, 100, 250, 400)
    table_positions = [(180, 380), (250, 360), (310, 370), (380, 380)]

    # Load munch sound
    munch_sound = pygame.mixer.Sound(munch_sound_path)
    munch_sound.set_volume(0.6)  # not too loud

    # Foods setup
    foods = {}
    for idx, (name, path) in enumerate(food_paths.items()):
        img = pygame.image.load(path).convert_alpha()
        img = remove_near_black(img, threshold=40)
        img = pygame.transform.smoothscale(img, (100, 100))
        rect = img.get_rect(center=table_positions[idx])
        foods[name] = {
            "img": img,
            "rect": rect,
            "visible": False,
            "state": "idle",
            "orig_pos": rect.center,
            "pause_timer": 0
        }

    house_rect = pygame.Rect(50, 500, 150, 150)
    fridge_opened = False
    fridge_timer = 0

    # 💤 Pet blinking
    blink_interval = 1000
    last_blink_time = pygame.time.get_ticks()
    pet_eye_open = True

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                return

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos

                if house_rect.collidepoint(mouse_pos):
                    running = False
                    return

                # ✅ Fridge Toggle
                if fridge_rect.collidepoint(mouse_pos):
                    if fridge_opened:
                        fridge_opened = False
                        for food in foods.values():
                            food["visible"] = False
                            food["state"] = "idle"
                            food["rect"].center = food["orig_pos"]
                    else:
                        fridge_opened = True
                        fridge_timer = pygame.time.get_ticks()

                # ✅ Food click logic
                for food in foods.values():
                    if food["visible"] and food["rect"].collidepoint(mouse_pos) and food["state"] == "idle":
                        food["state"] = "moving_to_pet"
                        # 🎵 Play munch sound
                        munch_sound.play(-1)  # loop while moving

        # Show foods after fridge opens
        if fridge_opened and pygame.time.get_ticks() - fridge_timer > 1000:
            for food in foods.values():
                food["visible"] = True

        # ✅ Food animation logic
        for food in foods.values():
            if food["state"] == "moving_to_pet":
                dx = pet_rect.centerx - food["rect"].centerx
                dy = pet_rect.centery - food["rect"].centery - 30
                distance = (dx ** 2 + dy ** 2) ** 0.5
                speed = 7

                if distance < speed:
                    food["state"] = "paused"
                    food["pause_timer"] = pygame.time.get_ticks()

                    # Stop munch sound when reaching Chopper
                    munch_sound.stop()

                    # Update stats and DB
                    feed_pet(user_id=1, user_name=username, pet_name=pet_name, times=1)
                    play_game(user_id=1, user_name=username, pet_name=pet_name, session_score=5, times=1)
                    print_pet_stats(user_id=1)

                    stats["XP"] += 5
                    xp_needed = stats["Level"] * 100
                    if stats["XP"] >= xp_needed:
                        stats["XP"] -= xp_needed
                        stats["Level"] += 1

                else:
                    food["rect"].x += dx / distance * speed
                    food["rect"].y += dy / distance * speed

            elif food["state"] == "paused":
                if pygame.time.get_ticks() - food["pause_timer"] > 500:
                    food["state"] = "returning"

            elif food["state"] == "returning":
                dx = food["orig_pos"][0] - food["rect"].centerx
                dy = food["orig_pos"][1] - food["rect"].centery
                distance = (dx ** 2 + dy ** 2) ** 0.5
                speed = 7
                if distance < speed:
                    food["rect"].center = food["orig_pos"]
                    food["state"] = "idle"
                else:
                    food["rect"].x += dx / distance * speed
                    food["rect"].y += dy / distance * speed

        # 💤 Pet blink
        current_time = pygame.time.get_ticks()
        if current_time - last_blink_time >= blink_interval:
            pet_eye_open = not pet_eye_open
            last_blink_time = current_time

        # Background
        screen.blit(bg_open if fridge_opened else bg_closed, (0, 0))

        # Draw foods
        for food in foods.values():
            if food["visible"]:
                screen.blit(food["img"], food["rect"])

        # Draw pet
        screen.blit(pet_open_img if pet_eye_open else pet_close_img, pet_rect)

        # XP bar + stats (removed hunger)
        font = pygame.font.SysFont(None, 36)

        bar_width = 300
        bar_height = 25
        bar_x = WIDTH - bar_width - 50
        bar_y = 30
        pygame.draw.rect(screen, (180, 180, 180), (bar_x, bar_y, bar_width, bar_height), border_radius=8)
        xp_ratio = stats["XP"] / (stats["Level"] * 100)
        fill_width = int(bar_width * xp_ratio)
        pygame.draw.rect(screen, (0, 255, 0), (bar_x, bar_y, fill_width, bar_height), border_radius=8)
        level_text = font.render(f"Level {stats['Level']}", True, (0, 0, 0))
        screen.blit(level_text, (bar_x, bar_y - 30))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()
