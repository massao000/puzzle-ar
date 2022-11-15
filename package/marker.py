import cv2
import random
import numpy as np

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

def imgCut(img):
    """画像の分割　シャッフル

    Args:
        img (_type_): 表示画像

    Returns:
        _type_: _description_
    """
    
    # 画像の分割数
    rows = 2  # 行数
    cols = 2  # 列数
    chunks = [ randomRotate(chunk) for row_img in np.array_split(img, rows, axis=0) for chunk in np.array_split(row_img, cols, axis=1) ]
    # chunks = []
    # for row_img in np.array_split(img, rows, axis=0):
    #     for chunk in np.array_split(row_img, cols, axis=1):
    #         chunks.append(chunk)
    # print(len(chunks))
    
    # h, w, ch = img.shape
    
    # cat1 = randomRotate(img[0:h//2, 0:w//2])
    # cat2 = randomRotate(img[0:h//2, w//2:w])
    # cat3 = randomRotate(img[h//2:h, 0:w//2])
    # cat4 = randomRotate(img[h//2:h, w//2:w])
    
    # カットした画像をランダムで出力
    # cat_list = [cat1, cat2, cat3, cat4]
    random.shuffle(chunks)
    return chunks
    

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
    
    # アフィン変換
    temp = cv2.warpPerspective(img.copy(), h, (frame.shape[1], frame.shape[0]))
    
    # 多角形を塗りつぶし表示
    cv2.fillConvexPoly(frame, pts_dst.astype(int), 0, 16)
    frame = cv2.add(frame, temp)
    
    return frame