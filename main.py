import os
import uuid
from difflib import SequenceMatcher

import requests

# 最新の画像を読み込む
IMG_URL = "https://img.youtube.com/vi/0MI5RFT38Ts/maxresdefault.jpg"
res = requests.get(IMG_URL)
newImgBinary = res.content

# 過去の画像を読み込む
PATH = "prev_img"
prevImgs = os.scandir(PATH)
for prevImg in prevImgs:
    prevImgPath = os.path.join(PATH, prevImg.name)
    with open(prevImgPath, "rb") as f:
        prevImgBinary = f.read()

    # 類似度を算出
    simirality = SequenceMatcher(None, prevImgBinary, newImgBinary).real_quick_ratio()
    if simirality == 1:
        # 同じ画像が存在したとき
        print("変化なし")
        break
else:
    # 1枚も同じ画像が存在しないとき
    print("スケジュールが更新された！！")

    # 新しい画像を保存
    newImgPath = os.path.join(PATH, str(uuid.uuid4())) + ".jpg"
    print(newImgPath)
    with open(newImgPath, "wb") as f:
        f.write(newImgBinary)

    # Xにポスト
