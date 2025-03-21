class Task:
    def __init__(self, description, deadline):
        self.description = description
        self.deadline = deadline
        self.completed = False

    def mark_completed(self):
        self.completed = True

    def __str__(self):
        status = "Выполнено" if self.completed else "Не выполнено"
        return f"Задача: {self.description}, Срок: {self.deadline}, Статус: {status}"


class TaskManager:
    def __init__(self):
        self.tasks = []

    def add_task(self, description, deadline):
        new_task = Task(description, deadline)
        self.tasks.append(new_task)
        return new_task

    def mark_task_completed(self, task_index):
        if 0 <= task_index < len(self.tasks):
            self.tasks[task_index].mark_completed()
            return True
        return False

    def get_active_tasks(self):
        return [task for task in self.tasks if not task.completed]

    def display_active_tasks(self):
        active_tasks = self.get_active_tasks()
        if not active_tasks:
            print("Нет активных задач")
        else:
            print("Активные задачи:")
            for i, task in enumerate(active_tasks):
                print(f"{i + 1}. {task}")

# Создаем менеджер задач
manager = TaskManager()

# Добавляем задачи
manager.add_task("Подготовить отчет", "21.04.2025")
manager.add_task("Позвонить клиенту", "25.03.2025")
manager.add_task("Оплатить счета", "30.03.2025")

# Выводим активные задачи
manager.display_active_tasks()

# Отмечаем одну задачу как выполненную
manager.mark_task_completed(1)

# Снова выводим активные задачи
manager.display_active_tasks()