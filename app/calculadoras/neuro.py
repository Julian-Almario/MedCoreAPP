import flet as ft
from modules.colors import *

def NIHSS():
    opciones_NIHSS = {
        "Nivel de conciencia": ["Alerta y responsive", "Excitable a una estimulación menor", "Excitable solo a la estimulación dolorosa", "Respuestas inexusuosas o reflejas"],
        "Preguntar mes y edad": ["Ambos correctos", "Una correcta", "Ninguna correcta"],
        "Cierre de ojos y Apretar manos": ["Ambos correctos", "Una correcta", "Ninguna correcta"],
        "Mirada conjugada": ["Normal", "Desviasion parcial", "Desviación forzada"],
        "Campos visuales": ["Normal", "Hemianopsia parcial", "Hemianopsia completa", "Hemianopsia Bilateral"],
        "Paralisis facial": ["Simetrico", "Paralisis menor", "Paralisis parcial", "Paralisis completa"],
        "Miembros superiores derecho": ["Normal/imposible comprobar", "Deriva", "Algun esfuerzo contra la gravedad", "Sin contra la gravedad" , "Sin movimiento"],
        "Miembros superiores izquierdo": ["Normal/imposible comprobar", "Deriva", "Algun esfuerzo contra la gravedad", "Sin contra la gravedad" , "Sin movimiento"],
        "Miembros inferior derecho": ["Normal/imposible comprobar", "Deriva", "Algun esfuerzo contra la gravedad", "Sin contra la gravedad" , "Sin movimiento"],
        "Miembros inferior izquierdo": ["Normal/imposible comprobar", "Deriva", "Algun esfuerzo contra la gravedad", "Sin contra la gravedad" , "Sin movimiento"],
        "Ataxia": ["Ninguna", "Una extremidad", "Dos extremidades"],
        "Afasia": ["Sin afasia", "Afasia leve-moderada", "Afasia grave", "Sin produccion del habla"],
        "Disartria": ["Ninguno/intubado o imposibilidad para la pruba", "Leve", "Grave"],
        "Atención": ["Normal", "Falta de atencion a estimulos bilateral en una modalidad sensorial", "Falta de atención hemisférica grave o falta de atención hemisférica ante más de una modalidad"],
        }
    # Mapeo de puntajes según índice en la lista
    selectores = {}
    for criterio, opciones in opciones_NIHSS.items():
        selectores[criterio] = ft.Dropdown(
            options=[ft.dropdown.Option(opcion) for opcion in opciones],
            label=criterio,
            width=400,
        )

    resultado_NIHSS = ft.Text("Puntaje total: -", text_align=ft.TextAlign.CENTER, color=TEXT_COLOR)
    interpretacion_NIHSS = ft.Text("Interpretación: -", text_align=ft.TextAlign.CENTER, color=TEXT_COLOR)

    def calcular_NIHSS(e):
        puntaje = 0

        for criterio, dropdown in selectores.items():
            if dropdown.value is None:
                continue
            opciones = opciones_NIHSS[criterio]
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
        resultado_NIHSS.value = f"Puntaje total: {puntaje}"
        interpretacion_NIHSS.value = f"Interpretación: {interpretacion}"
        resultado_NIHSS.color = color
        interpretacion_NIHSS.color = color

        resultado_NIHSS.update()
        interpretacion_NIHSS.update()

    for dropdown in selectores.values():
        dropdown.on_change = calcular_NIHSS

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
            resultado_NIHSS.value = "Puntaje total: -"
            interpretacion_NIHSS.value = "Interpretación: -"
            resultado_NIHSS.update()
            interpretacion_NIHSS.update()

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
                    title=ft.Text("NIHSS score", color=TEXT_COLOR),
                    subtitle=ft.Text("Evaluación neurologica", size=SUBTITLE_SIZE, color=TEXT_COLOR)
                ),
                content=ft.Container(
                    content=ft.Column(
                        controls=list(selectores.values()) + [resultado_NIHSS, interpretacion_NIHSS],
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