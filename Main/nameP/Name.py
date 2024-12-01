import tkinter as tk
import random
from PIL import Image, ImageTk
import os
import pygame  # pygame 라이브러리 추가

# pygame 초기화 (소리 기능 사용)
pygame.mixer.init()

# 현재 디렉토리 경로 설정 (Main 폴더 내)
base_dir = os.path.dirname(os.path.abspath(__file__))  # 현재 파일의 경로
img_dir = os.path.join(base_dir, 'imgs')  # 'imgs' 폴더 경로
bgm_dir = os.path.join(base_dir, 'BGMs')  # 'BGMs' 폴더 경로

# 소리 파일 경로
bgm_file = os.path.join(bgm_dir, 'bgm.mp3')  # 배경 음악 파일
correct_sound_file = os.path.join(bgm_dir, 'crt.wav')  # 정답 소리 파일 (crt.wav)
wrong_sound_file = os.path.join(bgm_dir, 'wrong.wav')  # 오답 소리 파일

# 배경 음악 재생 (반복 재생)
def play_bgm():
    pygame.mixer.music.load(bgm_file)
    pygame.mixer.music.play(-1, 0.0)  # 무한 반복 재생 (-1)

# 정답 소리 재생
def play_correct_sound():
    correct_sound = pygame.mixer.Sound(correct_sound_file)
    correct_sound.play()

# 오답 소리 재생
def play_wrong_sound():
    wrong_sound = pygame.mixer.Sound(wrong_sound_file)
    wrong_sound.play()

# 캐릭터 정보 (이미지 경로)
characters = [
    {'name': '샤샤핑', 'image': os.path.join(img_dir, 'shasha.jpg')},
    {'name': '포실핑', 'image': os.path.join(img_dir, 'posiel.jpg')},
    {'name': '조아핑', 'image': os.path.join(img_dir, 'joah.jpg')},
    {'name': '하츄핑', 'image': os.path.join(img_dir, 'hachu.jpg')},
    {'name': '대용핑', 'image': os.path.join(img_dir, 'DY.jpg')},
    {'name': '사랑핑', 'image': os.path.join(img_dir, 'sarang.jpg')},
    {'name': '윤서핑', 'image': os.path.join(img_dir, 'YS.jpg')},
    {'name': '의훈핑', 'image': os.path.join(img_dir, 'UH.jpg')},
]

# 점수 및 오답 횟수 초기화
score = 0
incorrect_count = 0
current_character = None
question_count = 0
total_questions = 10  # 게임의 총 문제 수
time_limit = 30  # 제한 시간 (초)

# 타이머 변수
time_left = time_limit
timer_running = False

# 랜덤 캐릭터를 선택하는 함수
def get_random_character():
    return random.choice(characters)

# 이미지와 캐릭터 이름을 업데이트하는 함수
def update_image():
    global current_character, time_left, timer_running
    current_character = get_random_character()

    # 이미지 경로 확인
    img_path = current_character['image']
    if not os.path.exists(img_path):  # 이미지 파일이 존재하는지 확인
        print(f"이미지 파일 {img_path}이(가) 없습니다!")
        return

    img = Image.open(img_path)
    img = img.resize((300, 300))  # 크기 조정
    img = ImageTk.PhotoImage(img)

    # 라벨에 이미지 업데이트
    image_label.config(image=img)
    image_label.image = img  # 이미지 저장

    # 이름 입력 필드 초기화
    name_entry.delete(0, tk.END)

    # 정답/오답 메시지 초기화
    result_label.config(text="")
    answer_label.config(text="")  # answer_label 초기화

    # 타이머 초기화
    time_left = time_limit
    timer_running = True
    timer_label.config(text=f"남은 시간: {time_left}초")
    start_timer()

    # 정답 확인 버튼을 다시 활성화
    check_button.grid(row=2, column=0, columnspan=2, padx=20, pady=10)
    
    # "다음 문제" 버튼을 비활성화
    next_button.grid_forget()  # 버튼 숨기기

# 타이머를 시작하는 함수
def start_timer():
    global time_left, timer_running
    if time_left > 0 and timer_running:
        time_left -= 1
        timer_label.config(text=f"남은 시간: {time_left}초")
        root.after(1000, start_timer)  # 1초 후에 다시 호출
    elif time_left == 0:
        check_answer()  # 시간 초과 시 자동으로 정답 체크

# 점수를 업데이트하고, 이름을 맞췄는지 체크하는 함수
def check_answer():
    global score, incorrect_count, question_count, timer_running
    user_input = name_entry.get().strip()

    if user_input == current_character['name']:
        score += 1
        result_label.config(text=f"정답입니다! 현재 점수: {score}", fg="green")
        answer_label.config(text="")  # 정답일 때는 정답 안내 안함
        play_correct_sound()  # 정답 소리
    else:
        incorrect_count += 1
        result_label.config(text=f"오답입니다!", fg="red")
        answer_label.config(text=f"정답은 {current_character['name']}입니다.", fg="blue")  # 정답 표시
        play_wrong_sound()  # 오답 소리

    # 점수와 오답 횟수 갱신
    score_label.config(text=f"점수: {score}")
    incorrect_label.config(text=f"오답 횟수: {incorrect_count}")

    # 정답 확인 버튼 숨기기
    check_button.grid_forget()

    # "다음 문제" 버튼을 활성화
    next_button.grid(row=6, column=0, columnspan=2, padx=20, pady=10)

    # 문제 푼 횟수 증가
    question_count += 1

    # 게임 종료 체크
    if question_count >= total_questions:
        next_button.config(text="게임 종료", command=root.quit)

    # 타이머 멈추기
    timer_running = False

# "다음 문제" 버튼을 눌렀을 때
def next_question():
    if question_count < total_questions:
        update_image()

# 기본 창 설정
root = tk.Tk()
root.title("티니핑 맞추기")
root.geometry("600x600")

# 폰트 설정
font_style = ("Comic Sans MS", 14)

# 이미지 표시
image_label = tk.Label(root)
image_label.grid(row=0, column=0, columnspan=2, padx=20, pady=20)

# 이름 입력 필드
name_entry = tk.Entry(root, font=font_style)
name_entry.grid(row=1, column=0, columnspan=2, padx=20, pady=10)

# "정답 확인" 버튼
check_button = tk.Button(root, text="정답 확인", font=("Comic Sans MS", 16), command=check_answer, bg="#4CAF50", fg="white", relief="raised", width=20)
check_button.grid(row=2, column=0, columnspan=2, padx=20, pady=10)

# 점수 표시
score_label = tk.Label(root, text=f"점수: {score}", font=font_style)
score_label.grid(row=3, column=0, padx=20, pady=10)

# 오답 횟수 표시
incorrect_label = tk.Label(root, text=f"오답 횟수: {incorrect_count}", font=font_style)
incorrect_label.grid(row=3, column=1, padx=20, pady=10)

# 타이머 표시
timer_label = tk.Label(root, text=f"남은 시간: {time_limit}초", font=font_style)
timer_label.grid(row=4, column=0, columnspan=2, padx=20, pady=10)

# 정답/오답 메시지 라벨
result_label = tk.Label(root, text="", font=font_style)
result_label.grid(row=5, column=0, columnspan=2, padx=20, pady=10)

# 정답 표시 라벨 (오답일 때만 표시)
answer_label = tk.Label(root, text="", font=font_style, fg="blue")
answer_label.grid(row=6, column=0, columnspan=2, padx=20, pady=10)

# "다음 문제" 버튼 (기본적으로 비활성화)
next_button = tk.Button(root, text="다음 문제", font=font_style, command=next_question, bg="#2196F3", fg="white", relief="raised", width=20)
next_button.grid_forget()  # 처음에는 보이지 않도록 설정

# 처음 이미지 및 캐릭터 업데이트
update_image()

# 배경 음악 시작
play_bgm()

# 창 실행
root.mainloop()
