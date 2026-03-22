# MedCore

**MedCore** es una aplicación multiplataforma para **móvil, web y escritorio**, desarrollada en Python utilizando el framework [Flet](https://flet.dev).
Su objetivo es centralizar calculadoras clínicas, valores de laboratorio de referencia y otros recursos útiles en una plataforma **intuitiva, modular y eficiente**.

## Tecnologías utilizadas

* **Python 3.10+**
* **[Flet](https://flet.dev/)** – Framework para interfaces web y de escritorio **FLET VERSION 0.28.3**
* **Arquitectura modular y escalable**

## Estructura del proyecto

```
MedCore/
├── app/
│   ├── modules/                 # Módulos y componentes
│   ├── assets/                  # Imágenes, íconos y anexos de guias
│   ├── storage/                 # Almacenamiento de las guias, notas y DB medicamentos
│   ├── calculadoras/            # Almacenamiento de calculadoras
│   └── main.py                  # Punto de entrada principal
│
├── backend/                     # Servidor de flak para descarga de guias
│   ├── guias/                   # Almacenamiento de guias
│   ├── imagenes/                # Almacenamiento de imagenes que usan las guias
│   ├── static/                  # HTML servidor
│   ├── app.py
│   ├── requirements.txt
│   └── vercel.json
│
├── README.md                # Documentación principal
├── LICENSE                  # Licencia
├── CODE_OF_CONDUCT.md       # Código de conducta
└── pyproject.toml           # Configuraciones de compilación
```

## Estado actual

* [x] Acceso completo sin conexión "Solo se necesita actualizar las perlas clinicas en caso de que las desees"
* Calculadoras médicas disponibles:

  * [x] Índice de Masa Corporal (IMC)
  * [x] Regla de Tres (Directa)
  * [x] Talla diana parental
  * [x] TFG – Ecuación de Schwartz 2009
  * [x] Criterios SLICC para diagnóstico de LES
  * [x] qSOFA (Sepsis)
  * [x] Puntaje SOFA (Sepsis)
  * [x] CKD-EPI 2021
  * [x] Brecha aniónica
  * [x] Sodio corregido
  * [x] WIFI score
* [x] Base de datos de medicamentos
* [x] Editor de base de datos de medicamentos
* [x] Búsqueda interactiva

## Advertencia
⚠️ Aviso de Exención de Responsabilidad⚠️

El uso de MedCore implica la aceptación de los siguientes puntos:
- Finalidad Académica: Esta aplicación ha sido desarrollada exclusivamente como un proyecto educativo y una herramienta de apoyo a la consulta rápida. No es un dispositivo médico certificado.
- Criterio Profesional: La información, cálculos y dosis proporcionados por MedCore son referenciales. En ningún caso sustituyen el juicio clínico, diagnóstico o tratamiento de un profesional de la salud titulado. El usuario es el único responsable de las decisiones médicas tomadas tras el uso de esta app.
- Verificación de Datos: A pesar del rigor en el desarrollo de las calculadoras (como CKD-EPI, SOFA o Schwartz), los resultados pueden presentar variaciones. Es obligación del clínico contrastar cualquier resultado con la literatura médica oficial y guías de práctica clínica vigentes.
- Actualización de Contenido: Debido a la naturaleza cambiante de la medicina, el contenido local (perlas clínicas, bases de datos de medicamentos) podría quedar desactualizado. El desarrollador no garantiza la vigencia absoluta de la información almacenada en el dispositivo.
- Privacidad: MedCore no está diseñado para el manejo de Datos Personales Sensibles de pacientes. Se insta al usuario a no ingresar información que permita identificar a personas en los módulos de notas o bases de datos locales.

## Objetivo

**MedCore** busca ser una herramienta de referencia para estudiantes de medicina, médicos generales, que buscan tener a mano todas las herramientas posibles en un solo lugar para un trabajo y un aprendizaje mas optimo.

*Inspirado en mi propia necesidad de contar con herramientas médicas en una sola aplicación.*