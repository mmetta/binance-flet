from flet import Page, View, AppBar, Container, Text, SnackBar, ElevatedButton, Radio, RadioGroup, Row, MainAxisAlignment, FontWeight, colors, padding, alignment, CrossAxisAlignment
from settings import read_themes, write_align

def view_settings(page: Page):
    
    tema = read_themes()
    
    btn_save = ElevatedButton(text='Salvar', on_click=lambda e: radiogroup_clicked(e))
    radio_align = RadioGroup(content=Row([
        Radio(value="left", label="Esquerda"),
        Radio(value="center", label="Centro"),
        Radio(value="right", label="Direita")
        ], alignment=MainAxisAlignment.CENTER))
    
    radio_align.value = tema["align_win"]
    
    def radiogroup_clicked(e):
        align_win = radio_align.value
        res = write_align(align_win)
        snack_bar = SnackBar(content=Text(res), show_close_icon=True)
        page.overlay.append(snack_bar)
        snack_bar.open = True
        page.update()
    
    page.views.append(
        View(
            "/settings",
                    [
                        AppBar(title=Text("Config"), center_title=True, bgcolor=colors.PRIMARY_CONTAINER),
                        Container(
                            content=Text("Configurações do app", size=16, weight=FontWeight.BOLD, color=colors.PRIMARY),
                            width=440,
                            padding=padding.only(bottom=0),
                            alignment=alignment.center,
                        ),
                        radio_align,
                        btn_save
                    ], horizontal_alignment=CrossAxisAlignment.CENTER
                )
            )
