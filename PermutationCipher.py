import math

def get_order(key):
    """
    Створює список індексів для символів ключа і 
    сортує ці індекси за алфавітним порядком літер ключа.
    Повертає порядок індексів стовпців після сортування ключа, 
    """
    return sorted(range(len(key)), key=lambda k: key[k])



def transpose_encrypt(text, key):
    """ 
    Функція шифрування тексту методом перестановки. 
    """
    key_order = get_order(key) # Отримую порядок стовпців
    n_cols = len(key) # Зберігаю кількість стовпців
    n_rows = math.ceil(len(text) / n_cols) # Загальна кількість рядків у таблиці
    padded_text = text.ljust(n_rows * n_cols)  # Заповнюємо пробілами для вирівнювання

    # Створюємо матрицю рядків
    matrix = [padded_text[i:i + n_cols] for i in range(0, len(padded_text), n_cols)]

    # Читаю текст по стовпцях (згідно з порядком ключа).
    encrypted = ""
    for index in key_order:
        for row in matrix:
            encrypted += row[index] # Зберігаємо символи стовпця
    return encrypted # Повертаю зашифрований текст




def transpose_decrypt(cipher, key):
    """ 
    Функція дешифрування, зашифрованого тексту методом перестановки, 
    відновлює таблицю по стовпцях.
    """
    key_order = get_order(key) # Отримую порядок стовпців
    n_cols = len(key) # Зберігаю кількість стовпців
    n_rows = math.ceil(len(cipher) / n_cols) # Загальна кількість рядків у таблиці
    n_full = n_rows * n_cols
    padded_cipher = cipher.ljust(n_full) # Доповнюю якщо не ділиться націло

    col_length = n_rows # Зберігаю кількість символів у кожному стовпці
    cols = [""] * n_cols # Підготовляю порожні стовпців
    index = 0

    # Розбиває шифртекст на колонки в правильному порядку (відповідно до ключа).
    for col_index in key_order: 
        cols[col_index] = padded_cipher[index:index + col_length]
        index += col_length

    decrypted = ""
    for row in zip(*cols): # Об’єдную елементи кожного рядка
        decrypted += "".join(row)
    return decrypted.rstrip()  # Видаляю зайві пробіли справа




# Подвійна перестановка: 
def double_transpose_encrypt(text, key1, key2):
    """ 
    Спочатку шифрує `text` з ключем `key1`, потім ще раз — з ключем `key2`
    """
    return transpose_encrypt(transpose_encrypt(text, key1), key2)


def double_transpose_decrypt(cipher, key1, key2):
    """ 
    У зворотньому порядку шифрування, спочатку розшифровує з `key2`, потім з `key1`.
    """
    return transpose_decrypt(transpose_decrypt(cipher, key2), key1)

