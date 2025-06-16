
def generate_key(text, key):
    """ 
    Функція для генерації повторюваної послідовності ключа,
    створює розширений ключ тієї ж довжини, що й текст,
    з урахуванням пробілів/символів.
    """
    key = key.upper()
    key_sequence = ""
    key_index = 0
    
    for char in text: # Проходжусь по кожному символу в тексті
        
        if char.isalpha(): # Якщо це літера то додаю наступну букву з ключа.
            key_sequence += key[key_index % len(key)]
            key_index += 1
            
        else: # Інакше просто додає символ без змін. Таким чином, ключ повторюється, але позиції пробілів та знаків зберігаються.
            key_sequence += char  # Зберігаю пробіли/символи
            
    return key_sequence




def encrypt_vigenere(plaintext, key):
    """ 
    Функція для шифрування тексту за допомогою шифру Віженера.
    """
    ciphertext = ""
    key_seq = generate_key(plaintext, key) # Створюю ключ 
    
    for p, k in zip(plaintext, key_seq):
        if p.isalpha():
            offset = 65 if p.isupper() else 97 # Визначаю, з якої літери починається алфавіт (A або a)
            k_offset = ord(k.upper()) - 65 # Обчислюю зсув від A для k (тобто скільки позицій зміщувати)
            
            encrypted_char = chr((ord(p.upper()) - 65 + k_offset) % 26 + offset) # ДОДАЮ зсув до p, та додаю залишок по довжині алфавіту 26(щоб уникнути від’ємних чисел)
            
            ciphertext += encrypted_char if p.isupper() else encrypted_char.lower() # Додаю зашифровану літеру до результату.
        else:
            ciphertext += p # Зберігаю пробіли/символи
    return ciphertext




def decrypt_vigenere(ciphertext, key):
    """ 
    Розшифровує текст, зашифрований шифром Віженера.
    Аналогічно до шифрування, але віднімає зсув замість додавання.
    """
    plaintext = ""
    key_seq = generate_key(ciphertext, key)
    for c, k in zip(ciphertext, key_seq):
        if c.isalpha():
            offset = 65 if c.isupper() else 97 # Визначаю, з якої літери починається алфавіт (A або a)
            k_offset = ord(k.upper()) - 65 # Обчислюю зсув від A для k (тобто скільки позицій зміщувати)
            
            decrypted_char = chr((ord(c.upper()) - 65 - k_offset + 26) % 26 + offset) # ВІДНІМАЮ зсув до p, та додаю залишок по довжині алфавіту 26(щоб уникнути від’ємних чисел)
            
            plaintext += decrypted_char if c.isupper() else decrypted_char.lower()# Додаю зашифровану літеру до результату.
        else:
            plaintext += c #
    return plaintext
