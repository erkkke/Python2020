for bullet in bullets:
bullet_x = bullet['x']
bullet_y = bullet['y']

if bullet['owner'] == client.tank_id:
    pygame.draw.circle(screen, (255, 255, 255), (bullet_x, bullet_y), 4)
else:
    pygame.draw.circle(screen, (0, 128, 0), (bullet_x, bullet_y), 4)

    if bullet_x in range(mytank_x - 31, mytank_x + 31):  # Уклонение от пуль
        if mytank_y < bullet_y:
            if bullet_y - mytank_y <= distance:
                client.turn_tank(client.token, 'RIGHT')
        elif mytank_y > bullet_y:
            if mytank_y - bullet_y <= distance:
                client.turn_tank(client.token, 'RIGHT')
    if bullet_y in range(mytank_y - 31, mytank_y + 31):
        if mytank_x < bullet_x:
            if bullet_x - mytank_x <= distance:
                client.turn_tank(client.token, 'DOWN')
        elif mytank_x > bullet_x:
            if mytank_x - bullet_x <= distance:
                client.turn_tank(client.token, 'DOWN')

for tank in tanks:
    tank_id = tank['id']
    tank_score = tank['score']
    tank_health = tank['health']
    tank_x = tank['x']
    tank_y = tank['y']
    tank_direction = tank['direction']

    if tank_id == client.tank_id:
        mytank_x = tank_x
        mytank_y = tank_y
        tank_d = tank_direction
        if tank_d == 'UP':
            client.turn_tank(client.token, random.choice(Direction))
        if remaining_time % 2 == 0:
            client.turn_tank(client.token, random.choice(Direction))
        draw_tank(tank_x, tank_y, tank_direction, 'Zhaiss')

    else:

        draw_tank2(tank_x, tank_y, tank_direction, tank_id)  # Файринг буллет
        if mytank_x in range(tank_x, tank_x + 31) and tank_y > mytank_y:
            client.turn_tank(client.token, 'DOWN')
            client.firing_bullet(client.token)
            client.turn_tank(client.token, 'RIGHT')
        elif mytank_x in range(tank_x, tank_x + 31) and tank_y < mytank_y:
            client.turn_tank(client.token, 'UP')
            client.firing_bullet(client.token)
            client.turn_tank(client.token, 'LEFT')
        elif mytank_y in range(tank_y, tank_y + 31) and tank_x > mytank_x:
            client.turn_tank(client.token, 'RIGHT')
            client.firing_bullet(client.token)
            client.turn_tank(client.token, 'DOWN')
        elif mytank_y in range(tank_y, tank_y + 31) and tank_x < mytank_x:
            client.turn_tank(client.token, 'LEFT')
            client.firing_bullet(client.token)
            client.turn_tank(client.token, 'UP')

    info_table(tank_id, tank_health, tank_score)
    info_sort()

except Exception as e:
# print(str(e))
pass