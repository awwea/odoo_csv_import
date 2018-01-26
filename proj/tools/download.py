#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import tqdm
import logging
import aiohttp
import asyncio
import aiofiles
import contextlib
import pandas as pd
import async_timeout
import uvloop

from common import DELIMITER, SQL3, VAR_IMG_DIR, TRANSIT_VARIANT

def get_urls():
    with contextlib.closing(SQL3) as con:
        df = pd.read_sql_query("""SELECT * FROM variant_1_color WHERE var_1_img IS NOT ''; """, con)
        #csvData = pandas.read_csv('origin/product.csv', skipinitialspace=True, usecols=['media',])
        #urls = list(csvData.media)
        urls = list(df['var_1_img'])
        return urls

def get_file_names():
    df = pd.read_csv(TRANSIT_VARIANT, skipinitialspace=True, delimiter=DELIMITER)
    fnames = list(df['var_img_name'])
    return fnames

asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

HEADERS = {'user-agent': (
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) '
            'AppleWebKit/537.36 (KHTML, like Gecko) '
            'Chrome/45.0.2454.101 Safari/537.36'),
}

@asyncio.coroutine
async def download(session, url):
    with async_timeout.timeout(300):
        params = {}
        async with session.get(url, headers=HEADERS, params=params) as response:
            #filename = os.path.basename(url)
            filename = '_'.join([url.split('/')[-2],url.split('/')[-1]])
            logging.info(' Downloading :::> %s \n', filename)

            async with aiofiles.open(os.path.join(VAR_IMG_DIR, filename), 'wb') as down:
                while True:
                    chunk = await response.content.readany()
                    if not chunk:
                        break
                    await down.write(chunk)
            logging.info('\n Done %s\n', filename)
            return await response.release()

@asyncio.coroutine
async def main(loop):
    urls = get_urls()
    connector = aiohttp.TCPConnector(limit=1000, use_dns_cache=True, loop=loop, verify_ssl=False)
    async with aiohttp.ClientSession(connector=connector) as session:
    #async with aiohttp.ClientSession(loop=loop) as session:
        for url in urls:
            await download(session, url)

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s')

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(loop))
