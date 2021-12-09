from random import choice,choices
from bs4 import BeautifulSoup
from requests import Session



with Session() as s:


    class get_info():

        def craete():

            try:

                response = s.get("https://my.telegram.org/apps").text

                result = BeautifulSoup(response, "html.parser")


                hash = result.find("input", {"name": "hash"})

                paltform = ['android', 'ios', "web"]

                app_title = "".join(choices(list("asdfghj1234567890klzxcvbnmqwertyuiop"), k=7))

                app_shortname = "".join(choices(list("qwertyuiopzxcvbnmasdfghjlk359678"), k=10))

                app_desc = "".join(choices(["craete app", "Craete", "makeing"], k=7))

                craete = s.post("https://my.telegram.org/apps/create",data={"hash": f"{hash.attrs['value']}", "app_title": f"{app_title}","app_shortname": f"{app_shortname}", "app_url": "","app_platform": f"{choice(paltform)}", "app_desc": f"{app_desc}"})

                if craete.status_code == 200:
                    return 200
                else:
                    return 100
            except:
                return {"Error": "There is a problem !"}





        def api_id():

            try:

                response = s.get("https://my.telegram.org/apps").text

                result = BeautifulSoup(response, "html.parser")

                L = list("<strong/>")

                api_id_tag = result.select("span > strong")

                api_id_List = api_id_tag[0]

                api_id = ""

                for i in api_id_List:
                    if not (i in L): api_id += str(i)


                return api_id

            except:
                return {"Error": "There is a problem !"}




        def api_hash():

            try:

                response = s.get("https://my.telegram.org/apps").text

                result = BeautifulSoup(response, "html.parser")

                api_hash_tag = result.findAll("span", {"class": "form-control input-xlarge uneditable-input"})

                api_hash_list = api_hash_tag[1]

                L = list('<span class="form-control input-xlarge uneditable-input" onclick="this.select();"></span>,')

                api_hash = ""

                for i in api_hash_list:
                    if not (i in L): api_hash += str(i)

                return api_hash

            except:
                return {"Error": "There is a problem !"}



    def sendpassword(phone):
        try:
            send_password = s.post("https://my.telegram.org/auth/send_password", data={"phone": f"{phone}"}).json()
            return send_password['random_hash']
        except:
            return {"Error": "There is a problem !"}





    def main(hash,phone,password):

        try:

            login = s.post(f"https://my.telegram.org/auth/login",data={"phone": f"{phone}","random_hash": f"{hash}","password": f"{password}"})

        except:
            return {"Error": "There is a problem !"}


        response = s.get("https://my.telegram.org/apps").text



        if "Save changes" in response:
            api_id = get_info.api_id()
            api_hash = get_info.api_hash()
            return {"api_id": api_id,"api_hash": api_hash}

        else:
            status = get_info.craete()
            if status == 200:
                api_id = get_info.api_id()
                api_hash = get_info.api_hash()

                return {"api_id": api_id,"api_hash": api_hash}
            return {"api_id": "Error","api_hash": "Error"}