import pygame
import random
import sys
import threading
import time

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Demo: Mutex vs Semáforo")
clock = pygame.time.Clock()

# Colores
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (65, 105, 225)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)

font = pygame.font.SysFont('Arial', 20)
small_font = pygame.font.SysFont('Arial', 16)
tiny_font = pygame.font.SysFont('Arial', 12)

# MUTEX: Solo 1 a la vez
player_lock = threading.Lock()

# SEMÁFORO: Máximo N a la vez
# Máximo 3 enemigos especiales (morados) simultáneos
special_enemy_semaphore = threading.Semaphore(3)

# ESTADO DEL JUEGO
class GameState:
    def __init__(self):
        self.player_x = 400
        self.player_y = 500
        self.enemies = []
        self.special_enemies = []  # Enemigos controlados por semáforo
        
        self.running = True
        self.special_count = 0  # Contador de especiales activos
        self.special_waiting = 0  # Cuántos esperan permiso
        
        # Log de eventos
        self.log_messages = []
        self.max_log = 5

game = GameState()

def add_log(message):
    """Agregar mensaje al log"""
    game.log_messages.append(message)
    if len(game.log_messages) > game.max_log:
        game.log_messages.pop(0)

# FUNCIONES DE DIBUJO
def draw_text(text, font, color, x, y):
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))

def draw_player(x, y):
    pygame.draw.rect(screen, BLUE, (x, y, 40, 40), border_radius=8)
    pygame.draw.circle(screen, WHITE, (x + 12, y + 12), 3)
    pygame.draw.circle(screen, WHITE, (x + 28, y + 12), 3)
    # Indicador de mutex
    pygame.draw.circle(screen, GREEN, (x + 20, y - 10), 5)
    draw_text("🔒", tiny_font, BLACK, x + 15, y - 25)

def draw_enemy(x, y, color, enemy_type='normal', enemy_id=None):
    pygame.draw.rect(screen, color, (x, y, 30, 30), border_radius=6)
    
    # Mostrar ID para enemigos especiales
    if enemy_type == 'special' and enemy_id:
        draw_text(str(enemy_id), tiny_font, WHITE, x + 10, y + 8)

def draw_info_panel():
    # Panel de información
    pygame.draw.rect(screen, (240, 240, 240), (0, 0, 800, 120))
    pygame.draw.line(screen, BLACK, (0, 120), (800, 120), 2)
    
    # Título
    draw_text("🔒 MUTEX vs 🚦 SEMÁFORO - Demostración Visual", font, BLACK, 20, 10)
    
    # Mutex info
    draw_text("🔒 MUTEX (Jugador Azul):", small_font, BLUE, 20, 40)
    estado_mutex = "🔒 BLOQUEADO" if player_lock.locked() else "🔓 LIBRE"
    draw_text(f"Estado: {estado_mutex}", small_font, BLACK, 20, 60)
    draw_text("Solo 1 hilo puede mover al jugador", tiny_font, BLACK, 20, 80)
    
    # Semáforo info
    draw_text("🚦 SEMÁFORO (Enemigos Morados):", small_font, PURPLE, 400, 40)
    draw_text(f"Activos: {game.special_count}/3", small_font, BLACK, 400, 60)
    draw_text(f"Esperando: {game.special_waiting}", small_font, ORANGE, 400, 80)
    draw_text("Máximo 3 enemigos especiales simultáneos", tiny_font, BLACK, 400, 100)

def draw_log():
    """Dibujar log de eventos"""
    log_y = 550
    draw_text("📋 Log de Eventos:", tiny_font, BLACK, 10, log_y)
    log_y += 15
    
    for i, msg in enumerate(game.log_messages):
        draw_text(msg, tiny_font, BLACK, 10, log_y + (i * 12))

def draw_legend():
    """Leyenda de colores"""
    legend_x = 600
    legend_y = 130
    
    # Enemigos normales
    pygame.draw.rect(screen, RED, (legend_x, legend_y, 15, 15))
    draw_text("Enemigos normales (sin límite)", tiny_font, BLACK, legend_x + 20, legend_y)
    
    # Enemigos especiales
    pygame.draw.rect(screen, PURPLE, (legend_x, legend_y + 20, 15, 15))
    draw_text("Enemigos especiales (máx 3)", tiny_font, BLACK, legend_x + 20, legend_y + 20)

# HILO: Enemigos Normales (sin límite)
def spawn_normal_enemies():
    """Enemigos rojos - aparecen sin restricción"""
    print("🧵 Hilo: Enemigos normales iniciado")
    
    while game.running:
        if random.randint(1, 60) == 1:  # Probabilidad de spawn
            new_enemy = {
                'x': random.randint(0, 770),
                'y': 120,
                'speed': 2,
                'color': RED,
                'type': 'normal'
            }
            game.enemies.append(new_enemy)
            add_log(f"🔴 Enemigo normal spawneado")
        
        time.sleep(0.016)
    
    print("🧵 Hilo: Enemigos normales terminado")

# HILO: Enemigos Especiales (CON SEMÁFORO)
def spawn_special_enemy_task(enemy_id):
    """
    Cada enemigo especial es un hilo independiente
    El SEMÁFORO limita cuántos pueden existir simultáneamente
    """
    print(f"  🚦 Enemigo especial #{enemy_id} esperando permiso...")
    game.special_waiting += 1
    add_log(f"🟣 Especial #{enemy_id} esperando... ({game.special_waiting} en cola)")
    
    # ⏳ Intentar tomar un permiso del semáforo (de los 3 disponibles)
    # Si no hay permisos, el hilo se BLOQUEA aquí hasta que se libere uno
    special_enemy_semaphore.acquire()
    
    game.special_waiting -= 1
    game.special_count += 1
    print(f"  ✅ Enemigo especial #{enemy_id} obtuvo permiso! ({game.special_count}/3)")
    add_log(f"✅ Especial #{enemy_id} activo ({game.special_count}/3)")
    
    # Crear el enemigo
    enemy = {
        'x': random.randint(0, 770),
        'y': 120,
        'speed': 3,
        'color': PURPLE,
        'type': 'special',
        'id': enemy_id
    }
    game.special_enemies.append(enemy)
    
    # Simular que el enemigo "vive" por un tiempo
    tiempo_vida = random.uniform(3, 6)
    time.sleep(tiempo_vida)
    
    # Remover el enemigo
    if enemy in game.special_enemies:
        game.special_enemies.remove(enemy)
    
    game.special_count -= 1
    print(f"  ❌ Enemigo especial #{enemy_id} terminado después de {tiempo_vida:.1f}s")
    add_log(f"❌ Especial #{enemy_id} terminó ({game.special_count}/3 activos)")
    
    # 🔓 Liberar el permiso (ahora otro enemigo puede usarlo)
    special_enemy_semaphore.release()

def spawn_special_enemies_manager():
    """Intenta crear enemigos especiales continuamente"""
    print("🧵 Hilo: Manager de enemigos especiales iniciado")
    enemy_counter = 0
    
    while game.running:
        if random.randint(1, 100) == 1:  # Probabilidad más baja
            enemy_counter += 1
            # Crear un NUEVO HILO para cada enemigo especial
            threading.Thread(
                target=spawn_special_enemy_task, 
                args=(enemy_counter,),
                daemon=True
            ).start()
        
        time.sleep(0.016)
    
    print("🧵 Hilo: Manager de enemigos especiales terminado")

# HILO: Movimiento del jugador automático (USA MUTEX)
def auto_move_player():
    """
    Este hilo mueve al jugador automáticamente
    El MUTEX asegura que solo un hilo modifique la posición
    """
    print("🧵 Hilo: Auto-movimiento iniciado")
    direction = 1  # 1 = derecha, -1 = izquierda
    
    while game.running:
        # 🔒 MUTEX: Tomar el candado antes de modificar posición
        with player_lock:
            game.player_x += 2 * direction
            
            # Cambiar dirección en los bordes
            if game.player_x >= 760:
                direction = -1
            elif game.player_x <= 0:
                direction = 1
        # 🔓 Al salir del 'with', el mutex se libera automáticamente
        
        time.sleep(0.03)
    
    print("🧵 Hilo: Auto-movimiento terminado")

# ACTUALIZAR ENEMIGOS
def update_enemies():
    """Mover todos los enemigos hacia abajo"""
    # Enemigos normales
    for enemy in game.enemies[:]:
        enemy['y'] += enemy['speed']
        if enemy['y'] > 600:
            game.enemies.remove(enemy)
    
    # Enemigos especiales
    for enemy in game.special_enemies[:]:
        enemy['y'] += enemy['speed']
        if enemy['y'] > 600:
            game.special_enemies.remove(enemy)

# INICIAR HILOS
print("\n" + "="*60)
print("🎮 INICIANDO DEMO: MUTEX vs SEMÁFORO")
print("="*60)
print("\n📌 Observa:")
print("  - Jugador azul: Solo 1 hilo puede moverlo (MUTEX)")
print("  - Enemigos morados: Máximo 3 a la vez (SEMÁFORO)")
print("  - Enemigos rojos: Sin límite\n")

# Hilo de enemigos normales
thread_normal = threading.Thread(target=spawn_normal_enemies, daemon=True)
thread_normal.start()

# Hilo de enemigos especiales
thread_special = threading.Thread(target=spawn_special_enemies_manager, daemon=True)
thread_special.start()

# Hilo de movimiento automático del jugador
thread_player = threading.Thread(target=auto_move_player, daemon=True)
thread_player.start()

# ============================================
# BUCLE PRINCIPAL (HILO PRINCIPAL)
# ============================================
print("🎨 Hilo principal (render) iniciado\n")

while game.running:
    screen.fill(WHITE)
    
    # Eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game.running = False
        
        # Control manual del jugador (también usa el mutex)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                with player_lock:  # 🔒 Proteger modificación
                    game.player_x = max(0, game.player_x - 30)
            elif event.key == pygame.K_RIGHT:
                with player_lock:  # 🔒 Proteger modificación
                    game.player_x = min(760, game.player_x + 30)
    
    # Actualizar posiciones
    update_enemies()
    
    # Dibujar todo
    draw_legend()
    
    # Dibujar enemigos normales
    for enemy in game.enemies:
        draw_enemy(enemy['x'], enemy['y'], enemy['color'], enemy['type'])
    
    # Dibujar enemigos especiales (con ID)
    for enemy in game.special_enemies:
        draw_enemy(enemy['x'], enemy['y'], enemy['color'], 
                  enemy['type'], enemy.get('id'))
    
    # Dibujar jugador (leyendo con mutex)
    with player_lock:
        px = game.player_x
    draw_player(px, game.player_y)
    
    # UI
    draw_info_panel()
    draw_log()
    
    # Instrucciones
    draw_text("Presiona ← → para mover manualmente (también usa MUTEX)", 
              tiny_font, BLACK, 10, 530)
    
    pygame.display.update()
    clock.tick(60)

# FINALIZAR
print("\n" + "="*60)
print("🎮 DEMO TERMINADA")
print("="*60)
print("Esperando que los hilos terminen...")

game.running = False
time.sleep(0.5)  # Dar tiempo a los hilos para terminar

pygame.quit()
sys.exit()
