# Player
playerX = 370
playerY = 480
playerX_change = 0

# Boss
bossX = 50
bossY = 50
bossX_change = 4 
bossY_change = 40

# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

# Bullet
# Ready - You can't see the bullet on the screen
# Fire - The bullet is currently moving
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 10
bullet_state = "ready"

contents = ""

f = open("Highscore.txt", "r")
if f.mode == "r":
    contents = f.read()
f.close()