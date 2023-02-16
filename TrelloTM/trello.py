import requests
import json


class TrelloAPIManager:
    def __init__(self, username):
        self.username = username

    @staticmethod
    def base_headers():
        return {
            "Accept": "application/json"
        }

    @staticmethod
    def get_list_id_with_name(list_data, name):
        try:
            return [data.get("id") for data in list_data if data.get("name") == name][0]
        except IndexError as e:
            print(e)

    @staticmethod
    def credentials():
        return {
            'key': '8d26caef9f3a42775c72296dcf1b2742',
            'token': 'ATTAd6a5f19488128551e34f0278ae41b5d4c65f9b0d5105768b9a45ff56d974b342FCF7A181'
        }

    def get_member_id(self):
        url = f"https://api.trello.com/1/members/{self.username}"
        response = requests.request(
            "GET",
            url,
            headers=self.base_headers(),
            params=self.credentials()
        )

        if response.status_code == 200:
            return json.loads(response.text).get("id")

    def get_boards(self):
        url = f"https://api.trello.com/1/members/{self.username}/boards"
        response = requests.request(
            "GET",
            url,
            headers=self.base_headers(),
            params=self.credentials()
        )
        if response.status_code == 200:
            return json.loads(response.text)

    def get_lists_on_a_board(self, board_id):
        url = f"https://api.trello.com/1/boards/{board_id}/lists"

        response = requests.request(
            "GET",
            url,
            headers=self.base_headers(),
            params=self.credentials()
        )

        if response.status_code == 200:
            return json.loads(response.text)

    def get_cards_on_a_list(self, list_id):
        url = f"https://api.trello.com/1/lists/{list_id}/cards"

        response = requests.request(
            "GET",
            url,
            headers=self.base_headers(),
            params=self.credentials()
        )

        if response.status_code == 200:
            return json.loads(response.text)

    def get_board_id_with_name(self, name):
        try:
            return [board.get("id") for board in self.get_boards() if board.get("name") == name][0]
        except IndexError as e:
            print(e)

    def get_board_members(self, board_id):
        url = f"https://api.trello.com/1/boards/{board_id}/memberships"

        response = requests.request(
            "GET",
            url,
            headers=self.base_headers(),
            params=self.credentials()
        )

        if response.status_code == 200:
            return json.loads(response.text)
