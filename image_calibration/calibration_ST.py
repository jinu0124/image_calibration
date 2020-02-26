import os
from calibration import calib
import tkinter

def directory():
    window = tkinter.Tk() # 최상위 레벨 윈도우창 생성

    window.title("Images Folder's Directory")
    window.geometry("720x400+100+100")
    window.resizable(1, 1)
    widget = tkinter.Label(window, text="Convert Image가 있는 폴더 경로를 입력해주세요.<버튼을 안만듦.. 입력 후 엔터 + 창 닫기>")
    widget.pack()

    def command(event):
        global dir
        dir = entry.get() #경로 문자열 받아오기

    entry = tkinter.Entry(window)
    entry.bind("<Return>", command) # call command
    entry.pack()
    window.mainloop() # window창이 종료될때 까지 실행

directory()
ROOT_DIR = dir# dir경로 받기
calib(ROOT_DIR)
