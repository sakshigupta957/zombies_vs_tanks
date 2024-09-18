import pgzrun
import random

TITLE = "Zombies vs Tanks"
WIDTH = 800
HEIGHT = 640

UP = 180
DOWN = 0
LEFT = 270
RIGHT = 90
BULLET_SPEED = 10

# Initialize the tank and bullet
blue_tank = Actor("tank_blue")
blue_tank.x = WIDTH / 2
blue_tank.y = HEIGHT / 2

bullet = Actor("bulletblue")
bullet_fired = False

zombie_list = []
ZOMBIE_SPEED = 1

score = 0
game_over = False

def draw():
    if not game_over:
        screen.blit("tank.png", (0, 0))  # Background
        blue_tank.draw()  # Draw the tank
        if bullet_fired:
            bullet.draw()  # Draw the bullet only when fired
        move_zombie()  # Move and draw zombies
        screen.draw.text(f"Score: {score}", (350, 150))  # Display score
    else:
        screen.fill("blue")  # Game over screen
        screen.draw.text(f"GAME OVER, Your score: {score}", (350, 150))

def update():
    global bullet_fired
    if keyboard.left:
        blue_tank.x -= 5
        blue_tank.angle = LEFT
    if keyboard.right:
        blue_tank.x += 5
        blue_tank.angle = RIGHT
    if keyboard.up:
        blue_tank.y -= 5
        blue_tank.angle = UP
    if keyboard.down:
        blue_tank.y += 5
        blue_tank.angle = DOWN
    if keyboard.space and not bullet_fired:
        bullet_fired = True
        sounds.laserretro_004.play()  # Play shooting sound
        if blue_tank.angle == LEFT:
            bullet.x = blue_tank.x - 30
            bullet.y = blue_tank.y
        elif blue_tank.angle == RIGHT:
            bullet.x = blue_tank.x + 30
            bullet.y = blue_tank.y
        elif blue_tank.angle == DOWN:
            bullet.x = blue_tank.x
            bullet.y = blue_tank.y + 30
        elif blue_tank.angle == UP:
            bullet.x = blue_tank.x
            bullet.y = blue_tank.y - 30

    shoot_bullet()

def shoot_bullet():
    global bullet_fired
    if bullet_fired:
        if blue_tank.angle == LEFT:
            bullet.x -= BULLET_SPEED
        elif blue_tank.angle == RIGHT:
            bullet.x += BULLET_SPEED
        elif blue_tank.angle == DOWN:
            bullet.y += BULLET_SPEED
        elif blue_tank.angle == UP:
            bullet.y -= BULLET_SPEED

        # Reset bullet if it goes off the screen
        if bullet.x >= WIDTH or bullet.x <= 0 or bullet.y >= HEIGHT or bullet.y <= 0:
            bullet_fired = False

def create_zombies():
    if len(zombie_list) < 10:
        loc_rand = random.randint(0, 3)
        z = Actor("zombie_stand.png")
        if loc_rand == 0:
            z.x = 1
            z.y = random.randint(40, HEIGHT - 40)
        elif loc_rand == 1:
            z.x = WIDTH - 1
            z.y = random.randint(40, HEIGHT - 40)
        elif loc_rand == 2:
            z.x = random.randint(40, WIDTH - 40)
            z.y = 1
        elif loc_rand == 3:
            z.x = random.randint(40, WIDTH - 40)
            z.y = HEIGHT - 1
        zombie_list.append(z)

def move_zombie():
    global score, game_over
    for zomb in zombie_list:
        if zomb.x < blue_tank.x:
            zomb.x += ZOMBIE_SPEED
        elif zomb.x > blue_tank.x:
            zomb.x -= ZOMBIE_SPEED
        if zomb.y < blue_tank.y:
            zomb.y += ZOMBIE_SPEED
        elif zomb.y > blue_tank.y:
            zomb.y -= ZOMBIE_SPEED

    # Check for collisions after movement
    for zomb in zombie_list:
        zomb.draw()  # Draw zombie
        if zomb.colliderect(bullet):
            zombie_list.remove(zomb)  # Remove zombie if hit by bullet
            score += 1  # Increase score
        if zomb.colliderect(blue_tank):
            game_over = True  # Game over if a zombie hits the tank

# Schedule zombie creation every 5 seconds
clock.schedule_interval(create_zombies, 5)

# Start the game loop
pgzrun.go()
