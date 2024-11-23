import pygame
import random

# Khởi tạo Pygame
pygame.init()

# Kích thước cửa sổ
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Game Bắn Chim')

# Màu sắc
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
pygame.mixer.music.load('background.mp3')  # Tải file nhạc nền
pygame.mixer.music.play(-1)  # Phát nhạc nền liên tục (-1 là phát lại liên tục)

# Tải hình ảnh
background = pygame.image.load('img_2.png')  # Hình nền cho trò chơi chính
menu_background = pygame.image.load('img_8.png')  # Hình nền cho màn hình menu
menu_background = pygame.transform.scale(menu_background, (width, height))  # Thay đổi kích thước hình nền menu cho vừa với màn hình

bird_image = pygame.image.load('img_10.png')
bird_image = pygame.transform.scale(bird_image, (50, 50))  # Thay đổi kích thước hình ảnh chim
gun_image = pygame.image.load('img_7.png')
gun_image = pygame.transform.scale(gun_image, (100, 100))  # Thay đổi kích thước hình ảnh khẩu súng
bullet_image = pygame.image.load('img_6.png')  # Tải hình ảnh viên đạn
bullet_image = pygame.transform.scale(bullet_image, (10, 10))  # Thay đổi kích thước viên đạn
hit_sound = pygame.mixer.Sound('shoot - Copy.wav')  # Tải âm thanh bắn trúng
shoot_sound = pygame.mixer.Sound('shoot - Copy.wav')  # Tải âm thanh bắn

# Đối tượng chim
class Bird:
    def __init__(self):
        self.x = random.randint(0, width - 50)
        self.y = random.randint(0, height // 4)  # Bắt đầu từ trên cao
        self.speed_x = random.choice([-3, -2, 2, 3])  # Tốc độ di chuyển theo chiều ngang
        self.speed_y = random.choice([1, 2])  # Tốc độ di chuyển theo chiều dọc
        self.is_alive = True  # Biến trạng thái sống

    def move(self):
        # Di chuyển chim
        self.x += self.speed_x
        self.y += self.speed_y

        # Đổi hướng nếu chim va chạm với biên
        if self.x <= 0 or self.x >= width - 50:
            self.speed_x *= -1  # Đảo chiều ngang
        if self.y >= height or self.y <= 0:
            self.speed_y *= -1  # Đảo chiều dọc

    def draw(self):
        if self.is_alive:  # Vẽ chim chỉ khi nó còn sống
            screen.blit(bird_image, (self.x, self.y))

# Đối tượng viên đạn
class Bullet:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = -10  # Tốc độ viên đạn

    def move(self):
        self.y += self.speed  # Di chuyển viên đạn lên trên

    def draw(self):
        screen.blit(bullet_image, (self.x, self.y))  # Vẽ viên đạn

# Khởi tạo danh sách chim và viên đạn
birds = [Bird() for _ in range(5)]
bullets = []  # Danh sách viên đạn

# Điểm số
score = 0
font = pygame.font.Font(None, 36)  # Sử dụng font mặc định

# Thay đổi hình ảnh con trỏ chuột thành khẩu súng
pygame.mouse.set_visible(False)  # Ẩn con trỏ chuột mặc định

# Hàm hiển thị menu chính với nút "Bắt đầu"
# Hàm vẽ nút bo tròn
def draw_rounded_button(surface, rect, color, radius):
    pygame.draw.rect(surface, color, rect, border_radius=radius)

# Hàm hiển thị menu chính với nút "Start" đẹp hơn
def show_main_menu():
    pygame.mouse.set_visible(True)  # Hiển thị con trỏ chuột khi ở menu
    menu_running = True
    while menu_running:
        screen.blit(menu_background, (0, 0))  # Vẽ hình nền menu

        # Vẽ nút bắt đầu với các góc bo tròn
        start_button_rect = pygame.Rect(width // 2 - 100, height // 2 - 50, 200, 60)
        draw_rounded_button(screen, start_button_rect, (0, 128, 255), 20)  # Nút xanh với bo góc

        # Hiệu ứng thay đổi màu khi rê chuột
        mouse_pos = pygame.mouse.get_pos()
        if start_button_rect.collidepoint(mouse_pos):
            draw_rounded_button(screen, start_button_rect, (0, 180, 255), 20)  # Đổi màu khi rê chuột

        # Vẽ chữ "Start" ở giữa nút
        start_text = font.render("Start", True, WHITE)
        screen.blit(start_text, (start_button_rect.centerx - start_text.get_width() // 2,
                                 start_button_rect.centery - start_text.get_height() // 2))

        # Xử lý sự kiện
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if start_button_rect.collidepoint(event.pos):  # Kiểm tra xem nút có được nhấn không
                    menu_running = False  # Thoát khỏi vòng lặp để bắt đầu trò chơi

        pygame.display.flip()


# Vòng lặp chính
def game_loop():
    global score, birds, bullets
    pygame.mouse.set_visible(False)  # Ẩn con trỏ chuột khi vào trò chơi
    running = True
    while running:
        screen.blit(background, (0, 0))  # Vẽ nền

        # Lấy vị trí chuột
        mouse_x, mouse_y = pygame.mouse.get_pos()

        # Vẽ khẩu súng theo vị trí chuột, căn giữa tại đáy màn hình
        gun_x = mouse_x - gun_image.get_width() // 2
        gun_y = height - gun_image.get_height() + 20  # Vị trí ở đáy màn hình với chút khoảng cách
        screen.blit(gun_image, (gun_x, gun_y))

        # Vẽ hồng tâm
        crosshair_size = 20  # Kích thước của hồng tâm
        pygame.draw.line(screen, RED, (mouse_x, mouse_y - crosshair_size), (mouse_x, mouse_y + crosshair_size), 2)  # Đường thẳng đứng
        pygame.draw.line(screen, RED, (mouse_x - crosshair_size, mouse_y), (mouse_x + crosshair_size, mouse_y), 2)  # Đường thẳng ngang

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Bắn viên đạn khi nhấn chuột
                bullet = Bullet(mouse_x, height - gun_image.get_height() + 20)  # Tạo viên đạn ở vị trí dưới khẩu súng
                bullets.append(bullet)
                shoot_sound.play()  # Phát âm thanh bắn

        # Di chuyển và vẽ viên đạn
        for bullet in bullets[:]:
            bullet.move()
            bullet.draw()

        # Di chuyển và vẽ chim
        for bird in birds:
            bird.move()
            bird.draw()

        # Kiểm tra va chạm giữa viên đạn và chim
        bullets_to_remove = []  # Danh sách viên đạn cần xóa
        for bullet in bullets:
            for bird in birds:
                if bird.x < bullet.x < bird.x + 50 and bird.y < bullet.y < bird.y + 50 and bird.is_alive:
                    bird.is_alive = False  # Đánh dấu chim đã bị bắn
                    bullets_to_remove.append(bullet)  # Thêm viên đạn cần xóa vào danh sách
                    hit_sound.play()  # Phát âm thanh bắn trúng
                    birds.append(Bird())  # Thêm chim mới
                    score += 1  # Tăng điểm khi bắn trúng

        # Xóa viên đạn trong danh sách
        for bullet in bullets_to_remove:
            if bullet in bullets:  # Kiểm tra xem viên đạn có trong danh sách hay không
                bullets.remove(bullet)

        # Hiển thị điểm số
        score_text = font.render(f'Score: {score}', True, BLACK)
        screen.blit(score_text, (10, 10))

        pygame.display.flip()
        pygame.time.delay(30)

# Chạy màn hình chính trước khi vào game
show_main_menu()
game_loop()

pygame.quit()
