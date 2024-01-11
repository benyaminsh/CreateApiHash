from random import choice, choices
from bs4 import BeautifulSoup
from requests import Session


class TelegramApi:

    def __init__(self, phone):
        self.phone = phone
        self.__session = Session()

    def __create_new(self):

        try:

            response = self.__session.get("https://my.telegram.org/apps").text

            result = BeautifulSoup(response, "html.parser")

            hash = result.find("input", {"name": "hash"})

            paltform = ['android', 'ios', "web"]

            app_title = "".join(choices(list("asdfghj1234567890klzxcvbnmqwertyuiop"), k=7))

            app_shortname = "".join(choices(list("qwertyuiopzxcvbnmasdfghjlk359678"), k=10))

            app_desc = "".join(choices(["craete app", "Craete", "makeing"], k=7))

            create_api = self.__session.post(
                "https://my.telegram.org/apps/create",
                data={"hash": f"{hash.attrs['value']}", "app_title": f"{app_title}",
                      "app_shortname": f"{app_shortname}", "app_url": "",
                      "app_platform": f"{choice(paltform)}", "app_desc": f"{app_desc}"}
            )

            if create_api.status_code == 200:
                return 200
            else:
                return 100
        except:
            return None

    def __get_api_id(self):

        try:

            response = self.__session.get("https://my.telegram.org/apps").text

            result = BeautifulSoup(response, "html.parser")

            L = list("<strong/>")

            api_id_tag = result.select("span > strong")

            api_id_List = api_id_tag[0]

            api_id = ""

            for i in api_id_List:
                if not (i in L): api_id += str(i)

            return api_id

        except:
            return None

    def __get_api_hash(self):

        try:

            response = self.__session.get("https://my.telegram.org/apps").text

            result = BeautifulSoup(response, "html.parser")

            api_hash_tag = result.findAll("span", {"class": "form-control input-xlarge uneditable-input"})

            api_hash_list = api_hash_tag[1]

            L = list('<span class="form-control input-xlarge uneditable-input" onclick="this.select();"></span>,')

            api_hash = ""

            for i in api_hash_list:
                if not (i in L): api_hash += str(i)

            return api_hash

        except:
            return None

    def send_password(self):
        try:
            send_password = self.__session.post("https://my.telegram.org/auth/send_password",
                                                data={"phone": self.phone}).json()
            return send_password['random_hash']
        except:
            return None

    def create_or_get(self, random_hash, password: str):
        try:

            login_api = self.__session.post(
                f"https://my.telegram.org/auth/login",
                data={"phone": self.phone, "random_hash": f"{random_hash}", "password": f"{password}"}
            )

            response = self.__session.get("https://my.telegram.org/apps").text

            if "Save changes" in response:
                api_id = self.__get_api_id()
                api_hash = self.__get_api_hash()
                return {"phone": self.phone, "api_id": api_id, "api_hash": api_hash}

            else:
                status = self.__create_new()
                if status == 200:
                    api_id = self.__get_api_id()
                    api_hash = self.__get_api_hash()

                    return {"phone": self.phone, "api_id": api_id, "api_hash": api_hash}

                return {"phone": self.phone, "api_id": "Error", "api_hash": "Error"}

        except:
            return None


api = TelegramApi(phone="+18399813748")

random_hash = api.send_password()  # By calling this function, the password will be sent to the user's account

if random_hash:
    password = input('Enter Password :')
    print(api.create_or_get(password=password, random_hash=random_hash))

else:
    print("The desired account was restricted by Telegram")
