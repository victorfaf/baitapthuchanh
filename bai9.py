import cv2
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

# Khởi tạo cửa sổ chính
root = tk.Tk()
root.title("Ứng dụng Tách Biên Ảnh")
root.geometry("800x600")

# Biến toàn cục để lưu ảnh gốc
img_original = None


# Chọn ảnh
def open_image():
    file_path = filedialog.askopenfilename()
    if file_path:
        global img_original
        img_original = cv2.imread(file_path)

        # Thay đổi kích thước ảnh về 512x512
        img_resized = cv2.resize(img_original, (512, 512))
        show_image(img_resized)


# Hiển thị ảnh trên giao diện
def show_image(img):
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img_pil = Image.fromarray(img_rgb)
    img_tk = ImageTk.PhotoImage(image=img_pil)
    lbl_img.config(image=img_tk)
    lbl_img.image = img_tk


# Áp dụng thuật toán tách biên Canny
def apply_edge_detection():
    if img_original is not None:
        # Thay đổi kích thước ảnh về 512x512
        img_resized = cv2.resize(img_original, (512, 512))

        # Chuyển đổi ảnh sang xám
        gray = cv2.cvtColor(img_resized, cv2.COLOR_BGR2GRAY)

        # Áp dụng bộ lọc Canny
        edges = cv2.Canny(gray, 100, 200)  # Tham số 100 và 200 là ngưỡng dưới và trên

        # Hiển thị ảnh tách biên
        show_image(edges)


# Khung hiển thị ảnh
lbl_img = tk.Label(root)
lbl_img.pack()

# Nút chọn ảnh
btn_open = tk.Button(root, text="Chọn Ảnh", command=open_image)
btn_open.pack()

# Nút áp dụng tách biên
btn_edge = tk.Button(root, text="Tách Biên", command=apply_edge_detection)
btn_edge.pack()

root.mainloop()
