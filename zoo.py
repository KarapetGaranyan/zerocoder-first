import pickle
import os


class Animal:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def make_sound(self):
        print("Некоторый звук животного")

    def eat(self):
        print(f"{self.name} ест.")

    def __str__(self):
        return f"{self.name}, возраст: {self.age}"


class Bird(Animal):
    def __init__(self, name, age, wingspan):
        super().__init__(name, age)
        self.wingspan = wingspan

    def make_sound(self):
        print(f"{self.name} чирикает!")

    def fly(self):
        print(f"{self.name} летит, размах крыльев: {self.wingspan} см")

    def __str__(self):
        return f"Птица: {super().__str__()}, размах крыльев: {self.wingspan} см"


class Mammal(Animal):
    def __init__(self, name, age, fur_color):
        super().__init__(name, age)
        self.fur_color = fur_color

    def make_sound(self):
        print(f"{self.name} рычит!")

    def run(self):
        print(f"{self.name} бежит. Цвет шерсти: {self.fur_color}")

    def __str__(self):
        return f"Млекопитающее: {super().__str__()}, цвет шерсти: {self.fur_color}"


class Reptile(Animal):
    def __init__(self, name, age, is_venomous):
        super().__init__(name, age)
        self.is_venomous = is_venomous

    def make_sound(self):
        print(f"{self.name} шипит!")

    def crawl(self):
        venomous_status = "ядовитый" if self.is_venomous else "неядовитый"
        print(f"{self.name} ползет. Статус: {venomous_status}")

    def __str__(self):
        venomous_status = "ядовитая" if self.is_venomous else "неядовитая"
        return f"Рептилия: {super().__str__()}, {venomous_status}"


# Функция для демонстрации полиморфизма
def animal_sound(animals):
    print("\nЗвуки животных:")
    for animal in animals:
        animal.make_sound()


class Employee:
    def __init__(self, name, employee_id, salary):
        self.name = name
        self.employee_id = employee_id
        self.salary = salary

    def work(self):
        print(f"{self.name} работает.")

    def __str__(self):
        return f"{self.name}, ID: {self.employee_id}"


class ZooKeeper(Employee):
    def __init__(self, name, employee_id, salary, area_responsibility):
        super().__init__(name, employee_id, salary)
        self.area_responsibility = area_responsibility

    def feed_animal(self, animal):
        print(f"{self.name} кормит {animal.name}.")

    def clean_enclosure(self):
        print(f"{self.name} убирает вольер в зоне {self.area_responsibility}.")

    def __str__(self):
        return f"Смотритель: {super().__str__()}, зона: {self.area_responsibility}"


class Veterinarian(Employee):
    def __init__(self, name, employee_id, salary, specialization):
        super().__init__(name, employee_id, salary)
        self.specialization = specialization

    def heal_animal(self, animal):
        print(f"{self.name} лечит {animal.name}. Специализация: {self.specialization}")

    def check_health(self, animal):
        print(f"{self.name} проверяет здоровье {animal.name}.")

    def __str__(self):
        return f"Ветеринар: {super().__str__()}, специализация: {self.specialization}"


# Композиция
class Zoo:
    def __init__(self, name, location):
        self.name = name
        self.location = location
        self.animals = []
        self.employees = []

    def add_animal(self, animal):
        self.animals.append(animal)
        print(f"{animal.name} добавлен в зоопарк {self.name}.")

    def add_employee(self, employee):
        self.employees.append(employee)
        print(f"{employee.name} принят на работу в зоопарк {self.name}.")

    def list_animals(self):
        print(f"\nЖивотные в зоопарке {self.name}:")
        if not self.animals:
            print("Животных нет")
            return
        for i, animal in enumerate(self.animals, 1):
            print(f"{i}. {animal}")

    def list_employees(self):
        print(f"\nСотрудники зоопарка {self.name}:")
        if not self.employees:
            print("Сотрудников нет")
            return
        for i, employee in enumerate(self.employees, 1):
            print(f"{i}. {employee}")

    def remove_animal(self, index):
        if 0 <= index < len(self.animals):
            animal = self.animals.pop(index)
            print(f"{animal.name} удален из зоопарка.")
            return True
        return False

    def remove_employee(self, index):
        if 0 <= index < len(self.employees):
            employee = self.employees.pop(index)
            print(f"{employee.name} уволен из зоопарка.")
            return True
        return False

    def save_to_file(self, filename="zoo_data.pickle"):
        """Сохраняет данные зоопарка в файл"""
        with open(filename, 'wb') as file:
            pickle.dump((self.name, self.location, self.animals, self.employees), file)
        print(f"Данные зоопарка сохранены в файл {filename}")

    def load_from_file(self, filename="zoo_data.pickle"):
        """Загружает данные зоопарка из файла"""
        if os.path.exists(filename):
            with open(filename, 'rb') as file:
                self.name, self.location, self.animals, self.employees = pickle.load(file)
            print(f"Данные зоопарка загружены из файла {filename}")
            return True
        else:
            print(f"Файл {filename} не найден")
            return False

    def __str__(self):
        return f"Зоопарк '{self.name}' в {self.location}, {len(self.animals)} животных, {len(self.employees)} сотрудников"


def create_demo_zoo():
    """Создает демонстрационный зоопарк с животными и сотрудниками"""
    zoo = Zoo("Счастливые животные", "Москва")

    # Добавляем животных
    parrot = Bird("Кеша", 3, 30)
    lion = Mammal("Симба", 5, "золотистый")
    snake = Reptile("Каа", 7, True)
    elephant = Mammal("Дамбо", 10, "серый")
    turtle = Reptile("Тортилла", 100, False)

    zoo.add_animal(parrot)
    zoo.add_animal(lion)
    zoo.add_animal(snake)
    zoo.add_animal(elephant)
    zoo.add_animal(turtle)

    # Добавляем сотрудников
    keeper1 = ZooKeeper("Иван", "ZK001", 35000, "птицы")
    keeper2 = ZooKeeper("Алексей", "ZK002", 35000, "млекопитающие")
    vet1 = Veterinarian("Мария", "VT001", 45000, "млекопитающие")
    vet2 = Veterinarian("Елена", "VT002", 48000, "рептилии")

    zoo.add_employee(keeper1)
    zoo.add_employee(keeper2)
    zoo.add_employee(vet1)
    zoo.add_employee(vet2)

    return zoo


def main_menu():
    """Отображает главное меню программы"""
    print("\n" + "=" * 40)
    print("СИСТЕМА УПРАВЛЕНИЯ ЗООПАРКОМ")
    print("=" * 40)
    print("1. Создать новый зоопарк")
    print("2. Загрузить существующий зоопарк")
    print("3. Выход")

    choice = input("Выберите действие (1-3): ")
    return choice


def zoo_menu():
    """Отображает меню управления зоопарком"""
    print("\n" + "=" * 40)
    print("МЕНЮ УПРАВЛЕНИЯ ЗООПАРКОМ")
    print("=" * 40)
    print("1. Информация о зоопарке")
    print("2. Список животных")
    print("3. Список сотрудников")
    print("4. Добавить животное")
    print("5. Добавить сотрудника")
    print("6. Удалить животное")
    print("7. Удалить сотрудника")
    print("8. Сохранить данные зоопарка")
    print("9. Вернуться в главное меню")

    choice = input("Выберите действие (1-9): ")
    return choice


def add_animal_menu(zoo):
    """Меню добавления животного"""
    print("\n" + "=" * 40)
    print("ДОБАВЛЕНИЕ ЖИВОТНОГО")
    print("=" * 40)
    print("1. Птица")
    print("2. Млекопитающее")
    print("3. Рептилия")
    print("4. Назад")

    choice = input("Выберите тип животного (1-4): ")

    if choice == "4":
        return

    name = input("Введите имя животного: ")

    while True:
        try:
            age = int(input("Введите возраст животного: "))
            break
        except ValueError:
            print("Возраст должен быть числом. Попробуйте снова.")

    if choice == "1":
        while True:
            try:
                wingspan = int(input("Введите размах крыльев (см): "))
                break
            except ValueError:
                print("Размах крыльев должен быть числом. Попробуйте снова.")
        animal = Bird(name, age, wingspan)

    elif choice == "2":
        fur_color = input("Введите цвет шерсти: ")
        animal = Mammal(name, age, fur_color)

    elif choice == "3":
        while True:
            is_venomous_input = input("Ядовитая? (да/нет): ").lower()
            if is_venomous_input in ["да", "нет"]:
                break
            print("Введите 'да' или 'нет'.")
        is_venomous = is_venomous_input == "да"
        animal = Reptile(name, age, is_venomous)

    else:
        print("Неверный выбор.")
        return

    zoo.add_animal(animal)


def add_employee_menu(zoo):
    """Меню добавления сотрудника"""
    print("\n" + "=" * 40)
    print("ДОБАВЛЕНИЕ СОТРУДНИКА")
    print("=" * 40)
    print("1. Смотритель")
    print("2. Ветеринар")
    print("3. Назад")

    choice = input("Выберите тип сотрудника (1-3): ")

    if choice == "3":
        return

    name = input("Введите имя сотрудника: ")
    employee_id = input("Введите ID сотрудника: ")

    while True:
        try:
            salary = int(input("Введите зарплату: "))
            break
        except ValueError:
            print("Зарплата должна быть числом. Попробуйте снова.")

    if choice == "1":
        area = input("Введите зону ответственности: ")
        employee = ZooKeeper(name, employee_id, salary, area)

    elif choice == "2":
        specialization = input("Введите специализацию: ")
        employee = Veterinarian(name, employee_id, salary, specialization)

    else:
        print("Неверный выбор.")
        return

    zoo.add_employee(employee)


def run_zoo_management_system():
    """Запускает систему управления зоопарком"""
    zoo = None

    while True:
        if zoo is None:
            choice = main_menu()

            if choice == "1":
                name = input("Введите название зоопарка: ")
                location = input("Введите местоположение зоопарка: ")
                zoo = Zoo(name, location)
                print(f"Зоопарк '{name}' создан!")

            elif choice == "2":
                filename = input("Введите имя файла (по умолчанию 'zoo_data.pickle'): ") or "zoo_data.pickle"
                temp_zoo = Zoo("Temp", "Temp")
                if temp_zoo.load_from_file(filename):
                    zoo = temp_zoo
                else:
                    print("Создаем демонстрационный зоопарк...")
                    zoo = create_demo_zoo()

            elif choice == "3":
                print("До свидания!")
                break

            else:
                print("Неверный выбор. Пожалуйста, выберите 1, 2 или 3.")

        else:  # zoo is not None
            choice = zoo_menu()

            if choice == "1":
                print(f"\nИнформация о зоопарке:\n{zoo}")

            elif choice == "2":
                zoo.list_animals()

            elif choice == "3":
                zoo.list_employees()

            elif choice == "4":
                add_animal_menu(zoo)

            elif choice == "5":
                add_employee_menu(zoo)

            elif choice == "6":
                zoo.list_animals()
                if not zoo.animals:
                    continue

                while True:
                    try:
                        index = int(input("\nВведите номер животного для удаления: ")) - 1
                        if zoo.remove_animal(index):
                            break
                        else:
                            print("Неверный номер. Попробуйте снова.")
                    except ValueError:
                        print("Введите число. Попробуйте снова.")

            elif choice == "7":
                zoo.list_employees()
                if not zoo.employees:
                    continue

                while True:
                    try:
                        index = int(input("\nВведите номер сотрудника для удаления: ")) - 1
                        if zoo.remove_employee(index):
                            break
                        else:
                            print("Неверный номер. Попробуйте снова.")
                    except ValueError:
                        print("Введите число. Попробуйте снова.")

            elif choice == "8":
                filename = input("Введите имя файла (по умолчанию 'zoo_data.pickle'): ") or "zoo_data.pickle"
                zoo.save_to_file(filename)

            elif choice == "9":
                save = input("Сохранить данные перед выходом? (да/нет): ").lower()
                if save == "да":
                    filename = input("Введите имя файла (по умолчанию 'zoo_data.pickle'): ") or "zoo_data.pickle"
                    zoo.save_to_file(filename)
                zoo = None

            else:
                print("Неверный выбор. Пожалуйста, выберите от 1 до 9.")


if __name__ == "__main__":
    run_zoo_management_system()