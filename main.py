import flet
from flet import AppBar, Theme, ThemeMode, Card, Column, Icon, Container, PopupMenuButton, PopupMenuItem, padding, alignment, Row, IconButton, icons, Page, Text, View, colors, FontWeight, CrossAxisAlignment
from settings import read_themes, write_themes
from binanceapi import data_objs, read_obj_list
from vw_settings import view_settings
from vw_wallet import view_wallet
from vw_buy_sell import view_buy_sell

def main(page: Page):
    page.title = "Binance Flet"
    page.window.width = 740
    conf = read_themes()
    page.theme = Theme(color_scheme_seed=conf["cor"])
    if conf["tema"] == "ThemeMode.LIGHT":
        tema = ThemeMode.LIGHT
    else:
        tema = ThemeMode.DARK
    page.theme_mode = tema
    card_list = Row()
    btn_update = IconButton(icons.UPDATE, disabled=False, on_click=lambda e: data_binance(e), bgcolor=colors.PRIMARY, icon_color=colors.SECONDARY_CONTAINER)

    def toggle_theme(e):
        if page.theme_mode == ThemeMode.DARK:
            page.theme_mode = ThemeMode.LIGHT
            save_themes()
        else:
            page.theme_mode = ThemeMode.DARK
            save_themes()
        page.update()

    def toggle_color(e):
        cor = e.control.data
        page.theme = Theme(color_scheme_seed=cor)
        save_themes()
        page.update()

    def save_themes():
        obj = {"tema": str(page.theme_mode), "cor": str(page.theme.color_scheme_seed)}
        write_themes(obj)
        
    def data_binance(e):
        btn_update.disabled = True
        btn_update.bgcolor = colors.GREY_200
        page.update()
        data_objs()
        pop_cards(None) 
        
    def pop_cards(e):
        objs = read_obj_list()
        # nonlocal rows
        rows = []
        for obj in objs:
            perc = Text(f"{obj["perc"]}%", weight=FontWeight.BOLD)
            if float(obj["perc"]) > 0:
                perc.color = "green"
            else:
                perc.color = "red"
            card=Card(
            content=Container(
                content=Column(
                    [
                        Row([Text(str(obj["symbol"]), weight=FontWeight.BOLD)]),
                        Row([Text("Abertura "), Text(str(obj["open"]))]),
                        Row([Text("Máxima "), Text(str(obj["hi"]))]),
                        Row([Text("Mínima "), Text(str(obj["low"]))]),
                        Row([Text("Amplitude "), Text(str(obj["amplitude"]))]),
                        Row([Text("Atual "), Text(str(obj["bid"]), weight=FontWeight.BOLD)]),
                        Row([Text("Variação "), perc]),
                    ]
                ),
                width=250,
                padding=padding.symmetric(vertical=10, horizontal=46),
                )
            )
            rows.append(card)
        nonlocal card_list
        card_list.controls = rows
        card_list.wrap = True
        btn_update.disabled = False
        btn_update.bgcolor = colors.PRIMARY
        page.update()

    ico_menu = PopupMenuButton(
        items=[
            PopupMenuItem(text="TEMAS"),
            PopupMenuItem(icon=icons.CONTRAST_OUTLINED, text="Dark/Light", on_click=toggle_theme),
            PopupMenuItem(),
            PopupMenuItem(content=Row([Icon(icons.SQUARE, color=colors.BLUE), Text("Azul")]), data="blue", on_click=toggle_color),
            PopupMenuItem(content=Row([Icon(icons.SQUARE, color=colors.AMBER), Text("Ambar")]), data="amber", on_click=toggle_color),
            PopupMenuItem(content=Row([Icon(icons.SQUARE, color=colors.PURPLE), Text("Lilás")]), data="purple", on_click=toggle_color),
            PopupMenuItem(content=Row([Icon(icons.SQUARE, color=colors.PINK), Text("Pink")]), data="pink", on_click=toggle_color),
            PopupMenuItem(content=Row([Icon(icons.SQUARE, color=colors.GREEN), Text("Verde")]), data="green", on_click=toggle_color),
        ])
    
    def route_change(e):
        page.views.clear()
        pop_cards(None)
        page.views.append(
            View(
                "/",
                [
                    AppBar(title=Text("Binance Flet app", color=colors.PRIMARY, weight=FontWeight.BOLD),
                        actions=[
                            IconButton(icons.WALLET_OUTLINED, on_click=open_wallet, bgcolor=colors.PRIMARY, icon_color=colors.SECONDARY_CONTAINER), Container(width=20),
                            IconButton(icons.CHECKLIST, on_click=open_buy_sell, bgcolor=colors.PRIMARY, icon_color=colors.SECONDARY_CONTAINER), Container(width=20),
                            IconButton(icons.SETTINGS_OUTLINED, on_click=open_settings, bgcolor=colors.PRIMARY, icon_color=colors.SECONDARY_CONTAINER), Container(width=40),
                            btn_update, Container(width=40),
                            ico_menu, Container(width=20),
                        ], bgcolor=colors.PRIMARY_CONTAINER),
                    Container(
                            content=Text("Home", size=16, weight=FontWeight.BOLD, color=colors.PRIMARY),
                            width=440,
                            padding=padding.only(bottom=0),
                            alignment=alignment.center,
                        ),
                    card_list,
                ], horizontal_alignment=CrossAxisAlignment.CENTER
            )
        )
        
        if page.route == "/wallet":
            view_wallet(page)
        
        if page.route == "/buy_sell":
            view_buy_sell(page)
        
        if page.route == "/settings":
            view_settings(page)
        
        page.update()

    def view_pop(e):
        # View pop => e.view
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    data_binance(None)

    def open_wallet(e):
        page.go("/wallet")

    def open_buy_sell(e):
        page.go("/buy_sell")

    def open_settings(e):
        page.go("/settings")

    page.go(page.route)

flet.app(target=main)