import tkinter as tk
import subprocess
import os
from PIL import Image, ImageTk
import pygame

# Same.py 실행 함수
def run_same():
    same_script = os.path.join("SameP", "Same.py")
    result = subprocess.run(['python', same_script], capture_output=True, text=True)
    if result.returncode != 0:
        print("Error:", result.stderr)
    else:
        print(result.stdout)

# Name.py 실행 함수
def run_name():
    name_script = os.path.join("NameP", "Name.py")
    result = subprocess.run(['python', name_script], capture_output=True, text=True)
    if result.returncode != 0:
        print("Error:", result.stderr)
    else:
        print(result.stdout)

# 음악 상태를 추적하는 변수
music_playing = True

# 음악 켜고 끄는 함수
def toggle_music():
    global music_playing
    if music_playing:
        pygame.mixer.music.stop()  # 음악 정지
        music_playing = False
        music_button.config(text="음악 재생")  # 버튼 텍스트 변경
    else:
        pygame.mixer.music.play(-1, 0.0)  # 음악 재생
        music_playing = True
        music_button.config(text="음악 정지")  # 버튼 텍스트 변경

# tkinter 윈도우 생성
root = tk.Tk()
root.title("메인 메뉴")
root.geometry("800x600")  # 창 크기 설정 (800x600)

# 배경 이미지 설정
bg_image_path = "background.jpg"
try:
    bg_image = Image.open(bg_image_path)
except FileNotFoundError:
    print(f"Error: {bg_image_path} not found!")
    exit()  # 프로그램 종료

bg_image = bg_image.resize((800, 600), Image.Resampling.LANCZOS)
bg_photo = ImageTk.PhotoImage(bg_image)

# Canvas 위젯을 사용하여 배경 이미지 추가
canvas = tk.Canvas(root, width=800, height=600)
canvas.pack(fill="both", expand=True)
canvas.create_image(0, 0, anchor="nw", image=bg_photo)

# pygame 초기화 (배경음악 재생을 위해)
pygame.mixer.init()
pygame.mixer.music.load("background_music.mp3")  # BGM 파일 경로
pygame.mixer.music.play(-1, 0.0)  # -1은 무한 반복, 0.0은 처음부터 재생

# 첫 번째 버튼: Same.py 실행
button_same = tk.Button(root, text="Same 시작", command=run_same)
# 중앙에서 살짝 아래 (x=400, y=300)
canvas.create_window(400, 300, window=button_same)

# 두 번째 버튼: Name.py 실행
button_name = tk.Button(root, text="Name 시작", command=run_name)
# 첫 번째 버튼 아래로 약간 위치 조정 (x=400, y=350)
canvas.create_window(400, 350, window=button_name)

# 음악 제어 버튼 (오른쪽 아래에 위치)
music_button = tk.Button(root, text="음악 정지", command=toggle_music)
canvas.create_window(750, 550, window=music_button)

# 메인 루프 실행
root.mainloop()
