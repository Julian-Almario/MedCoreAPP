import os
import flet as ft
import re

RUTA_NOTAS = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "data", "guias")
)
os.makedirs(RUTA_NOTAS, exist_ok=True)


def listar_notas():
    return [f for f in os.listdir(RUTA_NOTAS) if f.lower().endswith(".md")]


def algoritmos_and_note_page(page: ft.Page):

    lista_notas = ft.Column(spacing=10, expand=True)
    mostrar_barra = True
    current_view = "notas"
    layout_principal = ft.Column(expand=True)

    editor_title = None
    editor_content = None
    archivo_editando = None

    search_bar = ft.TextField(
        label="Buscar algoritmos...",
        on_change=lambda e: filter_current_value(),
        border=ft.InputBorder.UNDERLINE,
        border_color=ft.Colors.OUTLINE,
        bgcolor=ft.Colors.TRANSPARENT,
        filled=False,
        dense=True,
        content_padding=ft.padding.symmetric(horizontal=12, vertical=10),
        expand=True,
    )

    def slugify(text: str) -> str:
        text = text.strip()  # ❌ ya no forzamos a lower()
        text = re.sub(r"[^\w\s-]", "", text)
        text = re.sub(r"[\s]+", "_", text)
        return text or "nota"

    def pretty_title(filename: str) -> str:
        root = os.path.splitext(filename)[0]
        return re.sub(r'[_]+', ' ', root).strip()

    def filter_current_value():
        valor = (search_bar.value or "").strip()
        construir_notas(valor)
        page.update()

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

        lista_notas.controls.append(
            ft.Container(
                ft.Markdown(
                    contenido,
                    selectable=True,
                    extension_set=ft.MarkdownExtensionSet.GITHUB_WEB,
                    auto_follow_links=True,
                ),
                expand=True,
                padding=ft.padding.all(30),
            )
        )

        actualizar_layout(titulo, nombre_md)

    def abrir_editor(nombre_md=None):

        nonlocal current_view, editor_title, editor_content, archivo_editando

        current_view = "editor"
        archivo_editando = nombre_md

        titulo_val = ""
        contenido_val = ""

        if nombre_md:
            ruta = os.path.join(RUTA_NOTAS, nombre_md)
            try:
                titulo_val = pretty_title(nombre_md)
                with open(ruta, "r", encoding="utf-8") as f:
                    contenido_val = f.read()
            except Exception:
                pass

        editor_title = ft.TextField(
            label="Título",
            value=titulo_val,
            text_size=22,
        )

        editor_content = ft.TextField(
            label="Contenido (Markdown)",
            value=contenido_val,
            multiline=True,
            expand=True,
        )

        lista_notas.controls.clear()
        lista_notas.controls.extend([
            ft.Container(editor_title, padding=20),
            ft.Container(editor_content, padding=20, expand=True),
        ])

        actualizar_layout("Editor")

    def guardar_nota():

        nonlocal archivo_editando, current_view

        titulo = (editor_title.value or "").strip()
        if not titulo:
            return

        base_name = slugify(titulo)
        destino = base_name + ".md"

        # Si se está editando y cambia el nombre
        if archivo_editando and destino != archivo_editando:
            if os.path.exists(os.path.join(RUTA_NOTAS, destino)):
                i = 1
                while os.path.exists(os.path.join(RUTA_NOTAS, f"{base_name}_{i}.md")):
                    i += 1
                destino = f"{base_name}_{i}.md"

        try:
            with open(os.path.join(RUTA_NOTAS, destino), "w", encoding="utf-8") as f:
                f.write(editor_content.value or "")

            # Si cambió el nombre eliminar el antiguo
            if archivo_editando and archivo_editando != destino:
                try:
                    os.remove(os.path.join(RUTA_NOTAS, archivo_editando))
                except Exception:
                    pass

        except Exception:
            return

        archivo_editando = destino
        current_view = "nota"

        ver_nota(destino)

    def confirm_delete_note(filename: str):
        try:
            os.remove(os.path.join(RUTA_NOTAS, filename))
        except Exception:
            pass
        mostrar_lista()

    def construir_appbar(titulo_actual="", archivo_actual=None):

        if current_view == "nota":
            return ft.AppBar(
                toolbar_height=70,
                leading=ft.IconButton(
                    ft.Icons.ARROW_BACK,
                    on_click=lambda e: mostrar_lista()
                ),
                title=ft.Text(titulo_actual),
                bgcolor=ft.Colors.TRANSPARENT,
                actions=[
                    ft.IconButton(
                        ft.Icons.EDIT,
                        on_click=lambda e: abrir_editor(archivo_actual)
                    ),
                    ft.IconButton(
                        ft.Icons.DELETE,
                        icon_color=ft.Colors.RED,
                        on_click=lambda e: confirm_delete_note(archivo_actual)
                    ),
                ]
            )

        if current_view == "editor":
            return ft.AppBar(
                toolbar_height=70,
                leading=ft.IconButton(
                    ft.Icons.CLOSE,
                    on_click=lambda e: mostrar_lista()
                ),
                title=ft.Text("Editor de nota"),
                bgcolor=ft.Colors.TRANSPARENT,
                actions=[
                    ft.IconButton(
                        ft.Icons.SAVE,
                        on_click=lambda e: guardar_nota()
                    ),
                ]
            )

        return ft.AppBar(
            toolbar_height=70,
            title=ft.Container(
                content=search_bar,
                padding=ft.padding.symmetric(horizontal=40),
            ),
            actions=[
                ft.IconButton(
                    ft.Icons.ADD,
                    on_click=lambda e: abrir_editor()
                )
            ],
            bgcolor=ft.Colors.TRANSPARENT,
        )

    def mostrar_lista():
        nonlocal mostrar_barra, current_view
        mostrar_barra = True
        current_view = "notas"
        construir_notas()
        actualizar_layout("")

    area_notas_scroll = ft.Container(
        expand=True,
        content=ft.ListView(
            controls=[lista_notas],
            expand=True,
            padding=ft.padding.symmetric(horizontal=10, vertical=5),
        ),
    )

    def actualizar_layout(titulo="", archivo=None):

        layout_principal.controls.clear()
        page.appbar = construir_appbar(titulo, archivo)
        layout_principal.controls.append(area_notas_scroll)
        page.update()

    construir_notas()
    actualizar_layout("")

    return layout_principal