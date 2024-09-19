from flet import Page, View, AppBar, Container, Column, Row, Text, IconButton, Icon, icons, FontWeight, colors, padding, alignment, CrossAxisAlignment, MainAxisAlignment
from binanceapi import data_objs, read_obj_list, read_wallet, read_dolar_now


def view_wallet(page: Page):
    
    btn_update = IconButton(icons.UPDATE, disabled=False, tooltip="Atualizar", on_click=lambda e: update_data(e), bgcolor=colors.PRIMARY, icon_color=colors.SECONDARY_CONTAINER)
    cont = Container(content=Text("Aguarde..."))
    total = Text("", size=16, weight=FontWeight.BOLD, color=colors.PRIMARY)
    
    def pop_col(e):
        pars = read_obj_list()
        assets = read_wallet()
        # usdt = read_dolar_now()
        # TUS = 0.0
        TBR = 0.0
        cols = []
        for asset in assets:
            rows = []
            for par in pars:
                if par["symbol"] == asset["symbol"]:
                    subtotal = float(par["bid"]) * float(asset["quant"])
                    TBR += subtotal
                    perc = ((subtotal / float(asset["invest"])) -1) * 100
                    rend = Text(f"{float(perc):.2f}", weight=FontWeight.BOLD)
                    rend.color = "green" if perc > 0 else "red"
                    medio = float(asset["invest"]) / float(asset["quant"])
                    target = float(asset["ATH"]) * float(asset["quant"])
                    target_perc = ((target / float(asset["invest"]))-1) * 100
                    
                    item0 = Row([Text(str(f"{asset["symbol"]}"), size=16, weight=FontWeight.BOLD, color=colors.PRIMARY)], wrap=True)
                    item1 = Row([Text(str(f"Quant: {asset["quant"]}"))], wrap=True)
                    item2 = Row([Text(str(f"Valor atual: R$ {float(par["bid"]):.2f}"))], wrap=True)
                    item3 = Row([Text(str(f"Total atual: R$ {float(subtotal):.2f}"))], wrap=True)
                    item4 = Row([Text(str(f"Valor médio: R$ {float(medio):.3f}"))], wrap=True)
                    item5 = Row([Text(str(f"Investimento: R$ {float(asset["invest"]):.2f}"))], wrap=True)
                    item6 = Row([Text("Rendimento: "), rend], wrap=True)
                    item7 = Row([Text(str(f"Máxima histórica: R$ {float(asset["ATH"]):.2f}"))], wrap=True)
                    item8 = Row([Text(str(f"Data: {asset["date"]}"))], wrap=True)
                    item9 = Row([Text(str(f"Meta: R$ {float(target):.2f} ({float(target_perc):.2f}%)"))], wrap=True)
                    
                    rows.append(item0)
                    rows.append(item1)
                    rows.append(item2)
                    rows.append(item3)
                    rows.append(item4)
                    rows.append(item5)
                    rows.append(item6)
                    rows.append(item7)
                    rows.append(item8)
                    rows.append(item9)
                    cols.append(Container(Column(rows, width=250), bgcolor=colors.PRIMARY_CONTAINER, padding=20))
        cont.content = Row(cols, width=600, wrap=True)
        total.value = f"R$ {float(TBR):.2f}"
        btn_update.disabled = False
        btn_update.bgcolor = colors.PRIMARY
        page.update()
        
    def update_data(e):
        btn_update.disabled = True
        btn_update.bgcolor = colors.GREY_200
        page.update()
        data_objs()
        pop_col(None)    

    pop_col(None)
    
    page.views.append(
        View(
            "/settings",
                    [
                        AppBar(title=Text("Carteira"), center_title=True, bgcolor=colors.PRIMARY_CONTAINER,
                               actions=[
                                   btn_update, Container(width=20)
                               ]
                               ),
                        Container(
                            content=Row([
                               Text("Total geral: ", size=16, weight=FontWeight.BOLD, color=colors.PRIMARY),
                               total 
                            ], width=440, alignment=MainAxisAlignment.CENTER),
                            padding=padding.only(bottom=0),
                            alignment=alignment.center,
                        ),
                        cont,
                    ], horizontal_alignment=CrossAxisAlignment.CENTER
                )
            )
