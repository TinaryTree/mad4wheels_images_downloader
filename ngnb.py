import requests
from lxml import etree
import time
import threading
import queue

# hires_url = 'https://www.mad4wheels.com/img/free-car-images/hires/17502/dodge-charger-srt-hellcat-widebody-daytona-50th-anniversary-edition-2020-556190.jpg'
# desktop_url = 'https://www.mad4wheels.com/img/free-car-images/desktop/17502/dodge-charger-srt-hellcat-widebody-daytona-50th-anniversary-edition-2020-556190.jpg'
base_url = 'https://www.mad4wheels.com/dodge/charger-srt-hellcat-widebody-daytona-50th-anniversary-edition-2020'
req = requests.get(base_url)
html = etree.HTML(req.text)
img_urls = html.xpath('//div[@class="col-lg-4 mb-5"]//img[@class="horizontal"]/@src')
urls = (img_url.replace('desktop', 'hires') for img_url in img_urls)

q = queue.Queue()
for url in urls:
    q.put(url)
start = time.time()


def fetch_img_func(q):
    while True:
        try:
            url = q.get_nowait()  # 不阻塞的读取队列数据
            i = q.qsize()
        except Exception as e:
            print(e)
            break
        print('Current Thread Name Runing %s ... ' % threading.currentThread().name)
        print("当前还有%s个任务" % i)
        res = requests.get(url, stream=True)
        if res.status_code == 200:
            save_img_path = 'imgs/%s.jpg' % i
            # 保存下载的图片
            print(f'正在保存图片{i}')
            with open(save_img_path, 'wb') as fs:
                for chunk in res.iter_content(1024):
                    fs.write(chunk)
            print(f'正在保存图片{i}保存成功')


num = len(img_urls)  # 线程数
threads = []
for i in range(num):
    t = threading.Thread(target=fetch_img_func, args=(q,), name="child_thread_%s" % i)
    threads.append(t)
for t in threads:
    t.start()
for t in threads:
    t.join()

print(time.time() - start)
