"""Simple graphical interface for the photo editor."""

from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

from PIL import Image, ImageTk

from .catalog import Catalog
from .editor import Editor, brighten, denoise


class EditorApp(tk.Tk):
    """Tkinter based image editor."""

    def __init__(self) -> None:
        super().__init__()
        self.title("Photo Editor")
        self.geometry("600x600")
        self.catalog: Catalog | None = None
        self.images: list[Image.Image] = []
        self.current_index = 0
        self.editor: Editor | None = None
        self._build_ui()

    def _build_ui(self) -> None:
        top = ttk.Frame(self)
        top.pack(pady=5)
        ttk.Button(top, text="Open Folder", command=self.open_folder).pack(side=tk.LEFT, padx=5)
        ttk.Button(top, text="Save As...", command=self.save_image).pack(side=tk.LEFT)

        self.image_label = ttk.Label(self)
        self.image_label.pack(expand=True)

        controls = ttk.Frame(self)
        controls.pack(fill=tk.X, padx=10, pady=5)
        ttk.Label(controls, text="Brightness").pack(anchor=tk.W)
        self.brightness = tk.DoubleVar(value=1.0)
        ttk.Scale(controls, from_=0.5, to=1.5, orient=tk.HORIZONTAL, variable=self.brightness).pack(fill=tk.X)
        self.denoise_var = tk.IntVar(value=0)
        ttk.Checkbutton(controls, text="Denoise", variable=self.denoise_var).pack(anchor=tk.W)
        ttk.Button(controls, text="Apply", command=self.apply_edits).pack(pady=4)

        nav = ttk.Frame(self)
        nav.pack(pady=5)
        ttk.Button(nav, text="<< Prev", command=self.prev_image).grid(row=0, column=0, padx=5)
        ttk.Button(nav, text="Next >>", command=self.next_image).grid(row=0, column=1, padx=5)

    def open_folder(self) -> None:
        folder = filedialog.askdirectory()
        if not folder:
            return
        self.catalog = Catalog(path=Path(folder))
        self.catalog.load()
        self.images = list(self.catalog)
        if not self.images:
            messagebox.showerror("Error", "No images found")
            return
        self.current_index = 0
        self.load_image()

    def load_image(self) -> None:
        img = self.images[self.current_index]
        self.editor = Editor(image=img.copy())
        self._show_image(self.editor.image)

    def _show_image(self, img: Image.Image) -> None:
        disp = img.copy()
        disp.thumbnail((500, 500))
        self.tk_image = ImageTk.PhotoImage(disp)
        self.image_label.configure(image=self.tk_image)

    def apply_edits(self) -> None:
        if not self.editor:
            return
        self.editor.image = self.images[self.current_index].copy()
        if self.brightness.get() != 1.0:
            self.editor.apply(brighten, self.brightness.get())
        if self.denoise_var.get():
            self.editor.apply(denoise)
        self._show_image(self.editor.image)

    def save_image(self) -> None:
        if not self.editor:
            return
        path = filedialog.asksaveasfilename(defaultextension=".jpg")
        if not path:
            return
        self.editor.save(Path(path))

    def prev_image(self) -> None:
        if self.current_index > 0:
            self.current_index -= 1
            self.load_image()

    def next_image(self) -> None:
        if self.current_index < len(self.images) - 1:
            self.current_index += 1
            self.load_image()


def main() -> None:
    app = EditorApp()
    app.mainloop()


if __name__ == "__main__":
    main()
