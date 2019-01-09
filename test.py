import pygame, random, math

pygame.init()
pygame.joystick.init()
joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
joysticks[0].init()

size = width, height = 600, 400
camera, current_level, font, clock, exit = {'x': 0, 'y': 0}, None, pygame.font.Font(None, 24), pygame.time.Clock(), False

images = {
	'player': {
		'move': [pygame.image.load("player/1.png"), pygame.image.load("player/2.png"), pygame.image.load("player/3.png"), pygame.image.load("player/4.png")],
		'attack_default': [pygame.image.load("player/attack_default/1.png"), pygame.image.load("player/attack_default/2.png"), pygame.image.load("player/attack_default/3.png")],
		'attack_default2': [pygame.image.load("player/attack_default/4.png"), pygame.image.load("player/attack_default/5.png"), pygame.image.load("player/attack_default/6.png"), pygame.image.load("player/attack_default/7.png"), pygame.image.load("player/attack_default/8.png")]
	},
	'boss_tree': {
		'default': pygame.image.load('boss1.png'),
		'afk': [pygame.image.load("boss1/afk1.png"), pygame.image.load("boss1/afk2.png"), pygame.image.load("boss1/afk3.png")],
		'up': [pygame.image.load("boss1/up1.png"), pygame.image.load("boss1/up2.png"), pygame.image.load("boss1/up3.png"), pygame.image.load("boss1/up4.png")]
	},
	'health': pygame.image.load('health.png'),
	'effects': {
		'fire': [pygame.image.load("fire/1.png"), pygame.image.load("fire/2.png"), pygame.image.load("fire/3.png")]
	},
	'bullets': {
		'list': pygame.image.load('bullet_list.png')
	}
}

class Object:
	def __init__(self, x, y, image=None, xoffset=0, yoffset=0):
		self.x, self.y, self.image, self.type, self.image_speed, self.xoffset, self.yoffset, self.deform = x, y, image, None, .1, xoffset, yoffset, 0
		if self.image is not None:
			if type(self.image) == list:
				self.image_index, self.image_speed = 0, .1
				self.rect = self.image[0].get_rect()
			else: self.rect = self.image.get_rect()
			self.move(self.x, self.y)
		else: self.rect = None
	def set(self, image):
		self.image = image
		self.rect = self.image.get_rect()
		self.move(self.x, self.y)
	def move(self, x, y): self.rect[0], self.rect[1] = x, y
	def draw(self): 
		if self.deform > 0:
			if type(self.image) == list:
				self.dimage = pygame.transform.scale(self.image[int(self.image_index)], (self.rect[2] + int(self.rect[2] * .1 * self.deform), self.rect[3] + int(self.rect[3] * .15 * self.deform)))
				self.image_index += self.image_speed
				if self.image_index > len(self.image): self.image_index = 0
				if self.image_index < 0: self.image_index = len(self.image) - 1
			else: self.dimage = pygame.transform.scale(self.image, (self.rect[2] + int(self.rect[2] * .1 * self.deform), self.rect[3] + int(self.rect[3] * .15 * self.deform)))
			screen.blit(self.dimage, (self.rect[0] - self.xoffset - camera['x'] - (self.rect[2] * .1 * self.deform) * .5, self.rect[1] - self.yoffset - camera['y'] - (self.rect[3] * .15 * self.deform)))
			self.deform -= .1
		else:
			if type(self.image) == list:
				screen.blit(self.image[int(self.image_index)], (self.rect[0] - self.xoffset - camera['x'], self.rect[1] - self.yoffset - camera['y']))
				self.image_index += self.image_speed
				if self.image_index > len(self.image): self.image_index = 0
			else: screen.blit(self.image, (self.rect[0] - self.xoffset - camera['x'], self.rect[1] - self.yoffset - camera['y']))

class Table(Object):
	def __init__(self, x, y, xoffset=0, yoffset=0):
		self.x, self.y, self.image = x, y, pygame.image.load("table.png")
		self.rect = self.image.get_rect()
		self.rect[0], self.rect[1] = x, y
		self.xoffset, self.yoffset = xoffset, yoffset
		self.deform = 0
	def show(self, text, color=(0, 0, 0)):
		bitmap = font.render(text, True, color)
		screen.blit(bitmap, (self.x - self.xoffset - camera['x'], self.y - 25 - self.yoffset - camera['y']))

class Bullet(Object):
	def __init__(self, x, y, image=None, xoffset=0, yoffset=0, dir=0, speed=4, friendly=False, timeout=60):
		self.x, self.y, self.image = x, y, image
		self.type = "bullet"
		if self.image is not None:
			if type(self.image) == list:
				self.image_index, self.image_speed = 0, .1
				self.rect = self.image[0].get_rect()
			else: self.rect = self.image.get_rect()
			self.move(self.x, self.y)
		else: self.rect = None
		self.xoffset, self.yoffset = xoffset, yoffset
		self.dir, self.speed = dir, speed
		if type(self.image) == list:
			pass
		else:
			self.image = pygame.transform.rotate(self.image, self.dir)
		self.friendly = friendly
		self.timeout = timeout
		self.deform = 0
	def update(self):
		if self.timeout > 0:
			self.x += math.cos(math.radians(self.dir)) * self.speed
			self.y -= math.sin(math.radians(self.dir)) * self.speed

			if (self.x <= current_level.width * .08) or (self.x >= current_level.width * .92): return 1
			if (self.y >= current_level.height * .95) or (self.y <= current_level.height * .2): return 1
			for i in range(len(current_level.stack)):
				if current_level.stack[i].type == "boss" and self.friendly:
					if distance(self.x, self.y, current_level.stack[i].x, current_level.stack[i].y - 50) <= 70:
						current_level.add_effect(Object(self.x, self.y, image=images['effects']['fire'], xoffset=32, yoffset=32))
						if not current_level.stack[i].state:
							current_level.stack[i].hp -= 1
							current_level.stack[i].deform = 1
						return 1
				if current_level.stack[i].type == "player" and not self.friendly:
					if distance(self.x, self.y, current_level.stack[i].x, current_level.stack[i].y - 40) <= 40:
						current_level.add_effect(Object(self.x, self.y, image=images['effects']['fire'], xoffset=32, yoffset=32))
						current_level.stack[i].deform = 1
						return 1
			self.move(self.x, self.y)
			self.timeout -= 1
		else: return 1
		return 0

class Level:
	def __init__(self, name="no name", type=0, width=800, height=600, background={}, color=(255, 255, 255)):
		self.name, self.type, self.width, self.height = name, type, width, height
		self.background, self.stack, self.effect = background, [], []
		self.color = color
	def draw(self):
		screen.fill(self.color)
		if 'ground' in self.background: draw(self.background['ground'], -camera['x'], -camera['y'])
		arr = self.stack + self.effect
		for i in range(len(arr)):
			if arr[i].type == 'bullet':
				if arr[i].update():
					del self.stack[i]
					del arr[i]
					break
			elif arr[i].type == 'effect':
				if arr[i].image_index >= len(arr[i].image) - arr[i].image_speed:
					del self.effect[i - len(self.stack)]
					del arr[i]
					break

		for i in range(len(arr)):
			arr[i].draw()

		if 'layer' in self.background: draw(self.background['layer'], -camera['x'], -camera['y'])
		self.stack = sorted(self.stack, key=lambda x: x.y)
	def add_object(self, obj): self.stack.append(obj)
	def add_effect(self, effect):
		effect.type = 'effect'
		self.effect.append(effect)

level1 = Level(background={
	'ground': pygame.image.load('level1.png'),
	'layer': pygame.image.load('level1_pre.png')
}, name="live tree", color=(50, 104, 59))

player = Object(400, 450, image=images['player']['move'], xoffset=50, yoffset=90)
boss = Object(400, 350, image=images['boss_tree']['default'], xoffset=125, yoffset=210)
player.type, player.state, player.image_speed, player.xscale, player.hspd, player.vspd, player.g_speed = 'player', 0, 2, 1, 0, 0, [20, 20]
boss.type, boss.dir, boss.state, boss.d_damage, boss.timer, boss.hp, boss.g_speed = 'boss', 0, 0, 0, 300, 40, [50, 50]
boss.file = 'boss_tree.py'

f = open(boss.file)
boss.file = f.read()
f.close()

def distance(x1, y1, x2, y2): return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
def draw(image, x, y): screen.blit(image, (x, y))
def add_bullet(x, y, dir, speed=4, friendly=False, image=images['effects']['fire'], timeout=200): current_level.stack.append(Bullet(x, y, image=image, xoffset=32, yoffset=32, dir=dir, speed=speed, friendly=friendly, timeout=timeout))

level1.add_object(player)
level1.add_object(boss)
level1.add_object(Object(130, 180, image=pygame.image.load("stone.png"), xoffset=50, yoffset=80))
for i in range(10): level1.add_object(Object(boss.x - 200 + random.randint(0, 400), boss.y - 100 + random.randint(0, 200), image=pygame.image.load("grass.png"), xoffset=30, yoffset=40))
current_level = level1


def movement(): # player move:
	xaxis, yaxis, fr, speed = joysticks[0].get_axis(0), joysticks[0].get_axis(1), .2, 5

	player.hspd += min(max((xaxis * speed - player.hspd) * fr, -speed), speed)
	player.vspd += min(max((yaxis * speed - player.vspd) * fr, -speed), speed)

	if (player.x + player.hspd <= current_level.width * .08) or (player.x + player.hspd >= current_level.width * .92): player.hspd = 0
	if (player.y + player.vspd >= current_level.height * .95) or (player.y + player.vspd <= current_level.height * .2): player.vspd = 0
	
	val = player.xscale
	if xaxis != 0: val = 1 - 2 * (xaxis < 0)
	if player.xscale != val:
		player.xscale = val
		for key in images['player']:
			for i in range(len(images['player'][key])):
				images['player'][key][i] = pygame.transform.flip(images['player'][key][i], 1, 0)
	player.x += player.hspd
	player.y += player.vspd
	player.move(player.x, player.y)
	if not player.state:
		if xaxis != 0 or yaxis != 0:
			player.image_speed = .15
		else:
			player.image_speed = 0
			player.image_index = 0

	if player.state == 1:
		if player.image_index >= len(player.image) - player.image_speed:
			add_bullet(player.x - 20 + random.randint(0, 40), player.y - player.yoffset * .25 - 5 + random.randint(0, 10), 0, speed=0, friendly=True, timeout=1)
			player.state = 0
			player.image = images['player']['move']
			player.image_index = 0

	

	# shot:
	"""
	sxaxis, syaxis = joysticks[0].get_axis(2), joysticks[0].get_axis(3)
	if (abs(sxaxis) > .75 or abs(syaxis) > .75) and player.g_speed[0] >= player.g_speed[1]:
		add_bullet(player.x - 20, player.y - player.yoffset * .25, math.degrees(math.pi + math.atan2(syaxis, -sxaxis)), speed=9, friendly=True)
		player.g_speed[0] = 0
	"""
	if joysticks[0].get_button(0) and player.g_speed[0] >= player.g_speed[1]:
		if not player.state:
			player.state = 1
			l = ['attack_default', 'attack_default2']
			player.image = images['player'][l[random.randint(0, len(l) - 1)]]
			player.image_index = 0
			player.image_speed = .15
			player.g_speed[0] = 0
	if player.g_speed[0] < player.g_speed[1]: player.g_speed[0] += .6

def gui():
	hp = int(math.ceil((boss.hp + 20) / 20) - 1)
	for i in range(hp):
		draw(images['health'], 300 - (hp * 50) + 100 * i, 10)

screen = pygame.display.set_mode(size)
pygame.display.set_caption("Game")
while not exit:
	for event in pygame.event.get():
		if event.type == pygame.QUIT: exit = True
	movement()
	exec(boss.file)
	level1.draw()
	gui() # gui.

	camera['x'] += ((player.x - camera['x']) - width * .5) * .05
	camera['y'] += (((player.y - player.yoffset * .5) - camera['y']) - height * .5) * .05
	camera['x'] = min(max(camera['x'], 0), current_level.width - width)
	camera['y'] = min(max(camera['y'], 0), current_level.height - height)
	
	pygame.display.flip()
	clock.tick(60)

pygame.quit()