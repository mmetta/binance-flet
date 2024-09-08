from flet import Page, View, AppBar, Container, Text, FontWeight, colors, padding, alignment, CrossAxisAlignment


def view_buy_sell(page: Page):
    page.views.append(
        View(
            "/settings",
                    [
                        AppBar(title=Text("Compra e Venda"), bgcolor=colors.PRIMARY_CONTAINER),
                        Container(
                            content=Text("Registro de compra e venda de cryptos", size=16, weight=FontWeight.BOLD, color=colors.PRIMARY),
                            width=440,
                            padding=padding.only(bottom=0),
                            alignment=alignment.center,
                        ),
                    ], horizontal_alignment=CrossAxisAlignment.CENTER
                )
            )
