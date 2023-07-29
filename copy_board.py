import sys
import uuid

from PyQt6 import QtCore, QtGui, QtWidgets
import pyperclip
from PyQt6.QtCore import QPoint, Qt, QEvent
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QMainWindow, QListWidgetItem
import common
import time
from static import *
from sub_item import Ui_Form


class Ui_MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.search = None
        self.m_flag = False
        self._move_drag = False
        self._bottom_drag = False
        self._corner_drag = False
        self._right_drag = False
        self._top_rect = None
        self._padding = 10
        self.listWidget: MySignal | None = None
        self.label = None
        self.data = [{}]
        self.init_width = 300
        self.init_height = 200
        self.btnWidth = 40
        self.btnHeight = 30
        self.moved = True

        self.saved_flag = False
        self.title = "剪切板"
        self.SCREEN_WEIGHT = QtGui.QGuiApplication.primaryScreen().geometry().width()

    def setup(self):

        self.resize(self.init_width, self.init_height)
        central_widget = QtWidgets.QWidget(self)
        self.verticalLayoutWidget = QtWidgets.QWidget(central_widget)

        self.verticalLayoutWidget.setGeometry(0, 0, self.init_width, self.init_height)
        vertical_layout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        vertical_layout.setContentsMargins(0, 0, 0, 0)
        horizontal_layout = QtWidgets.QHBoxLayout()
        self.label = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label.setText("剪切板")
        horizontal_layout.addWidget(self.label)

        small = QtWidgets.QPushButton(self.verticalLayoutWidget)
        small.setIcon(QIcon(":/static/short.png"))
        small.setFixedWidth(self.btnWidth)
        small.setFixedHeight(self.btnHeight)

        horizontal_layout.addWidget(small)

        vertical_layout.addLayout(horizontal_layout)

        self.listWidget = MySignal(self.verticalLayoutWidget)
        self.listWidget.set_window(self)
        self.listWidget.itemClicked.connect(self.get_item)

        self.search = QtWidgets.QTextEdit(self.verticalLayoutWidget)
        self.search.setFixedHeight(30)
        self.search.hide()
        self.search.textChanged.connect(self.searchChange)
        self.search.installEventFilter(self)
        vertical_layout.addWidget(self.search)
        vertical_layout.addWidget(self.listWidget)

        self.setCentralWidget(central_widget)
        self.setWindowFlags(
            QtCore.Qt.WindowType.FramelessWindowHint | QtCore.Qt.WindowType.WindowStaysOnTopHint | QtCore.Qt.WindowType.SplashScreen)
        small.clicked.connect(self.onIconClicked)

        QtCore.QMetaObject.connectSlotsByName(self)
        self.show()
        # 托盘
        self.tray = QtWidgets.QSystemTrayIcon(self)
        self.tray.setIcon(QIcon(":/static/short.png"))
        self.trayMenu = QtWidgets.QMenu(self)
        show_action = self.trayMenu.addAction("显示")
        quit_action = self.trayMenu.addAction("退出")
        self.tray.setContextMenu(self.trayMenu)
        self.tray.show()
        show_action.triggered.connect(self.show_window)
        quit_action.triggered.connect(self.quit)
        self.tray.activated.connect(self.act)
        self.tray.setToolTip(self.title)
        self.setWindowTitle(self.title)
        # 定时保存
        timer = QtCore.QTimer(self)
        timer.timeout.connect(self.save_data)
        timer.start(5000)

    def searchChange(self):
        text = self.search.toPlainText()
        q_list = self.listWidget
        self.listWidget.clear()

        for i in self.data:
            if text == "":
                common.add_item(self.listWidget, i)
            else:
                if text in i['name']:
                    common.add_item(self.listWidget, i)

        print()

    def eventFilter(self, watched, event: QtCore.QEvent):
        search: QtWidgets.QTextEdit = self.search
        if watched == search:
            if event.type() == QtCore.QEvent.Type.FocusOut and search.toPlainText() == "":
                search.hide()
        return super().eventFilter(watched, event)

    # 鼠标按下事件
    def mousePressEvent(self, event: QtGui.QMouseEvent):
        if event.button() == QtCore.Qt.MouseButton.LeftButton and event.pos() in self._top_rect:
            self.m_flag = True
            self.m_Position = event.globalPosition() - self.pos().toPointF()
            event.accept()
            self.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.OpenHandCursor))
        if (event.button() == QtCore.Qt.MouseButton.LeftButton) and (event.pos() in self._corner_rect):
            self._corner_drag = True
            event.accept()
        elif (event.button() == QtCore.Qt.MouseButton.LeftButton) and (event.pos() in self._right_rect):
            self._right_drag = True
            event.accept()
        elif (event.button() == QtCore.Qt.MouseButton.LeftButton) and (event.pos() in self._bottom_rect):
            self._bottom_drag = True
            event.accept()
        elif (event.button() == QtCore.Qt.MouseButton.LeftButton) and (event.pos().y() < self.height()):
            # 鼠标左键点击标题栏区域
            self._move_drag = True
            self.move_DragPosition = event.globalPosition() - self.pos().toPointF()
            event.accept()

    # 鼠标移动事件
    def mouseMoveEvent(self, event: QtGui.QMouseEvent):
        if QtCore.Qt.MouseButton.LeftButton and self.m_flag:
            p = event.globalPosition() - self.m_Position
            self.move(int(p.x()), int(p.y()))  # 更改窗口位置
            event.accept()
        elif event.pos() in self._corner_rect:
            self.setCursor(QtCore.Qt.CursorShape.SizeFDiagCursor)
        elif event.pos() in self._bottom_rect:
            self.setCursor(QtCore.Qt.CursorShape.SizeVerCursor)
        elif event.pos() in self._right_rect:
            self.setCursor(QtCore.Qt.CursorShape.SizeHorCursor)
        else:
            self.setCursor(QtCore.Qt.CursorShape.ArrowCursor)

        # 当鼠标左键点击不放及满足点击区域的要求后，分别实现不同的窗口调整
        # 没有定义左方和上方相关的5个方向，主要是因为实现起来不难，但是效果很差，拖放的时候窗口闪烁，再研究研究是否有更好的实现
        if QtCore.Qt.MouseButton.LeftButton and self._right_drag:
            # 右侧调整窗口宽度
            self.resize(event.pos().x(), self.height())
            event.accept()
        elif QtCore.Qt.MouseButton.LeftButton and self._bottom_drag:
            # 下侧调整窗口高度
            self.resize(self.width(), event.pos().y())
            event.accept()
        elif QtCore.Qt.MouseButton.LeftButton and self._corner_drag:
            # 右下角同时调整高度和宽度
            self.resize(event.pos().x(), event.pos().y())
            event.accept()
        elif QtCore.Qt.MouseButton.LeftButton and self._move_drag:
            d = event.globalPosition() - self.move_DragPosition
            self.move(int(d.x()), int(d.y()))
            event.accept()

    def mouseReleaseEvent(self, event: QtGui.QMouseEvent):
        self.m_flag = False
        self.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.ArrowCursor))
        self._move_drag = False
        self._corner_drag = False
        self._bottom_drag = False
        self._right_drag = False

    def act(self, reason):
        if reason.value == 1 or reason.value == 3:
            self.show_window()

    def get_list(self):
        return self.listWidget

    def data(self):
        return self.data

    def set_data(self, data, itemLis):
        self.data = data
        self.listWidget.set_item_list(itemLis)

    def get_item(self, item):
        pyperclip.copy(self.data[self.listWidget.currentIndex().row()]['value'])

    def small_click(self, status):
        self.showMinimized()

    def close_click(self, status):
        self.tray = None
        self.close()

    def show_window(self):
        # 若是最小化，则先正常显示窗口，再变为活动窗口（暂时显示在最前面）
        self.showNormal()
        self.activateWindow()

    def save_data(self):
        if self.saved_flag and self.data is not None:
            common.save_data(self.data)

    def quit(self):
        self.tray.hide()
        sys.exit()

    def onIconClicked(self, reason):
        if self.isMinimized() or not self.isVisible():
            self.showNormal()
            self.activateWindow()
            self.setWindowFlags(QtCore.Qt.WindowType.Window)
            self.show()
        else:
            self.showMinimized()
            self.setWindowFlags(QtCore.Qt.WindowType.SplashScreen)

    def enterEvent(self, event):
        self.hide_or_show('show', event)

    def leaveEvent(self, event):
        self.hide_or_show('hide', event)

    def hide_or_show(self, mode, event):
        pos = self.frameGeometry().topLeft()
        WINDOW_WEIGHT = self.width()
        WINDOW_HEIGHT = self.height()

        SCREEN_WEIGHT = self.SCREEN_WEIGHT
        if mode == 'show' and self.moved:
            if pos.x() + WINDOW_WEIGHT >= SCREEN_WEIGHT:  # 右侧显示
                self.startAnimation(SCREEN_WEIGHT - WINDOW_WEIGHT + 2, pos.y())
                event.accept()
                self.moved = False
            elif pos.x() <= 0:  # 左侧显示
                self.startAnimation(0, pos.y())
                event.accept()
                self.moved = False
            elif pos.y() <= 0:  # 顶层显示
                self.startAnimation(pos.x(), 0)
                event.accept()
                self.moved = False
        elif mode == 'hide':
            if pos.x() + WINDOW_WEIGHT >= SCREEN_WEIGHT:  # 右侧隐藏
                self.startAnimation(SCREEN_WEIGHT - 2, pos.y())
                event.accept()
                self.moved = True
            elif pos.x() <= 2:  # 左侧隐藏
                self.startAnimation(2 - WINDOW_WEIGHT, pos.y())
                event.accept()
                self.moved = True
            elif pos.y() <= 2:  # 顶层隐藏
                self.startAnimation(pos.x(), 2 - WINDOW_HEIGHT)
                event.accept()
                self.moved = True

    def startAnimation(self, width, height):
        data = QtCore.QByteArray()
        data.append(b"geometry")
        animation = QtCore.QPropertyAnimation(self, data, self)
        startpos = self.geometry()
        animation.setDuration(200)
        newpos = QtCore.QRect(width, height, startpos.width(), startpos.height())
        animation.setEndValue(newpos)
        animation.start()

    def resizeEvent(self, QResizeEvent):
        self.verticalLayoutWidget.setFixedWidth(self.width())
        self.verticalLayoutWidget.setFixedHeight(self.height())
        self._right_rect = [QPoint(x, y) for x in range(self.width() - self._padding, self.width() + 1)
                            for y in range(1, self.height() - self._padding)]
        self._bottom_rect = [QPoint(x, y) for x in range(1, self.width() - self._padding)
                             for y in range(self.height() - self._padding, self.height() + 1)]
        self._corner_rect = [QPoint(x, y) for x in range(self.width() - self._padding, self.width() + 1)
                             for y in range(self.height() - self._padding, self.height() + 1)]
        self._top_rect = [QPoint(x, y) for x in range(1, self.width() - self._padding)
                          for y in range(1, 40)]

    def keyPressEvent(self, event: QtGui.QKeyEvent):
        code = event.key()
        search: QtWidgets.QTextEdit = self.search

        if 65 <= code <= 90 or 48 <= code <= 57:
            search.setFocus()
            if search.isHidden():
                search.show()
                search.setText(event.text())
            cursor = search.textCursor()
            cursor.movePosition(QtGui.QTextCursor.MoveOperation.EndOfWord)
            search.setTextCursor(cursor)


class MySignal(QtWidgets.QListWidget):

    def __init__(self, parent):
        super().__init__(parent)
        # 存放所有子item
        self.item_list: list[QListWidgetItem] = []
        self._bottom_rect = None
        self._right_rect = None
        self._corner_rect = None
        self.window_item = None

    def __int__(self):
        super().__init__()

    def set_window(self, window_item):
        self.window_item = window_item

    # 添加
    def mousePressEvent(self, event):
        if event.buttons() == QtCore.Qt.MouseButton.MiddleButton:
            self.window_item.saved_flag = True
            text: str = pyperclip.paste()
            name = text.replace(" ", "").replace("\n", "")[:10]
            res = {"name": text.replace(" ", "").replace("\n", ""), "value": text, "id": str(uuid.uuid1())}
            common.add_item(self, res)
            self.window_item.data.append(res)
            event.accept()
        else:
            super().mousePressEvent(event)

    # 删除
    def delete_item_by_id(self, id):
        self.window_item.saved_flag = True
        for i in range(len(self.window_item.data)):
            item = self.window_item.data[i]
            if item["id"] == id:
                self.window_item.data.pop(i)
                self.takeItem(i)
                return

    def edit_item(self, id, value):
        self.window_item.saved_flag = True
        for i in range(len(self.window_item.data)):
            item = self.window_item.data[i]
            if item["id"] == id:
                self.window_item.data[i]['name'] = value
                return

    def set_item_list(self, data):
        self.item_list = data

    def get_item_list(self):
        return self.item_list

    def keyPressEvent(self, event: QtGui.QKeyEvent):
        return self.window_item.keyPressEvent(event)
