import threading
from os import path as Path
from time import time
from typing import List

from Crypt import *

convert_chars = dict(a=1, b=2, c=3, d=4, e=5, f=6, g=7, h=8, i=9, j=10, k=11, l=12, m=13, n=14, o=15, p=16, q=17, r=18,
                     s=19, t=20, u=21, v=22, w=23, x=24, y=25, z=26, A=27, B=28, C=29, D=30, E=31, F=32, G=33, H=34,
                     I=35, J=36, K=37, L=38, M=39, N=40, O=41, P=42, Q=43, R=44, S=45, T=46, U=47, V=48, W=49, X=50,
                     Y=51, Z=52, ç=53, Ç=54)
symbols = {'#': "digits", '&': "char", '$': "origin", '%': 'convert_to_ASCII_chars'}
convert_to_chars = {v: k for k, v in convert_chars.items()}
digits = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
password = "545856525Emb"
alphabet = "ABCDEFGHIJKLMNOPQRSTUWXZ"
alphabet += alphabet.lower()


class Password:
    def __init__(self, username: str):
        self._root = ""
        self._root_raw = ""
        self._key = 0
        self._path = ""
        self.profile = username
        self.get_path()
        if self.profile is not None:
            self.origin_pw = ""
            self.len = 0
            self.passwords = dict()
            self.cases = 0
            self.numbers = 0
            self._memory1 = list()
            self._memory0 = list()
            self._foo = 0
            self._data = list()
            ### GETTING SETTLED ###
            t1 = threading.Thread(target=self.get_ready)
            t1.start()
            t1.join()

    def reset_password(self, website: str):
        """
        reset the password of site from the database
        :param website: password's website
        :return: erase it
        """
        foo = -1
        with open(self._path, 'r') as testR:
            data = testR.readlines()
            for i in range(len(data)):
                if website.lower() in data[i]:
                    foo = i
        if foo + 1:
            with open(self._path, 'w') as testW:
                data.remove(data[foo])
                for i in range(len(data)):
                    if data[i] == data[-1]:
                        testW.write(data[i].replace('\n', ''))
                    else:
                        testW.write(data[i])
                self.passwords.pop(website.lower().capitalize())

    def get_passwords(self):
        with open(self._path, 'r') as file:
            data = file.readlines()
            for inf in data:
                if ':' in inf:
                    for i in range(len(inf)):
                        if inf[i] == ':':
                            website = inf[:i]
                            self.passwords[website.capitalize()] = self.get_password(website)
                            break

    def get_ready(self):
        """
        settling the class for a returning user or a new one
        :return: assign vital variables for the class
        """
        if Path.isfile(self._path):
            self.get_key()
            t2 = threading.Thread(target=self.get_passwords)
            t2.start()
            self.origin_pw = self.get_origin_password
            t2.join()
        else:
            self.origin_pw = f'{self.profile}{rrg(1000, 9999)}'  # TODO: MAKE IT GUI INTERACTIVE
            self.len = len(self.origin_pw)
            self.get_key()
            self.create_origin()

    def get_path(self):
        """
        Get path for the data_base
        :return: assign the path to (self._path)
        """
        from os import getcwd, mkdir
        cwd = getcwd()  # getting popper path to the data_base
        cwd = cwd.split("\\")
        path = ""
        for i in range(3):
            if i == 1:
                path = Path.join(path, f'\\{cwd[i]}')
            else:
                path = Path.join(path, cwd[i])
        path = Path.join(path, "Temp")
        if not Path.isdir(path):  # if data_base folder doesn't exist
            mkdir(path)  # create one
        if self.profile is not None:
            path = Path.join(path, f"{self.profile}.txt")
        self._path = path

    # noinspection PyTypeChecker
    def translate(self, string: str, website='facebook', mode=1) -> str:
        """
        intermediary function to decrypt values correctly.\n
        :param string: string to be decrypted
        :param website: password's website, default value is used for root and origin.
        :param mode: modes : 1 == 'root' and 2 == 'passwords'
        :return: a string decrypted in format f'{value_decrypted}.{value_decrypted}{symbol}'* length_of_string
        """
        string = string.replace('\n', '')
        if mode == 1:
            string = string.split('$')
            for i in range(len(string)):
                string[i] = string[i].split('.')
            for i in range(len(string)):
                for j in range(len(string[i])):
                    string[i][j] = decrypt(string[i][j], self.len, self._key)
            y = ''
            for i in range(len(string)):
                for j in range(len(string[i])):
                    if j == 0 and len(string[i][j]) > 0:
                        y += str(string[i][j]) + '.'
                    elif j == 1 and len(string[i][j]) > 0:
                        y += str(string[i][j]) + '$'
            return y
        elif mode == 2:
            last_char = 0
            for i in range(len(string)):
                if string[i] == '#':
                    last_char = i
            numeric_changes = string[:last_char].split('#')
            chars_changes = string[slice(last_char + 1, len(string))].split('&')
            for i in range(len(numeric_changes)):
                numeric_changes[i] = numeric_changes[i].split('.')  # type: str
            for i in range(len(chars_changes)):
                chars_changes[i] = chars_changes[i].split('.')   # type: str
            str_numeric_changes = ''
            for i in range(len(numeric_changes)):
                for j in range(len(numeric_changes[i])):
                    if j == 0:
                        str_numeric_changes += str(
                            decrypt(numeric_changes[i][j], self.len, self._key, website=website)) + '.'
                    else:
                        str_numeric_changes += str(
                            decrypt(numeric_changes[i][j], self.len, self._key, website=website)) + '#'
            for i in range(len(chars_changes)):
                for j in range(len(chars_changes[i])):
                    if j == 0:
                        str_numeric_changes += str(
                            decrypt(chars_changes[i][j], self.len, self._key, website=website)) + '.'
                    else:
                        str_numeric_changes += str(
                            decrypt(chars_changes[i][j], self.len, self._key, website=website)) + '&'
            return str_numeric_changes[:len(str_numeric_changes) - 1]

    def create_origin(self):
        """
        mathematical equation the gives you the user's password, aka origin_password, can get user's password
        with (self.get_origin_password)
        :return:
        """
        self.get_key()
        if self._root == "":
            self.decode_root()
        for char in self.origin_pw:  # get the origin password and turn it into numbers
            if char in digits:
                self._memory0.append(int(char))
            else:
                self._memory0.append(convert_chars[char] + 10)
        for i in range(len(self._memory0)):  # get every numeric value and multiply it by the key
            self._memory0[i] = self._memory0[i] * self._key
            with open(self._path, 'a') as dt:
                if i == 0:
                    dt.write('\n')
                dt.write(f'!{encrypt(str(self._memory0[i]), self.len, self._key)}#')
        print(self._memory0)
        for number in self._memory0:  # add every number into memory into one number
            self._foo += number

    def generate_password(self, website: str):
        """
        generate a password using root as base and changing it randomly and registering every step
        into the data_base, to be reversed engineered with (self.get_password).
        uses (self.reset_password) to not repeat passwords for the same website\n
        :param website: website which this password is created for
        :return: assign the new password into the dict of password("self.passwords")
        """
        self.reset_password(website)
        self._memory0 = [0 for item in range(self.len * 10)]  # makes a list of '0' * length
        barz = self.get_origin()
        for i in barz:
            self._foo += int(i)   # type: List[int]
        print(self._foo)
        website = website.lower()
        sample = self._root
        foo = list(sample)  # transform sample into a list to be modifiable
        for i in range(len(str(self._foo))):
            self._memory0[i] = rrg(self.len)  # store randoms number into memory
            if not (foo[self._memory0[i]].isdigit()):  # make sure to not over write a already placed number
                foo[self._memory0[i]] = str(self._foo)[i]  # assign a digit of _foo into a random position in foo
                with open(self._path, 'a') as f:
                    if i == 0:
                        f.write(f"\n{website}:")  # registry the website and clues of the changes to data_base
                    f.write(
                        f'{encrypt(str(self._memory0[i]), self.len, self._key, website=website)}.{encrypt(str(self._foo)[i], self.len, self._key, website=website)}#')
        sample = "".join(foo)
        self._memory0 = [0 for item in range(self.len * 10)]
        while self.cases < 5:  # At least 5 upper cased letters and 5 numbers
            self.cases = 0
            for char in sample:  # counts how many capitalized char and numbers is in sample
                if char.isupper():
                    self.cases += 1
            if self.cases < 5:  # if the problem is chars do:
                foo = list(sample)
                for i in range(abs(self.cases - 5)):
                    self._memory0[i] = [rrg(self.len), rrg(1, 55)]  # type: str # get a random position and char
                    if not (foo[self._memory0[i][0]].isupper()):
                        foo[self._memory0[i][0]] = convert_to_chars[self._memory0[i][1]]
                        with open(self._path, 'a') as f:
                            f.write(
                                f'{encrypt(str(self._memory0[i][0]), self.len, self._key, website=website)}.{encrypt(str(self._memory0[i][1]), self.len, self._key, website=website)}&')  # registry it into the data_base
                sample = "".join(foo)
        self.passwords.update(
            {website.capitalize(): sample})  # make a entry for the new password into the dict of password
        self.cases = 0
        print(f'\t PASSWORD = {self.passwords}')

    def get_key(self):
        """
        Checks if there is the data_base to access;
        if it already has one, get into it and get data (key, root, length)
        if not starts to create a data_base and create a key, root and length.\n
        :return: assign self._key, self._root and self.length properly
        """
        if self._path == "":
            self.get_path()
        if Path.isfile(self._path):  # seeing if it already has data
            with open(self._path, 'r') as key:  # TODO decrypt data
                content = key.readlines()
            self.len = int(content[0])  # read data
            self._key = int(content[1])
            self._root_raw = self.translate(content[2], mode=1)
        else:
            self.create_root()
            with open(self._path, "w") as key:  # TODO crypt data
                content = str(rrg(25000, 50000))
                key.write(f'{self.len}\n{content}\n')  # write len and key
                self._key = int(content)
                for i in range(self.len):
                    key.write(
                        f'{encrypt(str(i), self.len, self._key)}.{encrypt(str(self._memory1[i]), self.len, self._key)}$')  # get the clues of the root to make the root_raw

    def decode_root(self):
        """
        get the root_raw from the data_base and translate it.\n
        :return: assign translated root into "self._root"
        """
        _clues_root = list()
        x = 0
        for i in range(len(self._root_raw)):  # get every entry using '$' as guide
            if self._root_raw[i] == '$':
                _clues_root.append(self._root_raw[slice(x, i)].split('.'))
                x = i + 1
        decoded_root = ""
        for i in range(self.len):  # converts clues into chars to decode the root
            decoded_root += chr(int(_clues_root[i][1]))
            # don't need to care about the position, cuz root entry is linear
        self._root = decoded_root

    def get_password(self, website):
        """
        uses data in data_base to get a already stabilized password.\n
        :param website: the website which password is being found for
        :return: gets the password of the specified website
        """
        self.get_key()
        if self._root == "":
            self.decode_root()
        with open(self._path, "r") as f:
            self._data = f.readlines()  # read data_base
        for item in self._data:  # search for the website specified
            if website in item:
                changes = item[(len(item) - len(f'{website}:')) * -1:]
                changes = self.translate(changes.replace('\n', ''), website=website, mode=2)
        _clues_change = list()
        x = 0
        y = 0
        if changes:
            for i in range(len(changes)):  # divide the symbols to do the proper decoding
                if changes[i] == '#' or changes[i] == '&':
                    _clues_change.append(changes[slice(x, i)].split('.'))
                    if changes[i] == '&':
                        _clues_change[y][1] = convert_to_chars[int(_clues_change[y][1])]
                    y += 1
                    x = i + 1
            decoded_password = "" + self._root  # get root to start applying the changes
            foo = list(decoded_password)
            for i in range(len(_clues_change)):
                try:
                    foo[int(_clues_change[i][0])] = _clues_change[i][1]
                except IndexError:
                    break
            decoded_password = "".join(foo)
            return decoded_password

    def create_root(self):
        """
        generate a root, a string with only special character which will be modified to create the passwords.\n
        :return: assigns the translated root to self._root
        """
        for i in range(self.len):  # limit it to the length that was configured
            x = 0
            while not (90 < x < 97 or 127 > x > 122 or 57 < x < 65 or 32 < x < 48):  # filter to only special characters
                x = rrg(33, 126)
            self._memory1.append(x)
            self._root += chr(self._memory1[i])  # store translated root
        print(self._root)

    def get_origin_password(self) -> str:
        """
        get origin_password, password which the user uses, to be used as authentication.\n
        :return: password stabilized at first entry.
        """
        ### GETTING DATA ###
        self.get_key()
        if self._root == '':
            self.decode_root()
        origin = list()
        ### REVERSIng ENGINEERING ###
        clues_origin = self.get_origin()
        for item in clues_origin:
            origin.append(int(item) / self._key)
        for i in range(len(origin)):
            if origin[i] > 9:
                origin[i] = convert_to_chars[origin[i] - 10]
            else:
                origin[i] = int(origin[i])
        for i in range(len(origin)):
            origin[i] = str(origin[i])
        return ''.join(origin)

    def get_origin(self):
        with open(self._path, 'r') as data:
            data_base = data.readlines()
            for i in range(len(data_base)):
                if data_base[i][0] == '!':
                    origins_root = data_base[i].replace('!', '')
        origins_root = decrypt(origins_root, self.len, self._key)
        clues_origin = origins_root.split('#')
        clues_origin.remove(clues_origin[-1])
        return clues_origin


class Profile:
    def __init__(self, username):
        self.username = username
        self.manager = Password(username)
        if self.username is not None:
            self.password = self.manager.origin_pw
            self.passwords = self.manager.passwords

    def search_password(self, website: str):
        print(threading.enumerate())
        website = website.lower().capitalize()
        if website in self.passwords:
            return self.passwords[website]
        else:
            return 'None'

    def __repr__(self):
        return self.username


if __name__ == '__main__':
    ### WORKING PERFECTLY SO FAR ###
    eduardo = Profile("eduardo")
    eduardo.manager.generate_password("FACEBOOK")
    print(eduardo.manager.get_origin_password())


