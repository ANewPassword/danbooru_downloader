# -*- coding: utf-8 -*-

import hashlib

def md5sum(path, chk):
    m = hashlib.md5() # 创建md5对象
    with open(path,'rb') as f:
        while True:
            data = f.read(4096)
            if not data:
                break
            m.update(data) # 更新md5对象

    file_md5 = m.hexdigest() # 返回md5对象
    del(m)
    if file_md5 == chk:
        return True
    else:
        return file_md5