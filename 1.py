import subprocess

def is_user_active(username):
    # Створюємо команду Powershell для запиту стану користувача
    command = f"quser /server:$env:COMPUTERNAME | Select-String {username}"

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

print(is_user_active('tu2'))