# -*- encoding: utf-8 -*-
# author: RenAilin
# time: 2020/10/20 22:53
import warnings

warnings.filterwarnings('ignore')
import os
import requests
import csv
from typing import List, Optional
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
from random import randint
from datetime import datetime
from traceback import format_exc

ncbi_url = 'https://www.ncbi.nlm.nih.gov/Structure/pdb/'
id_seq_path = 'id_seq.csv'


class DataHeper:
    @staticmethod
    def writer_csv_head(file_path: str, head: List, encoding='utf-8'):
        with open(file_path, 'w', encoding=encoding) as f:
            writer = csv.writer(f)
            writer.writerow(head)

    @staticmethod
    def write_csv_file(file_path: str,
                       mode='w',
                       head: Optional[List] = None,
                       data: Optional[List] = None,
                       encoding='utf-8'):
        try:
            with open(file_path, mode=mode, encoding=encoding) as f:
                writer = csv.writer(f)
                if mode == 'w':
                    if head is not None:
                        writer.writerow(head)
                    if data is not None:
                        writer.writerows(data)
                elif mode == 'a':
                    if data is not None:
                        writer.writerows(data)
                else:
                    raise ValueError('Get error mode')
                print(f"Finished write {len(data)} data to file {file_path}!")
        except Exception as e:
            print(f"When write to file {file_path} encounter error:{format_exc()}")


class Crawler:
    def __init__(self, path: str):
        self.ids = self.load_ids(path)
        # self.ids = ['1fbo', '3fiu']

    def load_ids(self, path: str):
        ids = [line.strip() for line in open(path).readlines()]
        print(f"There {len(ids)} unique ids.")
        return ids

    def get_ncbi(self):
        head = ['id', 'seq', 'full_seq']
        start = datetime.now()
        DataHeper.writer_csv_head(id_seq_path, head=head, encoding='gbk')
        for idx, id in enumerate(self.ids):
            examples = []
            try:
                url = ncbi_url + id
                print(f"Start getting id: {id} from url: {url}")

                # when on linux show pass into chrome_options
                # chrome_options = Options()
                # chrome_options.add_argument('--no-sandbox')
                # chrome_options.add_argument('--disable-dev-shm-usage')
                # chrome_options.add_argument('--headless')
                # driver = webdriver.Chrome(options=chrome_options)

                # when on mac
                driver = webdriver.Chrome()
                # put here the adress of your page
                driver.get(url)
                # put here the content you have put in Notepad, ie the XPath
                button = driver.find_element_by_id('download_sequence')
                button.click()
                time.sleep(randint(10, 15))
                # wait = WebDriverWait(driver, 10)
                # wait.until(EC.presence_of_element_located((By.CLASS_NAME, "seq gbff")))
                # print(driver.page_source.encode('utf-8'))
                soup = BeautifulSoup(driver.page_source, "lxml")
                # data = soup.select('#viewercontent1')
                # data = soup.find('div',attrs={'id':'viewercontent1'})
                data = soup.select('div > pre')
                # print(f'-->{data}')
                if len(data) > 0:  # one id has only one sequence data or more than one
                    for content in data:
                        pre_tag_str = content.string
                        lines = [l for l in pre_tag_str.split('\n') if l]
                        seq_str = ''.join(lines[1:])
                        examples.append([id, seq_str, pre_tag_str])
                        print(f"Finished getting seq of id: {id}: seq: {seq_str[:10]}")
                else:
                    examples.append([id, '', ''])
                    print(f"Id: {id} get no data from html!")
                end = datetime.now()
                print(f"Finished id:{id}, [{idx}/{len(self.ids)}] using {end - start}")
                driver.close()
                DataHeper.write_csv_file(id_seq_path, mode='a', data=examples, encoding='gbk')
            except Exception:
                print(f"When get seq of id: {id} encounter an error:{format_exc()}")
                continue
            time.sleep(1)
        print(f"Finisheh crawling!")

    def get_sequcen_data(self):
        url = 'https://www.ncbi.nlm.nih.gov/protein/158429209?report=FASTA'
        resp = requests.get(url)
        soup = BeautifulSoup(resp.text, 'html.parser')
        print(soup)
        data = soup.find('div', attrs={'id': 'viewercontent1'})
        print(data)


if __name__ == '__main__':
    ids_path = os.path.join('data/ids.txt')
    crawler = Crawler(ids_path)
    crawler.get_ncbi()
