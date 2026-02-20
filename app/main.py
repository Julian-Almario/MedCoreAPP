import flet as ft
import os
import json
from modules.cal import *
from modules.info import *
from modules.algoritmos import *
from modules.anciclopedia import *

def main(page: ft.Page):
    page.theme_mode = ft.ThemeMode.DARK
    page.adaptive = True
    page.title = "MedCore"

    # Scroll personalizado
    page.theme = ft.Theme(
        scrollbar_theme=ft.ScrollbarTheme(
            thickness=0,
            radius=0,
            thumb_color=ft.Colors.TRANSPARENT,
            track_color=ft.Colors.TRANSPARENT,
            track_border_color=ft.Colors.TRANSPARENT,
        )
    )

    current_page_index = 0
    main_content = ft.Column(expand=True)
# -------------------------------------------------------------------------------
    # Search bar general
    def search_bar(filtrar, buscar):
        return ft.TextField(
            label=buscar,
            on_change=filtrar,
            border=ft.InputBorder.UNDERLINE,
            border_color=ft.Colors.OUTLINE,
            bgcolor=ft.Colors.TRANSPARENT,
            filled=False,
            dense=True,
            content_padding=ft.padding.symmetric(horizontal=12, vertical=10),
            expand=True,
        )

    def list_content_search(list_content, mensaje_no_resultados):
        list_content.sort(key=lambda x: x["titulo"].lower())
        list_container = ft.Column(spacing=20)

        def build_list(filtered_items):
            list_container.controls.clear()
            if filtered_items:
                for cont in filtered_items:
                    list_container.controls.append(cont["componente"])
            else:
                list_container.controls.append(
                    ft.Container(
                        content=mensaje_no_resultados,
                        alignment=ft.alignment.center,
                        padding=50,
                    )
                )
            page.update()

        def filtrar_items(e):
            filtro = e.control.value.lower()
            filtered_items = []
            for cont in list_content:
                titulo = cont["titulo"].lower()
                tags = " ".join(cont["tags"]).lower()
                if filtro in titulo or filtro in tags:
                    filtered_items.append(cont)
            build_list(filtered_items)

        for cont in list_content:
            list_container.controls.append(cont["componente"])

        return list_container, filtrar_items

    def build_fixed_page(list_data, placeholder_busqueda):

        mensaje_no_resultados = ft.Text(
            value="No se encontraron resultados",
            style=ft.TextThemeStyle.BODY_MEDIUM,
            text_align=ft.TextAlign.CENTER,
            color=ft.Colors.ON_SURFACE_VARIANT,
        )

        list_container, filtrar_items = list_content_search(list_data, mensaje_no_resultados)

        search_field = search_bar(filtrar_items, placeholder_busqueda)

        # APPBAR SOLO PARA ESTA PANTALLA
        page.appbar = ft.AppBar(
            toolbar_height=70,
            bgcolor=ft.Colors.TRANSPARENT,
            title=ft.Container(
                content=search_field,
                padding=ft.padding.symmetric(horizontal=40),
            ),
        )

        return ft.Container(
            expand=True,
            content=ft.ListView(
                expand=True,
                padding=ft.padding.symmetric(horizontal=15, vertical=5),
                controls=[list_container],
            ),
        )

# -------------------------------------------------------------------------------
    # Ruta de medicamentos
    RUTA_MEDS = os.path.abspath(os.path.join(os.path.dirname(__file__), "data", "meds"))
    os.makedirs(RUTA_MEDS, exist_ok=True)

    def save_meds_to_json(meds_list):
        os.makedirs(RUTA_MEDS, exist_ok=True)
        ruta = os.path.join(RUTA_MEDS, "meds.json")
        with open(ruta, "w", encoding="utf-8") as f:
            json.dump(meds_list, f, ensure_ascii=False, indent=2)

    def load_meds_raw():
        ruta = os.path.join(RUTA_MEDS, "meds.json")
        if not os.path.exists(ruta):
            save_meds_to_json([])
        with open(ruta, "r", encoding="utf-8") as f:
            return json.load(f)

    def cargar_medicamentos_desde_json(ruta_archivo=None):
        meds = load_meds_raw()
        return sorted(meds, key=lambda m: m.get("nombre", "").lower())

        # ------------------------------------------
    def pagina_medicamentos(page: ft.Page):

        all_meds = cargar_medicamentos_desde_json()

        buscar = "Buscar medicamentos..."
        mensaje_no_resultados = ft.Text(
            value="No se encontraron medicamentos.",
            style=ft.TextThemeStyle.BODY_MEDIUM,
            text_align=ft.TextAlign.CENTER,
            color=ft.Colors.ON_SURFACE_VARIANT,
        )

        batch_size = 20
        current_index = 0
        current_data = all_meds
        list_container = ft.Column(spacing=20)
        loading = False

        def make_item(med):
            return crear_panel_medicamento(med)["componente"]

        def cargar_mas(need_update=True):
            nonlocal current_index, loading
            if loading:
                return
            loading = True
            try:
                if current_index >= len(current_data):
                    return

                end = min(current_index + batch_size, len(current_data))

                for i in range(current_index, end):
                    try:
                        list_container.controls.append(make_item(current_data[i]))
                    except Exception:
                        continue

                current_index = end

                if need_update:
                    page.update()

            finally:
                loading = False

        def on_scroll(e):
            if e.pixels >= e.max_scroll_extent - 150:
                cargar_mas()

        def filtrar_items(e):
            nonlocal current_data, current_index

            filtro = (e.control.value or "").lower()

            if not filtro:
                current_data = all_meds
            else:
                current_data = sorted(
                    [
                        m for m in all_meds
                        if filtro in m.get("nombre", "").lower()
                        or filtro in " ".join(m.get("tags", [])).lower()
                    ],
                    key=lambda x: x.get("nombre", "").lower()
                )

            current_index = 0
            list_container.controls.clear()

            if not current_data:
                list_container.controls.append(
                    ft.Container(
                        content=mensaje_no_resultados,
                        alignment=ft.alignment.center,
                        padding=50,
                    )
                )
            else:
                cargar_mas(False)

            page.update()

        if current_data:
            cargar_mas(False)
        else:
            list_container.controls.append(
                ft.Container(content=mensaje_no_resultados, alignment=ft.alignment.center, padding=50)
            )

        search_field = search_bar(filtrar_items, buscar)

        btn_add = ft.IconButton(
            icon=ft.Icons.ADD,
            icon_size=28,
            tooltip="Añadir medicamento",
            on_click=lambda e: open_med_dialog(page, med=None),
        )

        page.appbar = ft.AppBar(
            toolbar_height=70,
            bgcolor=ft.Colors.TRANSPARENT,
            title=ft.Container(
                content=search_field,
                padding=ft.padding.symmetric(horizontal=40),
            ),
            actions=[btn_add]
        )

        return ft.Container(
            expand=True,
            content=ft.ListView(
                expand=True,
                padding=ft.padding.symmetric(horizontal=10),
                controls=[list_container],
                on_scroll=on_scroll,
            ),
        )



# -------------------------------------------------------------------------------
    # Dialog para editar/crear un medicamento
    def open_med_dialog(page: ft.Page, med=None, on_save=None):
        is_new = med is None
        temp = {
            "nombre": "" if is_new else med.get("nombre", ""),
            "tags": "" if is_new else ",".join(med.get("tags", [])),
            "mecanismo": "" if is_new else med.get("mecanismo", ""),
            "indicaciones": "" if is_new else med.get("indicaciones", ""),
            "dosis": "" if is_new else med.get("dosis", ""),
            "contraindicaciones": "" if is_new else med.get("contraindicaciones", ""),
            "observaciones": "" if is_new else med.get("observaciones", "")
        }

        tf_nombre = ft.TextField(label="Nombre", value=temp["nombre"], expand=True)
        tf_tags = ft.TextField(label="Tags (separar por comas)", value=temp["tags"], expand=True)
        tf_mecanismo = ft.TextField(label="Mecanismo de acción", value=temp["mecanismo"], expand=True, multiline=True)
        tf_indicaciones = ft.TextField(label="Indicaciones", value=temp["indicaciones"], expand=True, multiline=True)
        tf_dosis = ft.TextField(label="Dosis", value=temp["dosis"], expand=True)
        tf_contra = ft.TextField(label="Contraindicaciones", value=temp["contraindicaciones"], expand=True, multiline=True)
        tf_obs = ft.TextField(label="Observaciones", value=temp["observaciones"], expand=True, multiline=True)

        def guardar(e):
            nombre = tf_nombre.value.strip()
            if not nombre:
                dlg_err = ft.AlertDialog(
                    title=ft.Text("Error"),
                    content=ft.Text("El nombre es obligatorio"),
                    actions=[ft.TextButton("Cerrar", on_click=lambda e: page.close(dlg_err))],
                    actions_alignment=ft.MainAxisAlignment.END,
                    modal=True,
                )
                page.open(dlg_err)
                return
            nuevo = {
                "nombre": nombre,
                "tags": [t.strip() for t in tf_tags.value.split(",") if t.strip()],
                "mecanismo": tf_mecanismo.value,
                "indicaciones": tf_indicaciones.value,
                "dosis": tf_dosis.value,
                "contraindicaciones": tf_contra.value,
                "observaciones": tf_obs.value
            }
            meds = load_meds_raw()
            if is_new:
                meds.append(nuevo)
            else:
                for i, m in enumerate(meds):
                    if m.get("nombre") == med.get("nombre"):
                        meds[i] = nuevo
                        break
                else:
                    meds.append(nuevo)
            save_meds_to_json(meds)
            page.close(dlg)
            show_meds()

        # Scroll interno para el dialogo
        content_list = ft.ListView(
            expand=True,
            padding=ft.padding.all(8),
            spacing=8,
            controls=[tf_nombre, tf_tags, tf_mecanismo, tf_indicaciones, tf_dosis, tf_contra, tf_obs],
        )

        dlg = ft.AlertDialog(
            title=ft.Text("Nuevo medicamento" if is_new else "Editar medicamento"),
            content=ft.Container(
                content=content_list,
                width=600,
                height=420,
            ),
            actions=[ft.TextButton("Cancelar", on_click=lambda e: page.close(dlg)), ft.ElevatedButton("Guardar", on_click=guardar)],
            actions_alignment=ft.MainAxisAlignment.END,
            modal=True,
        )
        page.open(dlg)

    def confirm_delete_med(page: ft.Page, med):
        def eliminar(e):
            meds = load_meds_raw()
            meds = [m for m in meds if m.get("nombre") != med.get("nombre")]
            save_meds_to_json(meds)
            page.close(dlg)
            show_meds()

        dlg = ft.AlertDialog(
            title=ft.Text("Confirmar eliminación"),
            content=ft.Text(f"¿Eliminar el medicamento '{med.get('nombre')}'?"),
            actions=[ft.TextButton("Cancelar", on_click=lambda e: page.close(dlg)), ft.TextButton("Eliminar", on_click=eliminar)],
            actions_alignment=ft.MainAxisAlignment.END,
            modal=True,
        )
        page.open(dlg)

    # Incluir botones Editar/Eliminar en los paneles de los medicamentos
    def crear_panel_medicamento(med: dict):
        panel_ref = ft.Ref[ft.ExpansionPanel]()

        def fila_info(titulo: str, contenido: str):
            return ft.Row(
                controls=[
                    ft.Container(
                        content=ft.Text(titulo, size=14, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_400),
                        width=150,
                        padding=ft.padding.symmetric(vertical=6),
                        alignment=ft.alignment.center_left
                    ),
                    ft.Container(
                        content=ft.Text(contenido, size=14, color=ft.Colors.ON_SURFACE),
                        padding=ft.padding.symmetric(vertical=6),
                        alignment=ft.alignment.center_left,
                        expand=True
                    )
                ],
                spacing=10
            )

        contenido_panel = ft.Column(
            controls=[
                fila_info("Mecanismo de acción:", med.get("mecanismo","")),
                fila_info("Indicaciones:", med.get("indicaciones","")),
                fila_info("Dosis:", med.get("dosis","")),
                fila_info("Contraindicaciones:", med.get("contraindicaciones","")),
                fila_info("Observaciones:", med.get("observaciones","")),
                ft.Row( # botones al final del panel
                    controls=[
                        ft.ElevatedButton("Editar", icon=ft.Icons.EDIT, on_click=lambda e, m=med: open_med_dialog(page, med=m)),
                        ft.ElevatedButton(
                            "Eliminar",
                            icon=ft.Icons.DELETE,
                            on_click=lambda e, m=med: confirm_delete_med(page, m),
                            style=ft.ButtonStyle(
                                bgcolor=ft.Colors.RED_900,
                                color=ft.Colors.BLUE_ACCENT
                            ),
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=10
                )
            ],
            spacing=8
        )

        def on_expand_change(e):
            panel = panel_ref.current
            is_expanded = panel.expanded
            panel.bgcolor = SECONDARY_COLOR if is_expanded else PRIMARY_COLOR
            panel.update()

        return {
            "titulo": med.get("nombre",""),
            "tags": med.get("tags", []),
            "componente": ft.ExpansionPanelList(
                on_change=on_expand_change,
                expand_icon_color=TEXT_COLOR,
                elevation=8,
                divider_color=TEXT_COLOR,
                controls=[
                    ft.ExpansionPanel(
                        ref=panel_ref,
                        header=ft.ListTile(
                            title=ft.Text(med.get("nombre",""), text_align=ft.TextAlign.LEFT),
                        ),
                        content=ft.Container(
                            content=contenido_panel,
                            padding=15
                        ),
                        bgcolor=PRIMARY_COLOR,
                        expanded=False
                    )
                ],
            )
        }
#-------------------------------------------
    # Contenido disponible
    def show_cals():
        main_content.controls.clear()
        main_content.controls.append(build_fixed_page(calculadoras, "Buscar calculadora..."))
        page.update()

    def show_meds():
        main_content.controls.clear()
        main_content.controls.append(pagina_medicamentos(page))
        page.update()
    

    def show_info():
        main_content.controls.clear()
        main_content.controls.append(info_page(page))
        page.update()


    def on_navigation_change(e):
        nonlocal current_page_index
        current_page_index = e.control.selected_index
        load_current_page()
        page.update()

    page.navigation_bar = ft.CupertinoNavigationBar(
        selected_index=current_page_index,
        bgcolor=PRIMARY_COLOR,
        inactive_color=SELECT_COLOR,
        active_color=TEXT_COLOR,
        on_change=on_navigation_change,
        destinations=[
            ft.NavigationBarDestination(
                icon=ft.Icons.CALCULATE_OUTLINED,
                label="Calculadoras"
            ),
            ft.NavigationBarDestination(
                icon=ft.Icons.NEWSPAPER,
                label="Algoritmos y guias"
            ),
            ft.NavigationBarDestination(
                icon=ft.Icons.LOCAL_PHARMACY_OUTLINED,
                label="Medicamentos"
            ),
            ft.NavigationBarDestination(
                icon=ft.Icons.BOOK,
                label="Anciclopedia clinica"
            ),
            ft.NavigationBarDestination(
                icon=ft.Icons.INFO_OUTLINED,
                label="Info"
            )
        ],
    )


    # Paginacion
    def load_current_page():
        if current_page_index == 0:
            page.appbar = None
            show_cals()
        elif current_page_index == 1:
            main_content.controls.clear()
            page.appbar = None
            main_content.controls.append(algoritmos_page(page))
        elif current_page_index == 2:
            page.appbar = None
            show_meds()
        elif current_page_index == 3:
            main_content.controls.clear()
            page.appbar = None
            main_content.controls.append(anciclopedia_page(page))
        elif current_page_index == 4:
            page.appbar = None
            show_info()

    load_current_page()
    page.add(main_content)
    page.update()


ft.app(target=main, assets_dir="assets")
