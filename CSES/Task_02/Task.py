"""Часова складність програми O(n) лінійна складність """
def find_sums(numbers, size):
    """Визначаємо змінну num_size для зберігання загальної кількості елементів"""
    num_size = len(numbers)

    result = []
    """Обчислюємо та додаємо до результату суму першого підсписку"""
    result.append(sum(numbers[0:size]))
    """Створюємо цикл for з кількості потрібних нам ітерацій для правильного завершення програми"""
    for i in range(num_size - size ):
        """В блоку else робимо математичні операції для отримання наступної суми підсписку"""
        x = result[-1]
        x = x - numbers[i] + numbers[size + i]
        result.append(x)
    return result


if __name__ == "__main__":
    print(find_sums([1], 1)) # [1]
    print(find_sums([1, 8, 2, 7, 3, 6, 4, 5], 6)) # [27, 30, 27]

    print(find_sums([1, 2, 3, 4, 5], 1)) # [1, 2, 3, 4, 5]
    print(find_sums([1, 2, 3, 4, 5], 2)) # [3, 5, 7, 9]
    print(find_sums([1, 2, 3, 4, 5], 3)) # [6, 9, 12]
    print(find_sums([1, 2, 3, 4, 5], 4)) # [10, 14]
    print(find_sums([1, 2, 3, 4, 5], 5)) # [15]

    numbers = list(range(10**5))
    sums = find_sums(numbers, 10**4)
    print(sums[5]) # 50045000
    print(sums[42]) # 50415000
    print(sums[1337]) # 633650002

