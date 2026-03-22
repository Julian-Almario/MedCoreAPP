import flet as ft
from modules.colors import *


def BallardScore():
    opciones_ballard = {
        "Postura": {
            "Flacido": -1,
            "Flexionado leve": 0,
            "Ligeramente flexionado": 1,
            "Moderamente Flexionado": 2,
            "Muy Flexionado": 3
        },

        "Muñeca": {
            ">90°": -1,
            "90°": 0,
            "60°": 1,
            "45°": 2,
            "30°": 3,
            "0°": 4
        },

        "Retroceso del brazo": {
            "180°": -1,
            "140-180°": 0,
            "110-140°": 1,
            "90-110°": 2,
            "<90°": 3
        },

        "Angulo popliteo": {
            "180°": -1,
            "160°": 0,
            "140°": 1,
            "120°": 2,
            "100°": 3,
            "90°": 4,
            "<90°": 5
        },

        "Signo de la bufanda": {
            "Sobrepasa la linea media": -1,
            "Sobrepasa la linea media flexionada": 0,
            "En la linea axilar": 1,
            "En la linea media": 2,
            "No sobrepasa la linea media": 3,
            "No sobrepasa la liena axilar": 4
        },

        "Talon - Oreja": {
            "Pie alcanza oreja facilmente": -1,
            "Pie cerca de la oreja": 0,
            "Resistencia moderada": 1,
            "Resistencia buena": 2,
            "Pie lejos de la oreja": 3,
            "Fuerte resistencia": 4
        }
    }

    selectores = {}

    for criterio, opciones in opciones_ballard.items():
        selectores[criterio] = ft.Dropdown(
            label=criterio,
            width=400,
            options=[ft.dropdown.Option(o) for o in opciones.keys()],
        )

    resultado_ballard = ft.Text(
        "Puntaje total: -",
        text_align=ft.TextAlign.CENTER,
        color=TEXT_COLOR
    )

    interpretacion_ballard = ft.Text(
        "Edad gestacional estimada: -",
        text_align=ft.TextAlign.CENTER,
        color=TEXT_COLOR
    )

    def calcular_ballard(e):

        total = 0
        completos = True

        for criterio, dropdown in selectores.items():
            if dropdown.value is None:
                completos = False
                continue
            total += opciones_ballard[criterio][dropdown.value]

        if not completos:
            resultado_ballard.value = "Puntaje total: -"
            interpretacion_ballard.value = "Edad gestacional estimada: -"
            resultado_ballard.update()
            interpretacion_ballard.update()
            return

        semanas = 24 + (total * 0.4)

        # Clasificación clínica
        if semanas < 37:
            clasificacion = "Pretérmino"
            color = "orange"
        elif 37 <= semanas <= 42:
            clasificacion = "A término"
            color = "green"
        else:
            clasificacion = "Postérmino"
            color = "red"

        resultado_ballard.value = f"Puntaje total: {total}"
        interpretacion_ballard.value = f"Edad gestacional: {semanas:.1f} semanas ({clasificacion})"

        resultado_ballard.color = color
        interpretacion_ballard.color = color

        resultado_ballard.update()
        interpretacion_ballard.update()

    for dropdown in selectores.values():
        dropdown.on_change = calcular_ballard


    panel_ref = ft.Ref[ft.ExpansionPanel]()
    panel_list_ref = ft.Ref[ft.ExpansionPanelList]()

    def on_expand_change(e):
        panel = panel_ref.current
        is_expanded = panel.expanded
        panel.bgcolor = SECONDARY_COLOR if is_expanded else PRIMARY_COLOR
        panel.update()

        if not is_expanded:
            for d in selectores.values():
                d.value = None
                d.update()
            resultado_ballard.value = "Puntaje total: -"
            interpretacion_ballard.value = "Edad gestacional estimada: -"
            resultado_ballard.update()
            interpretacion_ballard.update()

    return ft.ExpansionPanelList(
        ref=panel_list_ref,
        on_change=on_expand_change,
        expand_icon_color=TEXT_COLOR,
        elevation=8,
        divider_color=TEXT_COLOR,
        controls=[
            ft.ExpansionPanel(
                ref=panel_ref,
                header=ft.ListTile(
                    title=ft.Text("Ballard Score", color=TEXT_COLOR),
                    subtitle=ft.Text(
                        "Evaluación madurez neonatal",
                        size=SUBTITLE_SIZE,
                        color=TEXT_COLOR
                    )
                ),
                content=ft.Container(
                    content=ft.Column(
                        controls=list(selectores.values()) +
                        [resultado_ballard, interpretacion_ballard],
                        spacing=10,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER
                    ),
                    padding=ft.padding.symmetric(vertical=25, horizontal=50),
                    alignment=ft.alignment.center
                ),
                bgcolor=PRIMARY_COLOR,
                expanded=False,
            )
        ],
    )
