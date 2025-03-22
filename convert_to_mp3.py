import os
import sys
import json

sys.path.append(os.path.join(os.path.dirname(__file__), 'lib'))
from make_mp3 import MakeMp3

if __name__ == "__main__":
    name = "一問一答_all"
    with open(os.path.join(os.path.dirname(__file__),f'{name}.json'), encoding='utf-8') as f:
        obj = json.load(f)

    base_dir = os.path.join(os.path.dirname(__file__),"mp3")
    mk_mp3 = MakeMp3()

    dry_run = True
    dry_run = False

    for type_idx,type in enumerate(obj):
        print(type) # 一問一答
        for cat_idx,cat_obj in enumerate(obj[type]):
            cat_title = cat_obj["cat"]
            artist_name = " ".join([type,cat_title])
            print(f'  {cat_title}') # 憲法
            for sub_cat_idx, sub_cat_obj in enumerate(cat_obj["sub_cats"]):
                sub_cat_title = sub_cat_obj["title"]
                album_name = f'{sub_cat_idx +1:02d}_{sub_cat_title}'
                print(f'    {sub_cat_title}') # 総論
                output_dir = os.path.join(base_dir, type, f'{cat_idx+1:02d}_{cat_title}', album_name)
                mk_mp3.init(output_dir, dry_run)
                for idx,qa in enumerate(sub_cat_obj["q_and_a"]):
                    file_name = f'q_{idx+1}.mp3'
                    title = f'{cat_title}_{sub_cat_title}_{idx+1}'
                    texts1 = [
                        f'{cat_title} {sub_cat_title} 第{idx+1}問',
                        qa["question"],
                    ]
                    texts2 = [
                        qa["seigo"],
#                        qa["exp"],
#                        "以上"
                    ]
#                    texts2 = None
#                    mute_msec = 2000
                    mute_msec = 500
#                    mute_msec = 0
                    mk_mp3.mp3_tts(file_name, texts1, mute_msec, texts2, title, artist_name, album_name, 240)
                mk_mp3.finish()
