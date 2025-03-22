import random
import time


class Hero:
    def __init__(self, name, health=100, attack_power=20):
        self.name = name
        self.health = health
        self.attack_power = attack_power

    def attack(self, other):
        # Случайный множитель урона (от 0.8 до 1.2) для разнообразия
        damage_multiplier = random.uniform(0.8, 1.2)
        damage = int(self.attack_power * damage_multiplier)

        other.health = max(0, other.health - damage)
        return damage

    def is_alive(self):
        return self.health > 0


class Game:
    def __init__(self):
        self.player = None
        self.computer = None

    def setup(self):
        print("\n" + "=" * 50)
        print("       Добро пожаловать в игру \"БИТВА ГЕРОЕВ\"!")
        print("=" * 50)

        player_name = input("\nВведите имя вашего героя: ")

        # Создаем героя игрока
        self.player = Hero(player_name)

        # Список возможных имен для компьютерного героя
        computer_names = ["Тёмный лорд", "Рыцарь хаоса", "Древний маг", "Дракон", "Безумный король"]
        computer_name = random.choice(computer_names)

        # Создаем героя компьютера
        self.computer = Hero(computer_name)

        print(
            f"\nВаш герой: {self.player.name} (Здоровье: {self.player.health}, Сила атаки: {self.player.attack_power})")
        print(
            f"Противник: {self.computer.name} (Здоровье: {self.computer.health}, Сила атаки: {self.computer.attack_power})")

    def display_status(self):
        print("\n" + "-" * 40)
        print(f"{self.player.name}: Здоровье = {self.player.health}")
        print(f"{self.computer.name}: Здоровье = {self.computer.health}")
        print("-" * 40)

    def start(self):
        self.setup()

        round_number = 1

        print("\nНачинаем битву!")
        time.sleep(1)

        # Определяем, кто ходит первым (случайно)
        current_attacker = random.choice([self.player, self.computer])

        while self.player.is_alive() and self.computer.is_alive():
            print(f"\nРаунд {round_number}")
            time.sleep(0.5)

            if current_attacker == self.player:
                defender = self.computer
                input("\nНажмите ENTER для атаки...")
            else:
                defender = self.player
                print("\nПротивник готовится к атаке...")
                time.sleep(1)

            damage = current_attacker.attack(defender)

            print(f"{current_attacker.name} атакует {defender.name} и наносит {damage} урона!")

            # Меняем атакующего
            current_attacker = defender

            self.display_status()

            round_number += 1
            time.sleep(0.5)

        # Объявляем победителя
        print("\n" + "=" * 50)
        if self.player.is_alive():
            print(f"Поздравляем! {self.player.name} победил!")
        else:
            print(f"К сожалению, {self.computer.name} победил. Попробуйте еще раз!")
        print("=" * 50)

    def play_again(self):
        choice = input("\nХотите сыграть ещё раз? (да/нет): ").lower()
        return choice == 'да' or choice == 'y' or choice == 'yes'


if __name__ == "__main__":
    game = Game()

    while True:
        game.start()
        if not game.play_again():
            print("\nСпасибо за игру! До встречи!")
            break
        game = Game()  # Создаем новую игру