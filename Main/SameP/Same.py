import turtle as t
import random
import time
import os
import pygame  # pygame 추가

# 이미지 경로 설정 (현재 스크립트 위치 기준)
base_path = os.path.dirname(__file__)  # 현재 파일 위치
image_folder = os.path.join(base_path, 'images')  # 'images' 폴더 경로
sound_folder = os.path.join(base_path, 'sounds')  # 'sounds' 폴더 경로

# 이미지 파일 경로 설정
default_img = os.path.join(image_folder, 'default_img.gif')
t.addshape(default_img)

img_list = []
for i in range(8):
    img = os.path.join(image_folder, f'img{i}.gif')  # 동적으로 경로 생성
    t.addshape(img)
    img_list.append(img)
    img_list.append(img)  # 각 이미지를 두 번 추가하여 매칭 게임을 만듦

# 게임 진행을 위한 함수들
def find_card(x, y):
    min_idx = 0
    min_dis = 100

    for i in range(16):
        distance = turtles[i].distance(x, y)
        if distance < min_dis:
            min_dis = distance
            min_idx = i
    return min_idx

def score_update(m):
    score_pen.clear()
    score_pen.write(f"{m}   {score}점/{attempt}번 시도", False, "center", ("", 15))

def result(m):
    t.goto(0, -60)
    t.write(m, False, "center", ("", 30, "bold"))

def play(x, y):
    global click_num
    global first_pick
    global second_pick
    global attempt
    global score

    # 카드 클릭 시마다 사운드 재생
    pygame.mixer.Sound(os.path.join(sound_folder, "click_sound.wav")).play()

    if attempt == 12:
        # 게임 오버 시 모든 사운드 멈추고 Lose 사운드 재생
        pygame.mixer.stop()  # 모든 사운드 멈추기
        pygame.mixer.Sound(os.path.join(sound_folder, "lose_sound.wav")).play()  # Lose 사운드 재생
        result("Game Over")
    else:
        click_num += 1
        card_idx = find_card(x, y)
        turtles[card_idx].shape(img_list[card_idx])

        if click_num == 1:
            first_pick = card_idx
        elif click_num == 2:
            second_pick = card_idx
            click_num = 0
            attempt += 1

            if img_list[first_pick] == img_list[second_pick]:
                score += 1
                score_update("정답")
                if score == 8:
                    # 게임 승리 시 Win 사운드 재생
                    pygame.mixer.stop()  # 게임 승리 후 이전 사운드 멈추기
                    pygame.mixer.Sound(os.path.join(sound_folder, "win_sound.wav")).play()  # Win 사운드 재생
                    result("WIN!!")
            else:
                score_update("오답")
                turtles[first_pick].shape(default_img)
                turtles[second_pick].shape(default_img)

# 초기 설정
t.bgcolor('pink')
t.setup(700, 700)
t.up()
t.ht()
t.goto(0, 280)
t.write('기억력 대박핑', False, "center", ("", 30, "bold"))

# 점수 펜 객체 생성
score_pen = t.Turtle()
score_pen.up()
score_pen.ht()
score_pen.goto(0, 230)

# 터틀 객체 생성
turtles = []
pos_x = [-210, -70, 70, 210]
pos_y = [-250, -110, 30, 170]

#이중 for 문
for x in range(4):
    for y in range(4):
        new_turtle = t.Turtle()
        new_turtle.up()
        new_turtle.color("pink")
        new_turtle.speed(0)
        new_turtle.goto(pos_x[x], pos_y[y])
        turtles.append(new_turtle)

# 이미지 섞기
random.shuffle(img_list)

# 터틀에 이미지 설정(16마리)
for i in range(16):
    turtles[i].shape(img_list[i])

# 3초 후에 디폴트 이미지로 변경
time.sleep(3)
for i in range(16):
    turtles[i].shape(default_img)

# 게임 시작 사운드 재생 (3초 지연 후)   
pygame.mixer.init()  # pygame의 mixer 초기화
pygame.mixer.Sound(os.path.join(sound_folder, "start_sound.wav")).play()  # 게임 시작 시 사운드 재생

click_num = 0       # 클릭횟수
score = 0           # 점수
attempt = 0         # 시도한 횟수
first_pick = ""
second_pick = ""

t.onscreenclick(play)

t.done()