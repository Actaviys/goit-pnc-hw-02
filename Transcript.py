import re
from collections import Counter

# === Kasiski Examination ===
def kasiski_examination(ciphertext, min_len=3):
    """ 
    Функція методу Касіскі, шукає повторювані послідовності символів 
    у зашифрованому тексті.
    Ціль, виявити ймовірні відстані між повторами, щоб знайти довжину ключа.
    """
    spacings = []
    for i in range(len(ciphertext) - min_len):
        seq = ciphertext[i:i+min_len] # виділяємо підрядок довжини '3'
        for j in range(i + min_len, len(ciphertext) - min_len):
            if ciphertext[j:j+min_len] == seq:
                spacings.append(j - i) # зберігаємо відстань між повтореннями
    return spacings

def find_factors(numbers):
    """ 
    Функція для знаходження всіх множників кожного числа 
    зі вхідного списку `numbers`
    """
    factors = Counter()
    for number in numbers:
        for i in range(2, number + 1):
            if number % i == 0:
                factors[i] += 1 # рахуємо, скільки разів зустрічається кожен множник
    return factors
# #




# === Friedman Test ===
def friedman_test(ciphertext):
    """ 
    Функція тесту Фрідмана, 
    оцінює довжину ключа, базуючись на індексі співпадіння (IC).
    """
    N = len(ciphertext)
    freqs = Counter(ciphertext) # частота кожної букви
    numerator = sum(f * (f - 1) for f in freqs.values())
    denominator = N * (N - 1)
    IC = numerator / denominator if denominator != 0 else 0
    k_estimate = (0.027 * N) / ((N - 1) * IC - 0.038 * N + 0.065) # Формула оцінки довжини ключа (статистична модель)
    print(f"Індекс співпадіння: {IC:.4f}")
    return max(1, round(k_estimate))
# #




# === Частотний аналіз методом χ² (chi-squared test) ===
# Еталонна таблиця частотності літер в англійській мові (у %). Використовується в χ²-аналізі.
# Дані взято з Wikipedia - https://uk.wikipedia.org/wiki/%D0%90%D0%BD%D0%B3%D0%BB%D1%96%D0%B9%D1%81%D1%8C%D0%BA%D0%B0_%D0%B0%D0%B1%D0%B5%D1%82%D0%BA%D0%B0
ENGLISH_FREQ = {
    'A': 8.16, 'B': 1.49, 'C': 2.78, 'D': 4.25, 'E': 12.70,
    'F': 2.22, 'G': 2.01, 'H': 6.09, 'I': 6.96, 'J': 0.15,
    'K': 0.77, 'L': 4.02, 'M': 2.40, 'N': 6.74, 'O': 7.50,
    'P': 1.92, 'Q': 0.09, 'R': 5.98, 'S': 6.32, 'T': 9.05,
    'U': 2.75, 'V': 0.97, 'W': 2.36, 'X': 0.15, 'Y': 1.97,
    'Z': 0.07
}

def chi_squared_stat(text):
    """ 
    Функція для обчислення χ², 
    наскільки розподіл частот у вхідному тексті відрізняється від еталонного.
    """
    N = len(text)
    if N == 0:
        return float('inf')
    expected = {letter: ENGLISH_FREQ[letter] * N / 100 for letter in ENGLISH_FREQ}
    observed = Counter(text)
    
    # Формула χ² = сума ((спостережене - очікуване)^2 / очікуване)
    chi_squared = sum((observed.get(l, 0) - expected[l]) ** 2 / expected[l] for l in ENGLISH_FREQ)
    return chi_squared


def find_best_caesar_shift(text):
    """ 
    Функція для знаходження найкращого зсуву (0–25) для дешифрування вхідного тексту, 
    обчислює χ² для кожного варіанту.
    """
    min_chi = float('inf')
    best_shift = 0
    for shift in range(26):
        decrypted = ''.join( # зсув назад
            chr((ord(c) - ord('A') - shift) % 26 + ord('A')) if c.isalpha() else c
            for c in text
        )
        chi = chi_squared_stat(decrypted)
        if chi < min_chi: # обираємо зсув з найменшим χ²
            min_chi = chi
            best_shift = shift 
    return best_shift
# #




# === Vigenere breaker ===
def break_vigenere(ciphertext, key_len):
    """ 
    Функція для обчислення повного ключа шифру Віженера, 
    розбиває зашифрований текст на колонки і аналізує кожну.
    """
    key = '' # Змінна в якій буде зберігатися знайдений ключ
    for i in range(key_len):   
        column = ''.join(ciphertext[j] for j in range(i, len(ciphertext), key_len))
        shift = find_best_caesar_shift(column)
        key += chr((shift % 26) + ord('A')) # перетворює зсув у літеру ключа
    return key

def decrypt_vigenere(ciphertext, key):
    """ 
    Функція для розшифровки зашифрованого тексту, 
    використовуючи відомий ключ Віженера.
    """
    result = ''
    key_len = len(key)
    for i, c in enumerate(ciphertext):
        if c.isalpha():
            base = ord('A')
            shift = ord(key[i % key_len]) - base
            decrypted = chr((ord(c) - base - shift + 26) % 26 + base)
            result += decrypted
        else:
            result += c
    return result
# #




# === Повний процес дешифрування ===
def analyze_and_decrypt(ciphertext):
    """ 
    Функція для виконнаня повного процесу дешифрування без відомого ключа.
    Приймає зашифрований текст та пробує обчислити довжину ключа та сам ключ, 
    і пробує розшифрувати повідомлення за знайденим ключем.
    """
    ciphertext = re.sub(r'[^A-Z]', '', ciphertext.upper())
    if not ciphertext:
        print("Порожній або неправильний вхідний текст.")
        return ""

    print("\n--- Метод Касіскі ---")
    spacings = kasiski_examination(ciphertext)
    if spacings:
        factor_counts = find_factors(spacings)
        print("Ймовірні довжини ключа:", factor_counts.most_common(5))
    else:
        print("Не знайдено повторів для Касіскі.")

    print("\n--- Тест Фрідмана ---")
    estimated_len = friedman_test(ciphertext)
    print(f"Оцінка довжини ключа: {estimated_len}")

    key = break_vigenere(ciphertext, estimated_len)
    print(f"\nЗнайдений ключ: {key}")

    plaintext = decrypt_vigenere(ciphertext, key)
    return plaintext
# #
