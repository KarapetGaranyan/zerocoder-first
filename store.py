class Store:
    def __init__(self, name, address):
        self.name = name
        self.address = address
        self.items = {}

    def add_item(self, item_name, price):
        self.items[item_name] = price
        return f"{item_name} добавлен по цене {price}"

    def remove_item(self, item_name):
        if item_name in self.items:
            del self.items[item_name]
            return f"{item_name} удален из ассортимента"
        return f"{item_name} не найден в ассортименте"

    def get_price(self, item_name):
        return self.items.get(item_name)

    def update_price(self, item_name, new_price):
        if item_name in self.items:
            self.items[item_name] = new_price
            return f"Цена {item_name} обновлена до {new_price}"
        return f"{item_name} не найден в ассортименте"

    def __str__(self):
        return f"Магазин: {self.name}\nАдрес: {self.address}\nТоваров: {len(self.items)}"


# Создаем магазины
store1 = Store("Продукты у дома", "ул. Ленина, 15")
store2 = Store("ЭкоМаркет", "пр. Мира, 78")
store3 = Store("Фермерский рынок", "ул. Садовая, 42")

# Добавляем товары в первый магазин
store1.add_item("яблоки", 120)
store1.add_item("молоко", 85)
store1.add_item("хлеб", 45)
store1.add_item("сыр", 320)

# Добавляем товары во второй магазин
store2.add_item("органические яблоки", 180)
store2.add_item("гречка", 95)
store2.add_item("йогурт", 65)
store2.add_item("миндаль", 420)

# Добавляем товары в третий магазин
store3.add_item("помидоры", 150)
store3.add_item("огурцы", 110)
store3.add_item("зелень", 50)
store3.add_item("мед", 550)

# Тестируем методы на первом магазине
print(store1)
print("\nТовары в магазине:", store1.items)

# Добавляем новый товар
print("\n", store1.add_item("бананы", 140))
print("Товары после добавления:", store1.items)

# Получаем цену товара
milk_price = store1.get_price("молоко")
print(f"\nЦена молока: {milk_price}")

# Обновляем цену товара
print("\n", store1.update_price("хлеб", 52))
print("Товары после обновления цены:", store1.items)

# Удаляем товар
print("\n", store1.remove_item("сыр"))
print("Товары после удаления:", store1.items)

# Пробуем получить цену отсутствующего товара
print(f"\nЦена удаленного товара 'сыр': {store1.get_price('сыр')}")

# Пробуем обновить цену отсутствующего товара
print("\n", store1.update_price("колбаса", 280))