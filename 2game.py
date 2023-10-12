import pygame as pg
import time, random

Width = 800
Height = 600

Paddle_Height = 100
Paddle_Width = 10
Paddle2_Speed = 10
Paddle1_Speed = 10
Ball_X = 75
Ball_Y = 75
Ball_R = 10
Ball_SpeedX = -6
Ball_SpeedY = -8
Paddle1_Score = 0
Paddle2_Score = 0
Paddle1_Y = 250
Paddle2_Y = 250
Paddle1_Size = 120
Paddle2_Size = 120
P1y = 150

'''
화면에 오브젝트를 그리는 함수
Screen.fill() 또는 pg.draw.rect(), pg.draw.circle() 등을 사용하여 화면에 오브젝트들을 그린다.
'''
def Draw_Ball():
    pg.draw.circle(Screen, (255, 255 ,255), (Ball_X, Ball_Y), Ball_R)

def Draw_Paddle1():
    pg.draw.rect(Screen, (255, 255 ,255), (790, Paddle1_Y, 10, Paddle1_Size)) 

def Draw_Paddle2():
    pg.draw.rect(Screen, (255, 255 ,255), (0, Paddle2_Y, 10, Paddle2_Size))

def Draw_Net():
    global Net_Y
    Net_Y = 0
    for m in range(12):
        pg.draw.rect(Screen, (255, 255, 255), (395, Net_Y, 10, 40))
        Net_Y += 50

def Draw_Score():
    Screen.blit(P1Score_txt, (455, 25))
    Screen.blit(P2Score_txt, (320, 25))
'''
오브젝트의 이동을 연산하는 함수
볼의 이동, 패들이동, 충돌체크 등을 처리함.
'''
def Calc_Ball():
    global Ball_X, Ball_Y, Ball_SpeedX, Ball_SpeedY
    Ball_X += Ball_SpeedX
    Ball_Y += Ball_SpeedY
    if Ball_Y >= Height - Ball_R:
        Ball_SpeedY *= -1
    if Ball_Y <= 0 + Ball_R:
        Ball_SpeedY *= -1
    if Paddle2_Y <= Ball_Y:
        if Paddle2_Y + Paddle2_Size >= Ball_Y:
            if Ball_X <= 10:
                Ball_SpeedX *= -1
    if Paddle1_Y <= Ball_Y:
        if Paddle1_Y + Paddle1_Size >= Ball_Y:
            if Ball_X >= 790:
                Ball_SpeedX *= -1

def Calc_Paddle2():
    global Paddle2_Y, Paddle1_Score, P1y
    Paddle2_Y = P1y
    if Paddle2_Y >= Height - Paddle2_Size:
        P1y = Height - Paddle2_Size
        Paddle2_Y = Height - Paddle2_Size
    if Paddle2_Y <= 0:
        P1y = 0
        Paddle2_Y = 0
    if Ball_X <= 0:
        Reset_Ball()
        Paddle1_Score += 1

def Calc_Paddle1():
    global Paddle1_Y
    global Paddle2_Score
    Paddle1_Y = Ball_Y -40
    if Ball_X >= 800:
        Reset_Ball()
        Paddle2_Score += 1

def read_input_file(file_name):
    with open(file_name, 'r') as file:
        return file.read().strip()

def clear_input_file(file_name):
    with open(file_name, 'w') as file:
        file.write('')

input_file = 'input.txt'
clear_input_file(input_file)

'''
게임시작할 때, 새로운 세트를 시작할 때 볼의 초기화를 처리함.
'''
def Reset_Ball():
    global Ball_X, Ball_Y
    Ball_X = Width/2
    Ball_Y = random.randint(200, 400)

pg.init()
pg.display.set_caption("나의 게임")
pg.key.set_repeat(1, 5)
Screen = pg.display.set_mode((Width, Height))
Font_Paddle1Score = pg.font.Font("font/NanumGothic.ttf", 40)
Font_Paddle2Score = pg.font.Font("font/NanumGothic.ttf", 40)
Font_Event1ch = pg.font.Font("font/NanumGothic.ttf", 40)
Font_Event2ch = pg.font.Font("font/NanumGothic.ttf", 40)
Font_Event3ch = pg.font.Font("font/NanumGothic.ttf", 40)
Font_key1 = pg.font.Font("font/NanumGothic.ttf", 60)
Font_key2 = pg.font.Font("font/NanumGothic.ttf", 60)

Running = True
# 메인 게임 루프
Reset_Ball()
while Running:
    up = False
    down = False
    # 키보드/마우스 이벤트 처리
    for event in pg.event.get():
        if event.type == pg.QUIT:
            Running = False
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_q:
                Running = False
            elif event.key == pg.K_w:
                up = True
                P1y -= 1
            elif event.key == pg.K_s:
                down = True
                P1y += 1           
    input_command = read_input_file(input_file)
    if input_command == 'w':
        up = True
        P1y -= 60
    if input_command == 's':
        down = True
        P1y += 60
    clear_input_file(input_file)


    P1Score_txt = Font_Paddle1Score.render(str(Paddle1_Score), True, (255, 255, 0))
    P2Score_txt = Font_Paddle1Score.render(str(Paddle2_Score), True, (255, 255, 0))
    Font_Event1 = Font_Event1ch.render("Double Speed!", True, (255, 255, 0))
    Font_Event2 = Font_Event2ch.render("Double Speed!", True, (255, 255, 0))
    Font_Event3 = Font_Event3ch.render("Double Speed!", True, (255, 255, 0))
    up_txt = Font_key1.render("W", True, (255, 255, 0))
    down_txt = Font_key2.render("S", True, (255, 255, 0))
    # 백그라운드 그리기
    Screen.fill( (0,0,0))
    Draw_Net()
    # 오브젝트 그리기

    Draw_Paddle1()
    Draw_Paddle2()
    Draw_Score()
    Draw_Ball()
    
    # 오브젝트 계산
    Calc_Paddle1()
    Calc_Paddle2()
    Calc_Ball()
    if up == True:
        Screen.blit(up_txt, (70, 50))
    if down == True:
        Screen.blit(down_txt, (70, 100))

    # 최종 화면 갱신&타이밍
    pg.display.update()
    time.sleep(0.03)
pg.quit()