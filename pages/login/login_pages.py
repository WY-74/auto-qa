from base.web import WebKeys
import time


class DictWrapper:
    def __init__(self, data):
        self.data = data

    def __getattr__(self, key):
        if key in self.data:
            return self.data[key]
        else:
            raise AttributeError(f"'DictWrapper' object has no attribute '{key}'")



class LoginPages(WebKeys):
    def run(self, user: str, password: str, locators: dict):

        self.navigate("https://music-platform-beer.wanos.vip/music_backend/#/login")
        self.update_text(locators["user_update_text"], user)
        self.update_text(locators["password_update_text"], password)
        self.click(locators['submit_button'])
        time.sleep(5)
