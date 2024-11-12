import cv2
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

# Khởi tạo cửa sổ chính
root = tk.Tk()
root.title("Ứng dụng Lọc & Làm Mịn Ảnh")
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


# Áp dụng bộ lọc làm mịn Bilateral
def apply_smoothing():
    if img_original is not None:
        # Thay đổi kích thước ảnh về 512x512 nếu chưa làm mịn
        img_resized = cv2.resize(img_original, (512, 512))

        # Áp dụng bộ lọc Bilateral để làm mịn ảnh
        img_smoothed = cv2.bilateralFilter(img_resized, d=9, sigmaColor=75, sigmaSpace=75)
        show_image(img_smoothed)


# Khung hiển thị ảnh
lbl_img = tk.Label(root)
lbl_img.pack()

# Nút chọn ảnh
btn_open = tk.Button(root, text="Chọn Ảnh", command=open_image)
btn_open.pack()

# Nút áp dụng bộ lọc làm mịn
btn_smooth = tk.Button(root, text="Áp dụng Làm Mịn", command=apply_smoothing)
btn_smooth.pack()

root.mainloop()
