import win32net
import win32security
import ntsecuritycon as con
import subprocess

def check_password_enabled(username):
    try:
        user_info = win32net.NetUserGetInfo(None, username, 0)
        return user_info['password_expired'] == 0
    except Exception as e:
        print("Error checking password:", str(e))
        return False

def check_folder_access(username):
    try:
        security_descriptor = win32security.GetFileSecurity('D:\\' + username, win32security.DACL_SECURITY_INFORMATION)
        dacl = security_descriptor.GetSecurityDescriptorDacl()
        for ace in dacl:
            trustee_name, _, _ = win32security.LookupAccountSid(None, ace[1])
            if trustee_name.lower() == username.lower() and (ace[0] == con.FILE_GENERIC_READ or ace[0] == con.FILE_GENERIC_WRITE):
                return True
        return False
    except Exception as e:
        print("Error checking folder access:", str(e))
        return False

def check_admin_rights(username):
    try:
        output = subprocess.check_output(['net', 'localgroup', 'Administrators'])
        output_str = output.decode('utf-8')
        return username in output_str
    except subprocess.CalledProcessError:
        return False

def check_cmd_access(username):
    try:
        subprocess.Popen(['runas', '/user:' + username, 'cmd.exe'], stderr=subprocess.PIPE, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        return True
    except subprocess.CalledProcessError:
        return False

def check_powershell_access(username):
    try:
        subprocess.Popen(['runas', '/user:' + username, 'powershell.exe'], stderr=subprocess.PIPE, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        return True
    except subprocess.CalledProcessError:
        return False

def get_local_users_info():
    users_info_list = []
    try:
        resume_handle = 0
        while True:
            users = win32net.NetUserEnum(None, 0, resume_handle, 65535)
            for user in users[0]:
                user_info = {}
                username = user['name']
                user_info["Name"] = username
                user_info["PasswordEnabled"] = check_password_enabled(username)
                user_info["FolderAccess"] = check_folder_access(username)
                user_info["AdminRights"] = check_admin_rights(username)
                user_info["CmdAccess"] = check_cmd_access(username)
                user_info["PowershellAccess"] = check_powershell_access(username)
                users_info_list.append(user_info)
            resume_handle = users[2]
            if not resume_handle:
                break
    except Exception as e:
        print("Failed to retrieve user information:", str(e))

    return users_info_list

if __name__ == "__main__":
    users_info = get_local_users_info()
    for user_info in users_info:
        print(user_info)


