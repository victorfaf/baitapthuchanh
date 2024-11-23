import pygame, sys
from pygame.locals import *
import random
import time

WINDOWWIDTH = 800
WINDOWHEIGHT = 500
pygame.init()

# Tạo cửa sổ game
w = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
pygame.mixer.music.load('background.mp3')  # Tải file nhạc nền
pygame.mixer.music.play(-1)  # Phát nhạc nền liên tục (-1 là phát lại liên tục)
# Load hình ảnh
BG = pygame.image.load('img_13.png')  # Ảnh nền của trò chơi
BG = pygame.transform.scale(BG, (WINDOWWIDTH, WINDOWHEIGHT))  # Điều chỉnh kích thước ảnh nền
menu_BG = pygame.image.load('img_13.png')  # Ảnh nền của menu chính
menu_BG = pygame.transform.scale(menu_BG, (WINDOWWIDTH, WINDOWHEIGHT))  # Điều chỉnh kích thước ảnh nền menu

tao = pygame.image.load('tao1.png')
tao = pygame.transform.scale(tao, (40, 50))
cam = pygame.image.load('cam1.png')
cam = pygame.transform.scale(cam, (40, 50))
xoai = pygame.image.load('xoai.png')
xoai = pygame.transform.scale(xoai, (40, 50))
dua = pygame.image.load('dua.png')
dua = pygame.transform.scale(dua, (40, 50))
chuoi = pygame.image.load('chuoi.png')
chuoi = pygame.transform.scale(chuoi, (40, 50))


# Thay đổi con trỏ chuột bằng hình ảnh con mèo
meo = pygame.image.load('cat.png')  # Tải ảnh con mèo
meo = pygame.transform.scale(meo, (50, 50))  # Điều chỉnh kích thước của con mèo

meo1 = pygame.image.load('cat_close_mouth.png')  # Tải ảnh con mèo
meo1 = pygame.transform.scale(meo1, (50, 50))  # Điều chỉnh kích thước của con mèo
meo2 = meo
FPS = 20
fpsClock = pygame.time.Clock()

# Màu sắc
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Biến lưu điểm số
diem = 0

# Hàm tạo nút
def draw_button(text, font, color, rect, surface):
    pygame.draw.rect(surface, color, rect)
    text_surface = font.render(text, True, WHITE)
    surface.blit(text_surface, (
    rect[0] + (rect[2] - text_surface.get_width()) // 2, rect[1] + (rect[3] - text_surface.get_height()) // 2))


# Hàm hiển thị giao diện chính
def main_menu():
    menu = True
    font = pygame.font.SysFont('Arial', 50)
    button_rect = pygame.Rect(WINDOWWIDTH // 2 - 100, WINDOWHEIGHT // 2 - 50, 200, 100)

    while menu:
        w.blit(menu_BG, (0, 0))  # Hiển thị ảnh nền của menu chính
        draw_button('START', font, RED, button_rect, w)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    menu = False

        pygame.display.update()
        fpsClock.tick(FPS)


# Hàm khởi tạo vị trí và tốc độ ngẫu nhiên cho quả
def init_fruit(fruit_image):
    x_pos = random.randint(50, WINDOWWIDTH - 50)
    y_pos = random.randint(-100, -50)
    speed = random.randint(5, 20)
    return {"image": fruit_image, "x": x_pos, "y": y_pos, "speed": speed}

# Khởi tạo danh sách các quả
fruits = [init_fruit(tao), init_fruit(cam), init_fruit(xoai),init_fruit(dua),init_fruit(chuoi)]

# Hàm chính để chạy trò chơi
def game():
    global diem, meo2
    time0 = time.time()

    # Ẩn con trỏ chuột mặc định
    pygame.mouse.set_visible(False)

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                meo2 = meo1
                for fruit in fruits:
                    if event.pos[0] > fruit["x"] - 20 and event.pos[0] < fruit["x"] + 60 and event.pos[1] > fruit["y"] - 50 and event.pos[1] < fruit["y"] + 50:
                        if fruit["image"] == tao:
                            diem += 5
                        elif fruit["image"] == cam:
                            diem += 3
                        elif fruit["image"] == xoai:
                            diem += 2
                        elif fruit["image"] == dua:
                            diem += 6
                        elif fruit["image"] == chuoi:
                            diem += 1
                        fruit["y"] = random.randint(-100, -50)
                        fruit["x"] = random.randint(50, WINDOWWIDTH - 50)
            if event.type == pygame.MOUSEBUTTONUP:
                meo2 = meo

        w.blit(BG, (0, 0))  # Hiển thị ảnh nền của trò chơi

        # Di chuyển và vẽ các quả
        for fruit in fruits:
            fruit["y"] += fruit["speed"]
            w.blit(fruit["image"], (fruit["x"], fruit["y"]))
            if fruit["y"] > WINDOWHEIGHT:
                fruit["y"] = random.randint(-100, -50)
                fruit["x"] = random.randint(50, WINDOWWIDTH - 50)

        # Lấy vị trí của chuột và vẽ hình ảnh con mèo tại đó
        mouse_pos = pygame.mouse.get_pos()
        w.blit(meo2, (mouse_pos[0] - 25, mouse_pos[1] - 25))  # Vẽ hình con mèo tại vị trí chuột

        time1 = time.time()
        font = pygame.font.SysFont('Arial', 30)
        text = font.render('Score: {}'.format(diem), True, RED)
        text1 = font.render('Time: {}'.format(int(time1 - time0)), True, RED)
        w.blit(text, (50, 50))
        w.blit(text1, (50, 80))

        pygame.display.update()
        fpsClock.tick(FPS)


# Chạy chương trình
main_menu()  # Hiển thị menu chính trước
game()  # Sau khi nhấn nút START, trò chơi bắt đầu
