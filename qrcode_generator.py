"""
QRコード生成ツール
Copyright (c) 2026 大杉一実 (ohsugi kazumi)
Released under the MIT license
https://opensource.org/licenses/mit-license.php
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from PIL import Image, ImageTk
import qrcode
from pathlib import Path

class QRCodeGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("QRコード生成ツール")
        self.root.geometry("600x700")
        self.root.resizable(True, True)
        
        # 生成されたQRコード画像を保持
        self.qr_image = None
        self.qr_pil_image = None
        
        # UI の構築
        self.setup_ui()
    
    def setup_ui(self):
        """UI コンポーネントの配置"""
        
        # タイトルラベル
        title_label = ttk.Label(
            self.root,
            text="QRコード生成ツール",
            font=("Arial", 16, "bold")
        )
        title_label.pack(pady=10)
        
        # 入力フレーム
        input_frame = ttk.LabelFrame(self.root, text="URL入力", padding=10)
        input_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(input_frame, text="URL:").pack(side=tk.LEFT, padx=5)
        
        self.url_entry = ttk.Entry(input_frame)
        self.url_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        self.url_entry.bind("<Return>", lambda e: self.generate_qrcode())
        
        # ボタンフレーム
        button_frame = ttk.Frame(self.root)
        button_frame.pack(pady=10)
        
        generate_btn = ttk.Button(
            button_frame,
            text="QRコード生成",
            command=self.generate_qrcode
        )
        generate_btn.pack(side=tk.LEFT, padx=5)
        
        clear_btn = ttk.Button(
            button_frame,
            text="クリア",
            command=self.clear_qrcode
        )
        clear_btn.pack(side=tk.LEFT, padx=5)
        
        # QRコード表示フレーム
        qr_frame = ttk.LabelFrame(self.root, text="QRコード", padding=10)
        qr_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # キャンバスでQRコードを表示
        self.canvas = tk.Canvas(
            qr_frame,
            bg="white",
            cursor="hand2",
            highlightthickness=1,
            highlightbackground="gray"
        )
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        # 右クリックメニュー
        self.canvas.bind("<Button-3>", self.show_context_menu)
        
        # ステータスバー
        self.status_var = tk.StringVar(value="URLを入力してください")
        status_bar = ttk.Label(
            self.root,
            textvariable=self.status_var,
            relief=tk.SUNKEN,
            anchor=tk.W
        )
        status_bar.pack(fill=tk.X, side=tk.BOTTOM)
    
    def generate_qrcode(self):
        """QRコードを生成"""
        url = self.url_entry.get().strip()
        
        if not url:
            messagebox.showwarning("警告", "URLを入力してください")
            return
        
        try:
            # QRコード生成
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(url)
            qr.make(fit=True)
            
            # PIL Image に変換
            self.qr_pil_image = qr.make_image(fill_color="black", back_color="white")
            
            # キャンバスに表示
            self.display_qrcode_on_canvas()
            
            self.status_var.set(f"✓ QRコード生成完了: {url[:50]}...")
            
        except Exception as e:
            messagebox.showerror("エラー", f"QRコード生成に失敗しました:\n{str(e)}")
            self.status_var.set("エラーが発生しました")
    
    def display_qrcode_on_canvas(self):
        """PIL Image をキャンバスに表示"""
        if self.qr_pil_image is None:
            return
        
        # キャンバスサイズを取得
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        
        if canvas_width <= 1 or canvas_height <= 1:
            # ウィジェットがまだ配置されていない場合は更新を予約
            self.root.after(100, self.display_qrcode_on_canvas)
            return
        
        # QRコード画像をリサイズ（キャンバスサイズに合わせる）
        display_size = min(canvas_width, canvas_height) - 20
        display_size = max(display_size, 200)  # 最小サイズ
        
        resized_image = self.qr_pil_image.resize((display_size, display_size), Image.Resampling.LANCZOS)
        
        # PhotoImage に変換
        self.qr_image = ImageTk.PhotoImage(resized_image)
        
        # キャンバスをクリアして表示
        self.canvas.delete("all")
        self.canvas.create_image(
            canvas_width // 2,
            canvas_height // 2,
            image=self.qr_image
        )
    
    def clear_qrcode(self):
        """QRコードをクリア"""
        self.canvas.delete("all")
        self.url_entry.delete(0, tk.END)
        self.qr_pil_image = None
        self.qr_image = None
        self.status_var.set("クリアしました")
    
    def show_context_menu(self, event):
        """右クリックメニューを表示"""
        if self.qr_pil_image is None:
            messagebox.showinfo("情報", "QRコードを先に生成してください")
            return
        
        context_menu = tk.Menu(self.root, tearoff=False)
        context_menu.add_command(
            label="PNG として保存",
            command=lambda: self.save_as_png()
        )
        context_menu.add_command(
            label="JPG として保存",
            command=lambda: self.save_as_jpg()
        )
        context_menu.add_separator()
        context_menu.add_command(
            label="クリップボードにコピー",
            command=self.copy_to_clipboard
        )
        
        context_menu.post(event.x_root, event.y_root)
    
    def save_as_png(self):
        """PNG で保存"""
        if self.qr_pil_image is None:
            return
        
        file_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG Image", "*.png"), ("All Files", "*.*")],
            initialfile="qrcode.png"
        )
        
        if file_path:
            try:
                self.qr_pil_image.save(file_path, "PNG")
                messagebox.showinfo("成功", f"保存しました:\n{file_path}")
                self.status_var.set(f"✓ PNG として保存: {Path(file_path).name}")
            except Exception as e:
                messagebox.showerror("エラー", f"保存に失敗しました:\n{str(e)}")
    
    def save_as_jpg(self):
        """JPG で保存"""
        if self.qr_pil_image is None:
            return
        
        file_path = filedialog.asksaveasfilename(
            defaultextension=".jpg",
            filetypes=[("JPEG Image", "*.jpg;*.jpeg"), ("All Files", "*.*")],
            initialfile="qrcode.jpg"
        )
        
        if file_path:
            try:
                # JPG は RGB に変換が必要
                rgb_image = self.qr_pil_image.convert("RGB")
                rgb_image.save(file_path, "JPEG", quality=95)
                messagebox.showinfo("成功", f"保存しました:\n{file_path}")
                self.status_var.set(f"✓ JPG として保存: {Path(file_path).name}")
            except Exception as e:
                messagebox.showerror("エラー", f"保存に失敗しました:\n{str(e)}")
    
    def copy_to_clipboard(self):
        """クリップボードにコピー"""
        if self.qr_pil_image is None:
            return
        
        messagebox.showinfo(
            "情報",
            "このプログラムで直接クリップボードにコピーするには、\n" +
            "右クリック -> PNG/JPGで保存 をご利用ください"
        )


def main():
    root = tk.Tk()
    QRCodeGeneratorApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()