import flet as ft


def info_page(page: ft.Page):

    
    #Informacion del desarrollo
    creador_info = ft.Column(
        controls=[
            ft.Text("Created by Julian Almario Loaiza", size=18),
            ft.Text("Versión: 2.5.3 (Febrero 2026)", size=14, color=ft.Colors.OUTLINE),
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )

    # Lista de referencias
    referencias = [
        "- Singer M, Deutschman CS, Seymour CW, et al. The Third International Consensus Definitions for Sepsis and Septic Shock (Sepsis-3). JAMA. 2016;315(8):801–810. doi:10.1001/jama.2016.0287",
        "- Charles K, Lewis MJ, Montgomery E, Reid M. The 2021 Chronic Kidney Disease Epidemiology Collaboration Race-Free Estimated Glomerular Filtration Rate Equations in Kidney Disease: Leading the Way in Ending Disparities. Health Equity. 2024 Jan 12;8(1):39-45. doi: 10.1089/heq.2023.0038. PMID: 38250300; PMCID: PMC10797164.",
        "- Ohle R, O'Reilly F, O'Brien KK, Fahey T, Dimitrov BD. The Alvarado score for predicting acute appendicitis: a systematic review. BMC Med. 2011 Dec 28;9:139. doi: 10.1186/1741-7015-9-139. PMID: 22204638; PMCID: PMC3299622.",
        "- Singh, S., & Goel, A. (2023). A study of modified Wells score for pulmonary embolism and age-adjusted D-dimer values in patients at risk for deep venous thrombosis. Journal of Family Medicine and Primary Care, 12(9), 2020-2023. https://doi.org/10.4103/jfmpc.jfmpc_2455_22",
        "- Pandey, D. G., & Sharma, S. (2023). Biochemistry, Anion Gap. En StatPearls [Internet]. StatPearls Publishing. https://www.ncbi.nlm.nih.gov/books/NBK539757/",
        "- Petri, M., Orbai, A.-M., Alarcón, G. S., Gordon, C., Merrill, J. T., Fortin, P. R., Bruce, I. N., Isenberg, D., Wallace, D. J., Nived, O., Sturfelt, G., Ramsey-Goldman, R., Bae, S.-C., Hanly, J. G., Sanchez-Guerrero, J., Clarke, A., Aranow, C., Manzi, S., Urowitz, M., … Magder, L. S. (2012). Derivation and Validation of Systemic Lupus International Collaborating Clinics Classification Criteria for Systemic Lupus Erythematosus. Arthritis and rheumatism, 64(8), 2677-2686. https://doi.org/10.1002/art.34473",
        "- Edad corregida para bebés prematuros. (2018, diciembre 15). HealthyChildren.org. https://www.healthychildren.org/Spanish/ages-stages/baby/preemie/Paginas/Corrected-Age-For-Preemies.aspx",
        "- Hillier, T. A., Abbott, R. D., & Barrett, E. J. (1999). Hyponatremia: Evaluating the correction factor for hyperglycemia. The American Journal of Medicine, 106(4), 399-403. https://doi.org/10.1016/s0002-9343(99)00055-8",
        "- Peres Bota, D., Mélot, C., Lopes Ferreira, F., & Vincent, J.-L. (2003). Infection Probability Score (IPS): A method to help assess the probability of infection in critically ill patients. Critical Care Medicine, 31(11), 2579-2584. https://doi.org/10.1097/01.CCM.0000094223.92746.56",
        "- New Creatinine- and Cystatin C–Based Equations to Estimate GFR without Race | New England Journal of Medicine. (s. f.). Recuperado 17 de octubre de 2025, de https://www.nejm.org/doi/full/10.1056/NEJMoa2102953",
        "- Schwartz, G. J., Muñoz, A., Schneider, M. F., Mak, R. H., Kaskel, F., Warady, B. A., & Furth, S. L. (2009). New equations to estimate GFR in children with CKD. Journal of the American Society of Nephrology: JASN, 20(3), 629-637. https://doi.org/10.1681/ASN.2008030287",
        "- Bishop, E. H. (1964). PELVIC SCORING FOR ELECTIVE INDUCTION. Obstetrics and Gynecology, 24, 266-268.",
        "- Churpek, M. M., Snyder, A., Han, X., Sokol, S., Pettit, N., Howell, M. D., & Edelson, D. P. (2017). Quick Sepsis-related Organ Failure Assessment, Systemic Inflammatory Response Syndrome, and Early Warning Scores for Detecting Clinical Deterioration in Infected Patients outside the Intensive Care Unit. American Journal of Respiratory and Critical Care Medicine, 195(7), 906-911. https://doi.org/10.1164/rccm.201604-0854OC",
        "- Modi, S., Deisler, R., Gozel, K., Reicks, P., Irwin, E., Brunsvold, M., Banton, K., & Beilman, G. J. (2016). Wells criteria for DVT is a reliable clinical tool to assess the risk of deep venous thrombosis in trauma patients. World Journal of Emergency Surgery : WJES, 11, 24. https://doi.org/10.1186/s13017-016-0078-1"  
    ]

    # Informacion de referencias, terminos y condiciones, y privacidad
    info_panel = ft.ExpansionPanelList(
        expand_icon_color=ft.Colors.WHITE,
        elevation=8,
        divider_color=ft.Colors.WHITE,
        controls=[
            ft.ExpansionPanel(
                header=ft.ListTile(
                    title=ft.Row([
                        ft.Icon(name=ft.Icons.MENU_BOOK, size=20),
                        ft.Text("Referencias bibliográficas", text_align=ft.TextAlign.LEFT),
                    ])
                ),
                content=ft.Container(
                    content=ft.Column(
                        controls=[ft.Text(ref, size=14) for ref in referencias],
                        spacing=6
                    ),
                    padding=ft.padding.all(20)
                ),
                expanded=False,
                bgcolor=ft.Colors.BLUE_GREY_900,
            ),
            ft.ExpansionPanel(
                header=ft.ListTile(
                    title=ft.Row([
                        ft.Icon(name=ft.Icons.GAVEL, size=20),
                        ft.Text("Términos de uso y condiciones", text_align=ft.TextAlign.LEFT),
                    ])
                ),
                content=ft.Container(
                    content=ft.Text(
                        "La información médica contenida en esta aplicación ha sido recopilada cuidadosamente con fines educativos y de apoyo clínico. "
                        "No obstante, el uso que se le dé a esta información es responsabilidad exclusiva del usuario. "
                        "MedCore no reemplaza el juicio clínico profesional ni la consulta médica especializada.\n\n"
                        "El usuario acepta que cualquier decisión tomada con base en los datos proporcionados por la app es de su entera responsabilidad.",
                        size=14,
                        text_align=ft.TextAlign.LEFT,
                    ),
                    padding=ft.padding.all(20),
                ),
                expanded=False,
                bgcolor=ft.Colors.BLUE_GREY_900,
            ),
            ft.ExpansionPanel(
                header=ft.ListTile(
                    title=ft.Row([
                        ft.Icon(name=ft.Icons.LOCK, size=20),
                        ft.Text("Tratamiento de datos y privacidad", text_align=ft.TextAlign.LEFT),
                    ])
                ),
                content=ft.Container(
                    content=ft.Text(
                        "MedCore no recopila, transmite ni almacena información en servidores externos. "
                        "Toda la información ingresada, incluyendo historias clínicas, se guarda de manera local en el dispositivo del usuario.\n\n"
                        "Se recuerda que la historia clínica es un documento legal, privado y reservado. "
                        "Esta app fue diseñada únicamente como herramienta de organización de información médica para uso personal o profesional del usuario. "
                        "El manejo responsable y ético de los datos es esencial.",
                        size=14,
                        text_align=ft.TextAlign.LEFT,
                    ),
                    padding=ft.padding.all(20),
                ),
                expanded=False,
                bgcolor=ft.Colors.BLUE_GREY_900,
            ),
        ]
    )
    # Vista principal de información
    return ft.Column(
        scroll=ft.ScrollMode.AUTO,
        expand=True,
        controls=[
            ft.Container(height=20),
            ft.Container(
                content=creador_info,
                alignment=ft.alignment.center
            ),
            ft.Container(content=ft.Divider(thickness=1)),
            ft.Container(content=info_panel, padding=ft.padding.symmetric(horizontal=20)),
        ],
    )