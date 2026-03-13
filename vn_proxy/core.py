import requests
import random

class VietnamProxy:
    def __init__(self):
        self.api_url = "https://api.proxyscrape.com/v4/free-proxy-list/get?request=display_proxies&country=vn&proxy_format=protocolipport&format=json"
        self._proxies_data = []

    def fetch(self):
        """Làm mới danh sách proxy từ API"""
        try:
            response = requests.get(self.api_url, timeout=15)
            response.raise_for_status()
            self._proxies_data = response.json().get("proxies", [])
            return self
        except Exception as e:
            print(f"[vn-proxy] Error fetching data: {e}")
            return self

    def get_all(self, protocol=None):
        """Lấy danh sách proxy, có thể lọc theo protocol (http, socks4, socks5)"""
        if not self._proxies_data:
            self.fetch()
        
        if protocol:
            return [p['proxy'] for p in self._proxies_data if p.get('protocol') == protocol.lower()]
        return [p['proxy'] for p in self._proxies_data]

    def get_random(self, protocol=None):
        """Lấy 1 proxy ngẫu nhiên"""
        proxies = self.get_all(protocol)
        return random.choice(proxies) if proxies else None