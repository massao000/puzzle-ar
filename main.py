import streamlit as st
from streamlit_webrtc import webrtc_streamer
import cv2
# import cv2.aruco as aruco
import numpy as np
import os
import av
import random

from package import *

st.set_page_config(
    page_title="AR puzzle",
    page_icon="🧊",
    layout="wide"
)

aruco = cv2.aruco
# https://elsammit-beginnerblg.hatenablog.com/entry/2020/10/10/125246
# https://amdlaboratory.com/amdblog/opencv%E3%81%A8aruco%E3%83%9E%E3%83%BC%E3%82%AB%E3%83%BC%E3%82%92%E5%88%A9%E7%94%A8%E3%81%97%E3%81%9F%E7%94%BB%E5%83%8F%E3%83%9E%E3%83%83%E3%83%94%E3%83%B3%E3%82%B0/

# カメラメイン処理
def video_frame_callback(frame):
    frame = frame.to_ndarray(format = 'bgr24')

    # camera = cv2.VideoCapture(0)
    
    #　マーカの検出
    dictionary = aruco.Dictionary_get(aruco.DICT_5X5_50)
    # dictionary = aruco.getPredefinedDictionary(aruco.DICT_5X5_50)
    
    # corners:マーカの角 ids:マーカID
    corners, ids, rejectedImgPoints = aruco.detectMarkers(frame, dictionary)
    print(corners * 2)
    # 検出したマーカーの検出 囲みID表示
    frame = aruco.drawDetectedMarkers(frame, corners, ids)
    
    # マーカIDが存在するか
    if np.all(ids != None):
        # 検出されたマーカIDの数だけ繰り返す
        for i in range(len(ids)):
            # 検出されたマーカ座標のデータ
            pts_dst = np.array([
                (corners[i][0][0][0], corners[i][0][0][1]),
                (corners[i][0][1][0], corners[i][0][1][1]),
                (corners[i][0][2][0], corners[i][0][2][1]),
                (corners[i][0][3][0], corners[i][0][3][1]),
                    ])
            
            if ids[i] == 0:
                frame = overlapImg(img[0], pts_dst, frame)
            elif ids[i] == 1:
                frame = overlapImg(img[1], pts_dst, frame)
            elif ids[i] == 2:
                frame = overlapImg(img[2], pts_dst, frame)
            elif ids[i] == 3:
                frame = overlapImg(img[3], pts_dst, frame)

    return av.VideoFrame.from_ndarray(frame, format="bgr24")

# マーカーに表示する画像
if st.button('random'):
    try:
        img = cv2.imread("imgs/2022-10-30_024439-Trinart-characters.png")
        img = imgCut(img)
    except:
        pass
else:
    try:
        img = cv2.imread("imgs/2022-10-30_024439-Trinart-characters.png")
        img = imgCut(img)
    except:
        pass

webrtc_streamer(
    key="example", 
    video_frame_callback=video_frame_callback,
    rtc_configuration={  # Add this config
        "iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]
    }
)

st.title('Streamlit App Test')
st.write('Hello world')

with open("マーカbig.pdf", "rb") as pdf_file:
    PDFbyte = pdf_file.read()

st.download_button(
    label="ARマーカー",
    data=PDFbyte,
    file_name="ARmarker.pdf",
    mime='application/octet-stream')

st.image(img, caption='Sunrise by the mountains')


# tes
#Class
# class VideoProcessor:
#     def recv(self,frame):

#         img = frame.to_ndarray(format = 'bgr24')
#         img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
#         img = av.VideoFrame.from_ndarray(img, format='gray')

#         return img

# webrtc_streamer(key='example2', video_processor_factory=VideoProcessor)
