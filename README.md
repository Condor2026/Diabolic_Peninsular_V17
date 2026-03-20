## 🔥 DIABOLIC PENINSULAR v5.3

[![Version](https://img.shields.io/badge/version-5.3-red)](https://github.com/Condor2026/Diabolic_Peninsular_V17)
[![License](https://img.shields.io/badge/license-MIT-blue)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.8+-green)](https://python.org)
[![OSINT](https://img.shields.io/badge/OSINT-Pasivo%20%7C%20Analítico-blueviolet)](https://es.wikipedia.org/wiki/OSINT)

**DIABOLIC Peninsular** es una herramienta OSINT pasiva y analítica que monitoriza **62 periódicos digitales de la España peninsular** (desde Andalucía hasta Galicia, pasando por Madrid, Cataluña, País Vasco, etc.) para detectar, clasificar y visualizar patrones delictivos.  
No guarda datos personales, solo titulares, fechas y ubicaciones por comunidad autónoma. Filosofía: *"Un gran poder conlleva una gran responsabilidad"*.

---

## 📌 Índice

- [¿Qué hace DIABOLIC?](#qué-hace-diabolic)
- [Características clave](#características-clave)
- [Tecnología y arquitectura](#tecnología-y-arquitectura)
- [Instalación y uso](#instalación-y-uso)
- [Modo terminal (10 comandos)](#modo-terminal-10-comandos)
- [Modo web interactivo](#modo-web-interactivo)
- [Fuentes monitorizadas](#fuentes-monitorizadas)
- [Comunidades cubiertas](#comunidades-cubiertas)
- [Tipo de OSINT y metodología](#tipo-de-osint-y-metodología)
- [Ética, legalidad y protección de datos](#ética-legalidad-y-protección-de-datos)
- [Contribuciones y futuro](#contribuciones-y-futuro)
- [Licencia](#licencia)

---

## 🔍 ¿Qué hace DIABOLIC?

DIABOLIC automatiza el proceso de **scraping de noticias de sucesos** de medios locales y nacionales de la España peninsular. En lugar de leer docenas de periódicos cada día, la herramienta:

- **Extrae** automáticamente titulares, fechas, fuentes y ubicación geográfica (comunidad autónoma) de noticias relacionadas con delitos.
- **Clasifica** los incidentes en categorías (robo, estafa, narcotráfico, violencia, asesinato, etc.).
- **Almacena** los datos localmente en formato JSON, sin guardar ningún dato personal.
- **Analiza** tendencias temporales (7, 30, 90 días) y distribuciones por comunidad y tipo de delito.
- **Detecta conexiones** entre incidentes: misma zona, fechas cercanas, mismo modus operandi (alunicero, butrón, escalo…) que pueden indicar una misma banda.
- **Visualiza** los resultados mediante una interfaz web interactiva con gráficos de barras y filtros dinámicos.
- **Exporta** los datos a CSV o JSON para análisis externos.

---

## ⚙️ Características clave

### 🔁 Rotación de User‑Agent
Evita bloqueos de los periódicos simulando diferentes navegadores y versiones en cada petición.

### 🧠 Paginación inteligente
Prueba automáticamente hasta 12 formatos diferentes de paginación (`/pagina/2`, `?page=2`, `?offset=2`, etc.) y recuerda el que funciona para cada dominio.

### 🔎 Detector automático de URLs
Si una URL de un periódico deja de funcionar, el sistema busca rutas alternativas (`/sucesos`, `/local`, `/tribunales`, `/actualidad/sucesos`, etc.) y actualiza la configuración.

### 📊 Clasificación avanzada de delitos
Utiliza una lista amplia de palabras clave, incluyendo jerga local (peta, falcon, vuelco, alunicero, butrón, intrusismo…). Se puede extender fácilmente.

### 🔗 Conexiones entre incidentes
- **Por tipo y comunidad** (ej. 5 robos en Madrid en 7 días).
- **Por modus operandi** (detecta repetición de términos como “alunicero” o “butrón”).
- **Frecuencia temporal** (incidentes/día).

### 🌐 Interfaz web interactiva
- Gráficos de barras por comunidad y tipo de delito.
- Filtros por período (últimos 7, 30, 90 días).
- Lista de los últimos 20 incidentes.
- Botones para actualizar datos y exportar JSON/CSV.

### 🖥️ Menú terminal completo
10 comandos que permiten ejecutar todas las funciones sin necesidad de abrir el navegador.

---

## 🛠️ Tecnología y arquitectura

- **Lenguaje**: Python 3.8+
- **Framework web**: Flask (servidor ligero)
- **Scraping**: Requests + BeautifulSoup4
- **Almacenamiento**: JSON local (sin bases de datos externas)
- **Estructura modular**:
  - `DetectorURLs`: encargado de verificar y corregir URLs de periódicos.
  - `GestorDatos`: carga, guarda y procesa los incidentes.
  - `ExtractorNoticias`: realiza el scraping con rotación de User‑Agent y paginación inteligente.
- **Colores en terminal**: Códigos ANSI para una experiencia visual atractiva.

---

## 📥 Instalación y uso

### Requisitos
- Python 3.8 o superior.
- pip (gestor de paquetes de Python).

### Instalación manual
```bash
git clone https://github.com/Condor2026/Diabolic_Peninsular_V17
cd Diabolic_Peninsular_V17
pip install -r requirements.txt
python Diabolic_Peninsular_V17.py
