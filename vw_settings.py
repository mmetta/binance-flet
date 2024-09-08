from flet import Page, View, AppBar, Container, Text, FontWeight, colors, padding, alignment, CrossAxisAlignment


def view_settings(page: Page):
    page.views.append(
        View(
            "/settings",
                    [
                        AppBar(title=Text("Config"), bgcolor=colors.PRIMARY_CONTAINER),
                        Container(
                            content=Text("Configurações do app", size=16, weight=FontWeight.BOLD, color=colors.PRIMARY),
                            width=440,
                            padding=padding.only(bottom=0),
                            alignment=alignment.center,
                        ),
                    ], horizontal_alignment=CrossAxisAlignment.CENTER
                )
            )
