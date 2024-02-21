# імпортуємо модулі win32net і time
import win32net
import time

# створюємо функцію, яка отримує час останнього входу в систему
def get_last_logon(username):
    # отримуємо список користувачів і їх інформацію
    users, _, _ = win32net.NetUserEnum(None, 2)
    # перебираємо користувачів
    for user in users:
        # якщо знайшли потрібного користувача
        if user['name'] == username:
            # повертаємо його час останнього входу
            return user['last_logon']
    # якщо не знайшли потрібного користувача
    else:
        # повертаємо повідомлення про помилку
        return "Немає такого користувача"

# створюємо функцію, яка перетворює UNIX-час у формат чисел
def format_unix_time(unix_time):
    # перевіряємо, чи unix_time є числом
    if isinstance(unix_time, int):
        # визначаємо рядок з кодами форматування дати і часу
        time_format = "%Y-%m-%d %H:%M:%S"
        # перетворюємо UNIX-час у формат чисел
        formatted_time = time.strftime(time_format, time.gmtime(unix_time))
        # повертаємо результат
        return formatted_time
    else:
        # повертаємо те саме, що і unix_time
        return unix_time

# створюємо функцію, яка поєднує дві функції в одну
def combine_functions(outer, inner):
    # повертаємо лямбда-функцію, яка приймає будь-які аргументи
    return lambda *args: outer(inner(*args))

# створюємо функцію, яка знаходить час останнього входу в систему користувача і виводить його у форматі чисел
get_last_activity = combine_functions(format_unix_time, get_last_logon)

# викликаємо функцію з ім'ям користувача
print(get_last_activity("Admin"))

print(get_last_activity('Admin'))
print(get_last_activity('tu1'))
print(get_last_activity('tu2'))
print(get_last_activity('tu3'))
