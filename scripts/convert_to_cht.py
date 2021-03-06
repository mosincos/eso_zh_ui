#!/usr/bin/env python
# -*- coding:utf-8 -*-
# File          : convert_to_cht.py
# Author        : bssthu
# Project       : eso_zh_ui
# Description   : 转换为繁体
#   字典来源: https://github.com/BYVoid/OpenCC
# 


import os
import sys
import math
import multiprocessing
from multiprocessing import Pool

from utils.text_replacer import TextReplacer


def usage():
    print('usage:')
    print('python convert_to_cht.py input_file output_file')


def get_text_replacer(lines):
    """从一个字典文件构造简繁替换类

    Args:
        lines (list[str]): 替换表中的行

    Returns:
        text_replacer (TextReplacer): 替换工具
    """
    # 对应表
    replacement = []
    for line in lines:
        line = line.strip()
        if line != '':
            chs, cht = line.split('\t', 1)
            cht = cht.split(' ')[0]     # 如果有多种可能，随便取一个
            cht = cht.split('\t')[0]
            replacement.append((chs, cht))
    # 替换工具
    text_replacer = TextReplacer(replacement)
    return text_replacer


def split_lines_by_first_word_len(lines):
    """根据行中第一个词的长度来对行分组
    本方法没有通用性
    """
    l1 = []
    l2 = []
    l3 = []
    l4 = []
    for line in lines:
        key_len = len(line.strip().split('\t')[0])
        if key_len <= 0:
            continue
        elif key_len <= 2:
            l1.append(line)
        elif key_len <= 3:
            l2.append(line)
        elif key_len <= 4:
            l3.append(line)
        else:
            l4.append(line)

    assert len(l1) != 0
    assert len(l2) != 0
    assert len(l3) != 0
    assert len(l4) != 0
    return [l4, l3, l2, l1]


def prepare_cht_converter():
    """获取所有需要的简繁替换类，使用时按顺序调用

    Returns:
        replacer_list (list[TextReplacer]): 替换工具
    """

    # 字典文件
    cd = os.path.dirname(os.path.abspath(__file__))
    phrases_dict_path = os.path.join(cd, 'utils/data/STPhrases.txt')
    chars_dict_path = os.path.join(cd, 'utils/data/STCharacters.txt')
    other_dict_path = os.path.join(cd, '../translation/STOthers.txt')   # 人工整理的

    with open(phrases_dict_path, 'rt', encoding='utf-8') as fp:
        phrases_dict_lines = fp.readlines()
    with open(chars_dict_path, 'rt', encoding='utf-8') as fp:
        chars_dict_lines = fp.readlines()
    with open(other_dict_path, 'rt', encoding='utf-8') as fp:
        other_dict_lines = fp.readlines()
    phrases_dict_lines_group = split_lines_by_first_word_len(phrases_dict_lines)

    replacer_list = [
        get_text_replacer(other_dict_lines),
        get_text_replacer(phrases_dict_lines_group[0]),
        get_text_replacer(phrases_dict_lines_group[1]),
        get_text_replacer(phrases_dict_lines_group[2]),
        get_text_replacer(phrases_dict_lines_group[3]),
        get_text_replacer(chars_dict_lines),
        get_text_replacer(other_dict_lines)
    ]

    return replacer_list


def convert(input_text, text_replacer):
    """从字典构造简繁替换类

    Args:
        input_text (str): 待替换文本
        text_replacer (TextReplacer): 替换工具
    """
    return text_replacer.replace(input_text)


def main():
    if len(sys.argv) != 3:
        usage()
        sys.exit(2)

    # init file path
    print('init...')
    # 输入输出文本文件
    input_file_path, output_file_path = sys.argv[1], sys.argv[2]

    # 替换工具
    replacer_list = prepare_cht_converter()

    with open(input_file_path, 'rt', encoding='utf-8') as fp:
        lines = fp.readlines()

    # 文本预处理
    # 按行数平分文本
    input_text = []
    num_per_part = 1000     # 每份的行数
    part_num = int(math.ceil(len(lines) / num_per_part))    # 分成多少份
    for i in range(0, part_num):
        input_text.append(lines[num_per_part * i:num_per_part * (i + 1)])
    if part_num > 1:
        input_text.append(lines[num_per_part * (part_num - 1):])

    # 转换
    print('convert...')
    text_list = [''.join(partial_text) for partial_text in input_text]
    for text_replacer in replacer_list:
        # 每个 replacer 转一遍
        convert_args = [(partial_text, text_replacer) for partial_text in text_list]
        with Pool(processes=multiprocessing.cpu_count()) as pool:
            text_list = pool.starmap(convert, convert_args)

    # 结果
    output_text = ''.join(text_list)

    # 保存
    with open(output_file_path, 'wt', encoding='utf-8') as fp:
        fp.write(output_text)


if __name__ == '__main__':
    main()
