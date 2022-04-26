import cv2 as cv
import numpy as np
import math
from PIL import Image, ImageDraw, ImageFont


def select_point_in_image(img):
    """
    输入一张图像，鼠标选取图像一个或多个点，返回点坐标
    :param img:图像
    :return:[(x, y), (x, y), (x, y), ...]
    """
    def mouse_callback(event, x, y, flags, param):
        if event == cv.EVENT_LBUTTONDOWN:
            param.append((x, y))
            cv.circle(param[0], (x, y), 3, (255, 0, 0), -1)
            cv.putText(param[0], str(x) + "," + str(y), (x, y), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv.imshow("img", param[0])

    para = [img]
    cv.imshow("img", para[0])
    cv.setMouseCallback("img", mouse_callback, param=para)
    cv.waitKey(0)
    cv.destroyAllWindows()
    return para[1:]


def perspective_transform(img, coord):
    """
    透视变换
    :param img: 变换前图像
    :param coord:变换前图像中需要透视变换的四个坐标
    :return:变换后图像
    """
    def get_target_coords(ori_coord):
        coord_1, coord_2, coord_3, coord_4 = ori_coord
        x, y = coord_1
        width = int(math.sqrt(pow(abs(coord_1[0] - coord_2[0]), 2) + pow(abs(coord_1[1] - coord_2[1]), 2)))
        height = int(math.sqrt(pow(abs(coord_1[0] - coord_4[0]), 2) + pow(abs(coord_1[1] - coord_4[1]), 2)))
        return [[x, y], [x + width, y], [x + width, y + height], [x, y + height]]

    target_coord = get_target_coords(ori_coord=coord)
    img_height, img_width = img.shape[:2]
    trans_matrix = cv.getPerspectiveTransform(np.float32(coord), np.float32(target_coord))
    target_img = cv.warpPerspective(img, trans_matrix, (img_width, img_height))
    return target_img[target_coord[0][1]:target_coord[2][1], target_coord[0][0]:target_coord[1][0], :]


def blur_calculate(image):
    """
    模糊度计算
    :param image: 被计算模糊度的图像
    :return: 模糊度
    """
    image = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    image_lap = cv.Laplacian(image, 2)
    blur = sum(sum(image_lap)) / 255.0
    return blur


def modify_and_confirm_with_selectROI(ori_img, window_place=(800, 250)):
    """
    鼠标选取ROI，返回x, y, w, h
    :param ori_img: 图像
    :param window_place: 窗口位置，方便看
    :return: ROI x, y, w, h
    """
    cv.imshow('ori_img', ori_img)
    cv.moveWindow("ori_img", x=window_place[0], y=window_place[1])
    x, y, w, h = cv.selectROI("show", cv.resize(ori_img, None, None, fx=3, fy=3))
    cv.destroyAllWindows()
    x, y, w, h = int(x / 3), int(y / 3), int(w / 3), int(h / 3)
    return x, y, w, h


def cv2ImgAddChineseText(img, text, pos, textColor=(255, 255, 255), textSize=45):
    """
    在图片中打印中文字符
    :param img: 被打印图像
    :param text: 打印文本
    :param pos: 打印文本坐标
    :param textColor: 打印文本颜色
    :param textSize: 打印文本大小
    :return: 被打印后图像
    """
    if isinstance(img, np.ndarray):  # detect opencv format or not
        img = Image.fromarray(cv.cvtColor(img, cv.COLOR_BGR2RGB))
    draw = ImageDraw.Draw(img)
    fontText = ImageFont.truetype("utils/NotoSansCJK-Regular.ttc", textSize, encoding="utf-8")
    draw.text(pos, text, textColor, font=fontText)
    return cv.cvtColor(np.asarray(img), cv.COLOR_RGB2BGR)