import os
import sys
import time
import json
import getpass

sys.path.append(os.path.join(os.path.dirname(__file__), 'lib'))
from util import GoukakuDojo

if __name__ == "__main__":
    user = input("ユーザー名を入力してください。")
    password = getpass.getpass("パスワードを入力してください: ")

    gd = GoukakuDojo()
    gd.do_input(user, password)

    group = "一問一答"

    enable_categories = [
        "憲法",
        "行政法",
        "民法",
        "基礎法学",
        "商法",
        "一般知識"        
    ]

    result_obj = {group:[]}
    str_obj = gd.get_page_structure()
    for cat in str_obj[group]:
        if cat not in enable_categories:
            continue
        cat_obj = {"cat":cat,"sub_cats":[]}
        print(f'{group}/{cat}')
        sub_cat_objs = gd.get_sub_cat_objs(str_obj[group][cat])
        for sub_cat in sub_cat_objs:
            print(f'  {group}/{cat}/{sub_cat["title"]}')
            questions = gd.get_question_objs(sub_cat["href"])
            print(f'    {len(questions)}')
            q_and_a = []
            for q in questions[:3]:
                q_and_a.append(gd.handle_question(q))
            cat_obj["sub_cats"].append({"title":sub_cat["title"],"q_and_a":q_and_a})

        time.sleep(1)
        result_obj[group].append(cat_obj)

    with open("qand_a_dump.json", "w", encoding='utf-8') as f:
        json.dump(result_obj, f, indent=2, ensure_ascii=False)
    time.sleep(1)
    gd.exit()