# -*-coding:utf-8-*-
from urllib.parse import quote
import requests
import json
from concurrent import futures
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities

'''得到百度图片的真实下载地址'''

# phantomjs 设置
dcap = dict(DesiredCapabilities.PHANTOMJS)
dcap["phantomjs.page.settings.userAgent"] = (
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.100"
)


def my_print(msg, quiet=False):
    if not quiet:
        print(msg)


# def gen_query_url(keywords, face_only=False):
#     base_url = "https://image.baidu.com/search/index?tn=baiduimage"
#     keywords_str = "&word" + quote(keywords)
#     query_url = base_url + keywords_str
#     if face_only is True:
#         query_url += "&face=1"
#
#     return query_url


def get_image_url(keywords, max_number=10000, face_only=False):
    def decode_url(url):
        in_table = '0123456789abcdefghijklmnopqrstuvw'
        out_table = '7dgjmoru140852vsnkheb963wtqplifca'
        translate_table = str.maketrans(in_table, out_table)
        mapping = {'_z2C$q': ':', '_z&e3B': '.', 'AzdH3F': '/'}
        for k, v in mapping.items():
            url = url.replace(k, v)
        return url.translate(translate_table)

    base_url = "https://image.baidu.com/search/acjson?tn=resultjson_com&ipn=rj&ct=201326592"\
               "&lm=7&fp=result&ie=utf-8&oe=utf-8&st=-1"
    keywords_str = "&word={}&queryWord={}".format(
        quote(keywords), quote(keywords))
    query_url = base_url + keywords_str
    query_url += "&face={}".format(1 if face_only else 0)

    init_url = query_url + "&pn=0&rn=30"

    res = requests.get(init_url)
    init_json = json.loads(res.text.replace(r"\'", ""), encoding='utf-8', strict=False)
    total_num = init_json['listNum']

    target_num = min(max_number, total_num)
    crawl_num = min(target_num * 2, total_num)

    crawled_urls = list()
    batch_size = 30

    with futures.ThreadPoolExecutor(max_workers=5) as executor:
        future_list = list()

        def process_batch(batch_no, batch_size):
            image_urls = list()
            url = query_url + \
                  "&pn={}&rn={}".format(batch_no * batch_size, batch_size)
            try_time = 0
            while True:
                try:
                    response = requests.get(url)
                    break
                except Exception as e:
                    try_time += 1
                    if try_time > 3:
                        print(e)
                        return image_urls
            response.encoding = 'utf-8'
            res_json = json.loads(response.text.replace(r"\'", ""), encoding='utf-8', strict=False)
            for data in res_json['data']:
                if 'objURL' in data.keys():
                    image_urls.append(decode_url(data['objURL']))
                elif 'replaceUrl' in data.keys() and len(data['replaceUrl']) == 2:
                    image_urls.append(data['replaceUrl'][1]['ObjURL'])

            return image_urls

        for i in range(0, int((crawl_num + batch_size - 1) / batch_size)):
            future_list.append(executor.submit(process_batch, i, batch_size))
        for future in futures.as_completed(future_list):
            if future.exception() is None:
                crawled_urls += future.result()
            else:
                print(future.exception())

    return crawled_urls[:min(len(crawled_urls), target_num)]


def crawl_image_urls(keywords, max_number=10000, face_only=False, browser="phantomjs", quiet=False):
    my_print("\nScraping From Baidu Image Search ...\n", quiet)
    my_print("Keywords:  " + keywords, quiet)
    if max_number <= 0:
        my_print("Number:  No limit", quiet)
        max_number = 10000
    else:
        my_print("Number:  {}".format(max_number), quiet)
    my_print("Face Only:  {}".format(str(face_only)), quiet)
    my_print("Browser:  {}".format(browser), quiet)
    # query_url = gen_query_url(keywords, face_only)
    # my_print("Query URL:  " + query_url, quiet)

    if browser == "chrome":
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')  # 设置chrome无界面模式
        driver = webdriver.Chrome(executable_path="./bin/chromedriver", chrome_options=chrome_options)
    else:
        phantomjs_args = ["--webdriver-loglevel=none"]
        driver = webdriver.PhantomJS(executable_path="./bin/phantomjs",
                                     service_args=phantomjs_args, desired_capabilities=dcap)
    image_urls = get_image_url(keywords, max_number=max_number, face_only=face_only)
    driver.close()

    if max_number > len(image_urls):
        output_num = len(image_urls)
    else:
        output_num = max_number

    my_print("\n== {0} out of {1} crawled images urls will be used.\n".format(
        output_num, len(image_urls)), quiet)

    return image_urls[0:output_num]




