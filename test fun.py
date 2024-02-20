import win32net
import subprocess


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
    # Додайте ваш код для перевірки наявності теки на диску "D" для користувача
    pass

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


