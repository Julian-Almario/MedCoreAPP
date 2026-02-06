import flet as ft
from modules.colors import *

def tg18_colangitis():

    criterios_A = [
        ("Fiebre o escalofríos", 1),
        ("Respuesta inflamatoria en laboratorio", 1)
    ]

    criterios_B = [
        ("Ictericia", 1),
        ("Pruebas hepáticas colestásicas alteradas", 1)
    ]

    criterios_C = [
        ("Dilatación vía biliar en imagen", 1),
        ("Cálculo / estenosis / stent en imagen", 1)
    ]

    criterios_moderado = [
        ("Leucocitos >12,000 o <4,000", 1),
        ("Fiebre ≥39 °C", 1),
        ("Edad ≥75 años", 1),
        ("Bilirrubina total ≥5 mg/dl", 1),
        ("Albúmina <0.7 del normal", 1)
    ]

    A_checks, B_checks, C_checks = [], [], []
    moderate_checks = []

    severe_selector = ft.Checkbox(value=False)

    severe_list = ft.Text(
        "1. Hypotension requiring vasopressors\n"
        "2. Disturbance of consciousness\n"
        "3. PaO2/FiO2 < 300\n"
        "4. Oliguria or creatinine > 2 mg/dl\n"
        "5. INR > 1.5\n"
        "6. Platelet count < 100,000",
        size=15,
        color=TEXT_COLOR
    )

    dx_text = ft.Text(
        "Diagnóstico TG18: -",
        style=ft.TextThemeStyle.TITLE_MEDIUM,
        color=TEXT_COLOR,
        text_align=ft.TextAlign.CENTER
    )

    sev_text = ft.Text(
        "Severidad: -",
        style=ft.TextThemeStyle.HEADLINE_SMALL,
        color=TEXT_COLOR,
        text_align=ft.TextAlign.CENTER
    )

    plan_text = ft.Text(
        "Conducta: -",
        style=ft.TextThemeStyle.TITLE_MEDIUM,
        color=TEXT_COLOR,
        text_align=ft.TextAlign.CENTER
    )

    def calcular(e=None):

        A = any(cb.value for cb,_ in A_checks)
        B = any(cb.value for cb,_ in B_checks)
        C = any(cb.value for cb,_ in C_checks)

        severe = severe_selector.value
        moderate = sum(1 for cb,_ in moderate_checks if cb.value)

        if A and B and C:
            dx = "Diagnóstico definitivo"
        elif A and (B or C):
            dx = "Sospecha diagnóstica"
        else:
            dx = "No cumple criterios"

        if severe:
            grade = "Grade III (Severa)"
            color = "red"
            plan = "Soporte orgánico + ATB IV + drenaje biliar URGENTE"
        elif moderate >= 2:
            grade = "Grade II (Moderada)"
            color = "orange"
            plan = "ATB IV + drenaje biliar temprano"
        else:
            grade = "Grade I (Leve)"
            color = "green"
            plan = "ATB IV + soporte. Drenaje si no mejora"

        dx_text.value = f"Diagnóstico TG18: {dx}"
        sev_text.value = f"Severidad: {grade}"
        sev_text.color = color
        plan_text.value = f"Conducta: {plan}"

        dx_text.update()
        sev_text.update()
        plan_text.update()

    severe_selector.on_change = calcular

    def construir(criterios, lista):
        filas = []
        for texto,_ in criterios:
            chk = ft.Checkbox(value=False, on_change=calcular)
            lista.append((chk,1))
            filas.append(
                ft.Row(
                    [
                        ft.Container(ft.Text(texto, color=TEXT_COLOR), expand=True),
                        ft.Container(chk)
                    ],
                    height=32
                )
            )
        return filas

    panel_ref = ft.Ref[ft.ExpansionPanel]()

    def on_expand(e):
        p = panel_ref.current
        p.bgcolor = SECONDARY_COLOR if p.expanded else PRIMARY_COLOR
        p.update()

        if not p.expanded:
            for group in [A_checks, B_checks, C_checks, moderate_checks]:
                for cb,_ in group:
                    cb.value = False
                    cb.update()

            severe_selector.value = False
            severe_selector.update()

            dx_text.value = "Diagnóstico TG18: -"
            sev_text.value = "Severidad: -"
            plan_text.value = "Conducta: -"
            dx_text.update()
            sev_text.update()
            plan_text.update()


    severe_row = ft.Row(
        [
            ft.Container(
                ft.Text(
                    "¿El paciente tiene alguna de estas 6 condiciones?",
                    color=TEXT_COLOR
                ),
                expand=True
            ),
            ft.Container(severe_selector)
        ],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN
    )

    return ft.ExpansionPanelList(
        on_change=on_expand,
        expand_icon_color=TEXT_COLOR,
        elevation=8,
        controls=[
            ft.ExpansionPanel(
                ref=panel_ref,
                header=ft.ListTile(
                    title=ft.Text("Colangitis Aguda TG18", color=TEXT_COLOR),
                    subtitle=ft.Text(
                        "Diagnóstico + Severidad + Conducta",
                        size=SUBTITLE_SIZE,
                        color=TEXT_COLOR
                    )
                ),
                bgcolor=PRIMARY_COLOR,
                content=ft.Container(
                    padding=ft.padding.symmetric(25,45),
                    content=ft.Column(
                        [
                            ft.Text("Criterios Diagnósticos", weight="bold", color=TEXT_COLOR),

                            ft.Text("Inflamación sistémica (A)", weight="bold", color=TEXT_COLOR),
                            *construir(criterios_A, A_checks),

                            ft.Text("Colestasis (B)", weight="bold", color=TEXT_COLOR),
                            *construir(criterios_B, B_checks),

                            ft.Text("Imagen (C)", weight="bold", color=TEXT_COLOR),
                            *construir(criterios_C, C_checks),

                            ft.Divider(),

                            ft.Text("Criterios de severidad", weight="bold", color=TEXT_COLOR),
                            severe_row,
                            severe_list,
                            ft.Divider(),

                            *construir(criterios_moderado, moderate_checks),
                            ft.Divider(),

                            dx_text,
                            sev_text,
                            plan_text
                        ],
                        spacing=10,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER
                    )
                )
            )
        ]
    )
