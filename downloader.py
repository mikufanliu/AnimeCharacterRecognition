# -*- coding: utf-8 -*-
from __future__ import print_function
import shutil
import imghdr
import os
import concurrent.futures
import requests
import crawler

headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Proxy-Connection": "keep-alive",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36",
    "Accept-Encoding": "gzip, deflate, sdch",
    # 'Connection': 'close',
}


def download_image(image_url, dst_dir, file_name, timeout=20):
    response = None
    file_path = os.path.join(dst_dir, file_name)
    try_times = 0
    while True:
        try:
            try_times += 1
            response = requests.get(
                image_url, headers=headers, timeout=timeout)
            with open(file_path, 'wb') as f:
                f.write(response.content)
            response.close()

            file_type = imghdr.what(file_path)
            if file_type in ["jpg", "jpeg", "png", "bmp", "webp"]:
                new_file_name = "{}.{}".format(file_name, file_type)
                new_file_path = os.path.join(dst_dir, new_file_name)
                shutil.move(file_path, new_file_path)
                print("[OK:]  {}  {}".format(new_file_name, image_url))
            else:
                print()
                os.remove(file_path)
                print("[Err:]  {}".format(image_url))
            break
        except Exception as e:
            if try_times < 3:
                continue
            if response:
                response.close()
            print("[Fail:]  {}  {}".format(image_url, e.args))
            break


def download_images(image_urls, dst_dir, keywords, file_prefix="img", concurrency=50, timeout=20):
    with concurrent.futures.ThreadPoolExecutor(max_workers=concurrency) as executor:
        future_list = list()
        count = 0
        dst_dir = os.path.join(dst_dir, keywords)
        if not os.path.exists(dst_dir):
            os.makedirs(dst_dir)
        for image_url in image_urls:
            file_name = file_prefix + "_" + "%04d" % count
            future_list.append(executor.submit(
                download_image, image_url, dst_dir, file_name, timeout))
            count += 1
        concurrent.futures.wait(future_list, timeout=180)


def main(list_file, output="./download_images", max_number=100, threads=50, timeout=20, face_only=False,
         browser="phantomjs", quiet=False, file_prefix="img"):
    with open(list_file, encoding="utf-8") as keywords_list:
        for keywords in keywords_list:
            keywords = keywords.rstrip()  # 去除换行符
            crawled_urls = crawler.crawl_image_urls(keywords, max_number=max_number, face_only=face_only,
                                                    browser=browser, quiet=quiet)

            download_images(image_urls=crawled_urls, dst_dir=output, keywords=keywords,
                            concurrency=threads, timeout=timeout, file_prefix=file_prefix)

            img_count = len(os.listdir(os.path.join(output, keywords)))
            print("Get {} img of [{}] ".format(img_count, keywords))


if __name__ == '__main__':
    main("characters_name_list.txt", max_number=10)
