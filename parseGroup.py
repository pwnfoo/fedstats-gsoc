import ConfigParser
import os.path
from fedora.client import AccountSystem, AuthError

class GroupParser:

    def __init__(self):
        self.username = None
        self.password = None
        self.config = ConfigParser.RawConfigParser()
        try:
            self.config.read('fas_credentials.cfg')
            self.username = self.config.get('fas', 'username').strip('\'')
            self.password = self.config.get('fas', 'password').strip('\'')
            self.check_config()
        except:
            print("[*] Invalid / Missing Configuration file.")
    def check_config(self):
            if self.username.strip('\'') == 'FAS_USERNAME_HERE':
                print("[*] Please enter FAS credentials in fas_credentials.cfg")
                return False
            else:
                return True

    def group_users(self, group_name):
        userlist = list()
        group_json = {}
        account = AccountSystem(username=self.username,
                            password=self.password)
        try:
            group_json = account.group_members(group_name)
        except AuthError:
            print("[*] Invalid Username / Password")
        for user_desc in group_json:
            userlist.append(user_desc.values()[0])
        return userlist

obj = GroupParser()
print obj.group_users('commops')
