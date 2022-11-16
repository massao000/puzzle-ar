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

aruco = cv2.aruco

# https://github.com/whitphx/streamlit-webrtc#pull-values-from-the-callback
lock = threading.Lock()
result = {"percent": None, "ori_img": None}

def video_frame_callback(frame):
    global imgs
    global original_img
    global rows
    global cols
    global img
    global comparison_img

    frame = frame.to_ndarray(format = 'bgr24')
    
    # 黒色の背景の生成
    frame2 = np.zeros(frame.copy().shape, dtype=np.uint8)
    frame2.fill(0)
    # camera = cv2.VideoCapture(0)
    
    #　マーカの検出
    dictionary = aruco.Dictionary_get(aruco.DICT_5X5_50)
    # dictionary = aruco.getPredefinedDictionary(aruco.DICT_5X5_50)
    
    # corners:マーカの角 ids:マーカID
    corners, ids, rejectedImgPoints = aruco.detectMarkers(frame, dictionary)
    # print(corners * 2)
    # 検出したマーカーの検出 囲みID表示
    frame = aruco.drawDetectedMarkers(frame, corners, ids)
    
    # マーカIDが存在するか
    if np.all(ids != None):
        # 特定のマーカーが読み込まれたら画像のチェンジ
        if 10 in ids:
            original_img = cv2.imread(random.choice(imgs))
            original_img = cv2.resize(original_img, dsize=(500, 500))
            img, comparison_img = imgCut(original_img, rows, cols)
            # with lock:
            #     result["ori_img"] = original_img
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
                if ids[i] == 0 and len(img) >= 0:
                    frame, frame2 = overlapImg(img[0], pts_dst, frame, frame2)
                elif ids[i] == 1 and len(img) >= 1:
                    frame, frame2 = overlapImg(img[1], pts_dst, frame, frame2)
                elif ids[i] == 2 and len(img) >= 2:
                    frame, frame2 = overlapImg(img[2], pts_dst, frame, frame2)
                elif ids[i] == 3 and len(img) >= 3:
                    frame, frame2 = overlapImg(img[3], pts_dst, frame, frame2)
                elif ids[i] == 4 and len(img) >= 4:
                    frame, frame2 = overlapImg(img[4], pts_dst, frame, frame2)
                elif ids[i] == 5 and len(img) >= 5:
                    frame, frame2 = overlapImg(img[5], pts_dst, frame, frame2)
                elif ids[i] == 6 and len(img) >= 6:
                    frame, frame2 = overlapImg(img[6], pts_dst, frame, frame2)
                elif ids[i] == 7 and len(img) >= 7:
                    frame, frame2 = overlapImg(img[7], pts_dst, frame, frame2)
                elif ids[i] == 8 and len(img) >= 8:
                    frame, frame2 = overlapImg(img[8], pts_dst, frame, frame2)
                elif ids[i] == 9 and len(img) >= 9:
                    frame, frame2 = overlapImg(img[9], pts_dst, frame, frame2)
            except:
                pass
            
    frame3 = trimming(frame2)
    try:
        com = comparison(comparison_img, frame3)
        if  com > 0.99:
            cv2.putText(frame, f'{com}%', (0, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 10, 10), 5, cv2.LINE_AA)
        else:
            cv2.putText(frame, f'{com}%', (0, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 255, 255), 5, cv2.LINE_AA)
        # if  com > 0.97:
        #     with lock:
        #             result["percent"] = com
    except:
        pass
            # result["ori_img"] = original_img
            
        # if  com > 0.99:
        #     print('ok')
        # else:
        #     print('ng')
  
    return av.VideoFrame.from_ndarray(frame, format="bgr24")

ctx = webrtc_streamer(
    key="example", 
    video_frame_callback=video_frame_callback,
    rtc_configuration={  # Add this config
        "iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]
    },
    # media_stream_constraints={"video": True, "audio": False},
)

# マーカーに表示する画像
imgs = glob.glob('imgs/*')

# カットサイズ
rows, cols = 2, 2

max_m = 0

# Using "with" notation
with st.sidebar:
    option = st.selectbox(
        label = "パズルサイズ",
        options = ["2x2", "3x3"]
    )
    
    with open("マーカbig.pdf", "rb") as pdf_file:
        PDFbyte = pdf_file.read()

    st.download_button(
        label="ARマーカー",
        data=PDFbyte,
        file_name="ARmarker.pdf",
        mime='application/octet-stream')
    
    # # マーカーに表示する画像
    randm_img = st.button('random')
    if randm_img:
        try:
            original_img = cv2.imread(random.choice(imgs))
            original_img = cv2.resize(original_img, dsize=(500, 500))
            # 元画像, 比較画像
            img, comparison_img = imgCut(original_img, rows, cols)
        except:
            pass
    else:
        try:
            original_img = cv2.imread(random.choice(imgs))
            original_img = cv2.resize(original_img, dsize=(500, 500))
            # 元画像, 比較画像
            img, comparison_img = imgCut(original_img, rows, cols)
        except:
            pass
        
    # 正しい画像の表示
    st.image(cv2pil(original_img), caption='Sunrise by the mountains')
        
    
    # if result["ori_img"] is None:
    #     st.image(cv2pil(original_img), caption='Sunrise by the mountains')
    # else:
    #     with lock:
    #         st.image(cv2pil(result["ori_img"]), caption='Sunrise by the mountains')
        
    placeholder = st.empty()
    
    # これを使うとランダムボタン押すとストップする    
    # while ctx.state.playing:
    #     with lock:
    #         percent = result["percent"]
    #     if percent is None:
    #         continue
    #     placeholder.subheader(f'{percent}%')
    #     # print(percent)
    # #         placeholder.empty()
    # placeholder.subheader("0%")

# テスト表示
# image = Image.open('imgs/2022-10-30_024439-Trinart-characters.png')
# st.image(image, caption='Sunrise by the mountains')

# tes
#Class
# class VideoProcessor:
#     def recv(self,frame):

#         img = frame.to_ndarray(format = 'bgr24')
#         img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
#         img = av.VideoFrame.from_ndarray(img, format='gray')

#         return img

# webrtc_streamer(key='example2', video_processor_factory=VideoProcessor)
