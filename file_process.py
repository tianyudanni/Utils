import cv2 as cv
import os

import random


def walk_files(walk_path):
    """
    遍历文件夹下所有类型文件
    :param walk_path: 遍历文件夹路径
    :return: path列表
    """
    walk_tree = os.walk(walk_path)
    paths = []
    for dirName, subDirs, files in walk_tree:
        for file in files:
            paths.append(os.path.join(dirName, file))
    return paths


def read_images(image_paths):
    """
    接收带每张图片路径的列表，返回读取图片后列表
    :param image_paths: 图片路径列表
    :return: image列表
    """
    return [cv.imread(path) for path in image_paths]


def remove_files_by_key(folder, key):
    """
    移除文件夹中文件名包含关键词key的文件
    :param folder: 需要移除文件的文件夹路径
    :param key: 被移除文件名中包含的关键词
    """
    file_paths = walk_files(folder)
    for path in file_paths:
        if key in path:
            os.remove(path)


def remove_files_by_suffix(folder, suffix):
    """
    移除文件夹中文件后缀包含suffix内容的文件
    :param folder:
    :param suffix:
    """
    file_paths = walk_files(folder)
    for path in file_paths:
        basename, suf = os.path.splitext(path)
        if suffix in suf:
            os.remove(path)


def generate_train_val_test_sets(files_list, train_ratio, test=False):
    """
    输入包含路径的列表，根据train，val，test比例返回相应长度的路径列表
    :param files_list: 包含路径的列表
    :param train_ratio: 训练集比例
    :param test: 是否划分测试集
    :return: list, list, ? list
    """
    for i in range(3):
        random.shuffle(files_list)

    files_list_length = len(files_list)
    if test:
        test_ratio = input("please input expected test ratio: ")
        train_set = files_list[:int(train_ratio * files_list_length)]
        val_set = files_list[int(train_ratio * files_list_length):int((1 - test_ratio) * files_list_length)]
        test_set = files_list[int((1 - test_ratio) * files_list_length):]
        return train_set, val_set, test_set
    else:
        train_set = files_list[:int(train_ratio * files_list_length)]
        val_set = files_list[int(train_ratio * files_list_length):]
        return train_set, val_set


def write_txt(text_content_list, save_path):
    """
    将列表中的每个字符串元素写入txt文件中，一个列表元素写一行
    :param text_content_list: 需要写入txt的内容列表
    :param save_path: txt保存路径
    """
    with open(save_path, "w") as file:
        for one_line in text_content_list:
            file.write(one_line + "\n")


def change_image_format(image_folder, target_format):
    """
    改变目标文件夹下所有图片的格式为target_format指定的图片格式
    :param image_folder: 目标文件夹路径
    :param target_format: 指定图片格式，eg. jpg/png
    """
    file_paths = walk_files(walk_path=image_folder)
    for path in file_paths:
        file_text = os.path.splitext(path)[0]
        file_save_path = file_text + "." + target_format
        image = cv.imread(path)
        cv.imwrite(file_save_path, image)
        os.remove(path)

