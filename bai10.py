import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk
import threading


class ImageEditorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Ứng dụng Xử Lý Ảnh Chuyên Nghiệp")
        self.root.geometry("1000x700")

        # Biến lưu trữ ảnh gốc và ảnh đã xử lý
        self.img_original = None
        self.img_display = None

        # Tạo thanh menu
        self.create_menu()

        # Tạo thanh công cụ
        self.create_toolbar()

        # Tạo khung hiển thị ảnh với thanh cuộn
        self.create_image_display()

        # Tạo thanh trạng thái
        self.status = tk.StringVar()
        self.status.set("Sẵn sàng")
        self.create_status_bar()

    def create_menu(self):
        menubar = tk.Menu(self.root)

        # Menu File
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Mở Ảnh", command=self.open_image)
        file_menu.add_command(label="Lưu Ảnh", command=self.save_image)
        file_menu.add_separator()
        file_menu.add_command(label="Thoát", command=self.root.quit)
        menubar.add_cascade(label="File", menu=file_menu)

        # Menu Edit
        edit_menu = tk.Menu(menubar, tearoff=0)
        edit_menu.add_command(label="Làm Mịn Ảnh", command=self.apply_smoothing)
        edit_menu.add_command(label="Tách Biên", command=self.apply_edge_detection)
        edit_menu.add_command(label="Tăng Cường Ánh Sáng", command=self.enhance_image)
        menubar.add_cascade(label="Chỉnh Sửa", menu=edit_menu)

        # Menu Help
        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="Giới Thiệu", command=self.show_about)
        menubar.add_cascade(label="Trợ Giúp", menu=help_menu)

        self.root.config(menu=menubar)

    def create_toolbar(self):
        toolbar = ttk.Frame(self.root, relief=tk.RAISED, padding=2)

        btn_open = ttk.Button(toolbar, text="Mở Ảnh", command=self.open_image)
        btn_open.pack(side=tk.LEFT, padx=2, pady=2)

        btn_save = ttk.Button(toolbar, text="Lưu Ảnh", command=self.save_image)
        btn_save.pack(side=tk.LEFT, padx=2, pady=2)

        btn_smooth = ttk.Button(toolbar, text="Làm Mịn", command=self.apply_smoothing)
        btn_smooth.pack(side=tk.LEFT, padx=2, pady=2)

        btn_edge = ttk.Button(toolbar, text="Tách Biên", command=self.apply_edge_detection)
        btn_edge.pack(side=tk.LEFT, padx=2, pady=2)

        btn_enhance = ttk.Button(toolbar, text="Tăng Ánh Sáng", command=self.enhance_image)
        btn_enhance.pack(side=tk.LEFT, padx=2, pady=2)

        toolbar.pack(side=tk.TOP, fill=tk.X)

    def create_image_display(self):
        self.canvas = tk.Canvas(self.root, bg='gray')
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Thêm thanh cuộn
        self.scrollbar_y = tk.Scrollbar(self.canvas, orient=tk.VERTICAL, command=self.canvas.yview)
        self.scrollbar_x = tk.Scrollbar(self.canvas, orient=tk.HORIZONTAL, command=self.canvas.xview)
        self.canvas.configure(yscrollcommand=self.scrollbar_y.set, xscrollcommand=self.scrollbar_x.set)
        self.scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
        self.scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)

        self.image_container = ttk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.image_container, anchor='nw')
        self.image_container.bind("<Configure>", self.on_frame_configure)

    def create_status_bar(self):
        status_bar = ttk.Label(self.root, textvariable=self.status, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def on_frame_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def open_image(self):
        file_path = filedialog.askopenfilename(
            title="Chọn Ảnh",
            filetypes=[("Image Files", "*.png *.jpg *.jpeg *.bmp *.tiff")]
        )
        if file_path:
            try:
                self.status.set("Đang tải ảnh...")
                self.root.update_idletasks()
                self.img_original = cv2.imread(file_path)
                if self.img_original is None:
                    raise ValueError("Không thể tải ảnh. Vui lòng kiểm tra định dạng và đường dẫn.")
                self.img_display = self.resize_image(self.img_original, (512, 512))
                self.show_image(self.img_display)
                self.status.set("Ảnh đã được tải thành công.")
            except Exception as e:
                messagebox.showerror("Lỗi", str(e))
                self.status.set("Lỗi khi tải ảnh.")

    def save_image(self):
        if self.img_display is None:
            messagebox.showwarning("Cảnh Báo", "Không có ảnh nào để lưu.")
            return
        file_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG", "*.png"), ("JPEG", "*.jpg *.jpeg"), ("BMP", "*.bmp"), ("TIFF", "*.tiff")],
            title="Lưu Ảnh"
        )
        if file_path:
            try:
                # Chuyển đổi từ RGB sang BGR trước khi lưu
                img_to_save = cv2.cvtColor(self.img_display, cv2.COLOR_RGB2BGR)
                cv2.imwrite(file_path, img_to_save)
                messagebox.showinfo("Thành Công", f"Ảnh đã được lưu tại {file_path}")
                self.status.set(f"Ảnh đã được lưu tại {file_path}")
            except Exception as e:
                messagebox.showerror("Lỗi", f"Không thể lưu ảnh: {e}")
                self.status.set("Lỗi khi lưu ảnh.")

    def show_image(self, img):
        # Loại bỏ các widget cũ
        for widget in self.image_container.winfo_children():
            widget.destroy()

        img_pil = Image.fromarray(img)
        self.photo = ImageTk.PhotoImage(image=img_pil)
        lbl_img = ttk.Label(self.image_container, image=self.photo)
        lbl_img.pack()

    def resize_image(self, img, size):
        return cv2.resize(img, size, interpolation=cv2.INTER_AREA)

    def apply_smoothing(self):
        if self.img_original is None:
            messagebox.showwarning("Cảnh Báo", "Vui lòng mở một ảnh trước.")
            return
        threading.Thread(target=self._apply_smoothing).start()

    def _apply_smoothing(self):
        try:
            self.status.set("Đang làm mịn ảnh...")
            self.root.update_idletasks()
            img = cv2.resize(self.img_original, (512, 512))
            img_smoothed = cv2.bilateralFilter(img, d=9, sigmaColor=75, sigmaSpace=75)
            img_smoothed = cv2.cvtColor(img_smoothed, cv2.COLOR_BGR2RGB)
            self.img_display = img_smoothed
            self.show_image(self.img_display)
            self.status.set("Làm mịn ảnh thành công.")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể làm mịn ảnh: {e}")
            self.status.set("Lỗi khi làm mịn ảnh.")

    def apply_edge_detection(self):
        if self.img_original is None:
            messagebox.showwarning("Cảnh Báo", "Vui lòng mở một ảnh trước.")
            return
        threading.Thread(target=self._apply_edge_detection).start()

    def _apply_edge_detection(self):
        try:
            self.status.set("Đang tách biên ảnh...")
            self.root.update_idletasks()
            img = cv2.resize(self.img_original, (512, 512))
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            edges = cv2.Canny(gray, 100, 200)
            edges_rgb = cv2.cvtColor(edges, cv2.COLOR_GRAY2RGB)
            self.img_display = edges_rgb
            self.show_image(self.img_display)
            self.status.set("Tách biên ảnh thành công.")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể tách biên ảnh: {e}")
            self.status.set("Lỗi khi tách biên ảnh.")

    def enhance_image(self):
        if self.img_original is None:
            messagebox.showwarning("Cảnh Báo", "Vui lòng mở một ảnh trước.")
            return
        threading.Thread(target=self._enhance_image).start()

    def _enhance_image(self):
        try:
            self.status.set("Đang tăng cường chất lượng ảnh...")
            self.root.update_idletasks()
            img = cv2.resize(self.img_original, (512, 512))

            # Chuyển đổi ảnh sang không gian màu YUV và cân bằng histogram cho kênh Y
            img_yuv = cv2.cvtColor(img, cv2.COLOR_BGR2YUV)
            img_yuv[:, :, 0] = cv2.equalizeHist(img_yuv[:, :, 0])
            img_enhanced = cv2.cvtColor(img_yuv, cv2.COLOR_YUV2BGR)

            # Áp dụng CLAHE cho không gian màu LAB
            lab = cv2.cvtColor(img_enhanced, cv2.COLOR_BGR2LAB)
            clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
            lab[:, :, 0] = clahe.apply(lab[:, :, 0])
            img_clahe = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)

            # Chuyển đổi sang RGB để hiển thị
            img_final = cv2.cvtColor(img_clahe, cv2.COLOR_BGR2RGB)
            self.img_display = img_final
            self.show_image(self.img_display)
            self.status.set("Tăng cường chất lượng ảnh thành công.")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể tăng cường ảnh: {e}")
            self.status.set("Lỗi khi tăng cường ảnh.")

    def show_about(self):
        about_text = (
            "Ứng dụng Xử Lý Ảnh Chuyên Nghiệp\n"
            "Phiên bản 1.0\n"
            "Phát triển bởi proarmyy\n"
            "Sử dụng Python, Tkinter và OpenCV."
        )
        messagebox.showinfo("Giới Thiệu", about_text)


if __name__ == "__main__":
    root = tk.Tk()
    app = ImageEditorApp(root)
    root.mainloop()
