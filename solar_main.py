# coding: utf-8
# license: GPLv3
"""
Представление в плоском приближении солнечной или подобной ей системы
"""


import tkinter
from tkinter.filedialog import askopenfilename, asksaveasfilename
from solar_vis import *
from solar_model import *
from solar_input import *


class GlobalData:
    """Класс, содержащий переменные, которые используются в функциях"""

    __instance__ = None

    """
    Поле, хранящее единственный экземпляр **GlobalData**
    """

    def __init__(self):
        if GlobalData.__instance__ is not None:
            raise ValueError("Attempt to initialize another signleton class")
        self.perform_execution = False
        """Флаг цикличности выполнения расчёта"""
        self.physical_time = 0
        """Физическое время от начала расчёта.
        Тип: float"""
        self.displayed_time = None
        """Отображаемое на экране время.
        Тип: переменная tkinter"""
        self.time_step = None
        """Шаг по времени при моделировании.
        Тип: float"""
        self.space_objects = []
        """Список космических объектов."""
        self.space = None
        """Объект, представляющий космос
        Тип: холст tkinter"""
        self.start_button = None
        """Объект, представляющий кнопку начала
        Тип: кнопка tkinter"""

    @staticmethod
    def get_instance():
        """
        Статический метод, возвращающий экземпляр класса **GlobalData**
        """
        if GlobalData.__instance__ is None:
            GlobalData.__instance__ = GlobalData()
        return GlobalData.__instance__

    def reset(self):
        """
        Функция для сброса состояния
        """

        self.perform_execution = False
        self.physical_time = 0
        self.displayed_time = None
        self.time_step = None
        self.space_objects = []
        self.space = None
        self.start_button = None


def execution():
    """Функция исполнения -- выполняется циклически, вызывая обработку всех
    небесных тел, а также обновляя их положение на экране.
    Цикличность выполнения зависит от значения глобальной переменной
    perform_execution.
    При perform_execution == True функция запрашивает вызов самой себя по
    таймеру от 1 мс до 100 мс.
    """
    state = GlobalData.get_instance()
    recalculate_space_objects_positions(state.space_objects, state.time_step.get())
    for body in state.space_objects:
        update_object_position(state.space, body)
    state.physical_time += state.time_step.get()
    state.displayed_time.set("%.1f" % state.physical_time + " seconds gone")

    if state.perform_execution:
        state.space.after(101 - int(state.time_speed.get()), execution)


def start_execution():
    """Обработчик события нажатия на кнопку Start.
    Запускает циклическое исполнение функции execution.
    """
    state = GlobalData.get_instance()
    state.perform_execution = True
    state.start_button['text'] = "Pause"
    state.start_button['command'] = stop_execution

    execution()
    print('Started execution...')


def stop_execution():
    """Обработчик события нажатия на кнопку Start.
    Останавливает циклическое исполнение функции execution.
    """
    state = GlobalData.get_instance()
    state.perform_execution = False
    state.start_button['text'] = "Start"
    state.start_button['command'] = start_execution
    print('Paused execution.')


def open_file_dialog():

    """Открывает диалоговое окно выбора имени файла и вызывает
    функцию считывания параметров системы небесных тел из данного файла.
    Считанные объекты сохраняются в глобальный список space_objects
    """
    state = GlobalData.get_instance()
    state.perform_execution = False
    for obj in state.space_objects:
        state.space.delete(obj.image)  # удаление старых изображений планет
    input_filename = askopenfilename(filetypes=(("Text file", ".txt"),))
    state.space_objects = ImportFiles.read_space_objects_data_from_file(input_filename)
    max_distance = max(map(lambda obj: max(abs(obj.x), abs(obj.y)), state.space_objects))
    assert max_distance > 0, "Максимальная дистанция <= 0. Сломана загрузка файлов?"
    Scaler.calculate_scale_factor(max_distance)

    for obj in state.space_objects:
        if obj.type == "star:":
            create_star_image(state.space, obj)
        elif obj.type == "planet:":
            create_planet_image(state.space, obj)
        else:
            raise ValueError()


def save_file_dialog():
    """Открывает диалоговое окно выбора имени файла и вызывает
    функцию считывания параметров системы небесных тел из данного файла.
    Считанные объекты сохраняются в глобальный список space_objects
    """
    state = GlobalData.get_instance()
    out_filename = asksaveasfilename(filetypes=(("Text file", ".txt"),))
    ImportFiles.write_space_objects_data_to_file(out_filename, state.space_objects)


def main():
    """Главная функция главного модуля.
    Создаёт объекты графического дизайна библиотеки tkinter: окно, холст,
    фрейм с кнопками, кнопки.
    """
    state = GlobalData.get_instance()

    print('Modelling started!')
    state.physical_time = 0

    root = tkinter.Tk()
    # космическое пространство отображается на холсте типа Canvas
    space = tkinter.Canvas(root, width=WINDOW_WIDTH, height=WINDOW_HEIGHT, bg='black')
    space.pack(side=tkinter.TOP)
    space.place(x=0, y=0)
    # нижняя панель с кнопками
    frame = tkinter.Frame(root)
    frame.pack(side=tkinter.BOTTOM)

    state.start_button = tkinter.Button(frame, text="Start", command=start_execution, width=6)
    state.start_button.pack(side=tkinter.LEFT)

    state.time_step = tkinter.DoubleVar()
    state.time_step.set(1)
    time_step_entry = tkinter.Entry(frame, textvariable=state.time_step)
    time_step_entry.pack(side=tkinter.LEFT)

    state.time_speed = tkinter.DoubleVar()
    scale = tkinter.Scale(frame, variable=state.time_speed, orient=tkinter.HORIZONTAL)
    scale.pack(side=tkinter.LEFT)

    load_file_button = tkinter.Button(frame, text="Open file...", command=open_file_dialog)
    load_file_button.pack(side=tkinter.LEFT)
    save_file_button = tkinter.Button(frame, text="Save to file...", command=save_file_dialog)
    save_file_button.pack(side=tkinter.LEFT)

    state.displayed_time = tkinter.StringVar()
    state.displayed_time.set(str(state.physical_time) + " seconds gone")
    time_label = tkinter.Label(frame, textvariable=state.displayed_time, width=30)
    time_label.pack(side=tkinter.RIGHT)

    root.mainloop()
    print('Modelling finished!')


if __name__ == "__main__":
    main()
