# 🇻🇳 Vietnam Proxy Library

Thư viện Python nhẹ nhàng giúp lấy danh sách Proxy miễn phí tại Việt Nam từ nguồn **ProxyScrape API v4**. Hỗ trợ lọc theo giao thức (HTTP, SOCKS4) và lấy proxy ngẫu nhiên phục vụ cho các tác vụ Web Automation, Crawling hoặc nghiên cứu AI.

## 🚀 Tính năng chính

* **Tự động cập nhật:** Lấy dữ liệu mới nhất từ API mỗi khi `fetch()`.
* **Bộ lọc thông minh:** Dễ dàng lọc danh sách proxy theo `http` hoặc `socks4`.
* **Lấy ngẫu nhiên:** Hàm hỗ trợ lấy 1 proxy ngẫu nhiên để xoay vòng (rotate) tránh bị chặn IP.
* **Dữ liệu chi tiết:** Truy xuất được thông tin vùng (Hanoi, Ho Chi Minh City), ISP (Viettel, VNPT, FPT) của từng proxy.

## 🛠 Cài đặt

Di chuyển vào thư mục chứa thư viện và cài đặt bằng `pip`:

```bash
pip install .

```

*Lưu ý: Nếu bạn đang trong quá trình chỉnh sửa code và muốn thay đổi có hiệu lực ngay, hãy dùng lệnh:* `pip install -e .`

## 📖 Hướng dẫn sử dụng

### 1. Cách dùng cơ bản

```python
from vn_proxy import VietnamProxy

# Khởi tạo và tải danh sách proxy mới nhất
proxy_tool = VietnamProxy().fetch()

# Lấy 1 proxy ngẫu nhiên bất kỳ
print(f"Random Proxy: {proxy_tool.get_random()}")

# Lấy 1 proxy SOCKS4 ngẫu nhiên
socks_proxy = proxy_tool.get_random(protocol='socks4')
print(f"Random SOCKS4: {socks_proxy}")

```

### 2. Lấy danh sách Proxy theo loại

```python
# Lấy tất cả proxy HTTP hiện có
http_list = proxy_tool.get_all(protocol='http')
print(f"Tìm thấy {len(http_list)} proxy HTTP tại VN")

for proxy in http_list[:5]: # In thử 5 cái đầu tiên
    print(f" -> {proxy}")

```

### 3. Tích hợp với Selenium (Ví dụ nhanh)

```python
from selenium import webdriver
from vn_proxy import VietnamProxy

proxy = VietnamProxy().fetch().get_random(protocol='http')

options = webdriver.ChromeOptions()
options.add_argument(f'--proxy-server={proxy}')

driver = webdriver.Chrome(options=options)
driver.get("https://icanhazip.com") # Kiểm tra IP hiện tại

```

### 4. Kiểm tra Proxy còn sống (Check Alive)
Do proxy miễn phí hay bị die, bạn nên dùng hàm `check_alive` để lọc:

```python
proxy_tool = VietnamProxy().fetch()

# Kiểm tra đa luồng các proxy còn sống, phản hồi dưới 3 giây
proxy_tool.check_alive(timeout=3, max_workers=15)

# Chỉ lấy những proxy đã qua kiểm tra
safe_proxy = proxy_tool.get_random(only_alive=True)

```

## 📊 Cấu trúc dữ liệu chi tiết
Nếu bạn muốn lấy thông tin sâu hơn (như ISP, Thành phố), bạn có thể truy cập trực tiếp vào thuộc tính ẩn:

```python
all_data = proxy_tool._proxies_data
for item in all_data:
    print(f"IP: {item['ip']} - ISP: {item['ip_data']['isp']} - City: {item['ip_data']['city']}")

```

## ⚠️ Lưu ý

* **Độ ổn định:** Vì đây là danh sách proxy miễn phí (Free Public Proxies), tốc độ và độ sống (uptime) có thể không ổn định 100%.
* **Rate Limit:** Không nên gọi hàm `.fetch()` quá liên tục trong vòng vài giây để tránh bị API của ProxyScrape tạm khóa.