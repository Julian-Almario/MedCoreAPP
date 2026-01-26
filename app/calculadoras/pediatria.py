import flet as ft
from modules.colors import *


def BallardScore():

    edad_neonato = ft.TextField(
        label="Semanas",
        hint_text="Ej: 10",
        keyboard_type=ft.KeyboardType.NUMBER,
        text_align=ft.TextAlign.CENTER,
        width=400
    )

    opciones_ballard = {
        "Postura": ["N/A","Flacido", "Flexionado leve", "Ligeramente flexionado", "Moderamente Flexionado", "Muy Flexionado"],
        "Muñeca": [">90°", "90°", "60°", "45°", "30°", "0°"],
        "Retroceso del brazo": ["N/A", "180°", "140-180°", "110-140°", "90-110°", "<90°"],
        "Angulo popliteo": ["180°", "160°", "140°", "120°", "100°", "90°", "<90°"],
        "Signo de la bufanda": ["Sobrepasa la linea media", "Sobrepasa la linea media flexionada", "En la linea axilar", "En la linea media", "No sobrepasa la linea media", "No sobrepasa la liena axilar"],

        }
    # Mapeo de puntajes según índice en la lista
    selectores = {}
    for criterio, opciones in opciones_ballard.items():
        selectores[criterio] = ft.Dropdown(
            options=[ft.dropdown.Option(opcion) for opcion in opciones],
            label=criterio,
            width=400,
        )

    resultado_ballard = ft.Text("Puntaje total: -", text_align=ft.TextAlign.CENTER, color=TEXT_COLOR)
    interpretacion_ballard = ft.Text("Interpretación: -", text_align=ft.TextAlign.CENTER, color=TEXT_COLOR)

    def calcular_ballard(e):
        puntaje = -1

        for criterio, dropdown in selectores.items():
            if dropdown.value is None:
                continue
            opciones = opciones_ballard[criterio]
            indice = opciones.index(dropdown.value)
            puntaje += indice

        if puntaje == 0:
            interpretacion = "Sin impacto"
            color = "grey"
        elif 1 >= puntaje <= 4:
            interpretacion = "Impacto menor"
            color = "green"
        elif 5 >= puntaje <= 15:
            interpretacion = "Impacto moderado"
            color = "orange"
        elif 16 >= puntaje <= 20:
            interpretacion = "Impacto moderado --> severo"
            color = "orange"
        else:
            interpretacion = "Impacto severo"
            color = "red"
        resultado_ballard.value = f"Puntaje total: {puntaje}"
        interpretacion_ballard.value = f"Interpretación: {interpretacion}"
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
            interpretacion_ballard.value = "Interpretación: -"
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
                    title=ft.Text("Ballard Score (EXPERIMENTAL)", color=TEXT_COLOR),
                    subtitle=ft.Text("Evaluación madurez neonatal", size=SUBTITLE_SIZE, color=TEXT_COLOR)
                ),
                content=ft.Container(
                    content=ft.Column(
                        controls=list(selectores.values()) + [edad_neonato, resultado_ballard, interpretacion_ballard],
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