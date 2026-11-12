import pygame
import random
from pathlib import Path

pygame.init()
pygame.mixer.init()
WIDTH, HEIGHT = 900, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Coffee Rush")
CREAM = (255, 239, 209)
BROWN = (102, 59, 37)
LIGHT_BROWN = (196, 139, 94)
DARK_BROWN = (66, 38, 25)
PINK = (240, 156, 167)
GREEN = (112, 158, 112)
TEA_GREEN = (126, 173, 132)
WHITE = (255, 255, 255)
BLACK = (40, 40, 40)
BLUE = (115, 170, 220)
PURPLE = (165, 125, 205)
RED = (220, 80, 80)
YELLOW = (245, 200, 80)
SKIN = (255, 210, 170)
TAN_SKIN = (235, 185, 140)
DARK_SKIN = (142, 98, 70)
title_font = pygame.font.SysFont("arial", 38, bold=True)
text_font = pygame.font.SysFont("arial", 20, bold=True)
small_font = pygame.font.SysFont("arial", 16, bold=True)
large_font = pygame.font.SysFont("arial", 52, bold=True)
# Sounds
sound_folder = Path("assets") / "sounds"
pickup_sound = pygame.mixer.Sound(sound_folder / "pickup-notification.mp3")
success_sound = pygame.mixer.Sound(sound_folder / "success-notification.mp3")
error_sound = pygame.mixer.Sound(sound_folder / "error-notification.mp3")
win_sound = pygame.mixer.Sound(sound_folder / "win-notification.mp3")
game_over_sound = pygame.mixer.Sound(sound_folder / "game-over-notification.mp3")
pickup_sound.set_volume(0.45)
success_sound.set_volume(0.55)
error_sound.set_volume(0.45)
win_sound.set_volume(0.60)
game_over_sound.set_volume(0.60)
pygame.mixer.music.load(sound_folder / "ambience.mp3")
pygame.mixer.music.set_volume(0.25)
items = ["Coffee", "Tea", "Cake"]
levels = [
    {"target": 50, "time": 60, "multiplier": 1},
    {"target": 70, "time": 50, "multiplier": 1.25},
    {"target": 90, "time": 45, "multiplier": 1.5},
]
customers = [
    {"name": "MIA", "shirt": PINK, "hair": DARK_BROWN, "skin": SKIN, "speed": 4},
    {"name": "LEO", "shirt": BLUE, "hair": BROWN, "skin": TAN_SKIN, "speed": 6},
    {"name": "ZOE", "shirt": PURPLE, "hair": BLACK, "skin": DARK_SKIN, "speed": 8},
]
baristas = [
    {"name": "BERRY", "shirt": PINK, "apron": WHITE, "skin": SKIN},
    {"name": "SKY", "shirt": BLUE, "apron": WHITE, "skin": TAN_SKIN},
    {"name": "MINT", "shirt": TEA_GREEN, "apron": PURPLE, "skin": DARK_SKIN},
]
coffee_station = pygame.Rect(35, 300, 200, 150)
tea_station = pygame.Rect(350, 300, 200, 150)
cake_station = pygame.Rect(665, 300, 200, 150)
customer_zone = pygame.Rect(400, 160, 100, 100)
# ---------- Endless Rush settings ---------
# The game never ends. Every served order makes the next customer
# a little more impatient. You lose when 3 customers leave angry.
ENDLESS_LIVES = 3
ENDLESS_SPEED_UP = 0.08  # +8% patience speed per served order
FAST_BONUS = 20  # bonus when you serve while patience > 70%
FAST_LIMIT = 70
HIGHSCORE_FILE = Path("highscore.txt")
# Pause menu
pause_options = ["Resume", "Restart", "How to Play", "Back to Title"]
pause_index = 0
selected_barista = 0
mode = "levels"  # "levels" or "endless"
level = 1
player_x, player_y = 420, 450
player_speed = 5
item_in_hand = None
current_order = random.choice(items)
current_customer = random.choice(customers)
score = 0
time_left = levels[0]["time"]
patience = 100
lives = ENDLESS_LIVES
orders_served = 0
best_score = 0
new_record = False
message = ""
message_timer = 0
state = "menu"
screen_name = "menu"
instructions_from = "menu"  # where ESC on the instructions screen goes back to
music_playing = False
clock = pygame.time.Clock()
running = True


def load_best_score():
    try:
        return int(HIGHSCORE_FILE.read_text().strip())
    except (FileNotFoundError, ValueError):
        return 0


def save_best_score(value):
    HIGHSCORE_FILE.write_text(str(value))


best_score = load_best_score()


def new_customer():
    return random.choice(customers), random.choice(items)


def reset_game():
    global level, player_x, player_y, item_in_hand
    global current_order, current_customer, score, time_left, patience
    global lives, orders_served, new_record
    level = 1
    player_x, player_y = 420, 450
    item_in_hand = None
    current_customer, current_order = new_customer()
    score = 0
    time_left = levels[0]["time"]
    patience = 100
    lives = ENDLESS_LIVES
    orders_served = 0
    new_record = False


def start_game():
    global state, screen_name, music_playing
    reset_game()
    screen_name = "game"
    state = "playing"
    if not music_playing:
        pygame.mixer.music.play(-1)
        music_playing = True


def go_to_title():
    global state, screen_name, music_playing
    pygame.mixer.music.stop()
    music_playing = False
    reset_game()
    state = "menu"
    screen_name = "menu"


def end_game():
    global state, music_playing, best_score, new_record
    state = "game_over"
    pygame.mixer.music.stop()
    music_playing = False
    game_over_sound.play()
    if mode == "endless" and score > best_score:
        best_score = score
        new_record = True
        save_best_score(best_score)


def draw_centered(text, font, y, color=WHITE):
    surface = font.render(text, True, color)
    screen.blit(surface, (WIDTH // 2 - surface.get_width() // 2, y))


def draw_overlay(alpha=185):
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, alpha))
    screen.blit(overlay, (0, 0))


while running:
    delta_time = clock.tick(60) / 1000
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if state == "menu" and screen_name == "menu":
                if event.key == pygame.K_1:
                    selected_barista = 0
                elif event.key == pygame.K_2:
                    selected_barista = 1
                elif event.key == pygame.K_3:
                    selected_barista = 2
                elif event.key == pygame.K_m:
                    mode = "endless" if mode == "levels" else "levels"
                elif event.key == pygame.K_i:
                    instructions_from = "menu"
                    screen_name = "instructions"
                elif event.key == pygame.K_c:
                    screen_name = "credits"
                elif event.key == pygame.K_SPACE:
                    start_game()
            elif screen_name == "instructions":
                if event.key == pygame.K_ESCAPE:
                    if instructions_from == "paused":
                        screen_name = "game"
                    else:
                        screen_name = "menu"
            elif screen_name == "credits":
                if event.key == pygame.K_ESCAPE:
                    screen_name = "menu"
            # ----- Pause menu ----
            elif state == "paused":
                select = False
                if event.key in (pygame.K_UP, pygame.K_w):
                    pause_index = (pause_index - 1) % len(pause_options)
                elif event.key in (pygame.K_DOWN, pygame.K_s):
                    pause_index = (pause_index + 1) % len(pause_options)
                elif event.key in (pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4):
                    pause_index = event.key - pygame.K_1
                    select = True
                elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                    select = True
                if event.key == pygame.K_ESCAPE:
                    state = "playing"
                    pygame.mixer.music.unpause()
                elif select:
                    choice = pause_options[pause_index]
                    if choice == "Resume":
                        state = "playing"
                        pygame.mixer.music.unpause()
                    elif choice == "Restart":
                        reset_game()
                        state = "playing"
                        pygame.mixer.music.unpause()
                    elif choice == "How to Play":
                        instructions_from = "paused"
                        screen_name = "instructions"
                    elif choice == "Back to Title":
                        go_to_title()
            elif state == "level_complete" and event.key == pygame.K_SPACE:
                level += 1
                score = 0
                item_in_hand = None
                current_customer, current_order = new_customer()
                time_left = levels[level - 1]["time"]
                patience = 100
                state = "playing"
            elif state in ["game_over", "won"]:
                if event.key == pygame.K_r:
                    go_to_title()
                elif event.key == pygame.K_SPACE:
                    start_game()
            elif state == "playing" and event.key == pygame.K_SPACE:
                state = "paused"
                pause_index = 0
                pygame.mixer.music.pause()
            elif state == "playing" and event.key == pygame.K_e:
                player_rect = pygame.Rect(player_x, player_y, 38, 45)
                if player_rect.colliderect(coffee_station):
                    item_in_hand = "Coffee"
                    message, message_timer = "You picked up coffee!", 90
                    pickup_sound.play()
                elif player_rect.colliderect(tea_station):
                    item_in_hand = "Tea"
                    message, message_timer = "You picked up tea!", 90
                    pickup_sound.play()
                elif player_rect.colliderect(cake_station):
                    item_in_hand = "Cake"
                    message, message_timer = "You picked up a cake!", 90
                    pickup_sound.play()
                elif player_rect.colliderect(customer_zone):
                    if item_in_hand == current_order:
                        points = 10
                        message = "Order completed! +10 points"
                        if mode == "endless":
                            orders_served += 1
                            if patience > FAST_LIMIT:
                                points += FAST_BONUS
                                message = f"Fast service! +{points} points"
                        score += points
                        item_in_hand = None
                        current_customer, current_order = new_customer()
                        patience = 100
                        message_timer = 120
                        success_sound.play()
                    elif item_in_hand is None:
                        message, message_timer = "You are not holding anything!", 90
                        error_sound.play()
                    else:
                        message, message_timer = (
                            "That is not the customer's order!",
                            120,
                        )
                        error_sound.play()
    if state == "playing":
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            player_x -= player_speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            player_x += player_speed
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            player_y -= player_speed
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            player_y += player_speed
        player_x = max(0, min(player_x, WIDTH - 38))
        player_y = max(100, min(player_y, HEIGHT - 45))
        if mode == "levels":
            time_left -= delta_time
            patience_speed = current_customer["speed"] * levels[level - 1]["multiplier"]
        else:
            # Endless Rush: every served order speeds up the next customer
            patience_speed = current_customer["speed"] * (
                1 + orders_served * ENDLESS_SPEED_UP
            )
        patience -= patience_speed * delta_time
        if patience <= 0:
            patience = 100
            item_in_hand = None
            current_customer, current_order = new_customer()
            error_sound.play()
            if mode == "levels":
                score = max(0, score - 5)
                message, message_timer = "Customer left! -5 points", 120
            else:
                lives -= 1
                message, message_timer = f"Customer left! Lives: {lives}", 120
                if lives <= 0:
                    end_game()
        if mode == "levels":
            if time_left <= 0:
                time_left = 0
                end_game()
            if score >= levels[level - 1]["target"]:
                if level == 3:
                    state = "won"
                    pygame.mixer.music.stop()
                    music_playing = False
                    win_sound.play()
                else:
                    state = "level_complete"
    if message_timer > 0 and state == "playing":
        message_timer -= 1
    # Main game background
    screen.fill(CREAM)
    pygame.draw.rect(screen, (238, 211, 178), (0, 100, WIDTH, HEIGHT - 100))
    pygame.draw.rect(screen, DARK_BROWN, (0, 0, WIDTH, 100))
    title = title_font.render("COFFEE RUSH", True, WHITE)
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 15))
    if screen_name == "game":
        if mode == "levels":
            level_data = levels[level - 1]
            screen.blit(text_font.render(f"Level: {level}", True, WHITE), (30, 35))
            screen.blit(
                text_font.render(f"Score: {score}/{level_data['target']}", True, WHITE),
                (30, 65),
            )
            screen.blit(
                text_font.render(f"Time: {int(time_left)}", True, WHITE), (760, 65)
            )
        else:
            screen.blit(text_font.render("ENDLESS RUSH", True, YELLOW), (30, 35))
            screen.blit(text_font.render(f"Score: {score}", True, WHITE), (30, 65))
            screen.blit(text_font.render(f"Best: {best_score}", True, WHITE), (200, 65))
            screen.blit(
                text_font.render(f"Lives: {'<3 ' * lives}", True, RED), (760, 35)
            )
            screen.blit(
                text_font.render(f"Served: {orders_served}", True, WHITE), (760, 65)
            )
        screen.blit(
            text_font.render(f"Holding: {item_in_hand or 'Nothing'}", True, WHITE),
            (540, 65),
        )
        pygame.draw.rect(screen, WHITE, (330, 110, 240, 58), border_radius=10)
        draw_centered(f"Order: {current_order}", text_font, 118, DARK_BROWN)
        pygame.draw.rect(screen, BLACK, (360, 148, 180, 10), border_radius=5)
        patience_color = GREEN if patience > 35 else RED
        pygame.draw.rect(
            screen,
            patience_color,
            (360, 148, int(180 * patience / 100), 10),
            border_radius=5,
        )
        pygame.draw.rect(screen, BROWN, (110, 160, 680, 85), border_radius=12)
        pygame.draw.rect(screen, LIGHT_BROWN, (110, 160, 680, 18), border_radius=12)
        # Customer
        pygame.draw.circle(screen, current_customer["hair"], (450, 184), 25)
        pygame.draw.circle(screen, current_customer["skin"], (450, 190), 22)
        pygame.draw.circle(screen, BLACK, (442, 188), 3)
        pygame.draw.circle(screen, BLACK, (458, 188), 3)
        pygame.draw.rect(
            screen, current_customer["shirt"], (425, 210, 50, 42), border_radius=10
        )
        customer_name = small_font.render(current_customer["name"], True, WHITE)
        screen.blit(customer_name, (450 - customer_name.get_width() // 2, 230))
        # Stations
        pygame.draw.rect(screen, LIGHT_BROWN, coffee_station, border_radius=12)
        pygame.draw.rect(screen, BLACK, (80, 335, 65, 75), border_radius=8)
        pygame.draw.circle(screen, PINK, (112, 360), 12)
        screen.blit(text_font.render("COFFEE", True, WHITE), (82, 415))
        pygame.draw.rect(screen, TEA_GREEN, tea_station, border_radius=12)
        pygame.draw.rect(screen, WHITE, (410, 350, 75, 45), border_radius=8)
        pygame.draw.rect(screen, GREEN, (418, 355, 58, 30), border_radius=5)
        screen.blit(text_font.render("TEA", True, WHITE), (425, 415))
        pygame.draw.rect(screen, PINK, cake_station, border_radius=12)
        pygame.draw.rect(screen, WHITE, (700, 350, 125, 50), border_radius=8)
        pygame.draw.circle(screen, BROWN, (730, 375), 15)
        pygame.draw.circle(screen, LIGHT_BROWN, (790, 375), 15)
        screen.blit(text_font.render("CAKES", True, WHITE), (725, 415))
        # Player
        barista = baristas[selected_barista]
        pygame.draw.circle(screen, barista["skin"], (player_x + 19, player_y + 13), 13)
        pygame.draw.rect(
            screen,
            barista["shirt"],
            (player_x + 6, player_y + 25, 26, 20),
            border_radius=5,
        )
        pygame.draw.rect(
            screen, barista["apron"], (player_x + 12, player_y + 27, 14, 18)
        )
        if item_in_hand == "Coffee":
            pygame.draw.rect(screen, DARK_BROWN, (player_x + 14, player_y - 15, 12, 12))
        elif item_in_hand == "Tea":
            pygame.draw.rect(screen, GREEN, (player_x + 13, player_y - 15, 14, 12))
        elif item_in_hand == "Cake":
            pygame.draw.circle(screen, PINK, (player_x + 19, player_y - 10), 9)
        draw_centered("E: pick up / deliver     SPACE: pause", small_font, 555, BLACK)
        if message_timer > 0:
            draw_centered(message, small_font, 520, DARK_BROWN)
    # Menu
    if screen_name == "menu":
        draw_overlay()
        draw_centered("COFFEE RUSH", large_font, 165)
        if mode == "levels":
            draw_centered("Mode: LEVELS  -  complete all three levels!", text_font, 240)
        else:
            draw_centered(
                f"Mode: ENDLESS RUSH  -  survive as long as you can!  Best: {best_score}",
                text_font,
                240,
                YELLOW,
            )
        draw_centered("Press M to change mode", small_font, 270)
        draw_centered(
            f"Selected Barista: {baristas[selected_barista]['name']}", text_font, 315
        )
        draw_centered("1: Berry     2: Sky     3: Mint", small_font, 350)
        draw_centered("Press I: Instructions     Press C: Credits", small_font, 385)
        draw_centered("Press SPACE to start", text_font, 430)
    # Instructions
    elif screen_name == "instructions":
        draw_overlay(210)
        draw_centered("HOW TO PLAY", large_font, 105)
        instruction_lines = [
            "Move with Arrow Keys or WASD.",
            "Press E near a station to pick up an item.",
            "Bring the correct order to the customer.",
            "Press SPACE during the game to pause.",
            "LEVELS: reach the target score before time runs out.",
            "ENDLESS RUSH: no timer. Customers get faster and faster.",
            "Lose 3 customers and it's game over. Fast service = +20!",
        ]
        for index, line in enumerate(instruction_lines):
            draw_centered(line, text_font, 190 + index * 40)
        back_to = "pause menu" if instructions_from == "paused" else "menu"
        draw_centered(f"Press ESC to return to the {back_to}", text_font, 500)
    # Credits
    elif screen_name == "credits":
        draw_overlay(210)
        draw_centered("CREDITS", large_font, 145)
        draw_centered("Coffee Rush", text_font, 245)
        draw_centered("Created by: Group 5", text_font, 290)
        draw_centered("Made with Python and Pygame-ce", text_font, 335)
        draw_centered("2026", text_font, 380)
        draw_centered("Press ESC to return to the menu", text_font, 465)
    # Pause menu
    if state == "paused" and screen_name == "game":
        draw_overlay(170)
        draw_centered("PAUSED", large_font, 150)
        for index, option in enumerate(pause_options):
            y = 240 + index * 50
            if index == pause_index:
                pygame.draw.rect(
                    screen, YELLOW, (330, y - 8, 240, 42), border_radius=10
                )
                draw_centered(f"{index + 1}. {option}", text_font, y, DARK_BROWN)
            else:
                draw_centered(f"{index + 1}. {option}", text_font, y)
        draw_centered("Up/Down + ENTER   or   1-4     ESC: resume", small_font, 460)
    # Level complete screen
    if state == "level_complete":
        draw_overlay(180)
        draw_centered("LEVEL COMPLETE!", large_font, 220)
        draw_centered(f"Get ready for Level {level + 1}", text_font, 290)
        draw_centered("Press SPACE to continue", text_font, 330)
    # End screens
    elif state == "game_over":
        draw_overlay(180)
        draw_centered("GAME OVER", large_font, 200)
        if mode == "levels":
            draw_centered(f"You reached Level {level}", text_font, 270)
        else:
            draw_centered(
                f"Score: {score}     Orders served: {orders_served}", text_font, 270
            )
            if new_record:
                draw_centered("NEW RECORD!", title_font, 305, YELLOW)
            else:
                draw_centered(f"Best: {best_score}", text_font, 305)
        draw_centered("SPACE: play again     R: back to menu", text_font, 360)
    elif state == "won":
        draw_overlay(180)
        draw_centered("YOU WIN!", large_font, 220)
        draw_centered("You completed every level!", text_font, 290)
        draw_centered("SPACE: play again     R: back to menu", text_font, 330)
    pygame.display.flip()
pygame.quit()
