import os
from datetime import datetime
from pathlib import Path
import tkinter as tk
from tkinter import messagebox

from PIL import ImageGrab


FILE_PREFIX = "cap_"
INPUT_FILE = Path(__file__).resolve().with_name("input_txt.py")


def load_save_dir() -> str:
    if not INPUT_FILE.exists():
        raise FileNotFoundError("Khong tim thay input.txt. Hay chay input.py truoc.")

    save_dir = INPUT_FILE.read_text(encoding="utf-8").strip()
    if not save_dir:
        raise ValueError("input.txt dang rong. Hay chay input.py va nhap SAVE_DIR.")

    return save_dir


class ScreenCaptureApp:
    def __init__(self, root: tk.Tk, save_dir: str) -> None:
        self.root = root
        self.save_dir = save_dir
        self.start_x = 0
        self.start_y = 0
        self.rect_id = None

        self.root.title("Screen Capture Tool")
        self.root.attributes("-fullscreen", True)
        self.root.attributes("-alpha", 0.25)
        self.root.attributes("-topmost", True)
        self.root.configure(bg="black")
        self.root.config(cursor="cross")

        self.canvas = tk.Canvas(self.root, bg="black", highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.canvas.bind("<ButtonPress-1>", self.on_button_press)
        self.canvas.bind("<B1-Motion>", self.on_mouse_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_button_release)
        self.root.bind("<Escape>", self.cancel_capture)

    def on_button_press(self, event: tk.Event) -> None:
        self.start_x = event.x
        self.start_y = event.y
        if self.rect_id is not None:
            self.canvas.delete(self.rect_id)
        self.rect_id = self.canvas.create_rectangle(
            self.start_x,
            self.start_y,
            self.start_x,
            self.start_y,
            outline="red",
            width=2,
        )

    def on_mouse_drag(self, event: tk.Event) -> None:
        if self.rect_id is None:
            return
        self.canvas.coords(self.rect_id, self.start_x, self.start_y, event.x, event.y)

    def on_button_release(self, event: tk.Event) -> None:
        end_x, end_y = event.x, event.y
        x1 = min(self.start_x, end_x)
        y1 = min(self.start_y, end_y)
        x2 = max(self.start_x, end_x)
        y2 = max(self.start_y, end_y)

        # Bỏ qua nếu vùng chọn quá nhỏ.
        if (x2 - x1) < 2 or (y2 - y1) < 2:
            self.cancel_capture()
            return

        self.root.withdraw()
        self.root.update_idletasks()

        try:
            os.makedirs(self.save_dir, exist_ok=True)
            image = ImageGrab.grab(bbox=(x1, y1, x2, y2))
            file_name = f"{FILE_PREFIX}{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.png"
            file_path = os.path.join(self.save_dir, file_name)
            image.save(file_path)
            messagebox.showinfo("Screen Capture", f"Da luu anh:\n{file_path}")
        except Exception as exc:
            messagebox.showerror("Screen Capture", f"Loi khi chup man hinh:\n{exc}")
        finally:
            self.root.destroy()

    def cancel_capture(self, _event=None) -> None:
        self.root.destroy()


def main() -> None:
    try:
        save_dir = load_save_dir()
    except Exception as exc:
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror("Screen Capture", f"Loi SAVE_DIR:\n{exc}")
        root.destroy()
        return

    root = tk.Tk()
    ScreenCaptureApp(root, save_dir)
    root.mainloop()


if __name__ == "__main__":
    main()
