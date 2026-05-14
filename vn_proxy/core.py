import requests
import random
import concurrent.futures

class VietnamProxy:
    def __init__(self):
        self.api_url = "https://api.proxyscrape.com/v4/free-proxy-list/get?request=display_proxies&country=vn&proxy_format=protocolipport&format=json"
        self._proxies_data = []
        self._alive_proxies = []

    def fetch(self):
        """Làm mới danh sách proxy từ API"""
        try:
            response = requests.get(self.api_url, timeout=15)
            response.raise_for_status()
            self._proxies_data = response.json().get("proxies", [])
            # Reset danh sách alive khi fetch mới
            self._alive_proxies = [] 
            return self
        except Exception as e:
            print(f"[vn-proxy] Error fetching data: {e}")
            return self

    def _check_single_proxy(self, proxy_url, timeout):
        """Hàm nội bộ để kiểm tra 1 proxy"""
        proxies = {
            "http": proxy_url,
            "https": proxy_url,
        }
        try:
            # Kiểm tra bằng cách gọi tới một endpoint nhẹ
            response = requests.get(
                "https://www.gstatic.com/generate_204", 
                proxies=proxies, 
                timeout=timeout
            )
            if response.status_code == 204:
                return proxy_url
        except:
            return None
        return None

    def check_alive(self, protocol=None, timeout=5, max_workers=10):
        """
        Kiểm tra và lọc ra các proxy còn sống.
        - timeout: số giây tối đa chờ proxy phản hồi.
        - max_workers: số luồng kiểm tra đồng thời (càng cao càng nhanh).
        """
        candidates = self.get_all(protocol)
        alive_results = []

        print(f"[vn-proxy] Checking {len(candidates)} proxies...")

        # Sử dụng ThreadPoolExecutor để kiểm tra đa luồng (nhanh hơn rất nhiều)
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_proxy = {executor.submit(self._check_single_proxy, p, timeout): p for p in candidates}
            for future in concurrent.futures.as_completed(future_to_proxy):
                result = future.result()
                if result:
                    alive_results.append(result)

        self._alive_proxies = alive_results
        print(f"[vn-proxy] Found {len(alive_results)} alive proxies.")
        return alive_results

    def get_all(self, protocol=None, only_alive=False):
        """Lấy danh sách proxy"""
        if only_alive and self._alive_proxies:
            source = [{"proxy": p, "protocol": p.split('://')[0]} for p in self._alive_proxies]
        else:
            if not self._proxies_data:
                self.fetch()
            source = self._proxies_data
        
        if protocol:
            return [p['proxy'] for p in source if p.get('protocol') == protocol.lower()]
        return [p['proxy'] for p in source]

    def get_random(self, protocol=None, only_alive=False):
        """Lấy 1 proxy ngẫu nhiên (ưu tiên loại còn sống nếu only_alive=True)"""
        proxies = self.get_all(protocol, only_alive=only_alive)
        return random.choice(proxies) if proxies else None