import flet as ft
from modules.colors import *

# Constantes de líquidos en adultos (ml/kg/día)
BASAL_RESTRICTIVO = 25
BASAL_NORMAL = 42
BASAL_TERCER_ESPACIO = 60

# Bolo de líquidos (ml/kg)
BOLO_RESTRICTIVO = 25
BOLO_NORMAL = 40

# Mantenimiento pediátrico (ml/kg/día)
PED_RN = 120
PED_0_10 = 100
PED_10_20 = 50
PED_MAYOR_20 = 25

# Bolo de choque (ml/kg)
PED_BOLO_RESTRICTIVO_MIN = 20
PED_BOLO_RESTRICTIVO_MAX = 30
PED_BOLO_NORMAL_MIN = 30
PED_BOLO_NORMAL_MAX = 50

# Deshidratación
DHT_FACTORES = {
    "DHT I (5%)": 0.05,
    "DHT II (10%)": 0.10,
    "DHT III (15%)": 0.15,
    "DHT IV (20%)": 0.20,
}



def liquidos_adultos():
    peso_field = ft.TextField(
        label="Peso del paciente (kg)",
        hint_text="Ej: 70",
        keyboard_type=ft.KeyboardType.NUMBER,
        text_align=ft.TextAlign.CENTER,
        width=250
    )

    tipo_paciente = ft.Dropdown(
        label="Tipo de paciente",
        width=250,
        options=[
            ft.dropdown.Option("Restrictivo"),
            ft.dropdown.Option("Normal"),
            ft.dropdown.Option("Tercer espacio"),
        ],
        value="Normal"
    )

    resultado_basal = ft.Text(
        "Líquidos basales: -",
        style=ft.TextThemeStyle.HEADLINE_SMALL,
        color=TEXT_COLOR,
        text_align=ft.TextAlign.CENTER
    )

    resultado_bolo = ft.Text(
        "Bolo sugerido: -",
        style=ft.TextThemeStyle.TITLE_MEDIUM,
        color=TEXT_COLOR,
        text_align=ft.TextAlign.CENTER
    )

    formula_text = ft.Text(
        "",
        color=TEXT_COLOR,
        size=14,
        text_align=ft.TextAlign.CENTER
    )

    def calcular_liquidos(e=None):
        try:
            peso = float(peso_field.value)

            if tipo_paciente.value == "Restrictivo":
                basal_ml = peso * BASAL_RESTRICTIVO
                bolo_ml = peso * BOLO_RESTRICTIVO
                factor = BASAL_RESTRICTIVO

            elif tipo_paciente.value == "Tercer espacio":
                basal_ml = peso * BASAL_TERCER_ESPACIO
                bolo_ml = peso * BOLO_NORMAL
                factor = BASAL_TERCER_ESPACIO

            else:  # Normal
                basal_ml = peso * BASAL_NORMAL
                bolo_ml = peso * BOLO_NORMAL
                factor = BASAL_NORMAL

            resultado_basal.value = f"Líquidos basales: {basal_ml:.0f} ml/día"
            resultado_bolo.value = f"Bolo sugerido: {bolo_ml:.0f} ml"
            formula_text.value = f"Fórmula: {peso} kg x {factor} ml/kg"

        except ValueError:
            resultado_basal.value = "Líquidos basales: -"
            resultado_bolo.value = "Bolo sugerido: -"
            formula_text.value = ""

        resultado_basal.update()
        resultado_bolo.update()
        formula_text.update()

    peso_field.on_change = calcular_liquidos
    tipo_paciente.on_change = calcular_liquidos

    panel_ref = ft.Ref[ft.ExpansionPanel]()
    panel_list_ref = ft.Ref[ft.ExpansionPanelList]()

    def on_expand_change(e):
        panel = panel_ref.current
        is_expanded = panel.expanded
        panel.bgcolor = SECONDARY_COLOR if is_expanded else PRIMARY_COLOR
        panel.update()
        if not is_expanded:
            peso_field.value = ""
            tipo_paciente.value = "Normal"
            resultado_basal.value = "Líquidos basales: -"
            resultado_bolo.value = "Bolo sugerido: -"
            formula_text.value = ""
            peso_field.update()
            tipo_paciente.update()
            resultado_basal.update()
            resultado_bolo.update()
            formula_text.update()

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
                    title=ft.Text("líquidos en adultos (EXPERIMENTAL)", color=TEXT_COLOR)
                ),
                content=ft.Container(
                    content=ft.Column(
                        controls=[
                            peso_field,
                            tipo_paciente,
                            ft.Divider(),
                            resultado_basal,
                            resultado_bolo,
                            formula_text,
                        ],
                        spacing=12,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER
                    ),
                    padding=ft.padding.all(15)
                ),
                bgcolor=PRIMARY_COLOR,
                expanded=False,
            )
        ],
    )

def liquidos_pediatria():

    # -------- INPUTS --------
    peso_field = ft.TextField(
        label="Peso del niño (kg)",
        hint_text="Ej: 12",
        keyboard_type=ft.KeyboardType.NUMBER,
        text_align=ft.TextAlign.CENTER,
        width=250
    )

    edad_dias_field = ft.TextField(
        label="Edad (días)",
        hint_text="Ej: 10",
        keyboard_type=ft.KeyboardType.NUMBER,
        text_align=ft.TextAlign.CENTER,
        width=250
    )

    tipo_paciente = ft.Dropdown(
        label="Tipo de paciente",
        width=250,
        options=[
            ft.dropdown.Option("Restrictivo"),
            ft.dropdown.Option("Normal"),
        ],
        value="Normal"
    )

    grado_dht = ft.Dropdown(
        label="Grado de deshidratación",
        width=250,
        options=[
            ft.dropdown.Option("Sin deshidratación"),
            ft.dropdown.Option("DHT I (5%)"),
            ft.dropdown.Option("DHT II (10%)"),
            ft.dropdown.Option("DHT III (15%)"),
            ft.dropdown.Option("DHT IV (20%)"),
        ],
        value="Sin deshidratación"
    )

    # -------- RESULTADOS --------
    mantenimiento_text = ft.Text(
        "Mantenimiento: -",
        style=ft.TextThemeStyle.HEADLINE_SMALL,
        color=TEXT_COLOR,
        text_align=ft.TextAlign.CENTER
    )

    deficit_text = ft.Text(
        "Déficit por DHT: -",
        style=ft.TextThemeStyle.TITLE_MEDIUM,
        color=TEXT_COLOR,
        text_align=ft.TextAlign.CENTER
    )

    tiempo_text = ft.Text(
        "Tiempo de reposición: -",
        style=ft.TextThemeStyle.TITLE_MEDIUM,
        color=TEXT_COLOR,
        text_align=ft.TextAlign.CENTER
    )

    bolo_text = ft.Text(
        "Bolo inicial: -",
        style=ft.TextThemeStyle.TITLE_MEDIUM,
        color=TEXT_COLOR,
        text_align=ft.TextAlign.CENTER
    )

    soluciones_text = ft.Text(
        "",
        color=TEXT_COLOR,
        size=14,
        text_align=ft.TextAlign.CENTER
    )

    def calcular_liquidos(e=None):
        try:
            peso = float(peso_field.value)
            edad_dias = int(edad_dias_field.value)

            # ---- MANTENIMIENTO ----
            if edad_dias <= 7:
                mantenimiento = peso * PED_RN
                regla = "RN: 120 ml/kg/día"
            elif peso <= 10:
                mantenimiento = peso * PED_0_10
                regla = "0–10 kg: 100 ml/kg/día"
            elif peso <= 20:
                mantenimiento = (10 * PED_0_10) + ((peso - 10) * PED_10_20)
                regla = "100/50"
            else:
                mantenimiento = (
                    (10 * PED_0_10)
                    + (10 * PED_10_20)
                    + ((peso - 20) * PED_MAYOR_20)
                )
                regla = "100/50/25"

            # ---- DÉFICIT ----
            if grado_dht.value in DHT_FACTORES:
                deficit = peso * 1000 * DHT_FACTORES[grado_dht.value]
                horas = list(DHT_FACTORES.keys()).index(grado_dht.value) * 4
            else:
                deficit = 0
                horas = 0

            # ---- BOLO ----
            if tipo_paciente.value == "Restrictivo":
                bolo = f"{peso * PED_BOLO_RESTRICTIVO_MIN:.0f} – {peso * PED_BOLO_RESTRICTIVO_MAX:.0f} ml"
            else:
                bolo = f"{peso * PED_BOLO_NORMAL_MIN:.0f} – {peso * PED_BOLO_NORMAL_MAX:.0f} ml"

            # ---- TEXTOS ----
            mantenimiento_text.value = f"Mantenimiento: {mantenimiento:.0f} ml/día"
            deficit_text.value = f"Déficit por DHT: {deficit:.0f} ml"
            tiempo_text.value = f"Reposición en: {horas} horas"
            bolo_text.value = f"Bolo inicial: {bolo}"

            soluciones_text.value = (
                "• Iniciar con SSN 0.9%\n"
                "• Luego Lactato Ringer\n"
                "• Si no responde → Coloides 2–4 cc/kg (máx 3 dosis)\n"
                "• SSN 3%: 2–4 cc/kg por dosis (máx 3 dosis)"
            )

        except ValueError:
            mantenimiento_text.value = "Mantenimiento: -"
            deficit_text.value = "Déficit por DHT: -"
            tiempo_text.value = "Reposición en: -"
            bolo_text.value = "Bolo inicial: -"
            soluciones_text.value = ""

        mantenimiento_text.update()
        deficit_text.update()
        tiempo_text.update()
        bolo_text.update()
        soluciones_text.update()

    # Eventos
    peso_field.on_change = calcular_liquidos
    edad_dias_field.on_change = calcular_liquidos
    tipo_paciente.on_change = calcular_liquidos
    grado_dht.on_change = calcular_liquidos

    panel_ref = ft.Ref[ft.ExpansionPanel]()
    panel_list_ref = ft.Ref[ft.ExpansionPanelList]()

    def on_expand_change(e):
        panel = panel_ref.current
        is_expanded = panel.expanded
        panel.bgcolor = SECONDARY_COLOR if is_expanded else PRIMARY_COLOR
        panel.update()

        if not is_expanded:
            peso_field.value = ""
            edad_dias_field.value = ""
            tipo_paciente.value = "Normal"
            grado_dht.value = "Sin deshidratación"

            mantenimiento_text.value = "Mantenimiento: -"
            deficit_text.value = "Déficit por DHT: -"
            tiempo_text.value = "Reposición en: -"
            bolo_text.value = "Bolo inicial: -"
            soluciones_text.value = ""

            peso_field.update()
            edad_dias_field.update()
            tipo_paciente.update()
            grado_dht.update()
            mantenimiento_text.update()
            deficit_text.update()
            tiempo_text.update()
            bolo_text.update()
            soluciones_text.update()


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
                    title=ft.Text("Reposición de líquidos en niños (EXPERIMENTAL)", color=TEXT_COLOR)
                ),
                content=ft.Container(
                    content=ft.Column(
                        controls=[
                            peso_field,
                            edad_dias_field,
                            tipo_paciente,
                            grado_dht,

                            mantenimiento_text,
                            deficit_text,
                            tiempo_text,
                            bolo_text,

                            ft.Divider(),
                            soluciones_text,
                        ],
                        spacing=12,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER
                    ),
                    padding=ft.padding.all(15)
                ),
                bgcolor=PRIMARY_COLOR,
                expanded=False,
            )
        ],
    )
