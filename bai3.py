import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
import numpy as np
import math


# Hàm kiểm tra điều kiện tam giác
def kiem_tra_tam_giac(a, b, c):
    return a + b > c and a + c > b and b + c > a


# Hàm tính và vẽ hình tròn
def ve_hinh_tron():
    try:
        r = float(entry_ban_kinh.get())
        if r <= 0:
            raise ValueError("Bán kính phải lớn hơn 0.")

        dien_tich = math.pi * r ** 2
        chu_vi = 2 * math.pi * r

        plt.figure()
        circle = plt.Circle((0, 0), r, color='blue', fill=True, alpha=0.5)
        plt.gca().add_artist(circle)
        plt.xlim(-r - 1, r + 1)
        plt.ylim(-r - 1, r + 1)
        plt.title(f"Hình tròn với bán kính {r}")
        plt.gca().set_aspect('equal')
        plt.show()

        messagebox.showinfo("Kết quả", f"Chu vi: {chu_vi:.2f}\nDiện tích: {dien_tich:.2f}")
    except ValueError as e:
        messagebox.showerror("Lỗi", f"Giá trị không hợp lệ: {e}")


# Hàm tính và vẽ tam giác
def ve_hinh_tam_giac():
    try:
        a = float(entry_canh_1.get())
        b = float(entry_canh_2.get())
        c = float(entry_canh_3.get())
        if a <= 0 or b <= 0 or c <= 0:
            raise ValueError("Các cạnh phải lớn hơn 0.")
        if not kiem_tra_tam_giac(a, b, c):
            raise ValueError("Các cạnh không tạo thành một tam giác.")

        s = (a + b + c) / 2
        dien_tich = math.sqrt(s * (s - a) * (s - b) * (s - c))
        chu_vi = a + b + c

        plt.figure()
        plt.plot([0, a, b], [0, 0, math.sqrt(c ** 2 - ((a - b) ** 2) / 4)], 'bo-')
        plt.fill([0, a, b], [0, 0, math.sqrt(c ** 2 - ((a - b) ** 2) / 4)], 'cyan', alpha=0.5)
        plt.title(f"Tam giác với các cạnh {a}, {b}, {c}")
        plt.gca().set_aspect('equal')
        plt.show()

        messagebox.showinfo("Kết quả", f"Chu vi: {chu_vi:.2f}\nDiện tích: {dien_tich:.2f}")
    except ValueError as e:
        messagebox.showerror("Lỗi", f"Giá trị không hợp lệ: {e}")


# Hàm tính và vẽ hình chữ nhật
def ve_hinh_chu_nhat():
    try:
        a = float(entry_canh_1.get())
        b = float(entry_canh_2.get())
        if a <= 0 or b <= 0:
            raise ValueError("Các cạnh phải lớn hơn 0.")

        dien_tich = a * b
        chu_vi = 2 * (a + b)

        plt.figure()
        plt.plot([0, a, a, 0, 0], [0, 0, b, b, 0], 'bo-')
        plt.fill([0, a, a, 0], [0, 0, b, b], 'cyan', alpha=0.5)
        plt.title(f"Hình chữ nhật với các cạnh {a} và {b}")
        plt.gca().set_aspect('equal')
        plt.show()

        messagebox.showinfo("Kết quả", f"Chu vi: {chu_vi:.2f}\nDiện tích: {dien_tich:.2f}")
    except ValueError as e:
        messagebox.showerror("Lỗi", f"Giá trị không hợp lệ: {e}")


# Hàm tính và vẽ hình trụ
def ve_hinh_tru():
    try:
        r = float(entry_ban_kinh.get())
        h = float(entry_canh_1.get())
        if r <= 0 or h <= 0:
            raise ValueError("Bán kính và chiều cao phải lớn hơn 0.")

        dien_tich_xung_quanh = 2 * math.pi * r * h
        dien_tich_toan_phan = dien_tich_xung_quanh + 2 * math.pi * r ** 2
        the_tich = math.pi * r ** 2 * h

        # Vẽ hình trụ 2D
        theta = np.linspace(0, 2 * np.pi, 100)
        x = r * np.cos(theta)
        y1 = r * np.sin(theta)
        y2 = y1 + h

        plt.figure()
        plt.plot(x, y1, 'b')  # Đáy dưới
        plt.plot(x, y2, 'b')  # Đáy trên
        for i in range(0, len(x), 10):
            plt.plot([x[i], x[i]], [y1[i], y2[i]], 'g--')  # Đường trụ
        plt.fill_between(x, y1, y2, color='cyan', alpha=0.3)
        plt.title(f"Hình trụ với bán kính {r} và chiều cao {h}")
        plt.gca().set_aspect('equal')
        plt.show()

        messagebox.showinfo("Kết quả", f"Diện tích xung quanh: {dien_tich_xung_quanh:.2f}\n"
                                       f"Diện tích toàn phần: {dien_tich_toan_phan:.2f}\n"
                                       f"Thể tích: {the_tich:.2f}")
    except ValueError as e:
        messagebox.showerror("Lỗi", f"Giá trị không hợp lệ: {e}")


# Hàm tính và vẽ hình nón
def ve_hinh_non():
    try:
        r = float(entry_ban_kinh.get())
        h = float(entry_canh_1.get())
        if r <= 0 or h <= 0:
            raise ValueError("Bán kính và chiều cao phải lớn hơn 0.")

        the_tich = (1/3) * math.pi * r ** 2 * h
        dien_tich_xung_quanh = math.pi * r * math.sqrt(r ** 2 + h ** 2)
        dien_tich_toan_phan = dien_tich_xung_quanh + math.pi * r ** 2

        # Vẽ hình nón
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')

        # Dữ liệu cho hình nón
        z = np.linspace(0, h, 100)
        x = r * (1 - z/h) * np.cos(np.linspace(0, 2 * np.pi, 100))
        y = r * (1 - z/h) * np.sin(np.linspace(0, 2 * np.pi, 100))

        # Vẽ nón
        ax.plot_surface(x, y, z[:, None], alpha=0.5, color='cyan')

        ax.set_title(f"Hình nón với bán kính {r} và chiều cao {h}")
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        plt.show()

        messagebox.showinfo("Kết quả", f"Diện tích xung quanh: {dien_tich_xung_quanh:.2f}\n"
                                       f"Diện tích toàn phần: {dien_tich_toan_phan:.2f}\n"
                                       f"Thể tích: {the_tich:.2f}")
    except ValueError as e:
        messagebox.showerror("Lỗi", f"Giá trị không hợp lệ: {e}")


# Hàm tính và vẽ hình lục giác
def ve_hinh_luc_giac():
    try:
        a = float(entry_canh_1.get())
        if a <= 0:
            raise ValueError("Cạnh phải lớn hơn 0.")

        dien_tich = (3 * math.sqrt(3) * a ** 2) / 2
        chu_vi = 6 * a

        plt.figure()
        hexagon = plt.Polygon([(a * np.cos(np.pi/3 * i), a * np.sin(np.pi/3 * i)) for i in range(6)], color='cyan', alpha=0.5)
        plt.gca().add_artist(hexagon)
        plt.xlim(-a - 1, a + 1)
        plt.ylim(-a - 1, a + 1)
        plt.title(f"Hình lục giác với cạnh {a}")
        plt.gca().set_aspect('equal')
        plt.show()

        messagebox.showinfo("Kết quả", f"Chu vi: {chu_vi:.2f}\nDiện tích: {dien_tich:.2f}")
    except ValueError as e:
        messagebox.showerror("Lỗi", f"Giá trị không hợp lệ: {e}")


# Hàm thay đổi giao diện khi chọn hình học
def chon_hinh():
    selected_shape = combo.get()
    selected_type = combo_type.get()

    if selected_type == "2D":
        if selected_shape == "Hình tròn":
            entry_ban_kinh.pack()
            entry_canh_1.pack_forget()
            entry_canh_2.pack_forget()
            entry_canh_3.pack_forget()
            button_ve_2d.config(command=ve_hinh_tron)
        elif selected_shape == "Tam giác":
            entry_ban_kinh.pack_forget()
            entry_canh_1.pack()
            entry_canh_2.pack()
            entry_canh_3.pack()
            button_ve_2d.config(command=ve_hinh_tam_giac)
        elif selected_shape == "Hình chữ nhật":
            entry_ban_kinh.pack_forget()
            entry_canh_1.pack()
            entry_canh_2.pack()
            entry_canh_3.pack_forget()
            button_ve_2d.config(command=ve_hinh_chu_nhat)
    elif selected_type == "3D":
        if selected_shape == "Hình trụ":
            entry_ban_kinh.pack()
            entry_canh_1.pack()
            entry_canh_2.pack_forget()
            entry_canh_3.pack_forget()
            button_ve_2d.config(command=ve_hinh_tru)
        elif selected_shape == "Hình nón":
            entry_ban_kinh.pack()
            entry_canh_1.pack()
            entry_canh_2.pack_forget()
            entry_canh_3.pack_forget()
            button_ve_2d.config(command=ve_hinh_non)
        elif selected_shape == "Hình lục giác":
            entry_ban_kinh.pack_forget()
            entry_canh_1.pack()
            entry_canh_2.pack_forget()
            entry_canh_3.pack_forget()
            button_ve_2d.config(command=ve_hinh_luc_giac)


def add_placeholder(entry, placeholder):
    entry.insert(0, placeholder)
    entry.config(fg="grey")
    entry.bind("<FocusIn>", lambda e: on_focus_in(entry, placeholder))
    entry.bind("<FocusOut>", lambda e: on_focus_out(entry, placeholder))


def on_focus_in(entry, placeholder):
    if entry.get() == placeholder:
        entry.delete(0, tk.END)
        entry.config(fg="black")


def on_focus_out(entry, placeholder):
    if entry.get() == "":
        entry.insert(0, placeholder)
        entry.config(fg="grey")


# Giao diện chính
root = tk.Tk()
root.title("Ứng dụng hỗ trợ học hình học")

frame = tk.Frame(root)
frame.pack(pady=10)

# Chọn loại hình học (2D hoặc 3D)
label_loai_hinh = tk.Label(frame, text="Chọn loại hình học:")
label_loai_hinh.grid(row=0, column=0, padx=10, pady=5)

combo_type = ttk.Combobox(frame, values=["2D", "3D"], state="readonly")
combo_type.grid(row=0, column=1, padx=10, pady=5)
combo_type.bind("<<ComboboxSelected>>", lambda e: chon_hinh())

# Chọn hình học
label_chon = tk.Label(frame, text="Chọn hình:")
label_chon.grid(row=1, column=0, padx=10, pady=5)

combo = ttk.Combobox(frame, values=["Hình tròn", "Tam giác", "Hình chữ nhật", "Hình trụ", "Hình nón", "Hình lục giác"], state="readonly")
combo.grid(row=1, column=1, padx=10, pady=5)
combo.bind("<<ComboboxSelected>>", lambda e: chon_hinh())

# Nhập bán kính cho hình tròn và hình trụ
entry_ban_kinh = tk.Entry(root)
entry_ban_kinh.pack(pady=5)
add_placeholder(entry_ban_kinh, "Nhập bán kính (cho hình tròn/hình trụ)")

# Nhập cạnh hoặc chiều cao cho các hình
entry_canh_1 = tk.Entry(root)
entry_canh_1.pack(pady=5)
add_placeholder(entry_canh_1, "Nhập cạnh 1 hoặc chiều cao")

entry_canh_2 = tk.Entry(root)
entry_canh_2.pack(pady=5)
add_placeholder(entry_canh_2, "Nhập cạnh 2")

entry_canh_3 = tk.Entry(root)
entry_canh_3.pack(pady=5)
add_placeholder(entry_canh_3, "Nhập cạnh 3")

# Nút để vẽ hình
button_ve_2d = tk.Button(root, text="Vẽ và Tính")
button_ve_2d.pack(pady=10)

root.mainloop()
