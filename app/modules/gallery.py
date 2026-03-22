import os
import flet as ft
import re
import shutil
import time

RUTA_IMAGENES = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "data", "gallery")
)
os.makedirs(RUTA_IMAGENES, exist_ok=True)

EXTS = (".png", ".jpg", ".jpeg", ".webp", ".gif")


def listar_imagenes():
    return [f for f in os.listdir(RUTA_IMAGENES) if f.lower().endswith(EXTS)]


def gallery_page(page: ft.Page):

    lista = ft.Column(spacing=15, expand=True)
    current_view = "grid"
    layout_principal = ft.Column(expand=True)

    file_picker = ft.FilePicker()

    def guardar_archivo(e: ft.FilePickerResultEvent):
        if not e.files:
            return

        origen = e.files[0].path
        ext = os.path.splitext(origen)[1].lower()

        nombre = f"img_{int(time.time())}{ext}"
        destino = os.path.join(RUTA_IMAGENES, nombre)

        shutil.copy(origen, destino)
        construir_grid(search_bar.value or "")
        page.update()

    file_picker.on_result = guardar_archivo
    page.overlay.append(file_picker)


    def buscar(e):
        construir_grid(search_bar.value or "")

    search_bar = ft.TextField(
        label="Buscar imagen...",
        on_change=buscar,
        border=ft.InputBorder.UNDERLINE,
        border_color=ft.Colors.OUTLINE,
        bgcolor=ft.Colors.TRANSPARENT,
        dense=True,
        content_padding=ft.padding.symmetric(horizontal=12, vertical=10),
        expand=True,
    )


    def pretty(nombre):
        return re.sub(r'[_]+', ' ', os.path.splitext(nombre)[0]).strip()

    def renombrar_imagen(nombre_actual):

        base, ext = os.path.splitext(nombre_actual)
        tf = ft.TextField(value=base, autofocus=True)

        def guardar(e):
            nuevo = tf.value.strip()
            if not nuevo:
                return

            destino = nuevo + ext
            ruta_actual = os.path.join(RUTA_IMAGENES, nombre_actual)
            nueva_ruta = os.path.join(RUTA_IMAGENES, destino)

            i = 1
            while os.path.exists(nueva_ruta):
                destino = f"{nuevo}_{i}{ext}"
                nueva_ruta = os.path.join(RUTA_IMAGENES, destino)
                i += 1

            os.rename(ruta_actual, nueva_ruta)

            page.close(dlg)
            abrir_imagen(destino)

        dlg = ft.AlertDialog(
            title=ft.Text("Renombrar imagen"),
            content=tf,
            actions=[
                ft.TextButton("Cancelar", on_click=lambda e: page.close(dlg)),
                ft.ElevatedButton("Guardar", on_click=guardar),
            ],
        )

        page.open(dlg)

    def eliminar_imagen(nombre):

        def confirmar(e):
            ruta = os.path.join(RUTA_IMAGENES, nombre)

            if os.path.exists(ruta):
                os.remove(ruta)

            page.close(dlg)

            page.snack_bar = ft.SnackBar(
                ft.Text("Imagen eliminada correctamente"),
                bgcolor=ft.Colors.RED,
            )
            page.snack_bar.open = True

            mostrar_lista()

        dlg = ft.AlertDialog(
            title=ft.Text("Eliminar imagen"),
            content=ft.Text(f"¿Seguro que deseas eliminar '{pretty(nombre)}'?"),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda e: page.close(dlg)),
                ft.ElevatedButton(
                    "Eliminar",
                    color=ft.Colors.WHITE,
                    bgcolor=ft.Colors.RED,
                    on_click=confirmar,
                ),
            ],
        )

        page.open(dlg)

    def construir_appbar(titulo="", archivo=None):

        if current_view == "viewer":
            return ft.AppBar(
                leading=ft.IconButton(
                    ft.Icons.ARROW_BACK,
                    on_click=lambda e: mostrar_lista(),
                ),
                title=ft.Text(titulo),
                actions=[
                    ft.IconButton(
                        ft.Icons.DELETE,
                        tooltip="Eliminar",
                        icon_color=ft.Colors.RED,
                        on_click=lambda e: eliminar_imagen(archivo),
                    ),
                    ft.IconButton(
                        ft.Icons.EDIT,
                        tooltip="Renombrar",
                        on_click=lambda e: renombrar_imagen(archivo),
                    ),
                ],
                bgcolor=ft.Colors.TRANSPARENT,
            )

        return ft.AppBar(
            title=ft.Container(
                content=search_bar,
                padding=ft.padding.symmetric(horizontal=40),
            ),
            actions=[
                ft.IconButton(
                    ft.Icons.UPLOAD,
                    icon_size=28,
                    tooltip="Subir imagen",
                    on_click=lambda e: file_picker.pick_files(
                        allow_multiple=False,
                        file_type=ft.FilePickerFileType.IMAGE,
                    ),
                )
            ],
            bgcolor=ft.Colors.TRANSPARENT,
        )

    def mostrar_lista():
        nonlocal current_view
        current_view = "grid"
        construir_grid(search_bar.value or "")
        actualizar_layout("")


    def construir_grid(filtro=""):

        lista.controls.clear()
        archivos = listar_imagenes()
        filtro = filtro.lower()

        if not archivos:
            lista.controls.append(
                ft.Container(
                    expand=True,
                    alignment=ft.alignment.center,
                    content=ft.Text(
                        "No hay imágenes en la carpeta.",
                        size=18,
                        weight=ft.FontWeight.W_500,
                        color=ft.Colors.OUTLINE,
                        text_align=ft.TextAlign.CENTER,
                    ),
                )
            )
            page.update()
            return

        grid = ft.GridView(
            expand=True,
            runs_count=3,
            max_extent=300,
            child_aspect_ratio=1,
            spacing=15,
            run_spacing=15,
        )

        for archivo in sorted(archivos):

            if filtro and filtro not in archivo.lower():
                continue

            ruta = os.path.join(RUTA_IMAGENES, archivo)

            thumb = ft.Container(
                content=ft.Image(src=ruta, fit=ft.ImageFit.COVER),
                border_radius=15,
                clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
                ink=True,
                on_click=lambda e, a=archivo: abrir_imagen(a),
            )

            grid.controls.append(thumb)

        if not grid.controls:
            lista.controls.append(
                ft.Container(
                    expand=True,
                    alignment=ft.alignment.center,
                    content=ft.Text(
                        "No se encontraron coincidencias",
                        size=18,
                        weight=ft.FontWeight.W_500,
                        color=ft.Colors.OUTLINE,
                        text_align=ft.TextAlign.CENTER,
                    ),
                )
            )
        else:
            lista.controls.append(grid)

        page.update()

    def abrir_imagen(nombre):

        nonlocal current_view
        current_view = "viewer"

        lista.controls.clear()
        ruta = os.path.join(RUTA_IMAGENES, nombre)

        visor = ft.Container(
            expand=True,
            bgcolor=ft.Colors.BLACK,
            alignment=ft.alignment.center,
            content=ft.InteractiveViewer(
                min_scale=1,
                max_scale=6,
                boundary_margin=ft.margin.all(1000),
                pan_enabled=True,
                scale_enabled=True,
                constrained=False,
                content=ft.Container(
                    alignment=ft.alignment.center,
                    expand=True,
                    content=ft.Image(
                        src=ruta,
                        fit=ft.ImageFit.CONTAIN,
                    ),
                ),
            ),
        )

        lista.controls.append(visor)
        actualizar_layout(pretty(nombre), nombre)


    def actualizar_layout(titulo="", archivo=None):
        layout_principal.controls.clear()
        page.appbar = construir_appbar(titulo, archivo)
        layout_principal.controls.append(lista)
        page.update()

    construir_grid()
    actualizar_layout("")

    return layout_principal