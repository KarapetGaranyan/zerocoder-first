class User:
    def __init__(self, user_id, name):
        self.__user_id = user_id
        self.__name = name
        self.__access_level = 'user'

    def get_user_id(self):
        return self.__user_id

    def get_name(self):
        return self.__name

    def set_name(self, name):
        self.__name = name

    def get_access_level(self):
        return self.__access_level

    def __str__(self):
        return f"ID: {self.__user_id}, Name: {self.__name}, Access Level: {self.__access_level}"


class Admin(User):
    def __init__(self, user_id, name):
        super().__init__(user_id, name)
        self.__admin_access_level = 'admin'
        self.__user_list = []

    def get_admin_access_level(self):
        return self.__admin_access_level

    def add_user(self, user):
        if isinstance(user, User):
            # Проверяем, что пользователя с таким ID еще нет в списке
            for existing_user in self.__user_list:
                if existing_user.get_user_id() == user.get_user_id():
                    print(f"Пользователь с ID {user.get_user_id()} уже существует в системе")
                    return False
            self.__user_list.append(user)
            print(f"Пользователь {user.get_name()} успешно добавлен в систему")
            return True
        else:
            print("Ошибка: объект не является пользователем")
            return False

    def remove_user(self, user_id):
        for i, user in enumerate(self.__user_list):
            if user.get_user_id() == user_id:
                removed_user = self.__user_list.pop(i)
                print(f"Пользователь {removed_user.get_name()} с ID {user_id} успешно удален из системы")
                return True
        print(f"Пользователь с ID {user_id} не найден в системе")
        return False

    def list_users(self):
        if not self.__user_list:
            print("Список пользователей пуст")
            return []

        print("Список пользователей:")
        for user in self.__user_list:
            print(user)

        return self.__user_list

    def __str__(self):
        return f"ID: {self.get_user_id()}, Name: {self.get_name()}, " \
               f"Base Access Level: {self.get_access_level()}, Admin Access Level: {self.__admin_access_level}"

# Создаем администратора
admin1 = Admin(1, "Иван Петров")

# Создаем обычных пользователей
user1 = User(101, "Анна Смирнова")
user2 = User(102, "Сергей Иванов")
user3 = User(103, "Мария Козлова")

# Администратор добавляет пользователей в систему
admin1.add_user(user1)
admin1.add_user(user2)
admin1.add_user(user3)

# Выводим список пользователей
admin1.list_users()

# Удаляем пользователя
admin1.remove_user(102)

# Проверяем обновленный список
admin1.list_users()

# Пытаемся добавить пользователя с существующим ID
user4 = User(101, "Дмитрий Сидоров")
admin1.add_user(user4)