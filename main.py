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
    page_title="AR puzzle",
    page_icon="🧊",
    layout="wide"
)

video = VideoProcessor()

# ARマーカーのランダムができるか
is_random_img = False

option = st.sidebar.selectbox(
    label = "パズルサイズ",
    options = ["2x2", "3x3"]
)

if option == "2x2":
    video.rows, video.cols = 2, 2
    dsize=(500, 500)
elif option == "3x3":
    video.rows, video.cols = 3, 3
    dsize=(500, 500)
    
with open("マーカbig.pdf", "rb") as pdf_file:
    PDFbyte = pdf_file.read()

st.sidebar.download_button(
    label="ARマーカー",
    data=PDFbyte,
    file_name="ARmarker.pdf",
    mime='application/octet-stream')


placeholder_che = st.empty()
# 
agree = st.sidebar.checkbox('ARマーカーで画像のランダム抽選', key='q')

if not agree:
    randm_img = st.sidebar.button('単発ランダム抽選')
    if randm_img:
        try:
            video.original_img = cv2.imread(random.choice(video.imgs))
            video.original_img = cv2.resize(video.original_img, dsize=(500, 500))
            # print(video.original_img)
            # 元画像, 比較画像
            video.img, video.comparison_img = video.imgCut(video.original_img, video.rows, video.cols)
            # print(video.img)
        except:
            pass
    else:
        try:
            video.original_img = cv2.imread(random.choice(video.imgs))
            video.original_img = cv2.resize(video.original_img, dsize=(500, 500))
            # 元画像, 比較画像
            video.img, video.comparison_img = video.imgCut(video.original_img, video.rows, video.cols)
        except:
            pass
else:
    st.sidebar.info('マーカーでのランダム抽選中です')

# カメラメイン処理
def video_frame_callback(frame):
    global is_random_img
    global agree
    
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
        if 10 in ids and agree:
            video.original_img = cv2.imread(random.choice(video.imgs))
            video.original_img = cv2.resize(video.original_img, dsize=(500, 500))
            video.img, video.comparison_img = video.imgCut(video.original_img, video.rows, video.cols)
            is_random_img = True
        else:
            is_random_img = False
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
            except:
                pass
            
    frame3 = video.trimming(frame2)
    com = video.comparison(video.comparison_img, frame3)
    
    if  com > 0.997:
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
if agree and ctx.state.playing:
    cou = 0
    while agree:
        # print(is_random_img)
        if is_random_img:
            cou += 1
            placeholder.image(video.cv2pil(video.original_img), caption='元画像')
        else:
            placeholder.image(video.cv2pil(video.original_img), caption='元画像')
        if not agree or cou > 500:
            print('of')
            agree = False
            break
else:
    placeholder.image(video.cv2pil(video.original_img), caption='元画像')

# tes
#Class
# class VideoProcessor:
#     def recv(self,frame):

#         img = frame.to_ndarray(format = 'bgr24')
#         img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
#         img = av.VideoFrame.from_ndarray(img, format='gray')

#         return img
# class VideoProcessor:
#     def recv(self,frame):

#         img = frame.to_ndarray(format = 'bgr24')
#         img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

#         return av.VideoFrame.from_ndarray(img, format="bgr24")

# webrtc_streamer(key='example2', video_processor_factory=VideoProcessor)
