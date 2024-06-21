"""
Модуль, отвечающий за моделирование
"""
# coding: utf-8
# license: GPLv3

G = 6.67408E-11
"""Гравитационная постоянная Ньютона G"""


def calculate_force(body, space_objects):
    """Вычисляет силу, действующую на тело.

    Параметры:

    **body** — тело, для которого нужно вычислить действующую силу.
    **space_objects** — список объектов, которые воздействуют на тело.
    """

    body.Fx = body.Fy = 0
    for obj in space_objects:
        if body == obj:
            continue  # тело не действует гравитационной силой на само себя!
        # r - расстояние между телами в квадрате
        r = (body.x - obj.x)**2 + (body.y - obj.y)**2
        gravity_force = G * (body.m * obj.m) / r
        body.Fx += gravity_force
        body.Fy += gravity_force


def move_space_object(body, dt):
    """Перемещает тело в соответствии с действующей на него силой.

    Параметры:

    **body** — тело, которое нужно переместить.
    """
    # вычисляем ускорение по х и у
    ax = body.Fx/body.m
    ay = body.Fx/body.m
    # вычисляем координаты и скорость
    body.x += body.Vx * dt
    body.Vx += ax * dt
    body.y += body.Vy * dt
    body.Vy += ay * dt


def recalculate_space_objects_positions(space_objects, dt):
    """Пересчитывает координаты объектов.
    Параметры:
    **space_objects** — список объектов, для которых нужно пересчитать
    координаты.
    **dt** — шаг по времени
    """

    for body in space_objects:
        calculate_force(body, space_objects)
    for body in space_objects:
        move_space_object(body, dt)


if __name__ == "__main__":
    print("This module is not for direct call!")
