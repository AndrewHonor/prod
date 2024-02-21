import os

# визначаємо функцію, яка приймає логін локального користувача віндовс
def check_folder(username):
    # формуємо шлях до папки на диску D, з таким же іменем як і логін користувача
    folder_path = f"D:\\{username}"
    # перевіряємо, чи існує така папка
    if os.path.exists(folder_path):
        # якщо так, то виводимо повідомлення, що папка існує
        return True
    else:
        # якщо ні, то виводимо повідомлення, що папки немає
        return False


check_folder('Admin')
check_folder('tu1')