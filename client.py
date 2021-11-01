import os
import requests

from bs4 import BeautifulSoup


class Client(object):
    """docstring for Client"""
    def __init__(self, base_url="https://cc.akliz.net", username=None, password=None):
        super(Client, self).__init__()
        self.client = requests.session()
        self.logged_in = False
        self.base_url = base_url
        self._server_cache = {}
        self.username = username
        self.password = password

    def login(self, username=None, password=None, path=None):
        if not path:
            path = self.base_url
        if not username:
            if self.username:
                username = self.username
            else:
                raise Error

        if not password:
            if self.password:
                password = self.password
            else:
                raise Error


        result = self.client.get(path)
        if not result.ok:
            return False

        soup = BeautifulSoup(result.text, "html.parser")
        form = soup.find("form")
        form_url = form["action"]

        if form_url.startswith("/"):
            form_url = self.base_url + form_url

        creds = {"username": username, "password": password}
        result = self.client.post(form_url, data=creds, headers=dict(Referer=result.url))
        if result.ok:
            self.logged_in = True
            return True
        return False

    def get_servers(self):
        path = f"{self.base_url}/api/servers"
        result = self.client.get(path)
        if result.ok:
            self._server_cache = result.json()
            return self._server_cache

    def extract_server_data(self, server):
        data = [item for item in self._server_cache if item["id"] == server]
        return data[0]

    def get_console_output(self, server, type="RAW", timestamp=0):
        server_data = self.extract_server_data(server)
        path = f"{self.base_url}/api/servers/{server}/processes/{server_data['primaryProcessDir']}/output"
        result = self.client.get(path, params=dict(type=type, timestamp=timestamp))
        return result.json()

    def put_console_input(self, server, input=""):
        server_data = self.extract_server_data(server)
        path = f"{self.base_url}/api/servers/{server}/processes/{server_data['primaryProcessDir']}/input"
        result = self.client.post(path, data=dict(input=input))
        return result.ok

    def stop_server(self, server):
        path = f"{self.base_url}/api/servers/{server}"

        data = {"powerCommand":"STOP"}
        result = self.client.patch(path, json=data)
        return result.ok

    def force_stop_server(self, server):
        path = f"{self.base_url}/api/servers/{server}"
        data = {"powerCommand":"FORCE_STOP"}

        result = self.client.patch(path, json=data)
        return result.ok

    def start_server(self, server):
        path = f"{self.base_url}/api/server-starter/servers/{server}"
        data = {"powerCommand":"START"}

        result = self.client.patch(path, json=data)
        return result.ok

if __name__ == "__main__":
    username = os.environ.get("USERNAME")
    password = os.environ.get("PASSWORD")
    if username and password:
        client = Client(username=username, password=password)
