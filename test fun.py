import win32net
import subprocess
import time
import os

users_template = []
user_template = {
    'login': None,
    'Account active': None,  # Чи активний обліковий запис
    'Last logon': None,  # час останнього входу користувача
    'Local Group Memberships': None,  # Членство в локальних групах
    'has_password': False,  # По замовчуванню пароль відсутній
    'has_folder_d': False,  # По замовчуванню тека на диску "D" відсутня
    'folder_d_access': False,  # По замовчуванню доступ не заблоковано
    'cmd_access_blocked': False,  # По замовчуванню доступ до командного рядка не заблоковано
    'powershell_access_blocked': False  # По замовчуванню доступ до Powershell не заблоковано
}

def get_windows_users():
    #Створює список користувачів
    excluded_users = ["WDAGUtilityAccount", "Guest", "DefaultAccount"]
    users_list = []
    try:
        user_info, total, _ = win32net.NetUserEnum(None, 2)
        for user in user_info:
            username = user['name']
            if username not in excluded_users:
                users_list.append(username)
    except Exception as e:
        print("Помилка: ", e)
    return users_list


def is_user_active(user):
    # Створюємо команду Powershell для запиту стану користувача
    command = f"quser /server:$env:COMPUTERNAME | Select-String {user}"

    try:
        # Запускаємо команду Powershell і отримуємо результат
        output = subprocess.check_output(["powershell.exe", command], stderr=subprocess.STDOUT)

        # Перевіряємо, чи містить результат слово "Active"
        if b"Active" in output:
            return True
        else:
            return False
    except subprocess.CalledProcessError as e:
        # Якщо команда повертає ненульовий код виходу, то користувач не існує або виникла помилка
        print(f"Error: {e.output.decode()}")
        return None

def get_last_activity(user_time_acrive):
    # отримуємо список користувачів і їх інформацію
    users, _, _ = win32net.NetUserEnum(None, 2)
    # перебираємо користувачів
    for user in users:
        # якщо знайшли потрібного користувача
        if user['name'] == user_time_acrive:
            # повертаємо його час останнього входу
            unix_time = user['last_logon']
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
    # якщо не знайшли потрібного користувача
    else:
        # повертаємо повідомлення про помилку
        return "False"

def check_user_group(user):
    # отримуємо список груп, до яких належить користувач
    groups = win32net.NetUserGetLocalGroups(None, user)
    # перевіряємо, чи є серед них група адміністраторів
    if "Administrators" in groups:
        # якщо так, то виводимо повідомлення, що користувач є адміністратором
        return "ADMIN"
    else:
        # якщо ні, то виводимо повідомлення, що користувач є звичайним юзером
        return f"USER"

def check_has_password(user):
    # Створюємо команду PowerShell для отримання інформації про обліковий запис
    command = f"Get-LocalUser -Name {user} | Select-Object -ExpandProperty PasswordRequired"

    # Запускаємо команду PowerShell за допомогою subprocess і зберігаємо результат
    result = subprocess.run(["powershell", "-Command", command], capture_output=True, check=True)

    # Декодуємо результат з байтів у рядок
    output = result.stdout.decode()

    # Повертаємо результат без символів переносу рядка
    return output.strip()


def check_has_folder_d(user):
    # формуємо шлях до папки на диску D, з таким же іменем як і логін користувача
    folder_path = f"D:\\{user}"
    # перевіряємо, чи існує така папка
    if os.path.exists(folder_path):
        # якщо так, то виводимо повідомлення, що папка існує
        return True
    else:
        # якщо ні, то виводимо повідомлення, що папки немає
        return False

def check_folder_d_access(user):
    # Додайте ваш код для перевірки доступу до теки на диску "D" для користувача
    pass

def check_cmd_access_blocked(user):
    # Додайте ваш код для перевірки заблокованості доступу до командного рядка для користувача
    pass

def check_powershell_access_blocked(user):
    # Додайте ваш код для перевірки заблокованості доступу до Powershell для користувача
    pass

def get_user_details(user):
    new_user = user_template.copy()
    new_user['login'] = user
    new_user['Account active'] = is_user_active(user)
    new_user['Last logon'] = get_last_activity(user)
    new_user['Local Group Memberships'] =check_user_group(user)
    new_user['has_password'] = check_has_password(user)
    new_user['has_folder_d'] = check_has_folder_d(user)
    new_user['folder_d_access'] = check_folder_d_access(user)
    new_user['cmd_access_blocked'] = check_cmd_access_blocked(user)
    new_user['powershell_access_blocked'] = check_powershell_access_blocked(user)
    return new_user

# Отримання списку користувачів
users = get_windows_users()

# Отримання деталей для кожного користувача
for user in users:
    user_details = get_user_details(user)
    users_template.append(user_details)

print("Деталі користувачів Windows:", users_template)


