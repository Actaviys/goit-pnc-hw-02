from pathlib import Path


launching_text = """Оберіть потрібне шифрування.
`V` - Шифр Віженера
`P` - Шифр перестановки
`T` - Табличний шифр
`q` or `close` - Вихід з програми"""


#
def readerTextFile(file_path):
    """ 
    Функція для читання текстових файлів.
    Повертає весь текст файлу як один рядок.
    """
    try:
        with open(file_path, "r+", encoding="utf-8") as file:
            content = file.read().replace("\n", " ")
        return content
    except FileNotFoundError:
        return None
    except Exception:
        return None
#



# Обробка шифра Віженера #
import VigenereСipher
import Transcript
secret_key_v = "CRYPTOGRAPHY"

def funcEncryptVigenere_cipher():
    """ 
    Функція обробки команд, для шифра Віженера.
    """
    encrypt_msg_buff = ""
    text_from_file = readerTextFile("Original_Text.txt")
    if text_from_file == None:
        return print("Невірний шлях до файлу або файл пошкоджено!!!")
    else:
        while(True):
            cmd_regimeEncr = input("Оберіть режим шифрування Віженера: \
                \n`1` - Шифрування Віженера \n`2` - Дешифрування по відомому ключу \
                \n`3` - Дешифрування без ключа \n`b` - Повернутись назад \n-> ")
            if cmd_regimeEncr == "b" or cmd_regimeEncr == "B": break
            
            elif cmd_regimeEncr == "1":
                encrypt_msg_buff = VigenereСipher.encrypt_vigenere(text_from_file, secret_key_v)
                print(f"Зашифроване повідомлення: \n{encrypt_msg_buff}")
            
            elif cmd_regimeEncr == "2":
                message_decrypt = VigenereСipher.decrypt_vigenere(encrypt_msg_buff, secret_key_v)
                print(f"Розшифроване повідомлення за ключем: \n{message_decrypt}")
            
            elif cmd_regimeEncr == "3":
                msg_decrypted = Transcript.analyze_and_decrypt(encrypt_msg_buff)
                print(f"Спроба розшифрувати без відомого ключа: \n{msg_decrypted}")
            
            else: print("Невірна команда!")
# #



# Обробка шифра перестановки #
import PermutationCipher
secret_key1_p = "SECRET"
secret_key2_dp = "CRYPTO"

def commandFuncEncryptPermutation_cipher():
    """ 
    Функція обробки команд, для шифра перестановки.
    """
    encrypt_text_perm_buff = ""
    encrypt_text_double_perm_buff = ""
    text_from_file = readerTextFile("Original_Text.txt")
    if text_from_file == None:
        return print("Невірний шлях до файлу або файл пошкоджено!!!")
    else:
        while (True):
            regimeEncr = input("Оберіть режим для шифру перестановки: \
                \n`1` - Шифрування методом перестановки \n`2` - Дешифрування перестановки \
                \n`3` - Шифрування методом подвійної перестановки \n`4` - Дешифрування подвійної перестановки \
                \n`b` - Повернутись назад \n-> ")
            if regimeEncr == "b" or regimeEncr == "B": break
                
            elif regimeEncr == "1":
                encrypt_text_perm_buff = PermutationCipher.transpose_encrypt(text_from_file, secret_key1_p)
                print(f"Зашифроване повідомлення: \n{encrypt_text_perm_buff}")
                
                
            elif regimeEncr == "2":
                decrypt_perm_text = PermutationCipher.transpose_decrypt(encrypt_text_perm_buff, secret_key1_p)
                print(f"Дешифроване повідомлення: \n{decrypt_perm_text}")
            
            elif regimeEncr == "3":
                encrypt_text_double_perm_buff = PermutationCipher.double_transpose_encrypt(text_from_file, secret_key1_p, secret_key2_dp)
                print(f"Зашифроване повідомлення методом подвійної перестановки: \n{encrypt_text_double_perm_buff}")
            
            elif regimeEncr == "4":
                decrypt_double_perm_text = PermutationCipher.double_transpose_decrypt(encrypt_text_double_perm_buff, secret_key1_p, secret_key2_dp)
                print(f"Дешифроване повідомлення з подвійної перестановки: \n{decrypt_double_perm_text}")   
            
            else: print("Невірна команда!")
# #





# Обробка табличного шифру #
import TableCipher
secret_key_t = "MATRIX"
secret_key_tv = "CRYPTO"

def commandFuncEncryptTable_cipher():
    """ 
    Функція обробки команд, для звичайного табличного шифрування, 
    та з допомогою шифру Віженера.
    """
    encrypted_text_table_buff = ""
    encryptVigenere_text_buff = ""
    encryptTable_text_buff = ""
    
    text_from_file = readerTextFile("Original_Text.txt")
    if text_from_file == None:
        return print("Невірний шлях до файлу або файл пошкоджено!!!")
    else:
        while(True):
            regimeEncr = input("Оберіть тип табличного шифру: \
                \n`1` - Табличне шифрування \n`2` - Табличне дешифрування\
                \n`3` - Шифр Віженера з табличним шифруванням \n`4` - Дешифрування Віженера та табличного шифрів \
                \n`b` - Повернутись назад \n-> ")
            if regimeEncr == "b" or regimeEncr == "B": break
            
            elif regimeEncr == "1":
                encrypted_text_table_buff = TableCipher.matrix_encrypt(text_from_file, secret_key_t)
                print(encrypted_text_table_buff)
            
            elif regimeEncr == "2":
                decrypt_text_tabl = TableCipher.matrix_decrypt(encrypted_text_table_buff, secret_key_t)
                print(decrypt_text_tabl)
                
            elif regimeEncr == "3":
                encryptVigenere_text_buff = VigenereСipher.encrypt_vigenere(text_from_file, secret_key_tv)
                encryptTable_text_buff = TableCipher.matrix_encrypt(encryptVigenere_text_buff, secret_key_tv)
                print(encryptTable_text_buff)
                # funcCipherTable_and_CipherVigenere()
            
            elif regimeEncr == "4":
                decryptTable_text = TableCipher.matrix_decrypt(encryptTable_text_buff, secret_key_tv)
                decryptVigenere_text = VigenereСipher.decrypt_vigenere(decryptTable_text, secret_key_tv)
                print(decryptVigenere_text)
            
            else: print("Невірна команда!")
# #







#
def main():
    while(True):
        print(launching_text)
        input_commands = str(input("> "))
        if input_commands == "q" or input_commands == "close": break
        
        elif input_commands == "V" or input_commands == "v":
            print("Шифр Віженера")
            funcEncryptVigenere_cipher()
            
        elif input_commands == "P" or input_commands == "p":
            print("Шифр перестановки")
            commandFuncEncryptPermutation_cipher()
            
        elif input_commands == "T" or input_commands == "t":
            print("Табличний шифр")
            commandFuncEncryptTable_cipher()
            
        else: print(f"Невірна команда!")


if __name__ == '__main__':
    main()
#