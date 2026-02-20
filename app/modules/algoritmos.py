import os
import flet as ft
import re

RUTA_NOTAS = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data", "guias"))
os.makedirs(RUTA_NOTAS, exist_ok=True)


def listar_notas():
    return [f for f in os.listdir(RUTA_NOTAS) if f.lower().endswith(".md")]


def algoritmos_page(page: ft.Page):

    lista_notas = ft.Column(spacing=10, expand=True)
    mostrar_barra = True
    current_view = "notas"
    layout_principal = ft.Column(expand=True)

    search_bar = ft.TextField(
        label="Buscar algoritmos...",
        on_change=lambda e: filter_current_value(e),
        border=ft.InputBorder.UNDERLINE,
        border_color=ft.Colors.OUTLINE,
        bgcolor=ft.Colors.TRANSPARENT,
        filled=False,
        dense=True,
        content_padding=ft.padding.symmetric(horizontal=12, vertical=10),
        expand=True,
    )

    def construir_appbar(titulo_actual=""):

        if current_view == "nota":
            return ft.AppBar(
                toolbar_height=70,
                leading=ft.IconButton(
                    ft.Icons.ARROW_BACK,
                    tooltip="Volver",
                    on_click=lambda e: mostrar_lista()
                ),
                leading_width=50,
                title=ft.Text(titulo_actual),
                center_title=False,
                bgcolor=ft.Colors.TRANSPARENT,
            )

        else:
            return ft.AppBar(
                toolbar_height=70,
                leading_width=50,
                title=ft.Container(
                    content=search_bar,
                    padding=ft.padding.symmetric(horizontal=40),
                ),
                center_title=False,
                bgcolor=ft.Colors.TRANSPARENT,
            )

    def filter_current_value(_e=None):
        valor = (search_bar.value or "").strip()
        construir_notas(valor)
        page.update()

    def mostrar_lista():
        nonlocal mostrar_barra, current_view
        mostrar_barra = True
        current_view = "notas"
        construir_notas()
        actualizar_layout("")

    def pretty_title(filename: str) -> str:
        root = os.path.splitext(filename)[0]
        return re.sub(r'[_]+', ' ', root).strip()

    def construir_notas(filtro=""):

        lista_notas.controls.clear()
        archivos = listar_notas()
        filtro = (filtro or "").lower()
        encontrados = False

        if not archivos:
            lista_notas.controls.append(
                ft.Container(
                    content=ft.Text(
                        "No tienes notas. Crea una nueva nota.",
                        size=16,
                        color=ft.Colors.OUTLINE,
                        text_align=ft.TextAlign.CENTER
                    ),
                    alignment=ft.alignment.center,
                    height=120
                )
            )
            return

        for archivo in sorted(archivos, key=lambda x: x.lower()):

            nombre_sin_ext = os.path.splitext(archivo)[0]
            nombre_busqueda = re.sub(r'[_]+', ' ', nombre_sin_ext).lower()

            if filtro and filtro not in nombre_busqueda:
                continue

            card = ft.Card(
                content=ft.Container(
                    content=ft.Row(
                        controls=[
                            ft.Text(pretty_title(archivo), size=18),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    padding=20,
                    height=80,
                    alignment=ft.alignment.center,
                    on_click=lambda e, a=archivo: ver_nota(a),
                ),
                margin=ft.margin.symmetric(vertical=8, horizontal=16),
                elevation=2,
            )

            lista_notas.controls.append(card)
            encontrados = True

        if not encontrados:
            lista_notas.controls.append(
                ft.Container(
                    content=ft.Text(
                        "No hay notas que coincidan con la búsqueda.",
                        size=16,
                        color=ft.Colors.OUTLINE,
                        text_align=ft.TextAlign.CENTER
                    ),
                    alignment=ft.alignment.center,
                    height=120
                )
            )
    def ver_nota(nombre_md):

        nonlocal mostrar_barra, current_view

        mostrar_barra = False
        current_view = "nota"

        ruta_md = os.path.join(RUTA_NOTAS, nombre_md)

        try:
            with open(ruta_md, "r", encoding="utf-8") as f:
                contenido = f.read()
        except Exception:
            contenido = "No se pudo cargar la nota."

        lista_notas.controls.clear()

        titulo = pretty_title(nombre_md)

        lista_notas.controls.extend([
            ft.Container(
                ft.Markdown(
                    contenido,
                    selectable=True,
                    extension_set=ft.MarkdownExtensionSet.GITHUB_WEB,
                    expand=True,
                    auto_follow_links=True,
                ),
                expand=True,
                padding=ft.padding.all(30),
            ),
        ])

        actualizar_layout(titulo)

    area_notas_scroll = ft.Container(
        expand=True,
        content=ft.ListView(
            controls=[lista_notas],
            expand=True,
            padding=ft.padding.symmetric(horizontal=10, vertical=5),
        ),
    )

    def actualizar_layout(titulo=""):

        layout_principal.controls.clear()

        page.appbar = construir_appbar(titulo)

        layout_principal.controls.append(area_notas_scroll)

        page.update()

    construir_notas()
    actualizar_layout("")

    
    return layout_principal