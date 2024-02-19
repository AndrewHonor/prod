import win32net
import subprocess
users_template = []
user_template = {
        'login': None,
        'has_password': False,  # По замовчуванню пароль відсутній
        'has_folder_d': False,  # По замовчуванню тека на диску "D" відсутня
        'folder_d_access': False,    # По замовчуванню доступ не заблоковано
        'cmd_access_blocked': False,  # По замовчуванню доступ до командного рядка не заблоковано
        'powershell_access_blocked': False  # По замовчуванню доступ до Powershell не заблоковано
        }





def get_windows_users():
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

# Приклад використання функції
users = get_windows_users()
print("Список користувачів Windows:", users)


for user in users:
    new_user = user_template.copy()
    new_user['login'] = user


    def check_has_password(user):
        # Створюємо команду PowerShell для отримання інформації про обліковий запис
        command = f"Get-LocalUser -Name {user} | Select-Object PasswordRequired"

        # Запускаємо команду PowerShell за допомогою subprocess і зберігаємо результат
        result = subprocess.run(["powershell", "-Command", command], capture_output=True, check=True)

        # Декодуємо результат з байтів у рядок
        output = result.stdout.decode()

        # Повертаємо результат
        return output


    def check_has_folder_d(user):
        pass


    def check_folder_d_access(user):
        pass


    def check_cmd_access_blocked(user):
        pass


    def check_powershell_access_blocked(user):
        pass

###########################################################################



