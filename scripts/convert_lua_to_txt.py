#!/usr/bin/env python
# -*- coding:utf-8 -*-
# File          : convert_lua_to_txt.py
# Author        : bssthu
# Project       : eso_zh_ui
# Description   : 将从 mnf 中解出的， EsoUI 文件夹下的 en_client.lua 等转换为 .txt 文件
# 


import os
import sys

from objs.ui_mgr import UiMgr


def main():
    lang = 'zh'
    if len(sys.argv) == 2:
        lang = sys.argv[1]

    cd = sys.path[0]
    translation_path = os.path.join(cd, '../translation')

    # load lua
    pregame_file = os.path.join(translation_path, 'en_pregame.lua')
    client_file = os.path.join(translation_path, 'en_client.lua')

    ui_mgr = UiMgr()
    ui_mgr.load_lua_file(pregame_file)
    ui_mgr.load_lua_file(client_file)
    print('read %d lines.' % len(ui_mgr.ui_lines))

    # save merged lines
    translate_file = os.path.join(translation_path, '%s_translate.txt' % lang)
    if os.path.exists(translate_file):
        choose = input('%s_translate.txt file exists, merge? [y/N]' % lang)
        choose = choose.lower().strip()
        if choose != '' and choose[0] == 'y':
            print('merging to translate file.')
            ui_mgr.apply_translate_from_txt_file(translate_file)
        else:
            print('skipped.')
            return

    with open(translate_file, 'wt', encoding='utf-8') as fp:
        fp.writelines(ui_mgr.get_txt_lines(replace=True))
        print('save translate file succeed.')


if __name__ == '__main__':
    main()
