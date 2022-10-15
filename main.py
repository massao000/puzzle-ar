import streamlit as st
from streamlit_webrtc import webrtc_streamer
import cv2
# import cv2.aruco as aruco
import numpy as np
import os
import av

aruco = cv2.aruco

st.title('Streamlit App Test')
st.write('Hello world')

# https://elsammit-beginnerblg.hatenablog.com/entry/2020/10/10/125246
# https://amdlaboratory.com/amdblog/opencv%E3%81%A8aruco%E3%83%9E%E3%83%BC%E3%82%AB%E3%83%BC%E3%82%92%E5%88%A9%E7%94%A8%E3%81%97%E3%81%9F%E7%94%BB%E5%83%8F%E3%83%9E%E3%83%83%E3%83%94%E3%83%B3%E3%82%B0/

def overlapImg(img, pts_dst, frame):
    """画像をマッピング

    Args:
        img (_type_): マッピング画像
        pts_dst (_type_): 検出されたマーカ座標のデータ
        frame (_type_): 表示画面フレーム

    Returns:
        _type_: 
    """
    size = img.shape
    pts_src = np.array(
                [
                    [0,0],
                    [size[1] - 1, 0],
                    [size[1] - 1, size[0] -1],
                    [0, size[0] - 1 ]
                ],dtype=float
                )
    h, status = cv2.findHomography(pts_src, pts_dst)
    temp = cv2.warpPerspective(img.copy(), h, (frame.shape[1], frame.shape[0])) 
    cv2.fillConvexPoly(frame, pts_dst.astype(int), 0, 16)
    frame = cv2.add(frame, temp)
    
    return frame

# カメラメイン処理
def video_frame_callback(frame):
    frame = frame.to_ndarray(format = 'bgr24')

    # camera = cv2.VideoCapture(0)

    # マーカーに表示する画像
    img = cv2.imread("0001_kaguramea.png")
    img2 = cv2.imread("71y6cwHTrsL._AC_SL1418_.jpg")
    img3 = cv2.imread("20211015.jpg")
    
    # ret, feame = camera.read()
    
    #　マーカの検出
    dictionary = aruco.getPredefinedDictionary(aruco.DICT_5X5_100)
    # corners:マーカの角 ids:マーカID
    corners, ids, rejectedImgPoints = aruco.detectMarkers(frame, dictionary)
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
            
            if ids[i] == 1:
                frame = overlapImg(img, pts_dst, frame)
            elif ids[i] == 2:
                frame = overlapImg(img2, pts_dst, frame)
                
    cv2.imshow('test', frame)

    return av.VideoFrame.from_ndarray(frame, format="bgr24")

webrtc_streamer(key="example", video_frame_callback=video_frame_callback)

st.write('Hello world')

# test
st.title('Streamlit App Test')
st.write('Gray Scale')

#Class
class VideoProcessor:
    def recv(self,frame):

        img = frame.to_ndarray(format = 'bgr24')
        img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        img = av.VideoFrame.from_ndarray(img, format='gray')

        return img

webrtc_streamer(key='example', video_processor_factory=VideoProcessor)
