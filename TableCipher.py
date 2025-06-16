import math


def get_column_order(key):
    """
    Повертає порядок індексів стовпців згідно з алфавітним порядком букв ключа.
    Створює список позицій та сортує ці позиції відповідно до символів ключа, 
    для визначення порядку зчитування стовпців.
    """
    return sorted(range(len(key)), key=lambda i: key[i])



def matrix_encrypt(text, key):
    """ 
    Функція шифрування тексту з допомогою табличної перестановки, 
    базуючись на ключовій фразі.
    """
    n_cols = len(key) # Кількість стовпців = довжина ключа
    n_rows = math.ceil(len(text) / n_cols) # Кількість рядків

    # Доповнюємо текст до повної таблиці (враховуємо пробіли)
    padded_text = text.ljust(n_cols * n_rows, " ")

    # Формуємо таблицю рядків
    matrix = [padded_text[i:i + n_cols] for i in range(0, len(padded_text), n_cols)]

    # Отримуємо порядок стовпців згідно ключа
    col_order = get_column_order(key)
    
    # Читаємо по стовпцях у порядку сортування ключа
    ciphertext = ""
    for col in col_order:
        for row in matrix:
            ciphertext += row[col] # Додаю символ з цієї колонки
    return ciphertext



def matrix_decrypt(ciphertext, key):
    """ 
    Функція що розшифровує текст, зашифрований табличною перестановкою 
    з тим самим ключем.
    """
    n_cols = len(key) # Кількість стовпців
    n_rows = math.ceil(len(ciphertext) / n_cols) # Кількість рядків

    total_chars = n_cols * n_rows # Загальна кількість клітинок
    padded_cipher = ciphertext.ljust(total_chars, " ") # Доповнюємо, якщо потрібно

    # Отримуємо порядок колонок
    col_order = get_column_order(key)

    # Розбиваємо на стовпці в правильному порядку
    cols = [""] * n_cols # Підготовка пустих колонок
    index = 0
    for col in col_order:
        cols[col] = padded_cipher[index:index + n_rows] # Вставляємо кожну колонку
        index += n_rows

    # Збираємо по рядках
    plaintext = ""
    for i in range(n_rows):
        for j in range(n_cols):
            plaintext += cols[j][i] # Відновлюємо по рядках
    return plaintext.rstrip() # Повертає результат та видаляє пробіли праворуч

