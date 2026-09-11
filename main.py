import flet as ft

class Task(ft.Column):
    def __init__(self, task_name, task_status_change, task_delete):
        super().__init__()
        self.completed = False
        self.task_name = task_name
        self.task_status_change = task_status_change
        self.task_delete = task_delete

        self.display_task = ft.Checkbox(
            value=False, label=self.task_name, on_change=self.status_changed, expand=True
        )
        self.edit_name = ft.TextField(expand=True)

        self.display_view = ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                self.display_task,
                ft.Row(
                    spacing=0,
                    controls=[
                        ft.IconButton(
                            icon=ft.icons.CREATE_OUTLINED,
                            tooltip="ویرایش",
                            on_click=self.edit_clicked,
                            icon_color=ft.colors.GREY_400,
                        ),
                        ft.IconButton(
                            icon=ft.icons.DELETE_OUTLINE,
                            tooltip="حذف",
                            on_click=self.delete_clicked,
                            icon_color=ft.colors.RED_300,
                        ),
                    ],
                ),
            ],
        )

        self.edit_view = ft.Row(
            visible=False,
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                self.edit_name,
                ft.IconButton(
                    icon=ft.icons.DONE_OUTLINE_OUTLINED,
                    icon_color=ft.colors.GREEN,
                    tooltip="ذخیره",
                    on_click=self.save_clicked,
                ),
            ],
        )

        self.controls = [
            ft.Container(
                content=ft.Column(controls=[self.display_view, self.edit_view]),
                bgcolor=ft.colors.SURFACE_VARIANT,
                padding=10,
                border_radius=8,
            )
        ]

    def edit_clicked(self, e):
        self.edit_name.value = self.display_task.label
        self.display_view.visible = False
        self.edit_view.visible = True
        self.update()

    def save_clicked(self, e):
        self.display_task.label = self.edit_name.value
        self.display_view.visible = True
        self.edit_view.visible = False
        self.update()

    def status_changed(self, e):
        self.completed = self.display_task.value
        self.task_status_change(self)

    def delete_clicked(self, e):
        self.task_delete(self)

class TodoApp(ft.Column):
    def __init__(self):
        super().__init__()
        self.new_task = ft.TextField(
            hint_text="چه کاری باید انجام دهید؟",
            expand=True,
            border_radius=10,
            border_color=ft.colors.BLUE_400,
            on_submit=self.add_clicked,
        )
        self.tasks = ft.Column(spacing=10)
        
        self.filter = ft.Tabs(
            selected_index=0,
            animation_duration=300,
            on_change=self.tabs_changed,
            tabs=[
                ft.Tab(text="همه"),
                ft.Tab(text="در حال انجام"),
                ft.Tab(text="تکمیل شده"),
            ],
        )
        
        self.items_left = ft.Text("0 کار باقی مانده", color=ft.colors.GREY_400)
        self.progress_bar = ft.ProgressBar(value=0, color=ft.colors.BLUE_ACCENT, bgcolor=ft.colors.SURFACE_VARIANT, height=8, border_radius=5)
        self.progress_text = ft.Text("0%", color=ft.colors.BLUE_ACCENT, weight=ft.FontWeight.BOLD)

        self.controls = [
            ft.Row(
                [
                    ft.Text("⚡ داشبورد مدیریت کارها", style=ft.TextThemeStyle.HEADLINE_MEDIUM, weight=ft.FontWeight.BOLD),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            ft.Container(height=10),
            ft.Container(
                content=ft.Column(
                    [
                        ft.Row([ft.Text("میزان پیشرفت امروز", weight=ft.FontWeight.BOLD), self.progress_text], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                        self.progress_bar,
                    ]
                ),
                padding=15,
                bgcolor=ft.colors.SURFACE_VARIANT,
                border_radius=12,
                border=ft.border.all(1, ft.colors.WHITE10),
            ),
            ft.Container(height=10),
            ft.Row(
                controls=[
                    self.new_task,
                    ft.FloatingActionButton(
                        icon=ft.icons.ADD,
                        on_click=self.add_clicked,
                        bgcolor=ft.colors.BLUE_600,
                    ),
                ],
            ),
            ft.Column(
                controls=[
                    self.filter,
                    self.tasks,
                    ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                        controls=[
                            self.items_left,
                            ft.OutlinedButton(
                                text="حذف انجام‌شده‌ها",
                                on_click=self.clear_completed,
                                style=ft.ButtonStyle(color=ft.colors.RED_400)
                            ),
                        ],
                    ),
                ]
            ),
        ]

    def add_clicked(self, e):
        if self.new_task.value and self.new_task.value.strip():
            task = Task(self.new_task.value, self.task_status_change, self.task_delete)
            self.tasks.controls.append(task)
            self.new_task.value = ""
            self.update_stats()
            self.update()

    def task_status_change(self, task):
        self.update_stats()
        self.update()

    def task_delete(self, task):
        self.tasks.controls.remove(task)
        self.update_stats()
        self.update()

    def tabs_changed(self, e):
        self.update_visibility()

    def clear_completed(self, e):
        for task in self.tasks.controls[:]:
            if task.completed:
                self.task_delete(task)

    def update_visibility(self):
        status_idx = self.filter.selected_index
        statuses = ["همه", "در حال انجام", "تکمیل شده"]
        status = statuses[status_idx]
        
        for task in self.tasks.controls:
            task.visible = (
                status == "همه"
                or (status == "در حال انجام" and not task.completed)
                or (status == "تکمیل شده" and task.completed)
            )
        self.update()

    def update_stats(self):
        count = sum(1 for task in self.tasks.controls if not task.completed)
        total = len(self.tasks.controls)
        completed = total - count
        
        self.items_left.value = f"{count} کار باقی مانده"
        
        if total > 0:
            progress = completed / total
            self.progress_bar.value = progress
            self.progress_text.value = f"{int(progress * 100)}%"
        else:
            self.progress_bar.value = 0
            self.progress_text.value = "0%"

def main(page: ft.Page):
    page.title = "برنامه مدیریت کارهای مدرن"
    page.theme_mode = ft.ThemeMode.DARK
    page.window_width = 450
    page.window_height = 650
    page.window_resizable = True
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.padding = 20

    todo = TodoApp()
    page.add(todo)

ft.app(target=main)
