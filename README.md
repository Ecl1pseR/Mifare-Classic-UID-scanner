# Mifare Classic UID Scanner

Цей Python скрипт дозволяє сканувати та записувати унікальні ідентифікатори (UID) з NFC карт за допомогою NFC рідерів. Він безперервно сканує NFC картки та записує їх UID у файл, забезпечуючи, що кожен UID буде записаний тільки один раз (щоб уникнути повторень).

## Особливості

- **Сканування NFC Карт**: Автоматично визначає та сканує NFC картки, коли вони розміщені поруч з NFC рідером.
- **Запис Унікальних Ідентифікаторів**: Записує UID кожної сканованої картки у файл, забезпечуючи, що кожен UID буде записаний тільки один раз (щоб уникнути повторень).
- **Інтерактивний Вивід У Консоль**: Забезпечує інтерактивний вивід у консоль, інформуючи користувача про процес сканування та будь-які виявлені помилки.
- **Постійне Зберігання UID**: Зберігає записані UID у файлі з унікальною назвою, що базується на поточній даті.

## Залежності

- Python 3.x
- Бібліотека `smartcard` (встановлюється за допомогою `pip install pyscard`)

## Використання

1. Підключіть ваш NFC рідер до комп'ютера.
2. Запустіть Python скрипт `UID_scanner.py`.
3. Покладіть NFC картку на рідер.
4. Скрипт автоматично виявить та запише UID сканованої картки.
5. Кожний UID буде записаний у окремий файл з назвою `scanned_uid_<дата>.txt` у тій самій папці, що і скрипт.

## Примітка

- Цей скрипт потребує сумісного NFC рідера та відповідних драйверів, встановлених на вашій системі.
- Переконайтеся, що ваша система має необхідні дозволи для доступу до пристрою NFC рідера.
- У моєму випадку використовувався NFC рідер ACR122U
