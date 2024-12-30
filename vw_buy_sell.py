from flet import Page, View, AppBar, Text, IconButton, KeyboardType, DataTable, DataColumn, DataRow, DataCell, ScrollMode, Container, Icons, OutlinedButton, RadioGroup, Radio, FontWeight, TextField, Dropdown, dropdown, Colors, Column, Row, MainAxisAlignment, CrossAxisAlignment
from settings import read_pars, read_history
from binanceapi import read_wallet, read_cache, write_cache, update_wallet, update_history
from datetime import datetime


def view_buy_sell(page: Page):

    txt_title = Text("Compra e venda de cryptos - Cache: ", size=16,
                     weight=FontWeight.BOLD, color=Colors.PRIMARY)
    cache = read_cache()
    txt_cache = Text(value=cache, size=16, color=Colors.PRIMARY)
    tfd_cache = TextField(hint_text='Cache R$', width=200,
                          keyboard_type=KeyboardType.NUMBER, on_change=lambda e: on_change_cache(e))
    icon_edit = IconButton(Icons.EDIT, icon_size=16,
                           on_click=lambda e: edit_cache(e))
    icon_save = IconButton(Icons.CHECK, icon_size=16,
                           on_click=lambda e: save_cache(e))
    icon_cancel = IconButton(Icons.CANCEL, icon_size=16, icon_color=Colors.RED,
                             on_click=lambda e: cancel_cache(e))
    row_cache = Row([txt_cache, icon_edit])
    header = Row([
        txt_title,
        row_cache
    ],
        expand=True,
        alignment=MainAxisAlignment.CENTER
    )
    pars = read_pars()
    history_data_rows = DataTable(
        columns=[
            DataColumn(Text("Data")),
            DataColumn(Text("Tipo")),
            DataColumn(Text("Par")),
            DataColumn(Text("Quant."), numeric=True),
            DataColumn(Text("Preço unit."), numeric=True),
            DataColumn(Text("Preço médio"), numeric=True),
            DataColumn(Text("Acumulado"), numeric=True),
        ],
        rows=[]
    )
    dropdown_options = [dropdown.Option(text=option) for option in pars]
    dropdown_par = Dropdown(
        width=200,
        hint_text="Escolha um par",
        options=dropdown_options,
        on_change=lambda e: par_selected(e)
    )
    select_par = Row([dropdown_par],
                     expand=True,
                     alignment=MainAxisAlignment.CENTER
                     )
    tfd_quant = TextField(label='Quant', hint_text='Quant. em ADA', width=200)
    tfd_preco = TextField(label='Preço', hint_text='Preço unitário', width=200)
    txt_par = Text("Par:", size=14, weight=FontWeight.BOLD)
    txt_quant = Text("Quant:", size=14)
    txt_invest = Text("Invest:", size=14)
    txt_pmc = Text("PMC:", size=14)
    txt_ath = Text("0.0", size=14)
    txt_date = Text("0000-00-00", size=14)
    card_par = Container(
        content=Column([
            txt_par,
            txt_quant,
            txt_invest,
            txt_pmc,
            Row([txt_ath, txt_date])
        ], alignment=MainAxisAlignment.SPACE_AROUND))
    buy_sell = RadioGroup(content=Row([
        Radio(value="compra", label="Compra"),
        Radio(value="venda", label="Venda")]))
    buy_sell.value = "compra"

    btn_save = OutlinedButton(
        "Salvar",
        icon=Icons.SAVE,
        icon_color=Colors.PRIMARY,
        on_click=lambda e: save_wallet(e)
    )

    def on_change_cache(e):
        if not e.control.value.isdigit():
            e.control.value = ''.join(
                filter(lambda x: x.isdigit() or x in ',.', e.control.value))
            page.update()

    def edit_cache(e):
        cache = read_cache()
        tfd_cache.value = cache
        row_cache.controls = [tfd_cache, icon_save, icon_cancel]
        page.update()

    def save_cache(e):
        cache = tfd_cache.value
        # if '.' in cache:
        #     cache = cache.replace('.', ',')
        write_cache(cache)
        txt_cache.value = cache
        row_cache.controls = [txt_cache, icon_edit]
        page.update()

    def cancel_cache(e):
        row_cache.controls = [txt_cache, icon_edit]
        page.update()

    def par_selected(e):
        par = e.control.value
        wallet = read_wallet()
        data_par = [item for item in wallet if item['symbol'] == str(par)]
        if data_par:
            txt_par.value = str(f"Par: {data_par[0]['symbol']}")
            txt_quant.value = str(f"Quant: {data_par[0]['quant']}")
            txt_ath.value = str(data_par[0]['ATH'])
            txt_date.value = str(data_par[0]['date'])
            txt_invest.value = str(
                f"Invest: {float(data_par[0]['invest']):.2f}")
            pmc = float(data_par[0]['invest']) / float(data_par[0]['quant'])
            txt_pmc.value = str(
                f"PMC: {float(pmc):.2f}")
        else:
            txt_par.value = str(f"Par: {par}")
            txt_quant.value = str("Quant: 0.00")
            txt_invest.value = str("Invest: 0.00")
            txt_pmc.value = str("PMC: 0.00")
            txt_ath.value = ""
            txt_date.value = ""
        page.update()

    def save_wallet(e):
        if not tfd_quant.value or not tfd_preco.value or not buy_sell.value or txt_ath.value == "":
            return
        else:
            type = str(buy_sell.value)
            name = str(txt_par.value)
            quant = tfd_quant.value
            if ',' in quant:
                quant = quant.replace(',', '.')
            preco = tfd_preco.value
            if ',' in preco:
                preco = preco.replace(',', '.')
            ath = float(txt_ath.value)
            date = str(txt_date.value)
            valor = new_values(type, quant, preco)
            quant_new = valor[0]
            invest_new = valor[1]
            pmc_new = valor[2]
            txt_quant.value = f"Quant: {float(quant_new):.2f}"
            txt_invest.value = f"Invest: {float(invest_new):.2f}"
            txt_pmc.value = f"PMC: {float(pmc_new):.3f}"
            obj = {
                'symbol': name[5:],
                'quant': quant_new,
                'invest': invest_new,
                'ATH': ath,
                'date': date
            }
            data_atual = datetime.now()
            date = data_atual.strftime("%Y-%m-%d")
            data = {
                'date': date,
                'type': type,
                'symbol': name[5:],
                'quant': quant,
                'preco': preco,
                'pmc': f"{float(pmc_new):.4f}",
                'quant_new': quant_new
            }
            update_wallet(obj)
            update_history(data)
            dropdown_par.value = None
            tfd_preco.value = ''
            tfd_quant.value = ''
            page.update()
            pop_data_rows(None)

    def new_values(type, quant, preco):
        acomul = float(txt_quant.value[7:])
        invest = float(txt_invest.value[8:])
        total = float(quant) * float(preco)
        cache = read_cache()
        if ',' in cache:
            cache = cache.replace(',', '.')
        if type == 'compra':
            quant_new = float(quant) + acomul
            invest_new = (float(preco) * float(quant)) + invest
            pmc_new = invest_new / quant_new
            cache = float(cache) - total
        else:
            pmc_old = invest / acomul
            quant_new = acomul - float(quant)
            invest_new = invest - (float(pmc_old) * float(quant))
            pmc_new = pmc_old
            cache = float(cache) + total
        brl = str(f"{float(cache):.2f}")
        write_cache(brl)
        txt_cache.value = cache
        return quant_new, invest_new, pmc_new

    def pop_data_rows(e):
        history = read_history()
        if history:
            rows = []
            for item in history:
                data = DataRow(
                    cells=[
                        DataCell(Text(item['date'])),
                        DataCell(Text(item['type'])),
                        DataCell(Text(item['symbol'])),
                        DataCell(Text(item['quant'])),
                        DataCell(Text(item['preco'])),
                        DataCell(Text(item['pmc'])),
                        DataCell(Text(item['quant_new'])),
                    ]
                )
                rows.append(data)
            history_data_rows.rows = rows
            page.update()

    pop_data_rows(None)

    page.views.append(
        View(
            "/settings",
            [
                AppBar(title=Text("Compra e Venda"), center_title=True,
                       bgcolor=Colors.PRIMARY_CONTAINER),
                Container(
                    height=36,
                    content=Row([header],
                                expand=True,
                                alignment=MainAxisAlignment.CENTER
                                )),
                Container(
                    height=250,
                    content=Row([
                        Column([
                            select_par,
                            Row([tfd_quant],
                                expand=True,
                                alignment=MainAxisAlignment.CENTER
                                ),
                            Row([tfd_preco],
                                expand=True,
                                alignment=MainAxisAlignment.CENTER
                                ),
                            Row([buy_sell],
                                expand=True,
                                alignment=MainAxisAlignment.CENTER
                                )
                        ]
                        ),
                        Column([
                            Row([card_par],
                                expand=True,
                                alignment=MainAxisAlignment.CENTER
                                ),
                            Row([btn_save],
                                expand=True,
                                alignment=MainAxisAlignment.CENTER,
                                )
                        ]
                        )
                    ],
                        expand=True,
                        alignment=MainAxisAlignment.SPACE_AROUND
                    )),
                Container(
                    bgcolor=Colors.SECONDARY,
                    height=36,
                    content=Row([Text(value="HISTÓRICO", color=Colors.PRIMARY_CONTAINER, weight=FontWeight.BOLD, size=16)], expand=True,
                                alignment=MainAxisAlignment.CENTER)
                ),
                Row([
                    Column([
                        history_data_rows
                    ],
                        scroll=ScrollMode.ALWAYS,
                        alignment=MainAxisAlignment.SPACE_AROUND)
                ],
                    expand=True,
                    alignment=MainAxisAlignment.CENTER
                )
            ]
        )
    )
