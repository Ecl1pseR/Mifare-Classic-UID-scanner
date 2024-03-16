import os  # Імпортуємо модуль для взаємодії з операційною системою
import time  # Імпортуємо модуль для роботи з часом
from datetime import datetime  # Імпортуємо клас datetime для роботи з датою та часом
from smartcard.System import readers  # Імпортуємо модуль для роботи з NFC-рідерами
from smartcard.util import toHexString  # Імпортуємо функцію для конвертації даних в шістнадцятковий формат
from smartcard.Exceptions import NoCardException, CardConnectionException  # Імпортуємо виключення для NFC-карт

UID_FILE_PREFIX = "scanned_uid_"  # Префікс для назв файлів UID

def get_uid(connection):
    GET_UID = [0xFF, 0xCA, 0x00, 0x00, 0x00]  # Команда для отримання UID з карти
    data, sw1, sw2 = connection.transmit(GET_UID)  # Відправляємо команду та отримуємо відповідь
    if sw1 == 144:  # Перевіряємо, чи відповідь успішна
        return toHexString(data).replace(" ", "") + '000000000000'  # Повертаємо UID у шістнадцятковому форматі
    return None  # Якщо отримання UID невдале, повертаємо None

def check_uid_in_file(uid, file_path):
    with open(file_path, 'a+') as file:  # Відкриваємо файл для читання та запису
        file.seek(0)  # Переміщаємо курсор на початок файлу
        return uid in file.read()  # Перевіряємо, чи присутній UID у файлі

def create_uid_file(today_date):
    return f"{UID_FILE_PREFIX}{today_date}.txt"  # Створюємо назву файлу на основі поточної дати

def main():
    uid_count = 0  # Лічильник UID
    r = readers()  # Ініціалізуємо NFC-рідери
    if not r:  # Перевіряємо, чи знайдені рідери
        print("NFC-рідери не знайдені.")  # Виводимо повідомлення про відсутність рідерів
        print("Робота завершена. До побачення")  # Виводимо повідомлення про завершення роботи
        time.sleep(3)  # Затримка перед завершенням програми
        return

    print("Підключені рідери:", r)  # Виводимо інформацію про підключені рідери
    print("Кількість відсканованих UID:", uid_count)  # Виводимо початкове значення лічильника UID
    print("Покладіть карту для отримання UID...")  # Запрошуємо користувача покласти карту для сканування
    
    card_present = False  # Змінна для відстеження наявності карти
    today_date = datetime.now().strftime("%d%m%Y")  # Отримуємо поточну дату
    uid_file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), create_uid_file(today_date))  # Формуємо шлях до файлу UID

    try:
        while True:
            for reader in r:  # Проходимо по кожному рідеру
                with reader.createConnection() as connection:  # Встановлюємо з'єднання з кожним рідером
                    try:
                        connection.connect()  # Встановлюємо з'єднання з карткою
                        uid = get_uid(connection)  # Отримуємо UID з карти
                        if uid:  # Якщо отримали UID
                            if not card_present:  # Якщо карта вперше виявлена
                                if check_uid_in_file(uid, uid_file_path):  # Перевіряємо, чи вже записаний цей UID в файл
                                    print("\033[2J\033[H")  # Очищаємо екран
                                    print("Кількість відсканованих UID:", uid_count)  # Виводимо поточну кількість UID
                                    print("Цей UID вже записаний")  # Повідомляємо, що UID вже був записаний раніше                                
                                else:
                                    uid_count += 1  # Збільшуємо лічильник UID
                                    print("\033[2J\033[H")  # Очищаємо екран
                                    print("Кількість відсканованих UID:", uid_count)  # Виводимо поточну кількість UID
                                    with open(uid_file_path, 'a') as file:  # Відкриваємо файл для дописування
                                        file.write(uid + '\n')  # Записуємо UID у файл
                                    print("UID:", uid)  # Виводимо отриманий UID
                                card_present = True  # Встановлюємо прапорець, що карта присутня
                    except NoCardException:  # Обробляємо виняток, коли карта не знайдена
                        if card_present:  # Якщо карта була присутня
                            print("Покладіть іншу карту для отримання UID...")  # Запрошуємо покласти іншу карту для сканування
                            card_present = False  # Встановлюємо прапорець, що карта відсутня
                    except CardConnectionException as e:  # Обробляємо виняток, коли виникає помилка з'єднання з карткою
                        print("Помилка з'єднання з картою:", e)  # Виводимо повідомлення про помилку з'єднання
                        print("\033[2J\033[H")  # Очищаємо екран
                        print("Кількість відсканованих UID:", uid_count)  # Виводимо поточну кількість UID
                        print("UID:", uid)  # Виводимо отриманий UID
                        print("Покладіть іншу карту для отримання UID...")  # Запрошуємо покласти іншу карту для сканування
                        card_present = False  # Встановлюємо прапорець, що карта відсутня
    except KeyboardInterrupt:  # Обробляємо виняток, коли користувач натискає Ctrl+C
        print("\033[2J\033[H")  # Очищаємо екран
        print("Кількість відсканованих UID:", uid_count)  # Виводимо кількість відсканованих UID
        print("Програма завершена. До побачення")  # Виводимо повідомлення про завершення роботи програми
        time.sleep(2)  # Затримка перед завершенням програми

if __name__ == "__main__":
    main()  # Викликаємо головну функцію, якщо скрипт запускається безпосередньо
