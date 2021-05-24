chars = 'abcdefghijklmnopqrstuvwxyz0123456789'

import os
import time
from sys import argv, exit as sys_exit

import requests
from bs4 import BeautifulSoup


class Skip(Exception):
    pass


user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36 OPR/73.0.3856.400'

FOLDER_NAME = 'images'
STATIC_URL = 'https://prnt.sc/'  # 7  # https://prnt.sc/10i8n49

chars_len = len(chars) - 1

log_filename = FOLDER_NAME + '\\' + 'aaaaaa.log'
cur_dir = os.curdir + '\\' + FOLDER_NAME


def gen_img_url(start='aaaaaa'):
    CODE = '{0} {1} {2} {3} {4} {5}'

    a = chars.index(start[5]) + 1
    b = chars.index(start[4])
    c = chars.index(start[3])
    d = chars.index(start[2])
    e = chars.index(start[1])
    f = chars.index(start[0])

    temp = CODE.format(a, b, c, d, e, f)

    i0 = int(temp.split(' ')[0])
    i1 = int(temp.split(' ')[1])
    i2 = int(temp.split(' ')[2])
    i3 = int(temp.split(' ')[3])
    i4 = int(temp.split(' ')[4])
    i5 = int(temp.split(' ')[5])

    result = '{0}{1}{2}{3}{4}{5}'

    while i5 <= chars_len:
        while i4 <= chars_len:
            while i3 <= chars_len:
                while i2 <= chars_len:
                    while i1 <= chars_len:
                        while i0 <= chars_len:
                            yield result.format(chars[i5], chars[i4], chars[i3], chars[i2], chars[i1], chars[i0])
                            i0 += 1
                        i0 = 0
                        i1 += 1
                    i1 = 0
                    i2 += 1
                i2 = 0
                i3 += 1
            i3 = 0
            i4 += 1
        i4 = 0
        i5 += 1


def get_last_filename():
    files = os.listdir(cur_dir)
    files = [os.path.join(cur_dir, file) for file in files]
    return max(files, key=os.path.getctime).split('\\')[-1].split('.')[0]


def get_html(url):
    r = requests.get(url, stream=True, timeout=100, headers={'User-Agent': user_agent})
    return r.text


def get_img_url(html):
    soup = BeautifulSoup(html, 'lxml')
    url = soup.find('img', class_='no-click screenshot-image').get('src')
    if url.startswith('//st.prntscr.com'):
        print('[*] Invalid link')
        raise Skip
    else:
        return url


def save_img(url, filename):
    r = requests.get(url, stream=True)
    with open(os.path.abspath(FOLDER_NAME) + '\\' + filename + '.' + url.split('.')[-1], 'wb') as f:
        for chunk in r.iter_content(8192):
            f.write(chunk)


def main():
    start_time = time.time()
    # работа с аргументами
    if len(argv) < 2:  # вызывает ошибку если не хватает аргументов
        print(f'[X] Use "python {argv[0]} <imgs_count> <start_url [aaaaaa]>"')
        sys_exit(-1)
    else:
        rng = abs(int(argv[1]))
        total = rng

    # создание папки
    if not os.path.exists(FOLDER_NAME):
        os.mkdir(FOLDER_NAME)

    # создание лог файла
    if len(os.listdir(cur_dir)) < 1:
        with open(log_filename, 'w') as f:
            pass

    # определение старта
    if len(argv) < 3:
        start = get_last_filename()
        print(start)
    else:
        start = argv[2]
        if len(start) != 6:
            raise TypeError('[X] Length <start> must be 6')

    # генератор ссылок
    gen = gen_img_url(start)
    while rng:

        next_filename = next(gen)
        print(f'[*] {next_filename}, {rng - 1} left')
        try:
            save_img(get_img_url(get_html(STATIC_URL + next_filename)), next_filename)
            rng -= 1
        except Skip:
            continue

    delay = time.time() - start_time
    print(f"[*] Took {round(delay, 3)} sec, {round(total / delay, 3)} attempts per second.")


if __name__ == '__main__':
    main()
