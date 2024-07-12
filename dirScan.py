import requests
from fake_useragent import UserAgent
from datetime import datetime
from re import fullmatch
import threading
import queue
import time
import sys
import os


class DirScan:
    times = 0   # 可用数据数量

    def __init__(self, url, dict_file='php.txt', num=10):
        self.url = url  # 网址
        self.dict_file = dict_file  # 字典文件
        self.num = num  # 线程数量

    def handle_url(self):   # 验证url
        if fullmatch(r'^http[s]?://.*$', self.url):   # 判断url是否带有协议，匹配以http开头、s零或一次、://
            if self.url[-1] is '/':     # 判断url最后一位
                pass
            else:
                self.url = f"{self.url}/"
        else:
            if self.url[-1] is '/':
                self.url = f"http://{self.url}"
            else:
                self.url = f"http://{self.url}/"

    @staticmethod
    def http_request(real_url, file_name, lock, max_size, path):  # 发起请求，并存入数据
        while not real_url.empty():     # 队列不为空
            with lock:
                temp = real_url.get()   # 从队列获取url
                now = max_size - real_url.qsize()   # 获取当前处理进度
            headers = {
                'User-Agent': UserAgent().random
            }
            try:
                response = requests.get(url=temp, headers=headers)
            except requests.exceptions.RequestException as e:
                print(f"{e}\n")
                with lock:
                    DirScan.delete_file(path)
                sys.exit()
            except Exception as e:
                print(f"{e}\n")
                with lock:
                    DirScan.delete_file(path)
                sys.exit()
            code = [200, 300, 301, 302, 303, 304, 305, 307, 403]    # 允许的响应状态码
            temp_code = response.status_code
            with lock:
                if temp_code in code:
                    print(f'{now} / {max_size}  True {temp_code} {temp}')
                    DirScan.save_file(file_name, f"{temp_code} {temp}\n")
                    DirScan.times += 1
                else:
                    print(f'{now} / {max_size}            False {temp_code} {temp}')
            real_url.task_done()
            time.sleep(1)   # 必要方法，以此启动多线程

    def read_file(self):    # 读取字典
        with open(f"{self.dict_file}", "r", encoding="utf-8") as f:
            dict_list = f.read().splitlines()   # 去除\n换行方法
        for i in range(len(dict_list)):
            if dict_list[i][0] is '/':
                dict_list[i] = dict_list[i].replace('/', '', 1)     # 去除一行数据开头的/
        # 返回一个列表
        return dict_list

    def threads(self):  # 创建多线程
        self.handle_url()       # 处理url
        q = queue.Queue()
        dict_list = self.read_file()    # 读取字典
        for i in dict_list:
            q.put(f'{self.url}{i}')     # 存入队列
        file_name = self.creat_file()   # 创建文件
        max_size = q.qsize()    # 获取队列数量
        lock = threading.Lock()
        path = rf"{os.getcwd()}\{file_name}"  # 因为\{写在一起，需要使用原始字符串r转义
        for i in range(self.num):
            t = threading.Thread(target=self.http_request, args=(q, file_name, lock, max_size, path))
            t.start()
        q.join()    # 阻塞线程，直到队列中的所有项目被处理
        print("\n扫描结束")
        if DirScan.times:
            print(f"发现{DirScan.times}条可用数据，已存入{path}")
        else:
            DirScan.delete_file(path)
            print(f"发现{DirScan.times}条可用数据!")

    def creat_file(self):   # 创建文件
        file_name = self.url.split("/")[2]
        # 获取当前日期和时间
        current_datetime = datetime.now()
        # 格式化成字符串显示年月日时分秒
        current_datetime_str = current_datetime.strftime('%Y%m%d-%H%M%S')
        file_name = f"{file_name}_{current_datetime_str}.txt"
        if not os.path.exists(file_name):   # 不存在文件，就创建
            with open(file_name, 'a', encoding="utf-8"):
                pass
            return file_name
        else:
            return file_name

    @staticmethod
    def delete_file(path):   # 删除文件
        if os.path.exists(path):
            os.remove(path)

    @staticmethod
    def save_file(file_name, rs):   # 保存数据
        with open(file_name, "a", newline="", encoding="utf-8") as f:
            f.write(rs)


if __name__ == '__main__':
    length = len(sys.argv)
    if length == 2:
        DirScan(url=sys.argv[1]).threads()
    elif length == 3:
        if fullmatch(r'[1-9]|[1-9]*\d+', sys.argv[2]):      # 匹配1-9或1-9零或多次、0-9一次或多次
            DirScan(url=sys.argv[1], num=int(sys.argv[2])).threads()
        elif fullmatch(r'^.+\.txt$', sys.argv[2]):     # 匹配.txt结尾
            DirScan(url=sys.argv[1], dict_file=sys.argv[2]).threads()
        else:
            print(f"参数错误：{sys.argv[2]}")
            sys.exit()
    elif length == 4:
        DirScan(url=sys.argv[1], dict_file=sys.argv[2], num=int(sys.argv[3])).threads()
    else:
        print("参数错误")
        sys.exit()
