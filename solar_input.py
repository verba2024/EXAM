# coding: utf-8
# license: GPLv3

from solar_objects import Star, Planet


class ImportFiles(Star, Planet):
    def read_space_objects_data_from_file(input_filename):
        """
        Считывает данные о космических объектах из файла, создаёт сами объекты
        и вызывает создание их графических образов

        Параметры:

        **input_filename** — имя входного файла
        """

        objects = []
        with open(input_filename) as input_file:
            for line in input_file:
                if len(line.strip()) == 0 or line[0] == '#':
                    continue  # пустые строки и строки-комментарии пропускаем
                object_type = line.split()[0].lower()
                if object_type == "star:":
                    star = Star('', 0, '', 0, 0, 0, 0, 0)
                    ImportFiles.parse_star_parameters(line, star)
                    objects.append(star)
                elif object_type == "planet:":
                    planet = Planet('', 0, '', 0, 0, 0, 0, 0)
                    ImportFiles.parse_planet_parameters(line, planet)
                    objects.append(planet)
                else:
                    print("Unknown space object")

        return objects

    @staticmethod
    def parse_star_parameters(line, star):
        """Считывает данные о звезде из строки.
        Предполагается такая строка:
        Входная строка должна иметь следующий формат:
        Star <радиус в пикселах> <цвет> <масса> <x> <y> <Vx> <Vy>

        Здесь (x, y) — координаты звезды, (Vx, Vy) — скорость.
        Пример строки:
        Star 10 red 1000 1 2 3 4

        Параметры:

        **line** — строка с описанием планеты.
        **star** — объект планеты.
        """
        starz = line.split()
        star.type = str(starz[0])
        star.R = int(starz[1])
        star.color = str(starz[2])
        star.m = float(starz[3])
        star.x = float(starz[4])
        star.y = float(starz[5])
        star.Vx = float(starz[6])
        star.Vy = float(starz[7])

    @staticmethod
    def parse_planet_parameters(line, planet):
        """Считывает данные о планете из строки.
        Предполагается такая строка:
        Входная строка должна иметь следующий формат:
        Planet <радиус в пикселах> <цвет> <масса> <x> <y> <Vx> <Vy>

        Здесь (x, y) — координаты планеты, (Vx, Vy) — скорость.
        Пример строки:
        Planet 10 red 1000 1 2 3 4

        Параметры:

        **line** — строка с описанием планеты.
        **planet** — объект планеты.
        """
        planet_list = line.split()
        planet.type = str(planet_list[0])
        planet.R = float(planet_list[1])
        planet.color = str(planet_list[2])
        planet.m = int(planet_list[3])
        planet.x = float(planet_list[4])
        planet.y = float(planet_list[5])
        planet.Vx = float(planet_list[6])
        planet.Vy = float(planet_list[7])

    @staticmethod
    def write_space_objects_data_to_file(output_filename, space_objects):
        """Сохраняет данные о космических объектах в файл.
        Строки должны иметь следующий формат:
        Star <радиус в пикселах> <цвет> <масса> <x> <y> <Vx> <Vy>
        Planet <радиус в пикселах> <цвет> <масса> <x> <y> <Vx> <Vy>
        capitalize - функция, которая преобразует первый символ строки в верхний регистр
        Параметры:

        **output_filename** — имя входного файла
        **space_objects** — список объектов планет и звёзд
        """
        with open(output_filename, 'w') as out_file:
            for obj in space_objects:
                out_file.write(f"{obj.type.capitalize()} {obj.R} {obj.color} {obj.m} {obj.x} {obj.y} {obj.Vx} {obj.Vy}\n")

    def keep_statistics(outputfilename, statistics):
        """
        Функция, сохраняющая статистику в файл

        Параметры:

        :return:
        """
        with open(outputfilename, 'w') as out_file:
            for static in statistics:
                out_file.write(f"{static}\n")


if __name__ == "__main__":
    print("This module is not for direct call!")
