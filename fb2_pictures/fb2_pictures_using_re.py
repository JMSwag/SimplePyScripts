#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


"""Скрипт парсит файл формата fb2, вытаскивает из него картинки и сохраняет их в папке с таким же названием,
как файл fb2.
Аналогичен fb2_pictures.py, только для парсинга используются регулярные выражения, а не разбор
через xml парсер. Причиной создания этого аналога в том, что если парсер не сможет распарсить fb2, например,
при поломанной структуре fb2, тогда скрипт не сможет вытащить картинки."""


import base64
import io
import os
import re

from PIL import Image


def sizeof_fmt(num, suffix='B'):
    for unit in ['', 'Ki', 'Mi', 'Gi', 'Ti', 'Pi', 'Ei', 'Zi']:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, 'Yi', suffix)


def do(file_name, debug=True):
    dir_im = os.path.splitext(file_name)[0]
    if not os.path.exists(dir_im):
        os.makedirs(dir_im)
    debug and print(dir_im + ':')

    total_image_size = 0

    with open(file_name, encoding='utf8') as fb2:
        pattern = re.compile('<binary ((content-type=".+?") (id=".+?")'
                             '|(id=".+?") (content-type=".+?")) *?>(.+?)</binary>', re.DOTALL)

        find_content_type = re.compile('content-type="(.+?)"')
        find_id = re.compile('id="(.+?)"')

        for i, binary in enumerate(pattern.findall(fb2.read()), 1):
            try:
                im_id, content_type, im_base64 = None, None, None

                for part in binary:
                    if not part:
                        continue

                    match_id = find_id.search(part)
                    if im_id is None and match_id is not None:
                        im_id = match_id.group(1)

                    match_content_type = find_content_type.search(part)
                    if content_type is None and match_content_type is not None:
                        content_type = match_content_type.group(1)

                    if match_id is None and match_content_type is None:
                        im_base64 = part

                short_content_type = content_type.split('/')[-1]

                if 'jpeg' in short_content_type:
                    if not im_id.endswith('jpg') and not im_id.endswith('jpeg'):
                        im_id += '.' + short_content_type

                elif not im_id.endswith(short_content_type):
                    im_id += '.' + short_content_type

                im_file_name = os.path.join(dir_im, im_id)
                im_data = base64.b64decode(im_base64.encode())
                with open(im_file_name, mode='wb') as f:
                    f.write(im_data)

                im = Image.open(io.BytesIO(im_data))
                count_bytes = len(im_data)
                total_image_size += count_bytes
                debug and print('    {}. {} {} format={} size={}'.format(i, im_id, sizeof_fmt(count_bytes),
                                                               im.format, im.size))

            except:
                import traceback
                traceback.print_exc()

        file_size = os.path.getsize(file_name)
        debug and print()
        debug and print('fb2 file size =', sizeof_fmt(file_size))
        debug and print('total image size = {} ({:.2f}%)'.format(sizeof_fmt(total_image_size),
                                                                 total_image_size / file_size * 100))


if __name__ == '__main__':
    fb2_file_name = 'Непутевый ученик в школе магии 1. Зачисление в школу (Часть 1).fb2'
    do(fb2_file_name)
