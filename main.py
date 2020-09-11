import requests
from requests_toolbelt import sessions


class UndersideApi(object):
    session = sessions.BaseUrlSession(base_url='https://underside.tjcache.pw/api/v1/message/')
    trans_table = str.maketrans('\u200e\u200b', '01')
    encr_table = str.maketrans('01', '\u200e\u200b')

    @staticmethod
    def bin2ascii(bin: str) -> str:
        n = int(bin, 2)
        return n.to_bytes((n.bit_length() + 7) // 8, 'big').decode()

    @staticmethod
    def ascii2bin(string: str) -> str:
        return bin(int.from_bytes(string.encode(), 'big')).replace('b', '')

    def code_decryption(self, json: dict) -> str:
        return self.bin2ascii(json.get('code', '').translate(self.trans_table))

    def code_encryption(self, code: str) -> str:
        return self.ascii2bin(code).translate(self.encr_table)

    def encode(self, message: str) -> str:
        request = self.session.post('encode/', json={'message': message})
        return self.code_decryption(request.json())

    def decode(self, code: str) -> str:
        request = self.session.post('decode/', json={'code': self.code_encryption(code)})
        return request.json().get('text', '')


if __name__ == "__main__":
    api = UndersideApi()
    print(code := api.encode('Hello'))
    print(api.decode(code))