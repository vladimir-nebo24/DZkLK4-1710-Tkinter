import tkinter as tk
from tkinter import filedialog, messagebox


class UserProfileTkinter:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Профиль пользователя - Tkinter")
        self.root.geometry("450x600")
        self.root.minsize(400, 500)
        self.root.configure(bg='#f8f9fa')

        # Для хранения изображения
        self.avatar_photo = None
        self.upload_btn = None

        self.setup_ui()

    def setup_ui(self):
        """Настройка графического интерфейса"""
        self.create_scrollable_frame()
        self.setup_main_window()

    def create_scrollable_frame(self):
        """Создание прокручиваемой области"""
        self.canvas = tk.Canvas(self.root, bg='#f8f9fa', highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.main_frame = tk.Frame(self.canvas, bg='#f8f9fa')
        self.canvas_window = self.canvas.create_window((0, 0), window=self.main_frame, anchor="nw")

        self.main_frame.bind("<Configure>", self._on_frame_configure)
        self.canvas.bind("<Configure>", self._on_canvas_configure)
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

    def _on_frame_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def _on_canvas_configure(self, event):
        self.canvas.itemconfig(self.canvas_window, width=event.width)

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def setup_main_window(self):
        """Создание и расположение виджетов"""
        self.create_header_section()
        self.create_profile_section()

    def create_header_section(self):
        """Создание шапки с градиентным фоном"""
        header_frame = tk.Frame(self.main_frame, bg='#667eea', height=180)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)

        center_frame = tk.Frame(header_frame, bg='#667eea')
        center_frame.place(relx=0.5, rely=0.5, anchor='center')

        # Создаем аватарку
        self.create_avatar_section(center_frame)

    def create_avatar_section(self, parent):
        """Создание аватарки с кнопкой загрузки при наведении"""
        self.avatar_container = tk.Frame(parent, bg='#667eea')
        self.avatar_container.pack()

        self.avatar_canvas = tk.Canvas(self.avatar_container, width=120, height=120,
                                       bg='#667eea', highlightthickness=0,
                                       cursor='hand2')
        self.avatar_canvas.pack()

        # Создаем круглую аватарку по умолчанию
        self.create_default_avatar()

        # Кнопка загрузки (изначально скрыта)
        self.upload_btn = tk.Label(self.avatar_container, text="📷 Загрузить фото",
                                   font=('Arial', 9, 'bold'), bg='white', fg='#667eea',
                                   relief='raised', bd=1, padx=8, pady=3,
                                   cursor='hand2')

        # Привязываем события мыши
        self.avatar_canvas.bind("<Enter>", self._on_avatar_enter)
        self.avatar_canvas.bind("<Leave>", self._on_avatar_leave)
        self.avatar_canvas.bind("<Button-1>", self.upload_photo)

        self.upload_btn.bind("<Enter>", self._on_button_enter)
        self.upload_btn.bind("<Leave>", self._on_avatar_leave)
        self.upload_btn.bind("<Button-1>", self.upload_photo)

    def _on_avatar_enter(self, event):
        """При наведении на аватарку - показываем кнопку"""
        self.upload_btn.pack(pady=(8, 0))
        self.avatar_canvas.create_rectangle(0, 0, 120, 120, fill='black', stipple='gray50', tags='overlay')

    def _on_button_enter(self, event):
        """При наведении на кнопку - меняем стиль"""
        self.upload_btn.configure(bg='#f0f0f0', relief='sunken')

    def _on_avatar_leave(self, event):
        """При уходе с аватарки или кнопки - скрываем кнопку"""
        x, y = self.avatar_container.winfo_pointerxy()
        widget = self.avatar_container.winfo_containing(x, y)

        if widget not in [self.avatar_canvas, self.upload_btn]:
            self.upload_btn.pack_forget()
            self.avatar_canvas.delete('overlay')

    def create_default_avatar(self):
        """Создание аватарки по умолчанию"""
        self.avatar_canvas.delete("all")
        self.avatar_canvas.create_oval(10, 10, 110, 110, fill='#e74c3c', outline='white', width=4)
        self.avatar_canvas.create_text(60, 60, text="ВН", fill='white',
                                       font=('Arial', 24, 'bold'))

    def upload_photo(self, event=None):
        """Загрузка фотографии с использованием tkinter.PhotoImage"""
        try:
            file_path = filedialog.askopenfilename(
                title="Выберите фотографию",
                filetypes=[
                    ("Изображения", "*.jpg *.jpeg *.png *.bmp *.gif"),
                    ("Все файлы", "*.*")
                ]
            )

            if file_path:
                # Загружаем изображение с помощью tkinter
                self.avatar_photo = tk.PhotoImage(file=file_path)

                # Масштабируем изображение до нужного размера
                width = self.avatar_photo.width()
                height = self.avatar_photo.height()

                # Определяем коэффициент масштабирования
                scale = min(100 / width, 100 / height)
                new_width = int(width * scale)
                new_height = int(height * scale)

                # Создаем уменьшенную версию изображения
                self.avatar_photo = self.avatar_photo.subsample(
                    max(1, width // new_width),
                    max(1, height // new_height)
                )

                # Очищаем canvas и отображаем фото в круге
                self.avatar_canvas.delete("all")

                # Создаем круглую маску (рисуем круг)
                self.avatar_canvas.create_oval(10, 10, 110, 110, fill='#667eea', outline='white', width=4)

                # Отображаем фото поверх круга (будет видна только часть внутри круга)
                self.avatar_canvas.create_image(60, 60, image=self.avatar_photo)

                # Скрываем кнопку после загрузки
                self.upload_btn.pack_forget()
                self.avatar_canvas.delete('overlay')

                messagebox.showinfo("Успех", "Фотография успешно загружена!")

        except Exception as e:
            messagebox.showerror("Ошибка",
                                 f"Не удалось загрузить фото: {str(e)}\n\nПопробуйте выбрать изображение в формате GIF или PGM")

    def create_profile_section(self):
        """Создание основной секции с информацией"""
        content_frame = tk.Frame(self.main_frame, bg='white')
        content_frame.pack(fill=tk.BOTH, expand=True, padx=0, pady=0)

        tk.Frame(content_frame, height=30, bg='white').pack()

        name_label = tk.Label(content_frame, text="Владимир Небогатиков",
                              font=('Arial', 22, 'bold'), fg='#2c3e50', bg='white')
        name_label.pack(pady=(0, 5))

        position_label = tk.Label(content_frame, text="Студент 2 курса",
                                  font=('Arial', 14), fg='#7f8c8d', bg='white')
        position_label.pack(pady=(0, 25))

        self.create_separator(content_frame)

        self.create_info_section(content_frame, "Биография",
                                 "Уроженец города Щёлково. Сейчас учусь в МАИ на направлении 'Инноватика'. Увлекаюсь UFC, футболом, баскетболом. Имею рельефный пресс.")

        self.create_separator(content_frame)

        self.create_info_section(content_frame, "Навыки", "Python, MySQL")

        self.create_separator(content_frame)

        self.create_experience_section(content_frame)

        tk.Frame(content_frame, height=30, bg='white').pack()

    def create_separator(self, parent):
        separator = tk.Frame(parent, height=1, bg='#ecf0f1')
        separator.pack(fill=tk.X, padx=30, pady=20)

    def create_info_section(self, parent, title, content):
        section_frame = tk.Frame(parent, bg='white')
        section_frame.pack(fill=tk.X, padx=30, pady=0)

        title_label = tk.Label(section_frame, text=title,
                               font=('Arial', 16, 'bold'), fg='#2c3e50',
                               bg='white', anchor='w')
        title_label.pack(fill=tk.X, pady=(0, 10))

        content_label = tk.Label(section_frame, text=content,
                                 font=('Arial', 12), fg='#34495e', bg='white',
                                 justify='left', wraplength=380, anchor='w')
        content_label.pack(fill=tk.X)

        def update_wraplength(event=None):
            new_width = parent.winfo_width() - 60
            content_label.configure(wraplength=max(300, new_width))

        parent.bind('<Configure>', update_wraplength)

    def create_experience_section(self, parent):
        section_frame = tk.Frame(parent, bg='white')
        section_frame.pack(fill=tk.X, padx=30, pady=0)

        title_label = tk.Label(section_frame, text="Опыт работы",
                               font=('Arial', 16, 'bold'), fg='#2c3e50',
                               bg='white', anchor='w')
        title_label.pack(fill=tk.X, pady=(0, 20))

        exp1_frame = tk.Frame(section_frame, bg='white')
        exp1_frame.pack(fill=tk.X, pady=(0, 20))

        exp1_title = tk.Label(exp1_frame, text="Разнорабочий",
                              font=('Arial', 13, 'bold'), fg='#2c3e50', bg='white', anchor='w',
                              wraplength=380, justify='left')
        exp1_title.pack(fill=tk.X)

        exp1_company = tk.Label(exp1_frame, text="ООО 'Дядя Рафик'",
                                font=('Arial', 12), fg='#3498db', bg='white', anchor='w')
        exp1_company.pack(fill=tk.X, pady=(5, 0))

        exp1_period = tk.Label(exp1_frame, text="Лето 2023",
                               font=('Arial', 11), fg='#7f8c8d', bg='white', anchor='w')
        exp1_period.pack(fill=tk.X, pady=(2, 0))

        exp2_frame = tk.Frame(section_frame, bg='white')
        exp2_frame.pack(fill=tk.X, pady=(0, 10))

        exp2_title = tk.Label(exp2_frame, text="Технический инженер",
                              font=('Arial', 13, 'bold'), fg='#2c3e50', bg='white', anchor='w')
        exp2_title.pack(fill=tk.X)

        exp2_company = tk.Label(exp2_frame, text="У бати",
                                font=('Arial', 12), fg='#3498db', bg='white', anchor='w')
        exp2_company.pack(fill=tk.X, pady=(5, 0))

        exp2_period = tk.Label(exp2_frame, text="Июнь 2025 - настоящее время",
                               font=('Arial', 11), fg='#7f8c8d', bg='white', anchor='w')
        exp2_period.pack(fill=tk.X, pady=(2, 0))

        def update_exp_wraplength(event=None):
            new_width = section_frame.winfo_width() - 60
            exp1_title.configure(wraplength=max(300, new_width))

        section_frame.bind('<Configure>', update_exp_wraplength)

    def run(self):
        self.root.mainloop()


if __name__ == '__main__':
    app = UserProfileTkinter()
    app.run()