# coding: utf-8
# license: GPLv3

"""Модуль визуализации.
Нигде, кроме этого модуля, не используются экранные координаты объектов.
Функции, создающие графические объекты и перемещающие их на экране, принимают
физические координаты
"""

HEADER_FONT = "Arial-16"
"""Шрифт в заголовке"""

WINDOW_WIDTH = 800
"""Ширина окна"""

WINDOW_HEIGHT = 800
"""Высота окна"""


class Scaler:
    """
    Класс, отвечающий за масштабирование
    """
    scale_factor = None
    """Масштабирование экранных координат по отношению к физическим.
    Тип: float
    Мера: количество пикселей на один метр."""

    def __init__(self):
        raise AssertionError()

    @staticmethod
    def calculate_scale_factor(max_distance):
        """Вычисляет значение глобальной переменной **scale_factor** по данной
        характерной длине"""
        Scaler.scale_factor = 0.4 * min(WINDOW_HEIGHT, WINDOW_WIDTH) / max_distance

    @staticmethod
    def scale_x(x):
        """Возвращает экранную **x** координату по **x** координате модели.
        Принимает вещественное число, возвращает целое число.
        В случае выхода **x** координаты за пределы экрана возвращает
        координату, лежащую за пределами холста.

        Параметры:
        **x** — x-координата модели.
        """
        return int(x * Scaler.scale_factor) + WINDOW_WIDTH//2

    @staticmethod
    def scale_y(y):
        """Возвращает экранную **y** координату по **y** координате модели.
        Принимает вещественное число, возвращает целое число.
        В случае выхода **y** координаты за пределы экрана возвращает
        координату, лежащую за пределами холста.
        Направление оси развёрнуто, чтобы у модели ось **y** смотрела вверх.

        Параметры:
        **y** — y-координата модели.
        """
        return int(-y * Scaler.scale_factor) - WINDOW_HEIGHT//2


def create_star_image(space, star):
    """Создаёт отображаемый объект звезды.

    Параметры:

    **space** — холст для рисования.
    **star** — объект звезды.
    """

    x = Scaler.scale_x(star.x)
    y = Scaler.scale_y(star.y)
    r = star.R
    star.image = space.create_oval(
        [x - r, y - r],
        [x + r, y + r],
        fill=star.color
    )


def create_planet_image(space, planet):
    """Создаёт отображаемый объект планеты.

    Параметры:

    **space** — холст для рисования.
    **planet** — объект планеты.
    """
    x = Scaler.scale_x(planet.x)
    y = Scaler.scale_y(planet.y)
    r = planet.R
    planet.image = space.create_oval(
        [x - r, y - r],
        [x + r, y + r],
        fill=planet.color
    )


def update_system_name(space, system_name):
    """Создаёт на холсте текст с названием системы небесных тел.
    Если текст уже был, обновляет его содержание.

    Параметры:

    **space** — холст для рисования.
    **system_name** — название системы тел.
    """
    space.create_text(30, 80, tag="header", text=system_name, font=HEADER_FONT)


def update_object_position(space, body):
    """Перемещает отображаемый объект на холсте.

    Параметры:

    **space** — холст для рисования.
    **body** — тело, которое нужно переместить.
    """
    x = Scaler.scale_x(body.x)
    y = Scaler.scale_y(body.y)
    r = body.R
    if x + r < 0 or x - r > WINDOW_WIDTH or y + r < 0 or y - r > WINDOW_HEIGHT:
        # положить за пределы окна
        space.coords(body.image, WINDOW_WIDTH + r, WINDOW_HEIGHT + r,
                     WINDOW_WIDTH + 2*r, WINDOW_HEIGHT + 2*r)
    space.coords(body.image, x - r, y - r, x + r, y + r)


if __name__ == "__main__":
    print("This module is not for direct call!")
