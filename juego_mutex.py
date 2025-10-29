import pygame
import random
import sys
import threading
import time

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Juego de Evasión Multihilo")
clock = pygame.time.Clock()

# Colores
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (65, 105, 225)
BLACK = (0, 0, 0)
DARK_BLUE = (25, 25, 112)
LIGHT_BLUE = (173, 216, 230)

# Fuentes
font = pygame.font.SysFont('Arial', 24)
big_font = pygame.font.SysFont('Arial', 36)

# MUTEX: Candados para proteger variables compartidas
game_state_lock = threading.Lock()  # Protege score, lives, level
enemies_lock = threading.Lock()     # Protege la lista de enemigos
player_lock = threading.Lock()      # Protege posición del jugador

# VARIABLES DEL JUEGO (compartidas entre hilos)
class GameState:
    def __init__(self):
        self.player_x = 400
        self.player_y = 500
        self.player_size = 50
        self.player_speed = 5
        
        self.enemies = []
        self.enemy_size = 30
        self.enemy_speed = 3
        self.enemy_spawn_rate = 20
        
        self.score = 0
        self.lives = 3
        self.level = 1
        self.max_level = 5
        self.game_time = 0
        self.final_score = 0
        
        self.running = True
        self.game_over = False

game = GameState()

# FUNCIONES DE DIBUJO
def draw_text(text, font, color, x, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.center = (x, y)
    screen.blit(text_surface, text_rect)

def draw_player(x, y):
    pygame.draw.rect(screen, BLUE, (x, y, game.player_size, game.player_size), border_radius=10)
    pygame.draw.rect(screen, LIGHT_BLUE, (x + 5, y + 5, game.player_size - 10, game.player_size - 10), border_radius=5)
    pygame.draw.circle(screen, WHITE, (x + 15, y + 15), 5)
    pygame.draw.circle(screen, WHITE, (x + 35, y + 15), 5)
    pygame.draw.arc(screen, WHITE, (x + 10, y + 25, 30, 15), 0, 3.14, 2)

def draw_enemy(x, y):
    pygame.draw.rect(screen, RED, (x, y, game.enemy_size, game.enemy_size), border_radius=8)
    pygame.draw.rect(screen, (255, 150, 150), (x + 5, y + 5, game.enemy_size - 10, game.enemy_size - 10), border_radius=4)
    pygame.draw.line(screen, BLACK, (x + 5, y + 5), (x + game.enemy_size - 5, y + game.enemy_size - 5), 2)
    pygame.draw.line(screen, BLACK, (x + game.enemy_size - 5, y + 5), (x + 5, y + game.enemy_size - 5), 2)

def draw_game_info():
    pygame.draw.rect(screen, (240, 240, 240), (0, 0, 800, 50))
    pygame.draw.line(screen, BLACK, (0, 50), (800, 50), 2)
    
    # Leer con mutex para evitar inconsistencias
    with game_state_lock:
        score_text = game.score
        lives_text = game.lives
        level_text = game.level
        speed_text = game.enemy_speed
    
    draw_text(f"Puntos: {score_text}", font, DARK_BLUE, 100, 25)
    draw_text(f"Vidas: {lives_text}", font, DARK_BLUE, 250, 25)
    draw_text(f"Velocidad: {speed_text:.1f}", font, DARK_BLUE, 450, 25)
    draw_text(f"Nivel: {level_text}", font, DARK_BLUE, 650, 25)

# HILO DE LÓGICA DEL JUEGO
def game_logic_thread():
    """
    Hilo secundario que maneja:
    - Generación de enemigos
    - Movimiento de enemigos
    - Detección de colisiones
    - Actualización de score y nivel
    """
    print("🧵 Hilo de lógica iniciado")
    
    while game.running:
        if not game.game_over:
            # Aumentar dificultad con el tiempo
            with game_state_lock:
                game.game_time += 1
                if game.game_time % 300 == 0:
                    game.enemy_speed += 0.5
                if game.game_time % 600 == 0 and game.enemy_spawn_rate > 5:
                    game.enemy_spawn_rate -= 1
            
            # Verificar subida de nivel
            with game_state_lock:
                if game.score >= game.level * 50 and game.level < game.max_level:
                    game.level += 1
                    game.enemy_speed += 1
                    if game.enemy_spawn_rate > 8:
                        game.enemy_spawn_rate -= 2
            
            # Generar enemigos (MUTEX para acceder a enemies)
            with game_state_lock:
                spawn_rate = game.enemy_spawn_rate
            
            if random.randint(1, spawn_rate) == 1:
                with enemies_lock:
                    game.enemies.append([random.randint(0, 800 - game.enemy_size), 0])
            
            # Mover enemigos y detectar colisiones
            with enemies_lock:
                enemies_to_remove = []
                
                for enemy in game.enemies[:]:
                    enemy[1] += game.enemy_speed
                    
                    # Enemigo salió de la pantalla
                    if enemy[1] > 600:
                        enemies_to_remove.append(enemy)
                        with game_state_lock:
                            game.score += 1
                    else:
                        # Detectar colisión con jugador
                        with player_lock:
                            px, py = game.player_x, game.player_y
                        
                        if (px < enemy[0] + game.enemy_size and
                            px + game.player_size > enemy[0] and
                            py < enemy[1] + game.enemy_size and
                            py + game.player_size > enemy[1]):
                            
                            enemies_to_remove.append(enemy)
                            with game_state_lock:
                                game.lives -= 1
                                if game.lives <= 0:
                                    game.final_score = game.score
                                    game.game_over = True
                
                # Remover enemigos marcados
                for enemy in enemies_to_remove:
                    if enemy in game.enemies:
                        game.enemies.remove(enemy)
        
        # Dormir brevemente para no saturar CPU
        time.sleep(0.0167)  # ~60 FPS
    
    print("🧵 Hilo de lógica terminado")

# FUNCIÓN GAME OVER
def show_game_over():
    screen.fill(WHITE)
    draw_text("GAME OVER", big_font, RED, 400, 150)
    draw_text(f"Puntuación final: {game.final_score}", font, BLACK, 400, 220)
    draw_text(f"Nivel alcanzado: {game.level}", font, BLACK, 400, 260)
    draw_text("Presiona ENTER para jugar de nuevo", font, BLACK, 400, 350)
    pygame.display.update()

    waiting = True
    while waiting:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game.running = False
                return
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                waiting = False
    
    # Reiniciar juego
    with game_state_lock, enemies_lock, player_lock:
        game.player_x = 400
        game.player_y = 500
        game.enemies = []
        game.score = 0
        game.lives = 3
        game.enemy_speed = 3
        game.enemy_spawn_rate = 20
        game.game_time = 0
        game.level = 1
        game.game_over = False

# INICIAR HILO DE LÓGICA
logic_thread = threading.Thread(target=game_logic_thread, daemon=True)
logic_thread.start()

# HILO PRINCIPAL: Renderizado y Input
print("🎮 Hilo principal (render + input) iniciado")

while game.running:
    screen.fill(WHITE)

    # Manejar eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game.running = False

    # Input del jugador (MUTEX para modificar posición)
    if not game.game_over:
        keys = pygame.key.get_pressed()
        with player_lock:
            if keys[pygame.K_LEFT] and game.player_x > 0:
                game.player_x -= game.player_speed
            if keys[pygame.K_RIGHT] and game.player_x < 800 - game.player_size:
                game.player_x += game.player_speed

    # Dibujar enemigos (MUTEX para leer lista)
    with enemies_lock:
        enemies_copy = game.enemies.copy()  # Copiar para no bloquear mucho tiempo
    
    for enemy in enemies_copy:
        draw_enemy(enemy[0], enemy[1])

    # Dibujar jugador
    with player_lock:
        px, py = game.player_x, game.player_y
    draw_player(px, py)
    
    # Dibujar UI
    draw_game_info()
    
    # Game Over
    if game.game_over:
        show_game_over()

    pygame.display.update()
    clock.tick(60)

print("🎮 Juego terminado, esperando hilo de lógica...")
logic_thread.join(timeout=2)  # Esperar a que termine el hilo
pygame.quit()
sys.exit()
