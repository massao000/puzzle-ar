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
    # page_icon="ð§",
    layout="wide"
)

video = VideoProcessor()

# ARãã¼ã«ã¼ã®ã©ã³ãã ãã§ããã
is_random_img = False

up_img = st.sidebar.file_uploader("ãªãªã¸ãã«ç»å", type=['png', 'jpg'])

option = st.sidebar.selectbox(
    label = "ããºã«ãµã¤ãº (æ¨ªxç¸¦)",
    options = ["2x2", "3x3", "4x4", "5x5", "3x2", "4x3", "5x4", "2x3", "3x4"]
)
# 7x7ã¾ã§ããã
# print(imgs)
if up_img:
    imgs = pil2cv(Image.open(up_img))
    dsize=(500, 500)
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
    elif option == "3x2": # æ¨ªé· 2:1
        video.rows, video.cols = 2, 3
        imgs = glob.glob(f'imgs/2-1/*')
        dsize=(750, 500)
    elif option == "4x3": # æ¨ªé· 2:1
        video.rows, video.cols = 3, 4
        imgs = glob.glob(f'imgs/2-1/*')
        dsize=(750, 500)
    elif option == "5x4": # æ¨ªé· 2:1
        video.rows, video.cols = 4, 5
        imgs = glob.glob(f'imgs/2-1/*')
        dsize=(750, 500)
    elif option == "2x3": # ç¸¦é· 1:2
        video.rows, video.cols = 3, 2
        imgs = glob.glob(f'imgs/1-2/*')
        # dsize=(460, 900)
        dsize=(358, 760)
    elif option == "3x4": # ç¸¦é· 1:2
        video.rows, video.cols = 4, 3
        imgs = glob.glob(f'imgs/1-2/*')
        # dsize=(460, 900)
        dsize=(358, 760)
    imgs = pil2cv(Image.open(random.choice(imgs)))
    original_img = cv2.resize((imgs), dsize=dsize)
    video.img, video.comparison_img = video.imgCut(original_img, video.rows, video.cols)

# é£æåº¦
level = st.sidebar.radio(
    label = "ããããã",
    options = ["ãããã", "ãµã¤ã", "ããããã"],
    horizontal=True
)
# st.sidebar.text('ãããã:å¥ãæ¿ã ãµã¤ã:90åº¦ ããããã:90åº¦180åº¦åè»¢')

# st.sidebar.info('ãã¼ã«ã¼50çªã§ã®ã©ã³ãã æ½é¸ã§ã')

if (level == "ãããã"):
    video.level = 0
elif (level == "ãµã¤ã"):
    video.level = 1
elif (level == "ããããã"):
    video.level = 2
else:
    video.level = 0

placeholder_che = st.empty()
# 
# agree = st.sidebar.button('ARãã¼ã«ã¼ã§ç»åã®ã©ã³ãã æ½é¸', key='q')
randm_img = st.sidebar.button('ç»åæ½é¸')
if up_img:
    try:
        original_img = pil2cv(Image.open(up_img))
        original_img = cv2.resize(original_img, dsize=dsize)
        # print(original_img)
        # åç»å, æ¯è¼ç»å
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
            # åç»å, æ¯è¼ç»å
            video.img, video.comparison_img = video.imgCut(original_img, video.rows, video.cols)
            # print(video.img)
        except:
            pass
    else:
        try:
            original_img = cv2.imread(random.choice(imgs))
            original_img = cv2.resize(original_img, dsize=dsize)
            # åç»å, æ¯è¼ç»å
            video.img, video.comparison_img = video.imgCut(original_img, video.rows, video.cols)
        except:
            pass

# dictionary = video.aruco.Dictionary_get(video.aruco.DICT_5X5_50)
# ã«ã¡ã©ã¡ã¤ã³å¦ç
def video_frame_callback(frame):
    global video
    global is_random_img
    # global agree
    
    frame = frame.to_ndarray(format = 'bgr24')
    
    # é»è²ã®èæ¯ã®çæ
    frame2 = np.zeros(frame.copy().shape, dtype=np.uint8)
    frame2.fill(0)
    
    # h, w = self.original_img.shape[:2]
    # frame[0:h, 0:w] = self.original_img
    
    #ããã¼ã«ã®æ¤åº
    dictionary = video.aruco.Dictionary_get(video.aruco.DICT_5X5_50)
    # dictionary = video.aruco.getPredefinedDictionary(video.aruco.DICT_5X5_50)
    
    # corners:ãã¼ã«ã®è§ ids:ãã¼ã«ID
    corners, ids, rejectedImgPoints = video.aruco.detectMarkers(frame, dictionary)
    # print(corners * 2)
    # æ¤åºãããã¼ã«ã¼ã®æ¤åº å²ã¿IDè¡¨ç¤º
    frame = video.aruco.drawDetectedMarkers(frame, corners, ids)
    
    # ãã¼ã«IDãå­å¨ããã
    if np.all(ids != None):
        # ç¹å®ã®ãã¼ã«ã¼ãèª­ã¿è¾¼ã¾ãããç»åã®ãã§ã³ã¸
        # if 10 in ids and agree:
        #     original_img = cv2.imread(random.choice(imgs))
        #     original_img = cv2.resize(original_img, dsize=(500, 500))
        #     video.img, video.comparison_img = video.imgCut(original_img, video.rows, video.cols)
        #     is_random_img = True
        # else:
        #     is_random_img = False
            # cv2.imshow('img', original_img)
        
        # æ¤åºããããã¼ã«IDã®æ°ã ãç¹°ãè¿ã
        for i in range(len(ids)):
            # æ¤åºããããã¼ã«åº§æ¨ã®ãã¼ã¿
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
    
    if  com > 0.9980:
    # if  com > 0.9975:
        # ãã
        cv2.putText(frame, f'{com}%', (0, 50), cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 0), 8, cv2.LINE_AA)
        # æå­
        cv2.putText(frame, f'{com}%', (0, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 10, 10), 3, cv2.LINE_AA)
    else:
        # ãã
        cv2.putText(frame, f'{com}%', (0, 50), cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 0), 8, cv2.LINE_AA)
        # æå­
        cv2.putText(frame, f'{com}%', (0, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 255, 255), 3, cv2.LINE_AA)
        
    return av.VideoFrame.from_ndarray(frame, format="bgr24")

# https://github.com/whitphx/streamlit-webrtc#pull-values-from-the-callback
# lock = threading.Lock()
# result = {"percent": None, "ori_img": None}

ctx = webrtc_streamer(
    key="example", 
    video_frame_callback=video_frame_callback,
    # ã¯ã©ã¹ã§ããå ´åã¯video_processor_factoryã«ãããã¤recvé¢æ°ãframeå¦çã«ä½¿ã
    # video_processor_factory=VideoProcessor, 
    rtc_configuration={  # Add this config
        "iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]
    },
    # video_receiver_size = 10
    # media_stream_constraints={"video": True, "audio": False},
)
    
placeholder = st.sidebar.empty()
# æ­£ããç»åã®è¡¨ç¤º
if ctx.state.playing:
    if up_img:
        placeholder.image(up_img, caption='åç»å')
    else:
        placeholder.image(cv2pil(original_img), caption='åç»å')
    
with open("ãµã³ãã«.pdf", "rb") as pdf_file:
    PDFbyte = pdf_file.read()

st.download_button(
    label="ARãã¼ã«ã¼ãã¦ã³ã­ã¼ã",
    data=PDFbyte,
    file_name="ARmarker.pdf",
    mime='application/octet-stream')

st.write(f"""
# éã³æ¹

â»ããã§ä½¿ç¨ãã¦ããç»åã¯å¨ã¦ãç»åçæAIãä½¿ãä½æãããã®ã«ãªãã¾ãã

### PCæ¨å¥¨

ä»¥ä¸ã®ãã®ãæºå
* ARãã¼ã«ã¼(ARãã¼ã«ã¼ãã¦ã³ã­ã¼ããã¯ãªãã¯)
* ã«ã¡ã©

`èµ¤ãstartãã¿ã³`ãæ¼ããããã°ããå¾ã¡ã¾ãã

ã«ã¡ã©ã®æ åãåºåããã¾ãã

ãã¼ã«ã¼ã®`marker-0`ããããã¨ç»åã®ä¸é¨ãè¡¨ç¤ºããã¾ãã

ãã¨ã¯ããµã¤ããã¼ãããããºã«ãµã¤ãºãå¤æ´ãããããããã®å¤æ´ãç»åæ½é¸ãªã©ãã¦éã³ã¾ãã

ãã£ã¦ãããã¯ãã¼ã»ã³ãã¼ã¸ãéããªã£ããä¸è´ãã¦ãããã¨ã«ãªãã¾ãã

## ãµã¤ããã¼ã«ã¤ãã¦

### ããºã«ãµã¤ãº æ¨ªxç¸¦

|ãµã¤ãº|å¿è¦ãã¼ã«ã¼çªå·|
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

### ããããã

|ããããã|è©³ç´°|
|--|--|
|ãããã|å¥ãæ¿ã|
|ãµã¤ã|å¥ãæ¿ãã90åº¦åè»¢|
|ããããã|å¥ãæ¿ãã90åº¦åè»¢&180åº¦åè»¢|

### ç»åæ½é¸

ãã¿ã³ãæ¼ãã¨ã©ã³ãã ã«ç»åãå¤æ´ã§ãã
""")
