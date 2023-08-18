from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtGui import QIcon, QFontDatabase, QFont
from static import *


class Ui_Form(QtWidgets.QWidget):

    def __init__(self, parent_item, id):
        super().__init__()
        self.edit = None
        self.horizontalLayout = None
        self.horizontalLayoutWidget = None
        self.label = None
        self.parent_item = parent_item
        self.id = id

    def setupUi(self):
        super(Ui_Form, self).__init__()
        fontDb = QFontDatabase.addApplicationFont(":static/font/ico.ttf")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(1)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel()
        self.label.setObjectName("itemLabel")
        self.horizontalLayout.addWidget(self.label)

        self.edit = QtWidgets.QPushButton()
        self.edit.setObjectName("edit")
        self.edit.setFont(QFont('element'))
        self.edit.setFixedWidth(50)
        self.edit.setFixedHeight(30)
        self.edit.setObjectName("edit")
        self.edit.setText(chr(0xe764))
        self.edit.clicked.connect(self.edit_item)

        self.delete = QtWidgets.QPushButton()
        self.delete.setObjectName("delete")
        self.delete.setFont(QFont('element'))
        self.delete.setText(chr(0xe7c9))
        self.delete.setFixedWidth(50)
        self.delete.setFixedHeight(30)
        self.delete.setObjectName("delete")
        self.delete.clicked.connect(self.delete_item)

        self.horizontalLayout.addWidget(self.edit)
        self.horizontalLayout.addWidget(self.delete)
        self.horizontalLayout.setStretch(0, 3)
        self.horizontalLayout.setStretch(1, 1)
        self.horizontalLayout.setStretch(2, 1)
        self.setLayout(self.horizontalLayout)

    def getLabel(self):
        return self.label

    def get_label_text(self):
        return self.label.text()

    def delete_item(self):
        self.parent_item.delete_item_by_id(self.id)

    def edit_item(self):
        value, ok = QtWidgets.QInputDialog.getText(self, "编辑", "请输入标题:")
        if ok:
            self.label.setText(str(value))
            self.parent_item.edit_item(self.id, value)
