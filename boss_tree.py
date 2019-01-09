if boss.g_speed[0] < boss.g_speed[1]: boss.g_speed[0] += 1
if boss.image == images['boss_tree']['default']:
	if boss.state == 1:
		boss.g_speed[1] = 10
		boss.dir = math.degrees(math.atan2(boss.y - (player.y - player.yoffset * .25), player.x - boss.x))
		if boss.g_speed[0] >= boss.g_speed[1]:
			boss.deform = .5
			add_bullet(boss.x + math.cos(math.radians(boss.dir)) * 50, boss.y - math.sin(math.radians(boss.dir)) * 10 - 10, boss.dir - 10 + random.randint(0, 20), speed=9, image=images['bullets']['list'])
			boss.g_speed[0] = 0
	elif boss.state == 2:
		boss.g_speed[1] = 50
		if boss.g_speed[0] >= boss.g_speed[1]:
			boss.deform = 2
			if boss.d_damage % 2:
				for j in range(360 / 40):
					add_bullet(boss.x + math.cos(math.radians(j * 40)) * 50, boss.y - math.sin(math.radians(j * 40)) * 10 - 10, j * 40 - 5 + random.randint(0, 10), speed=7, image=images['bullets']['list'])
			else:
				for j in range(360 / 40):
					add_bullet(boss.x + math.cos(math.radians(j * 40 + 20)) * 50, boss.y - math.sin(math.radians(j * 40 + 20)) * 10 - 10, j * 40 + 15 + random.randint(0, 10), speed=7, image=images['bullets']['list'])	
			boss.d_damage += 1
			boss.g_speed[0] = 0
if boss.image != images['boss_tree']['up']:
	if boss.timer > 0: boss.timer -= 1
	else:
		val = random.randint(0, 2)
		while val == boss.state: val = random.randint(0, 2)
		boss.state = val
		if not val:
			boss.image = images['boss_tree']['up']
			boss.image_index, boss.image_speed = len(images['boss_tree']['up']) - 1, -.05
		else:
			if boss.image == images['boss_tree']['afk']: boss.image = images['boss_tree']['up']
			boss.image_index, boss.image_speed = 0, .05
		boss.timer = 300 + random.randint(0, 200) * (val > 0)
else:
	if not boss.state:
		if boss.image_index <= abs(boss.image_speed): 
			boss.image, boss.image_index, boss.image_speed = images['boss_tree']['afk'], 0, .1
	else:
		if boss.image_index >= len(boss.image) - boss.image_speed: 
			boss.image, boss_image_index = images['boss_tree']['default'], 0