import requests


class Proxy:
    def __init__(self, info: str):
        values = info.split(':')
        if values[0] not in ['socks5', 'socks4']:
            raise Exception("Не верный тип прокси - Тип должен быть -> socks5 или socks4")
        if not values[2].isdigit():
            raise Exception('Порт должен быть числом!')
        if len(values) == 3:
            self.public = True
            self.proxy_type = values[0]
            self.host = values[1]
            self.port = int(values[2])
        elif len(values) == 5:
            self.public = False
            self.proxy_type = values[0]
            self.host = values[1]
            self.port = int(values[2])
            self.username = values[3]
            self.password = values[4]
        else:
            raise Exception('Не вервый формат прокси!\n'
                            'Должно быть так -> proxy_type:host:port:login:password')

    def to_str(self) -> str:
        base = f'{self.host}:{self.port}'
        if self.public:
            return base
        return f'{base}:{self.username}:{self.password}'

    def is_valid(self):
        proxies = {
            'http': self.to_str(),
            'https': self.to_str()
        }

        url = 'https://www.google.com/'

        try:
            requests.get(url, proxies=proxies)
        except requests.exceptions.RequestException as e:
            raise Exception("Прокси не валидна!")

    def to_dict(self) -> dict:
        base = {'proxy_type': 'socks5',
                "addr": self.host,
                "port": self.port}

        if self.public:
            return base
        base.update({"username": self.username, "password": self.password})
        return base

    def to_tuple(self) -> tuple:
        if self.public:
            return self.proxy_type, self.host, self.port
        return self.proxy_type, self.host, self.port, True, self.username, self.password


    def __str__(self):
        return f'{self.proxy_type}:{self.host}:{self.port}'
