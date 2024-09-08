import flet
from flet import AppBar, Theme, ThemeMode, Icon, Container, PopupMenuButton, PopupMenuItem, Row, SnackBar, AlertDialog, TextButton, alignment, MainAxisAlignment, padding, TextAlign, ListView, OutlinedButton, IconButton, icons, ElevatedButton, Page, Text, View, colors, FontWeight, CrossAxisAlignment, TextField
from settings import read_themes


def main(page: Page):
    page.title = "Fácil Flet"
    page.window.width = 880
    conf = read_themes()
    page.theme = Theme(color_scheme_seed=conf["cor"])
    if conf["tema"] == "ThemeMode.LIGHT":
        tema = ThemeMode.LIGHT
    else:
        tema = ThemeMode.DARK
    page.theme_mode = tema
    