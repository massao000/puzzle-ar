# メインで
import cv2
import numpy as np
import random
from PIL import Image, ImageChops

# https://elsammit-beginnerblg.hatenablog.com/entry/2020/10/10/125246
# https://amdlaboratory.com/amdblog/opencv%E3%81%A8aruco%E3%83%9E%E3%83%BC%E3%82%AB%E3%83%BC%E3%82%92%E5%88%A9%E7%94%A8%E3%81%97%E3%81%9F%E7%94%BB%E5%83%8F%E3%83%9E%E3%83%83%E3%83%94%E3%83%B3%E3%82%B0/

# https://qiita.com/derodero24/items/f22c22b22451609908ee
def pil2cv(image):
    """ PIL型 -> OpenCV型 
    
    Args:
        image (_type_): 変換画像

    Returns:
        _type_: _description_
    """
    new_image = np.array(image, dtype=np.uint8)
    if new_image.ndim == 2:  # モノクロ
        pass
    elif new_image.shape[2] == 3:  # カラー
        new_image = cv2.cvtColor(new_image, cv2.COLOR_RGB2BGR)
    elif new_image.shape[2] == 4:  # 透過
        new_image = cv2.cvtColor(new_image, cv2.COLOR_RGBA2BGRA)
    return new_image

def cv2pil(image):
    """ OpenCV型 -> PIL型 
    
    Args:
        image (_type_): 変換画像

    Returns:
        _type_: _description_
    """
    new_image = image.copy()
    if new_image.ndim == 2:  # モノクロ
        pass
    elif new_image.shape[2] == 3:  # カラー
        new_image = cv2.cvtColor(new_image, cv2.COLOR_BGR2RGB)
    elif new_image.shape[2] == 4:  # 透過
        new_image = cv2.cvtColor(new_image, cv2.COLOR_BGRA2RGBA)
    new_image = Image.fromarray(new_image)
    return new_image


def comparison(ori_img, img):
    """画像の比較

    Args:
        ori_img (_type_): オリジナル画像
        img (_type_): _description_

    Returns:
        _type_: _description_
    """
    # https://office54.net/python/module/opencv-numpy-compare
    img_size = (500, 500)
    
    # 画像をリサイズする
    image1 = cv2.resize(ori_img, img_size)
    image2 = cv2.resize(img, img_size)
    
    # 画像をヒストグラム化する
    image1_hist = cv2.calcHist([image1], [0], None, [256], [0, 256])
    image2_hist = cv2.calcHist([image2], [0], None, [256], [0, 256])

    # ヒストグラムした画像を比較
    # print(cv2.compareHist(image1_hist, image2_hist, 0))
    return round(cv2.compareHist(image1_hist, image2_hist, 0), 4)

def trimming(img):
    """画像の無駄な部分を削除

    Args:
        img (_type_): _description_

    Returns:
        _type_: _description_
    """
    # https://qiita.com/derodero24/items/f22c22b22451609908ee
    new_image = cv2pil(img)
    
    # https://water2litter.net/rum/post/python_crop_margin/
    # 背景色の抽出
    bg_img = Image.new('RGB', new_image.size, new_image.getpixel((0,0)))

    # 差分画像の生成
    diff_img = ImageChops.difference(new_image, bg_img)

    # クロップ範囲の計算
    crop_range = diff_img.convert('RGB').getbbox()

    # クロップの実行と出力
    crop_img = new_image.crop(crop_range)

    # https://qiita.com/derodero24/items/f22c22b22451609908ee
    # cv2_img = np.array(crop_img, dtype=np.uint8)
    cv2_img = pil2cv(crop_img)
    
    return cv2_img

def randomRotate(cat_img):
    """画像のランダム回転

    Args:
        cat_img (_type_): カット画像

    Returns:
        _type_: _description_
    """
    
    rotate_number = [0, 1, 2, 3]
    rando = random.choice(rotate_number)
    
    if (rando == 1):
        return cv2.rotate(cat_img, cv2.ROTATE_90_CLOCKWISE)
    elif (rando == 2):
        return cv2.rotate(cat_img, cv2.ROTATE_90_COUNTERCLOCKWISE)
    elif (rando == 3):
        return cv2.rotate(cat_img, cv2.ROTATE_180)
    else:
        return cat_img

def concat_tile(im_list_2d):
    """画像の結合

    Args:
        im_list_2d (_type_): 分割された元画像のデータ

    Returns:
        _type_: _description_
    """
    # https://note.nkmk.me/python-opencv-hconcat-vconcat-np-tile/
    return cv2.vconcat([cv2.hconcat(im_list_h) for im_list_h in im_list_2d])

def imgCut(img, rows=2, cols=2):
    """画像の分割　シャッフル

    Args:
        img (_type_): _description_
        rows int : 行数
        cols int : 列数

    Returns:
        _type_: _description_
    """
    # chunks = [ chunk for row_img in np.array_split(img, rows, axis=0) for chunk in np.array_split(row_img, cols, axis=1) ]
    # chunks = [ randomRotate(chunk) for row_img in np.array_split(img, rows, axis=0) for chunk in np.array_split(row_img, cols, axis=1) ]
    chunks = [ chunk for row_img in np.array_split(img, rows, axis=0) for chunk in np.array_split(row_img, cols, axis=1) ]
    chunks_random = [ randomRotate(i) for i in chunks]
    
    # 余白の追加
    chunks_whitespace = [ cv2.copyMakeBorder(i, 7, 7, 7, 7, cv2.BORDER_CONSTANT, value=[0,0,0]) for i in chunks ]
    
    # 元画像に余白を追加
    start = 0
    num = rows
    two_list = []
    for i in range(rows):
        l = []
        for j in range(start, num):
            l.append(chunks_whitespace[j])
        two_list.append(l)
        start += rows
        num += rows
    # 比較用画像
    comparison_img = concat_tile(two_list)

    random.shuffle(chunks_random)
    
    return chunks_random, comparison_img

def overlapImg(img, pts_dst, frame, frame2):
    """画像をマッピング

    Args:
        img (_type_): マッピング画像
        pts_dst (_type_): 検出されたマーカ座標のデータ
        frame (_type_): 表示画面フレーム
        frame2 (_type_): 表示画面の背景
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
    # 特定の物体の検知
    h, status = cv2.findHomography(pts_src, pts_dst)

    # アフィン変換
    temp = cv2.warpPerspective(img.copy(), h, (frame.shape[1], frame.shape[0]))
    
    # 多角形を塗りつぶし表示
    cv2.fillConvexPoly(frame, pts_dst.astype(int), 0, 16)
    frame = cv2.add(frame, temp)
    
    # 分割された画像を追加
    frame2 = cv2.add(frame2, temp)
    
    return frame, frame2


aruco = cv2.aruco
#マーカを検出       
dictionary = aruco.getPredefinedDictionary(aruco.DICT_5X5_50)

camera = cv2.VideoCapture(0)
camera.set(cv2.CAP_PROP_FPS, 60)
camera.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

# マーカーに表示する画像\
imgs = [
    # "imgs/0001_kaguramea.png",
    # # "imgs/71y6cwHTrsL._AC_SL1418_.jpg",
    # # "20211015.jpg",
    # "imgs/2022-10-30_024439-Trinart-characters.png",
    # "imgs/2022-10-30_005405-waifu.png",
    # "imgs/2022-10-29_230626-waifu.png",
    r"imgs\2-1\00001_steps-50_scale-7.5_720x448_seed-8939454022723035.png"
    ]

# print(random.choice(imgs))

original_img = cv2.imread(random.choice(imgs))
dsize=(750,500)
original_img = cv2.resize(original_img, dsize=dsize)

cv2.imshow('img', original_img)

# カットサイズ
rows, cols = 2, 3

img, comparison_img = imgCut(original_img, rows, cols)
max_m = 0
while True:
    ret, frame = camera.read()
    
    # 黒色の背景の生成
    frame2 = np.zeros(frame.copy().shape, dtype=np.uint8)
    frame2.fill(0)
    
    #　マーカの検出
    # corners:マーカの角 ids:マーカID
    corners, ids, rejectedImgPoints = aruco.detectMarkers(frame, dictionary)
    # print(corners * 2)
    # print(ids)
    
    # 検出したマーカーの検出 囲みID表示
    frame = aruco.drawDetectedMarkers(frame, corners, ids)
    
    # マーカIDが存在するか
    if np.all(ids != None):
        # 特定のマーカーが読み込まれたら画像のチェンジ
        if 10 in ids:
            original_img = cv2.imread(random.choice(imgs))
            original_img = cv2.resize(original_img, dsize=dsize)
            img, comparison_img = imgCut(original_img, rows, cols)
            cv2.imshow('img', original_img)
        
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
    # print(frame2)
    # frame2 = frame2[50 : 150, 100 : random.randint(200, 250)]
    # points = np.array([(50, 50), (100, 50), (250, 200), (180, 250)])
    # cv2.polylines(frame2, [points], True, (255, 255, 0))
    
    frame3 = trimming(frame2)
    cv2.imshow('test2', frame3)
    
    com = comparison(comparison_img, frame3)
    # print(com)
    if  com > 0.99:
        # フチ
        cv2.putText(frame, f'{com}%', (0, 50), cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 0), 8, cv2.LINE_AA)
        # 文字
        cv2.putText(frame, f'{com}%', (0, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 10, 10), 3, cv2.LINE_AA)
    else:
        # フチ
        cv2.putText(frame, f'{com}%', (0, 50), cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 0), 8, cv2.LINE_AA)
        # 文字
        cv2.putText(frame, f'{com}%', (0, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 255, 255), 3, cv2.LINE_AA)
    
    
    cv2.imshow('test', frame)
    
    
    
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
camera.release()
cv2.destroyAllWindows()
