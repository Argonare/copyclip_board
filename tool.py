import json
import os

from common import add_item
from copy_board import Ui_MainWindow


# 创建缓存数据
def check_init(ui: Ui_MainWindow):
    item_list=[]
    path = os.environ['USERPROFILE'] + "/剪切板/data.json"
    saved = []
    if not os.path.exists(path):
        os.mkdir(os.environ['USERPROFILE'] + "/剪切板")
        with open(path, 'w', encoding="utf-8") as f:
            f.write("[]")
        # os.system(r'attrib +h ' + path)
        os.chmod(path, 755)
    else:
        with open(path, 'r', encoding="utf-8") as f:
            data = f.read()
            if data == "":
                saved = []
            else:
                saved = json.loads(data)

        for i in saved:
            item=add_item(ui.get_list(), i)
            item_list.append(item)
    ui.set_data(saved,item_list)
