import uuid
import os
from PyQt6 import QtWidgets, QtCore
from PyQt6.QtGui import QFontMetrics
from PyQt6.QtWidgets import QListWidgetItem
import json

from sub_item import Ui_Form


def get_dialog(json_data, parent):
    if json_data["id"] is None:
        json_data["id"] = str(uuid.uuid1())

    dialog = Ui_Form(parent, json_data["id"])
    dialog.setupUi()
    label: QtWidgets.QLabel = dialog.getLabel()
    metrics = QFontMetrics(label.font())
    short_text = metrics.elidedText(json_data['name'], QtCore.Qt.TextElideMode.ElideLeft, label.width())
    label.setText(short_text)
    return dialog


def add_item(item_list: QtWidgets.QListWidget, json_data):
    window = item_list
    item = QListWidgetItem()
    item.setSizeHint(QtCore.QSize(50, 40))
    dialog = get_dialog(json_data, window)
    window.addItem(item)

    window.setItemWidget(item, dialog)
    return item


def save_data(data):
    path = os.environ['USERPROFILE'] + "/剪切板/data.json"
    with open(path, "w", encoding="utf-8") as f:
        f.write(json.dumps(data))
