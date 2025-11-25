# Login Page
import pygame
import sys
from Main_page import main_page

pygame.init()

# -------------------------
# Screen setup
# -------------------------
WIDTH, HEIGHT = 1200, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tiny Tails Login")

# -------------------------
# Colors & Fonts
# -------------------------
BG_COLOR = (100, 189, 191)
TITLE_BG = (242, 141, 23)
TITLE_TEXT_COLOR = (255, 243, 216)
INPUT_BG = (255, 243, 216)
INPUT_BORDER = (190, 170, 130)
BUTTON_BG = (42, 107, 128)
BUTTON_TEXT = (255, 255, 255)
LOADING_TEXT = (46, 90, 114)
LOADING_BAR_BG = (42, 107, 128)
LOADING_BAR_FG = (70, 160, 170)
ERROR_TEXT = (200, 50, 50)

font_large = pygame.font.SysFont(None, 72)
font_med = pygame.font.SysFont(None, 40)
font_small = pygame.font.SysFont(None, 28)

# -------------------------
# Pet image
# -------------------------
pet_img = pygame.image.load("pet2.png").convert_alpha()
pet_img = pygame.transform.smoothscale(pet_img, (400, 400))
pet_rect = pet_img.get_rect(center=(900, 250))  # Adjust position as needed

# -------------------------
# InputBox class
# -------------------------
class InputBox:
    def __init__(self, x, y, w, h, placeholder="", default_text=""):


        self.rect = pygame.Rect(x, y, w, h)
        self.color = INPUT_BORDER
        self.text = default_text if default_text else ""
        self.placeholder = placeholder
        self.txt_surface = font_med.render(self.text if self.text else placeholder, True, INPUT_BORDER)
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = True
                self.color = BUTTON_BG
                if self.text == '':
                    self.txt_surface = font_med.render('', True, self.color)
            else:
                self.active = False
                self.color = INPUT_BORDER
                if self.text == '':
                    self.txt_surface = font_med.render(self.placeholder, True, self.color)

        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_RETURN:
                self.active = False
                self.color = INPUT_BORDER
            elif event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            else:
                if len(self.text) < 15:
                    self.text += event.unicode
            if self.text == '':
                self.txt_surface = font_med.render(self.placeholder, True, INPUT_BORDER)
            else:
                self.txt_surface = font_med.render(self.text, True, BUTTON_BG)

    def draw(self, screen):
        pygame.draw.rect(screen, INPUT_BG, self.rect, 0, border_radius=8)
        pygame.draw.rect(screen, self.color, self.rect, 3, border_radius=8)
        screen.blit(self.txt_surface, (self.rect.x + 10, self.rect.y + 8))

# -------------------------
# Input boxes
# -------------------------
username_box = InputBox(100, 180, 300, 50, "Username")
petname_box = InputBox(100, 250, 300, 50, "Pet Name", default_text="Chopper")

# -------------------------
# Draw functions
# -------------------------
def draw_title():
    rect = pygame.Rect(50, 50, 400, 80)
    pygame.draw.rect(screen, TITLE_BG, rect, border_radius=25)
    title1 = font_large.render('TINY', True, TITLE_TEXT_COLOR)
    title2 = font_large.render('TAILS', True, TITLE_TEXT_COLOR)
    screen.blit(title1, (rect.x + 20, rect.y + 5))
    screen.blit(title2, (rect.x + 150, rect.y + 30))

def draw_button():
    btn_rect = pygame.Rect(100, 320, 300, 50)
    pygame.draw.rect(screen, BUTTON_BG, btn_rect, border_radius=10)
    btn_text = font_med.render("Sign Up", True, BUTTON_TEXT)
    screen.blit(btn_text, (btn_rect.x + btn_rect.width//2 - btn_text.get_width()//2, btn_rect.y + 10))
    return btn_rect

def draw_loading_bar(progress):
    bar_bg_rect = pygame.Rect(100, 380, 300, 15)
    pygame.draw.rect(screen, LOADING_BAR_BG, bar_bg_rect, border_radius=8)
    bar_fg_rect = pygame.Rect(100, 380, int(300 * progress), 15)
    pygame.draw.rect(screen, LOADING_BAR_FG, bar_fg_rect, border_radius=8)
    loading_text = font_small.render("Loading...", True, LOADING_TEXT)
    screen.blit(loading_text, (100, 405))

# -------------------------
# Main loop
# -------------------------
def main():
    clock = pygame.time.Clock()
    button = draw_button()
    loading = False
    loading_progress = 0.0
    error_msg = ""

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            username_box.handle_event(event)
            petname_box.handle_event(event)

            if event.type == pygame.MOUSEBUTTONDOWN:
                if button.collidepoint(event.pos):
                    if username_box.text.strip() == "":
                        error_msg = "Please enter your name"
                        loading = False
                    else:
                        error_msg = ""
                        loading = True
                        loading_progress = 0.0

        screen.fill(BG_COLOR)
        draw_title()

        # Pet image
        screen.blit(pet_img, pet_rect)

        # Username label + error
        label_surface = font_small.render("Username:", True, BUTTON_BG)
        screen.blit(label_surface, (username_box.rect.x, username_box.rect.y - 25))
        if error_msg:
            error_surface = font_small.render(error_msg, True, ERROR_TEXT)
            screen.blit(error_surface, (username_box.rect.x + label_surface.get_width() + 10, username_box.rect.y - 25))
        username_box.draw(screen)

        # Pet name input box
        petname_box.draw(screen)

        # Login button
        button = draw_button()

        # Loading bar
        if loading:
            loading_progress += 0.01
            if loading_progress >= 1.0:
                loading_progress = 1.0
                loading = False
                stats = {"Kitchen":50,"Bathroom":50,"Bedroom":50,"Gaming Room":50}
                main_page(username_box.text, petname_box.text, stats)
            draw_loading_bar(loading_progress)

        pygame.display.flip()
        clock.tick(60)

if __name__ == '__main__':
    main()