import streamlit as st
from streamlit_webrtc import webrtc_streamer
import threading

import cv2
# import cv2.aruco as aruco
import numpy as np
import os
import av
import random
from PIL import Image
import glob

from package import *

st.set_page_config(
    page_title="infinity AR puzzle",
    # page_icon="🧊",
    layout="wide"
)

video = VideoProcessor()

# ARマーカーのランダムができるか
is_random_img = False

up_img = st.sidebar.file_uploader("オリジナル画像", type=['png', 'jpg'])

option = st.sidebar.selectbox(
    label = "パズルサイズ (横x縦)",
    options = ["2x2", "3x3", "4x4", "5x5", "3x2", "4x3", "5x4", "2x3", "3x4"]
)

option_rotate = st.sidebar.selectbox(
    label = "カメラの読み取り向き",
    options = ["上下左右反転", "デフォルト"]
)
# 7x7までいける
# print(imgs)
if up_img:
    imgs = pil2cv(Image.open(up_img))
    height, width, channels = imgs.shape
    
    box_size = 0
    if height < width:
        # 2:1
        dsize=(750, 500)
    elif height > width:
        # 1:2
        box_size = 1
        dsize=(375, 750)
    else:
        # 1:1
        box_size = 2
        dsize=(500, 500)
        
    if option == "2x2" and box_size == 2:
        video.rows, video.cols = 2, 2
    elif option == "3x3" and box_size == 2:
        video.rows, video.cols = 3, 3
    elif option == "4x4" and box_size == 2:
        video.rows, video.cols = 4, 4
    elif option == "5x5" and box_size == 2:
        video.rows, video.cols = 5, 5
    elif option == "3x2" and box_size == 0: # 横長 2:1
        video.rows, video.cols = 2, 3
    elif option == "4x3" and box_size == 0: # 横長 2:1
        video.rows, video.cols = 3, 4
    elif option == "5x4" and box_size == 0: # 横長 2:1
        video.rows, video.cols = 4, 5
    elif option == "2x3" and box_size == 1: # 縦長 1:2
        video.rows, video.cols = 3, 2
    elif option == "3x4" and box_size == 1: # 縦長 1:2
        video.rows, video.cols = 4, 3

    original_img = cv2.resize(imgs, dsize=dsize)
    video.img, video.comparison_img = video.imgCut(original_img, video.rows, video.cols)
else:
    if option == "2x2":
        video.rows, video.cols = 2, 2
        imgs = glob.glob(f'imgs/1-1/*')
        dsize=(500, 500)
    elif option == "3x3":
        video.rows, video.cols = 3, 3
        imgs = glob.glob(f'imgs/1-1/*')
        dsize=(500, 500)
    elif option == "4x4":
        video.rows, video.cols = 4, 4
        imgs = glob.glob(f'imgs/1-1/*')
        dsize=(500, 500)
    elif option == "5x5":
        video.rows, video.cols = 5, 5
        imgs = glob.glob(f'imgs/1-1/*')
        dsize=(500, 500)
    elif option == "3x2": # 横長 2:1
        video.rows, video.cols = 2, 3
        imgs = glob.glob(f'imgs/2-1/*')
        dsize=(750, 500)
    elif option == "4x3": # 横長 2:1
        video.rows, video.cols = 3, 4
        imgs = glob.glob(f'imgs/2-1/*')
        dsize=(750, 500)
    elif option == "5x4": # 横長 2:1
        video.rows, video.cols = 4, 5
        imgs = glob.glob(f'imgs/2-1/*')
        dsize=(750, 500)
    elif option == "2x3": # 縦長 1:2
        video.rows, video.cols = 3, 2
        imgs = glob.glob(f'imgs/1-2/*')
        dsize=(375, 750)
    elif option == "3x4": # 縦長 1:2
        video.rows, video.cols = 4, 3
        imgs = glob.glob(f'imgs/1-2/*')
        dsize=(358, 760)
    img = pil2cv(Image.open(random.choice(imgs)))
    original_img = cv2.resize((img), dsize=dsize)
    video.img, video.comparison_img = video.imgCut(original_img, video.rows, video.cols)

# 難易度
level = st.sidebar.radio(
    label = "むずかしさ",
    options = ["かんたん", "ふつう", "むずかしい"],
    horizontal=True
)
# st.sidebar.text('かんたん:入れ替え ふつう:90度 むずかしい:90度180度回転')

# st.sidebar.info('マーカー50番でのランダム抽選です')

if (level == "かんたん"):
    video.level = 0
elif (level == "ふつう"):
    video.level = 1
elif (level == "むずかしい"):
    video.level = 2
else:
    video.level = 0

placeholder_che = st.empty()
# 
# agree = st.sidebar.button('ARマーカーで画像のランダム抽選', key='q')
randm_img = st.sidebar.button('画像抽選')
if up_img:
    try:
        original_img = pil2cv(Image.open(up_img))
        original_img = cv2.resize(original_img, dsize=dsize)
        # print(original_img)
        # 元画像, 比較画像
        video.img, video.comparison_img = video.imgCut(original_img, video.rows, video.cols)
        # print(video.img)
    except:
        pass
else:
    if randm_img:
        try:
            original_img = cv2.imread(random.choice(imgs))
            original_img = cv2.resize(original_img, dsize=dsize)
            # print(original_img)
            # 元画像, 比較画像
            video.img, video.comparison_img = video.imgCut(original_img, video.rows, video.cols)
            # print(video.img)
        except:
            pass
    else:
        try:
            original_img = cv2.imread(random.choice(imgs))
            original_img = cv2.resize(original_img, dsize=dsize)
            # 元画像, 比較画像
            video.img, video.comparison_img = video.imgCut(original_img, video.rows, video.cols)
        except:
            pass

st.write(f"""
# 遊び方

※ここで使用している画像は全て、画像生成AIを使い作成したものになります。

### PC推奨

以下のものを準備
* ARマーカー(ARマーカーダウンロードをクリック)
* カメラ

`赤いstartボタン`を押すし、しばらく待ちます。

カメラの映像が出力されます。

マーカーの`marker-0`をかざすと画像の一部が表示されます。

あとは、サイドバーから、パズルサイズを変更や、むずかしさの変更、画像抽選などして遊びます。

あっているかはパーセンテージが青くなったら一致していることになります。

## サイドバーについて

### パズルサイズ 横x縦

|サイズ|必要マーカー番号|
|--|--|
|2x2|0~3|
|3x3|0~8|
|4x4|0~15|
|5x5|0~24|
|3x2|0~5|
|4x3|0~11|
|5x4|0~19|
|2x3|0~5|
|3x4|0~11|

### むずかしさ

|むずかしさ|詳細|
|--|--|
|かんたん|入れ替え|
|ふつう|入れ替え、90度回転|
|むずかしい|入れ替え、90度回転&180度回転|

### 画像抽選

ボタンを押すとランダムに画像を変更できる
""")


# dictionary = video.aruco.Dictionary_get(video.aruco.DICT_5X5_50)
# カメラメイン処理
def video_frame_callback(frame):
    global video
    global is_random_img
    global option_rotate
    # global agree
    
    frame = frame.to_ndarray(format = 'bgr24')
    
    # 黒色の背景の生成
    frame2 = np.zeros(frame.copy().shape, dtype=np.uint8)
    frame2.fill(0)
    
    # h, w = self.original_img.shape[:2]
    # frame[0:h, 0:w] = self.original_img
    
    #　マーカの検出
    dictionary = video.aruco.Dictionary_get(video.aruco.DICT_5X5_50)
    # dictionary = video.aruco.getPredefinedDictionary(video.aruco.DICT_5X5_50)
    
    # corners:マーカの角 ids:マーカID
    corners, ids, rejectedImgPoints = video.aruco.detectMarkers(frame, dictionary)
    # print(corners * 2)
    # 検出したマーカーの検出 囲みID表示
    frame = video.aruco.drawDetectedMarkers(frame, corners, ids)
    
    # マーカIDが存在するか
    if np.all(ids != None):
        # 特定のマーカーが読み込まれたら画像のチェンジ
        # if 10 in ids and agree:
        #     original_img = cv2.imread(random.choice(imgs))
        #     original_img = cv2.resize(original_img, dsize=(500, 500))
        #     video.img, video.comparison_img = video.imgCut(original_img, video.rows, video.cols)
        #     is_random_img = True
        # else:
        #     is_random_img = False
            # cv2.imshow('img', original_img)
        
        # 検出されたマーカIDの数だけ繰り返す
        for i in range(len(ids)):
            # 検出されたマーカ座標のデータ
            pts_dst = np.array([
                (corners[i][0][0][0], corners[i][0][0][1]),
                (corners[i][0][1][0], corners[i][0][1][1]),
                (corners[i][0][2][0], corners[i][0][2][1]),
                (corners[i][0][3][0], corners[i][0][3][1]),
                    ])
            
            try:
                if ids[i] == 0 and len(video.img) >= 0:
                    frame, frame2 = video.overlapImg(video.img[0], pts_dst, frame, frame2)
                elif ids[i] == 1 and len(video.img) >= 1:
                    frame, frame2 = video.overlapImg(video.img[1], pts_dst, frame, frame2)
                elif ids[i] == 2 and len(video.img) >= 2:
                    frame, frame2 = video.overlapImg(video.img[2], pts_dst, frame, frame2)
                elif ids[i] == 3 and len(video.img) >= 3:
                    frame, frame2 = video.overlapImg(video.img[3], pts_dst, frame, frame2)
                elif ids[i] == 4 and len(video.img) >= 4:
                    frame, frame2 = video.overlapImg(video.img[4], pts_dst, frame, frame2)
                elif ids[i] == 5 and len(video.img) >= 5:
                    frame, frame2 = video.overlapImg(video.img[5], pts_dst, frame, frame2)
                elif ids[i] == 6 and len(video.img) >= 6:
                    frame, frame2 = video.overlapImg(video.img[6], pts_dst, frame, frame2)
                elif ids[i] == 7 and len(video.img) >= 7:
                    frame, frame2 = video.overlapImg(video.img[7], pts_dst, frame, frame2)
                elif ids[i] == 8 and len(video.img) >= 8:
                    frame, frame2 = video.overlapImg(video.img[8], pts_dst, frame, frame2)
                elif ids[i] == 9 and len(video.img) >= 9:
                    frame, frame2 = video.overlapImg(video.img[9], pts_dst, frame, frame2)
                elif ids[i] == 10 and len(video.img) >= 10:
                    frame, frame2 = video.overlapImg(video.img[10], pts_dst, frame, frame2)
                elif ids[i] == 11 and len(video.img) >= 11:
                    frame, frame2 = video.overlapImg(video.img[11], pts_dst, frame, frame2)
                elif ids[i] == 12 and len(video.img) >= 12:
                    frame, frame2 = video.overlapImg(video.img[12], pts_dst, frame, frame2)
                elif ids[i] == 13 and len(video.img) >= 13:
                    frame, frame2 = video.overlapImg(video.img[13], pts_dst, frame, frame2)
                elif ids[i] == 14 and len(video.img) >= 14:
                    frame, frame2 = video.overlapImg(video.img[14], pts_dst, frame, frame2)
                elif ids[i] == 15 and len(video.img) >= 15:
                    frame, frame2 = video.overlapImg(video.img[15], pts_dst, frame, frame2)
                elif ids[i] == 16 and len(video.img) >= 16:
                    frame, frame2 = video.overlapImg(video.img[16], pts_dst, frame, frame2)
                elif ids[i] == 17 and len(video.img) >= 17:
                    frame, frame2 = video.overlapImg(video.img[17], pts_dst, frame, frame2)
                elif ids[i] == 18 and len(video.img) >= 18:
                    frame, frame2 = video.overlapImg(video.img[18], pts_dst, frame, frame2)
                elif ids[i] == 19 and len(video.img) >= 19:
                    frame, frame2 = video.overlapImg(video.img[19], pts_dst, frame, frame2)
                elif ids[i] == 20 and len(video.img) >= 20:
                    frame, frame2 = video.overlapImg(video.img[20], pts_dst, frame, frame2)
                elif ids[i] == 21 and len(video.img) >= 21:
                    frame, frame2 = video.overlapImg(video.img[21], pts_dst, frame, frame2)
                elif ids[i] == 22 and len(video.img) >= 22:
                    frame, frame2 = video.overlapImg(video.img[22], pts_dst, frame, frame2)
                elif ids[i] == 23 and len(video.img) >= 23:
                    frame, frame2 = video.overlapImg(video.img[23], pts_dst, frame, frame2)
                elif ids[i] == 24 and len(video.img) >= 24:
                    frame, frame2 = video.overlapImg(video.img[24], pts_dst, frame, frame2)
                elif ids[i] == 25 and len(video.img) >= 25:
                    frame, frame2 = video.overlapImg(video.img[25], pts_dst, frame, frame2)
                elif ids[i] == 26 and len(video.img) >= 26:
                    frame, frame2 = video.overlapImg(video.img[26], pts_dst, frame, frame2)
                elif ids[i] == 27 and len(video.img) >= 27:
                    frame, frame2 = video.overlapImg(video.img[27], pts_dst, frame, frame2)
                elif ids[i] == 28 and len(video.img) >= 28:
                    frame, frame2 = video.overlapImg(video.img[28], pts_dst, frame, frame2)
                elif ids[i] == 29 and len(video.img) >= 29:
                    frame, frame2 = video.overlapImg(video.img[29], pts_dst, frame, frame2)
                elif ids[i] == 30 and len(video.img) >= 30:
                    frame, frame2 = video.overlapImg(video.img[30], pts_dst, frame, frame2)
                elif ids[i] == 31 and len(video.img) >= 31:
                    frame, frame2 = video.overlapImg(video.img[31], pts_dst, frame, frame2)
                elif ids[i] == 32 and len(video.img) >= 32:
                    frame, frame2 = video.overlapImg(video.img[32], pts_dst, frame, frame2)
            except:
                pass

    frame3 = video.trimming(frame2)
    com = video.comparison(video.comparison_img, frame3, dsize)
    
    if not option_rotate == "デフォルト":
        frame = cv2.flip(frame, -1)
    
    
    if  com > 0.9980:
        # if  com > 0.9975:
        # フチ
        cv2.putText(frame, f'{com}%', (0, 50), cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 0), 8, cv2.LINE_AA)
        # 文字
        cv2.putText(frame, f'{com}%', (0, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 10, 10), 3, cv2.LINE_AA)
    else:
        # フチ
        cv2.putText(frame, f'{com}%', (0, 50), cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 0), 8, cv2.LINE_AA)
        # 文字
        cv2.putText(frame, f'{com}%', (0, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 255, 255), 3, cv2.LINE_AA)
        
    
    return av.VideoFrame.from_ndarray(frame, format="bgr24")

# https://github.com/whitphx/streamlit-webrtc#pull-values-from-the-callback
# lock = threading.Lock()
# result = {"percent": None, "ori_img": None}

ctx = webrtc_streamer(
    key="example", 
    video_frame_callback=video_frame_callback,
    # クラスでする場合はvideo_processor_factoryにするかつrecv関数をframe処理に使う
    # video_processor_factory=VideoProcessor, 
    rtc_configuration={  # Add this config
        "iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]
    },
    # video_receiver_size = 10
    # media_stream_constraints={"video": True, "audio": False},
)
    
placeholder = st.sidebar.empty()
# 正しい画像の表示
if ctx.state.playing:
    if up_img:
        placeholder.image(up_img, caption='元画像')
    else:
        placeholder.image(cv2pil(original_img), caption='元画像')
    
with open("サンプル.pdf", "rb") as pdf_file:
    PDFbyte = pdf_file.read()

st.download_button(
    label="ARマーカーダウンロード",
    data=PDFbyte,
    file_name="ARmarker.pdf",
    mime='application/octet-stream')