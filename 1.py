# Імпортуємо модуль subprocess для запуску команд PowerShell
import subprocess

# Визначаємо функцію, яка приймає на себе логін і видавати інформацію по стрічці PasswordRequired
def check_password_required(username):
    # Створюємо команду PowerShell для отримання інформації про обліковий запис
    command = f"Get-LocalUser -Name {username} | Select-Object -ExpandProperty PasswordRequired"

    # Запускаємо команду PowerShell за допомогою subprocess і зберігаємо результат
    result = subprocess.run(["powershell", "-Command", command], capture_output=True, check=True)

    # Декодуємо результат з байтів у рядок
    output = result.stdout.decode()

    # Повертаємо результат без символів переносу рядка
    return output.strip()

# Викликаємо функцію з прикладним логіном
print(check_password_required("tu3"))
