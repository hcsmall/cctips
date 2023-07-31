import requests
import random
import string
import threading
import time
from bs4 import BeautifulSoup

# 用户选择代理文本文件路径
PROXY_FILE_PATH = "proxies.txt"

# 代理池
proxy_pool = []

def load_proxies(file_path):
    """
    从文件加载代理列表
    """
    with open(file_path, "r") as f:
        return [line.strip() for line in f]

def generate_random_cookie():
    """
    生成随机Cookie
    """
    characters = string.ascii_letters + string.digits
    cookie = ''.join(random.choice(characters) for i in range(32))
    return cookie

def fetch(url, proxy, user_agent, method, cookie):
    """
    使用指定代理、User-Agent、请求方法和Cookie获取网页内容
    """
    headers = {
        "User-Agent": user_agent,
        "Cookie": cookie
    }

    try:
        response = requests.request(method, url, proxies={"http": proxy, "https": proxy}, headers=headers, timeout=10)
        response.raise_for_status()  # 检查响应是否成功，若不成功则抛出异常
        print(f"成功使用代理 {proxy} 和 {user_agent} 以 {method.upper()} 方法和 Cookie 访问 {url}")
        return response.text
    except requests.exceptions.Timeout:
        print(f"代理 {proxy} 和 {user_agent} 以 {method.upper()} 方法和 Cookie 访问 {url} 超时，请尝试其他代理。")
    except requests.exceptions.RequestException as e:
        print(f"代理 {proxy} 和 {user_agent} 以 {method.upper()} 方法和 Cookie 访问 {url} 出现错误：{str(e)}")

    return None

def crawl_with_proxy(proxy, url, user_agent, method, stay_time):
    """
    使用指定代理、User-Agent和请求方法进行爬取
    """
    cookie = generate_random_cookie()

    html = fetch(url, proxy, user_agent, method, cookie)
    if html:
        # 在这里可以进行网页内容的处理
        soup = BeautifulSoup(html, "lxml")
        # 示例：获取网页标题
        print(f"使用代理 {proxy} 和 {user_agent} 以 {method.upper()} 方法和 Cookie 访问 {url} 成功，标题：{soup.title.text}")

        # 停留指定时间，模拟用户访问行为
        time.sleep(stay_time)

def main():
    global proxy_pool
    proxy_pool = load_proxies(PROXY_FILE_PATH)
    
    # 获取用户输入的网站地址
    target_website = input("请输入您想要访问的网站地址：")
    
    # 获取用户输入的浏览器选择
    browser_choice = input("请输入您想要使用的浏览器（谷歌/火狐）：").lower()

    # 获取用户输入的请求方法
    request_method = input("请输入您想要使用的请求方法（GET/POST/OPTIONS/HEAD/PUT等常见的请求方法）：").upper()

    # 获取用户输入的停留时间
    stay_time = float(input("请输入您想要停留的时间（以秒为单位）："))

    # 获取用户输入的线程数量
    num_threads = int(input("请输入您想要使用的线程数量："))

    # 根据浏览器选择设置不同的User-Agent头
    if browser_choice == "谷歌":
        user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    elif browser_choice == "火狐":
        user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0"
    else:
        print("无效的浏览器选择。请重新运行并输入正确的浏览器名称（谷歌/火狐）。")
        return

    # 使用多线程并发访问
    threads = []
    for i in range(num_threads):
        proxy = random.choice(proxy_pool)
        thread = threading.Thread(target=crawl_with_proxy, args=(proxy, target_website, user_agent, request_method, stay_time))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

if __name__ == "__main__":
    main()
