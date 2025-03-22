from abc import ABC, abstractmethod
import random


# Абстрактный класс для оружия (Шаг 1)
class Weapon(ABC):
    def __init__(self, name, damage_range):
        self.name = name
        self.damage_range = damage_range  # Кортеж (min_damage, max_damage)

    @abstractmethod
    def attack(self):
        """Абстрактный метод атаки, который должен быть реализован в подклассах"""
        pass

    def get_damage(self):
        """Возвращает случайное значение урона из допустимого диапазона"""
        return random.randint(self.damage_range[0], self.damage_range[1])


# Конкретные типы оружия (Шаг 2)
class Sword(Weapon):
    def __init__(self, name="Меч", damage_range=(8, 12)):
        super().__init__(name, damage_range)

    def attack(self):
        damage = self.get_damage()
        message = f"Атака мечом! Нанесено {damage} урона"
        return damage, message


class Bow(Weapon):
    def __init__(self, name="Лук", damage_range=(5, 15)):
        super().__init__(name, damage_range)

    def attack(self):
        damage = self.get_damage()
        message = f"Выстрел из лука! Нанесено {damage} урона"
        return damage, message


class Wand(Weapon):
    def __init__(self, name="Волшебная палочка", damage_range=(3, 20)):
        super().__init__(name, damage_range)

    def attack(self):
        damage = self.get_damage()
        message = f"Магический удар! Нанесено {damage} урона"
        return damage, message


# Класс Fighter (Шаг 3)
class Fighter:
    def __init__(self, name, health=100, weapon=None):
        self.name = name
        self.health = health
        self.weapon = weapon

    def change_weapon(self, weapon):
        """Метод для смены оружия"""
        self.weapon = weapon
        print(f"{self.name} берёт {weapon.name}")

    def attack(self, monster):
        """Метод для атаки монстра"""
        if self.weapon is None:
            print(f"{self.name} не имеет оружия!")
            return False

        damage, message = self.weapon.attack()
        print(f"{self.name}: {message}")
        monster.take_damage(damage)

        if monster.health <= 0:
            print(f"{self.name} победил {monster.name}!")
            return True
        else:
            print(f"{monster.name} остался жив. Оставшееся здоровье: {monster.health}")
            return False

    def take_damage(self, damage):
        """Метод для получения урона"""
        self.health -= damage
        if self.health < 0:
            self.health = 0


# Класс Monster
class Monster:
    def __init__(self, name, health=50, damage_range=(3, 8)):
        self.name = name
        self.health = health
        self.damage_range = damage_range

    def attack(self, fighter):
        """Метод для атаки игрока"""
        damage = random.randint(self.damage_range[0], self.damage_range[1])
        print(f"{self.name} атакует {fighter.name} и наносит {damage} урона!")
        fighter.take_damage(damage)

        if fighter.health <= 0:
            print(f"{self.name} победил {fighter.name}!")
            return True
        else:
            print(f"{fighter.name} остался жив. Оставшееся здоровье: {fighter.health}")
            return False

    def take_damage(self, damage):
        """Метод для получения урона"""
        self.health -= damage
        if self.health < 0:
            self.health = 0


# Реализация боя (Шаг 4)
def battle(fighter, monster):
    """Реализация боя между бойцом и монстром"""
    print(f"\n=== Бой: {fighter.name} против {monster.name} ===")

    round_num = 1
    while fighter.health > 0 and monster.health > 0:
        print(f"\nРаунд {round_num}")

        # Боец атакует монстра
        if fighter.attack(monster):  # Монстр побежден
            return True

        # Монстр атакует бойца
        if monster.attack(fighter):  # Боец побежден
            return False

        round_num += 1

    # На случай ничьей или неожиданной ситуации
    return fighter.health > 0


def main():
    # Создаем бойца
    player = Fighter("Герой")

    # Создаем оружие
    sword = Sword()
    bow = Bow()
    wand = Wand()

    # Создаем монстров
    goblin = Monster("Гоблин", health=30, damage_range=(2, 6))
    orc = Monster("Орк", health=60, damage_range=(4, 10))
    dragon = Monster("Дракон", health=100, damage_range=(8, 15))

    # Проводим сражения
    player.change_weapon(sword)
    battle(player, goblin)

    # Если герой победил, лечим его и даем новое оружие
    if player.health > 0:
        player.health = min(100, player.health + 30)  # Немного лечим героя
        print(f"\n{player.name} отдыхает и восстанавливает здоровье. Текущее здоровье: {player.health}")

        player.change_weapon(bow)
        battle(player, orc)

    # Если герой все еще жив, встречаем финального босса
    if player.health > 0:
        player.health = min(100, player.health + 50)  # Полное исцеление перед финальным боссом
        print(f"\n{player.name} хорошо отдохнул и восстановил здоровье. Текущее здоровье: {player.health}")

        player.change_weapon(wand)
        battle(player, dragon)


if __name__ == "__main__":
    main()