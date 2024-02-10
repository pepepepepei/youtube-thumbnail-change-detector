import os
import uuid
from difflib import SequenceMatcher

import functions_framework
import requests
from markupsafe import escape


@functions_framework.http
def hello_http(request):
    """HTTP Cloud Function.
    Args:
        request (flask.Request): The request object.
        <https://flask.palletsprojects.com/en/1.1.x/api/#incoming-request-data>
    Returns:
        The response text, or any set of values that can be turned into a
        Response object using `make_response`
        <https://flask.palletsprojects.com/en/1.1.x/api/#flask.make_response>.
    """
    request_json = request.get_json(silent=True)
    request_args = request.args

    if request_json and "name" in request_json:
        name = request_json["name"]
    elif request_args and "name" in request_args:
        name = request_args["name"]
    else:
        name = "World"
    return f"Hello {escape(name)}!"


def detector():
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
        simirality = SequenceMatcher(
            None, prevImgBinary, newImgBinary
        ).real_quick_ratio()
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
