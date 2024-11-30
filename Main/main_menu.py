import tkinter as tk
import subprocess
import os
from PIL import Image, ImageTk

# Same.py 실행 함수
def run_same():
    same_script = os.path.join("SameP", "Same.py")
    subprocess.run(['python', same_script])

# Name.py 실행 함수
def run_name():
    name_script = os.path.join("NameP", "Name.py")
    subprocess.run(['python', name_script])

# tkinter 윈도우 생성
root = tk.Tk()
root.title("메인 메뉴")
root.geometry("500x400")  # 윈도우 크기 설정 (배경 이미지 크기에 맞게 조정)

# 배경 이미지 설정
bg_image_path = "background.jpg"  # 같은 폴더에 있는 배경 이미지
bg_image = Image.open(bg_image_path)  # 이미지 열기
bg_image = bg_image.resize((500, 400), Image.Resampling.LANCZOS)  # 윈도우 크기에 맞게 이미지 리사이즈
bg_photo = ImageTk.PhotoImage(bg_image)  # tkinter에서 사용할 수 있는 형식으로 변환

# Canvas 위젯을 사용하여 배경 이미지 추가
canvas = tk.Canvas(root, width=500, height=400)
canvas.pack(fill="both", expand=True)

# 배경 이미지 캔버스에 추가
canvas.create_image(0, 0, anchor="nw", image=bg_photo)

# 첫 번째 버튼: Same.py 실행
button_same = tk.Button(root, text="Same 시작", command=run_same)
button_same.place(x=50, y=100)  # 버튼 위치 조정

# 두 번째 버튼: Name.py 실행
button_name = tk.Button(root, text="Name 시작", command=run_name)
button_name.place(x=50, y=150)  # 버튼 위치 조정

# 메인 루프 실행
root.mainloop()
