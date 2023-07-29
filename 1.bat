 pyinstaller -F -i static/icon.ico main.py -p common.py -p copy_board.py -p static.py -p sub_item.py -p tool.py



pyrcc5 -o static.py 1.qrc
pyinstaller -F -w -i static/icon.ico main.py -p common.py -p copy_board.py -p static.py -p sub_item.py -p tool.py --noconsole