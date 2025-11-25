import pygame
import sqlite3
import sys

# Initialize Pygame
pygame.init()

# Screen setup
WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pet App")

# Colors
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
BLACK = (0, 0, 0)
BLUE = (100, 149, 237)

# Fonts
font = pygame.font.SysFont(None, 32)

# Database setup
conn = sqlite3.connect("Sql_db.db")
cursor = conn.cursor()
cursor.execute('''
CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    petname TEXT
)
''')
conn.commit()

# Login fields
username = ""
petname = ""
active_field = None

# Sidebar
sidebar_open = False
sidebar_rect = pygame.Rect(0, 0, 200, HEIGHT)

# Buttons
admin_button_rect = pygame.Rect(10, 10, 40, 40)
signout_button_rect = pygame.Rect(50, 200, 100, 40)

current_user = None

def draw_login():
    screen.fill(WHITE)
    # Username box
    pygame.draw.rect(screen, GRAY, (200, 100, 200, 40))
    txt_surface = font.render(username, True, BLACK)
    screen.blit(txt_surface, (210, 110))
    # Petname box
    pygame.draw.rect(screen, GRAY, (200, 160, 200, 40))
    txt_surface2 = font.render(petname, True, BLACK)
    screen.blit(txt_surface2, (210, 170))
    # Login button
    pygame.draw.rect(screen, BLUE, (250, 240, 100, 40))
    login_txt = font.render("Login", True, WHITE)
    screen.blit(login_txt, (270, 250))

def draw_main():
    screen.fill(WHITE)
    # Admin button
    pygame.draw.rect(screen, BLUE, admin_button_rect)
    screen.blit(font.render("A", True, WHITE), (20, 15))
    # Sidebar
    if sidebar_open:
        pygame.draw.rect(screen, GRAY, sidebar_rect)
        if current_user:
            screen.blit(font.render(f"User: {current_user[1]}", True, BLACK), (20, 50))
            screen.blit(font.render(f"Pet: {current_user[2]}", True, BLACK), (20, 100))
            pygame.draw.rect(screen, BLUE, signout_button_rect)
            screen.blit(font.render("Sign Out", True, WHITE), (55, 210))

def login_user():
    global current_user
    cursor.execute("INSERT INTO PetStats(user_name, pet_name) VALUES (?,?)", (username, petname))
    conn.commit()
    cursor.execute("SELECT * FROM PetStats ORDER BY id DESC LIMIT 1")
    current_user = cursor.fetchone()

running = True
on_login = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if on_login:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if 200 <= event.pos[0] <= 400 and 100 <= event.pos[1] <= 140:
                    active_field = "username"
                elif 200 <= event.pos[0] <= 400 and 160 <= event.pos[1] <= 200:
                    active_field = "petname"
                elif 250 <= event.pos[0] <= 350 and 240 <= event.pos[1] <= 280:
                    if username.strip() and petname.strip():
                        login_user()
                        on_login = False
            if event.type == pygame.KEYDOWN and active_field:
                if event.key == pygame.K_BACKSPACE:
                    if active_field == "username":
                        username = username[:-1]
                    else:
                        petname = petname[:-1]
                else:
                    if active_field == "username":
                        username += event.unicode
                    else:
                        petname += event.unicode
        else:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if admin_button_rect.collidepoint(event.pos):
                    sidebar_open = not sidebar_open
                if sidebar_open and signout_button_rect.collidepoint(event.pos):
                    current_user = None
                    username = ""
                    petname = ""
                    on_login = True
                    sidebar_open = False

    if on_login:
        draw_login()
    else:
        draw_main()

    pygame.display.flip()

pygame.quit()
conn.close()
sys.exit()