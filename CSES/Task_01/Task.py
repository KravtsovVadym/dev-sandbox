"""Класична задача Йосипа Флавія (Josephus problem)"""

def version_one(numbers: int) -> list[int]:
    """Cтворюємо поточне коло з N гравців, об'єктів, орків, ельфів"""
    circle = list(range(1, numbers + 1))

    """Змінна для зберігання порядку виключення гравців, об'єктів, орків, ельфів"""
    exclusion_order = []
    """Сurrent index гравця"""
    index = 0
    """Цикл працює доки circle players list не буде пустий"""
    while circle:
        """Шукаємо наступний індекс гравця"""
        index = (index + 1) % len(circle)
        """Добавляємо гравця який на черзі та видаляемо с кола"""
        exclusion_order.append(circle.pop(index))
    return exclusion_order




if __name__ == "__main__":
    print(version_one(1))  # [1]
    print(version_one(2))  # [2, 1]
    print(version_one(3))  # [2, 1, 3]
    print(version_one(7))  # [2, 4, 6, 1, 5, 3, 7]

    order = version_one(10 ** 5)
    print(order[-5:])  # [52545, 85313, 36161, 3393, 68929]


