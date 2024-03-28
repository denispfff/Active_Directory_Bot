import subprocess
import json
from datetime import datetime
from logger import file_logger


class Users:
    def __init__(self):
        self.group_dict = {}
        self.reverse_group_dict = {}
        self.user_dict = {}
        self.last_logon_date = {}
        self.user_connection_status = {}
        self.user_connection_ID = {}
        self.get_user_data()

    def renew(self):
        self.get_users()
        self.get_users_connection_status()

    def get_user_data(self):
        self.get_users()
        self.get_users_connection_status()

    def get_users(self):
        powershell_command = r'Get-AdUser -Filter * | ConvertTo-Json'

        result = subprocess.run(['powershell', '-command', powershell_command], capture_output=True, text=True,
                                shell=True)
        all_users_json = json.loads(result.stdout)
        for OU_user_json in all_users_json:
            if "OU=" in OU_user_json.get("DistinguishedName", ""):
                dn_string = OU_user_json.get("DistinguishedName")
                user_name = OU_user_json.get('Name')
                components = [component.split("=") for component in dn_string.split(",")]
                dn_dict = {key.strip(): value.strip() for key, value in components}

                self.user_dict[user_name] = OU_user_json.get('Enabled', False)
                if user_name not in self.group_dict.setdefault(dn_dict['OU'], []):
                    self.group_dict[dn_dict['OU']].append(user_name)

        for key, values in self.group_dict.items():
            for value in values:
                self.reverse_group_dict[value] = key

    def get_last_logon_date(self, user_name):
        powershell_command = (
            f'$username = "{user_name}"; '
            f'$user = Get-ADUser -Identity $username -Properties lastLogon; '
            f'$user.lastLogon'
        )

        result = subprocess.run(['powershell', '-command', powershell_command], capture_output=True, text=True,
                                shell=True)
        last_logon_timestamp = int(result.stdout)
        if last_logon_timestamp:
            dt_object = datetime.fromtimestamp(int(last_logon_timestamp / 10 ** 7) - 11644473600)
            return dt_object.strftime("%H:%M:%S   %d-%m-%Y")
        else:
            return "никогда!"

    def get_users_connection_status(self):
        powershell_command = (
            "$Header = 'UserName', 'ID', 'State', 'Idle', 'Logon', 'Time'; "
            "(quser) "
            "-replace 'rdp-tcp#\\d{1,3}' "
            "-replace '^[\\s>]' "
            "-replace '\\s+', ',' "
            "| ConvertFrom-Csv -Header $Header "
            "| ConvertTo-Json"
        )

        result = subprocess.run(['powershell', '-command', 'chcp 65001;', powershell_command], capture_output=True,
                                text=True,
                                shell=True)

        status_user_json = json.loads(result.stdout[24:])[1:]

        for user_json in status_user_json:
            user_name = user_json.get('UserName', None)
            self.user_connection_status[user_name] = user_json.get('State', None)
            self.user_connection_ID[user_name] = user_json.get('ID', 0)

    def get_user_status(self, user_name):
        if not self.user_dict.get(user_name, False):
            return 0
        elif self.user_connection_status.get(user_name, False) == 'Active':
            return 1
        else:
            return 2

    def enable_AD_user(self, user_name):
        powershell_command = f'Enable-ADAccount -Identity "{user_name}"'
        result = subprocess.run(['powershell', '-command', powershell_command], capture_output=True, text=True,
                                shell=True)
        if result.stderr:
            file_logger.info(f"Невозможно разблокировать пользователя {user_name}.")
        else:
            self.user_dict[user_name] = True
            self.user_connection_status[user_name] = 2

    def disable_AD_user(self, user_name):
        self.user_dict[user_name] = False
        self.user_connection_status[user_name] = 0
        powershell_command = f'Disable-ADAccount -Identity "{user_name}"'
        subprocess.run(['powershell', '-command', powershell_command], capture_output=True, text=True, shell=True)

        if ID := self.user_connection_ID.get(user_name, False):
            cmd_command = f'logoff {ID}'
            subprocess.run(['powershell', '-command ', cmd_command], capture_output=True, text=True, shell=True)
            self.user_connection_ID[user_name] = 0

    def enable_AD_group(self, group_name):
        for user_name in self.group_dict[group_name]:
            self.enable_AD_user(user_name)

    def disable_AD_group(self, group_name):
        for user_name in self.group_dict[group_name]:
            self.disable_AD_user(user_name)


AD_users = Users()
