import subprocess
import re
def get_user_info(username):
    try:
        # Викликаємо команду для отримання інформації про користувача
        result = subprocess.run(['net', 'user', username], capture_output=True, text=True)
        output = result.stdout

        # Виводимо інформацію про користувача
        print(output)
        return output
    except Exception as e:
        print("Сталася помилка при отриманні інформації про користувача:", e)


def parse_info(info_str):
    info_dict = {}
    # Визначення шаблонів для пошуку ключ-значення
    patterns = [
        (r'User name\s+([^\n]+)', 'User name'),
        (r'Full Name\s+([^\n]+)', 'Full Name'),
        (r'Country/region code\s+([^\n]+)', 'Country/region code'),
        (r'Account active\s+([^\n]+)', 'Account active'),
        (r'Account expires\s+([^\n]+)', 'Account expires'),
        (r'Password last set\s+([^\n]+)', 'Password last set'),
        (r'Password expires\s+([^\n]+)', 'Password expires'),
        (r'Password changeable\s+([^\n]+)', 'Password changeable'),
        (r'Password required\s+([^\n]+)', 'Password required'),
        (r'User may change password\s+([^\n]+)', 'User may change password'),
        (r'Workstations allowed\s+([^\n]+)', 'Workstations allowed'),
        (r'Logon script\s+([^\n]+)', 'Logon script'),
        (r'User profile\s+([^\n]+)', 'User profile'),
        (r'Home directory\s+([^\n]+)', 'Home directory'),
        (r'Last logon\s+([^\n]+)', 'Last logon'),
        (r'Logon hours allowed\s+([^\n]+)', 'Logon hours allowed'),
        (r'Local Group Memberships\s+([^\n]+)', 'Local Group Memberships'),
        (r'Global Group memberships\s+([^\n]+)', 'Global Group memberships')
    ]
    # Пошук та збір інформації за допомогою регулярних виразів
    for pattern, key in patterns:
        match = re.search(pattern, info_str)
        if match:
            info_dict[key] = match.group(1).strip()
        else:
            info_dict[key] = None

    return info_dict

# Викликаємо функцію для користувача з ім'ям "Admin"
x = get_user_info("Admin")
y = parse_info(x)
for key, value in y.items():
    print(f"{key}: {value}")

