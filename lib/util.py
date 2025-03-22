import time
import json
import getpass
import random
from urllib.parse import urlparse, parse_qs
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

class GoukakuDojo():
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.driver.get('https://www.pro.goukakudojyo.com/')
        login_ele = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.LINK_TEXT, "ログイン"))
        )
        login_ele.click()

    def do_input(self, user, password):
        user_ele = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "input[type=text]"))
        )
        user_ele.send_keys(user)
        pass_ele = self.driver.find_element(By.CSS_SELECTOR, "input[type=password]")
        pass_ele.send_keys(password)
        submit_ele = self.driver.find_element(By.CSS_SELECTOR, "input[type=submit]")
        submit_ele.click()

    def exit(self):
        self.driver.quit()        

    def get_page_structure(self):
        return {
            "練習問題":{
                "憲法":"https://www.pro.goukakudojyo.com/worksheet/w_category.php?groupID=1",
                "行政法":"https://www.pro.goukakudojyo.com/worksheet/w_category.php?groupID=2",
                "基礎法学":"https://www.pro.goukakudojyo.com/worksheet/w_category.php?groupID=3",
                "民法":"https://www.pro.goukakudojyo.com/worksheet/w_category.php?groupID=4",
                "商法":"https://www.pro.goukakudojyo.com/worksheet/w_category.php?groupID=5",
                "基礎知識":"https://www.pro.goukakudojyo.com/worksheet/w_category.php?groupID=6",
                "多肢選択式":"https://www.pro.goukakudojyo.com/worksheet/w_category.php?groupID=7",
                "記述式":"https://www.pro.goukakudojyo.com/worksheet/w_category.php?groupID=8",
            },
            "過去問":{
                "年度別過去問":{
                    "令和6年":"https://www.pro.goukakudojyo.com/worksheet2/w_subcatnendo.php?nendoID=41",
                    "令和5年":"https://www.pro.goukakudojyo.com/worksheet2/w_subcatnendo.php?nendoID=40",
                    "令和4年":"https://www.pro.goukakudojyo.com/worksheet2/w_subcatnendo.php?nendoID=39",
                    "令和3年":"https://www.pro.goukakudojyo.com/worksheet2/w_subcatnendo.php?nendoID=38",
                    "令和2年":"https://www.pro.goukakudojyo.com/worksheet2/w_subcatnendo.php?nendoID=37",
                    "令和元年":"https://www.pro.goukakudojyo.com/worksheet2/w_subcatnendo.php?nendoID=36",
                    "平成30年":"https://www.pro.goukakudojyo.com/worksheet2/w_subcatnendo.php?nendoID=35",
                    "平成29年":"https://www.pro.goukakudojyo.com/worksheet2/w_subcatnendo.php?nendoID=34",
                    "平成28年":"https://www.pro.goukakudojyo.com/worksheet2/w_subcatnendo.php?nendoID=33",
                    "平成27年":"https://www.pro.goukakudojyo.com/worksheet2/w_subcatnendo.php?nendoID=32",
                },
                "法令別過去問":{
                    "基礎法学":"https://www.pro.goukakudojyo.com/worksheet2/w_category.php?groupID=3",
                    "憲法":"https://www.pro.goukakudojyo.com/worksheet2/w_category.php?groupID=1",
                    "行政法":"https://www.pro.goukakudojyo.com/worksheet2/w_category.php?groupID=2",
                    "民法":"https://www.pro.goukakudojyo.com/worksheet2/w_category.php?groupID=4",
                    "商法":"https://www.pro.goukakudojyo.com/worksheet2/w_category.php?groupID=5",
                    "基礎知識":"https://www.pro.goukakudojyo.com/worksheet2/w_category.php?groupID=6",
                    "多肢選択式":"https://www.pro.goukakudojyo.com/worksheet2/w_category.php?groupID=7",
                    "記述式":"https://www.pro.goukakudojyo.com/worksheet2/w_category.php?groupID=8",
                }
            },
            "一問一答":{
                "憲法":"https://www.pro.goukakudojyo.com/worksheetMT/w_category.php?groupID=1",
                "行政法":"https://www.pro.goukakudojyo.com/worksheetMT/w_category.php?groupID=2",
                "民法":"https://www.pro.goukakudojyo.com/worksheetMT/w_category.php?groupID=4",
                "基礎法学":"https://www.pro.goukakudojyo.com/worksheetMT/w_category.php?groupID=3",
                "商法":"https://www.pro.goukakudojyo.com/worksheetMT/w_category.php?groupID=5",
                "一般知識":"https://www.pro.goukakudojyo.com/worksheetMT/w_category.php?groupID=6",
            },
            "各種テスト":{
                "単元テスト":"https://www.pro.goukakudojyo.com/unit/w_ut_top.php",
                "統合テスト":"https://www.pro.goukakudojyo.com/exam/w_em_top.php"
            }
        }
    
    def goto(self, url):
        self.driver.get(url)

    def get_sub_cat_objs(self, url):
        # 行政法、の一階層下の一覧ページを想定
        self.driver.get(url)
        table_ele = WebDriverWait(self.driver, 30).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "table.practiceList.cate-content-list"))
        )
        rows = table_ele.find_elements(By.TAG_NAME, "tr")
        ret_objs = []
        for row in rows:
            try:
                a_ele = row.find_element(By.TAG_NAME, "a")
                td_ele = row.find_element(By.TAG_NAME, "td")
                title = a_ele.text
                href = a_ele.get_attribute("href")
                num = int(td_ele.text.replace("問",""), 10)
            except NoSuchElementException:
                continue

            ret_objs.append({
                "title":title,
                "href":href,
                "num":num
            })
        self.driver.back()
        return ret_objs

    def get_question_objs(self, url):
        # 行政法、行政法総論の各質問一覧ページを想定
        self.driver.get(url)
        table_ele = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "#main > table.practiceList.subcat"))
            
        )
        rows = table_ele.find_elements(By.TAG_NAME, "tr")
        question_ids = []
        for row in rows:
            try:
                # 各列のリンク先urlからqueIDを抽出
                a_ele = row.find_element(By.TAG_NAME, "a")
                parsed_url = urlparse(a_ele.get_attribute("href"))
                queIdInt = int(parse_qs(parsed_url.query).get('queID', [None])[0], 10)
                question_ids.append(queIdInt)
            except NoSuchElementException:
                pass
        self.driver.back()
        return question_ids


    def handle_question(self, id):
        result_obj = {}
        self.driver.get(f'https://www.pro.goukakudojyo.com/worksheetMT/w_main.php?queID={id}')
        que_ele = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "#main > div.mondai-wrap > div"))
        )
        result_obj.update({"question":que_ele.text})

        time.sleep(1)

        r_ele = self.driver.find_element(By.ID, "Radio1")
        if random.random() < 0.5:
            r_ele = self.driver.find_element(By.ID, "Radio2")
        self.driver.execute_script("arguments[0].click();", r_ele)

        ans_ele = WebDriverWait(self.driver, 60).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "#panel > div.kaisetsu-wrap > div.kekka > p > strong"))
        )
        result_obj.update({"seigo":ans_ele.text})
        
        kai_ele = WebDriverWait(self.driver, 60).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "#panel > div.kaisetsu-wrap > div.que-kai"))
        )
        result_obj.update({"exp":kai_ele.text})
        time.sleep(1)
        return result_obj

