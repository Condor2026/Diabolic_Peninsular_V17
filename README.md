# DIABOLIC Peninsular v5.3

[![Version](https://img.shields.io/badge/version-5.3-red)](https://github.com/Condor2026/Diabolic_Peninsular_V17)
[![License](https://img.shields.io/badge/license-MIT-blue)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.8+-green)](https://python.org)
[![OSINT](https://img.shields.io/badge/OSINT-Pasivo%20%7C%20Analítico-blueviolet)](https://es.wikipedia.org/wiki/OSINT)
[![Termux](https://img.shields.io/badge/Termux-Compatible-orange)](https://termux.com)
[![Linux](https://img.shields.io/badge/Linux-Compatible-lightgrey)](https://linux.org)

**DIABOLIC Peninsular** es una herramienta OSINT pasiva y analítica que **monitoriza 62 periódicos digitales de la España peninsular** (desde Andalucía hasta Galicia, pasando por Madrid, Cataluña, País Vasco, etc.) para detectar, clasificar y visualizar patrones delictivos.  
No guarda datos personales, solo titulares, fechas y ubicaciones por comunidad autónoma. Filosofía: *“Un gran poder conlleva una gran responsabilidad”*.

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

### Requisitos comunes
- Python 3.8 o superior.
- `git` (para clonar el repositorio).
- Conexión a Internet.

### 🔧 Instalación paso a paso

#### 📱 Opción 1: En Termux (Android)

```bash
# Actualizar paquetes e instalar Python y git
pkg update && pkg upgrade -y
pkg install python git -y

# Instalar dependencias Python
pip install requests beautifulsoup4 flask

# Clonar el repositorio
git clone https://github.com/Condor2026/Diabolic_Peninsular_V17
cd Diabolic_Peninsular_V17

# Ejecutar la herramienta
python Diabolic_Peninsular_V17.py
```

🐧 Opción 2: En Linux (Debian/Ubuntu y derivados)

```bash
# Actualizar repositorios e instalar Python3, pip y git
sudo apt update
sudo apt install python3 python3-pip git -y

# Instalar dependencias Python
pip3 install requests beautifulsoup4 flask

# Clonar el repositorio
git clone https://github.com/Condor2026/Diabolic_Peninsular_V17
cd Diabolic_Peninsular_V17

# Ejecutar la herramienta
python3 Diabolic_Peninsular_V17.py
```

📦 Opción 3: Instalación manual con requirements.txt (cualquier sistema)

```bash
git clone https://github.com/Condor2026/Diabolic_Peninsular_V17
cd Diabolic_Peninsular_V17
pip install -r requirements.txt
python Diabolic_Peninsular_V17.py
```

💡 Nota: Si prefieres usar python3 en lugar de python, ajusta el comando según tu sistema.

---

🖥️ Modo terminal (10 comandos)

Al ejecutar Diabolic_Peninsular_V17.py aparece un menú con las siguientes opciones:

```
╔════════════════════════════════════════════════════╗
║           M E N Ú   P R I N C I P A L              ║
╚════════════════════════════════════════════════════╝
[1]  Extraer noticias de hoy
[2]  Extraer noticias de los últimos 7 días
[3]  Extraer noticias de los últimos 30 días
[4]  Extraer noticias de los últimos 90 días
[5]  Analizar tendencias (resumen estadístico)
[6]  Detectar conexiones entre incidentes
[7]  Ver últimas noticias almacenadas
[8]  Exportar a CSV
[9]  Exportar a JSON
[10] Iniciar servidor web interactivo
[0]  Salir
```

Cada opción ejecuta la acción correspondiente y muestra los resultados en la terminal.

---

🌐 Modo web interactivo

La opción 10 lanza un servidor Flask local (por defecto en http://localhost:5000). Desde el navegador podrás:

· Ver gráficos de barras interactivos.
· Filtrar por comunidad autónoma y tipo de delito.
· Consultar la lista de incidentes.
· Exportar los datos a CSV o JSON con un clic.

---

📰 Fuentes monitorizadas

La herramienta rastrea 62 periódicos digitales de toda la España peninsular. La lista incluye medios de:

· Andalucía (Diario de Sevilla, Granada Hoy, Málaga Hoy, etc.)
· Madrid (El Mundo, El País, ABC, etc.)
· Cataluña (La Vanguardia, El Periódico, etc.)
· Comunidad Valenciana (Las Provincias, Levante-EMV, etc.)
· País Vasco (El Correo, Deia, etc.)
· Galicia (La Voz de Galicia, Faro de Vigo, etc.)
· Castilla y León, Castilla-La Mancha, Extremadura, Murcia, Cantabria, Asturias, Navarra, La Rioja, Aragón, etc.

Nota: La lista completa se puede consultar/editando en config.json.

---

🗺️ Comunidades cubiertas

· Andalucía
· Aragón
· Asturias
· Cantabria
· Castilla-La Mancha
· Castilla y León
· Cataluña
· Comunidad Valenciana
· Extremadura
· Galicia
· La Rioja
· Madrid
· Murcia
· Navarra
· País Vasco

---

🧠 Tipo de OSINT y metodología

· OSINT Pasivo: No interactúa con los sistemas de los periódicos más allá de lo que un usuario normal haría.
· Extracción selectiva: Solo recoge información de sucesos (policial, judicial, seguridad ciudadana).
· Anonimización: No almacena datos personales de los implicados, solo el lugar, fecha y tipo de delito.
· Enfoque analítico: No se limita a recopilar noticias, sino que busca patrones que puedan ayudar a entender la delincuencia en España peninsular.

---

⚖️ Ética, legalidad y protección de datos

DIABOLIC respeta estrictamente la legalidad española y europea:

· Solo accede a contenido público y no requiere autenticación.
· No almacena información personal (nombres, DNI, etc.).
· El código es abierto y transparente.
· Se recomienda utilizar la herramienta únicamente con fines académicos, periodísticos o de investigación criminal legítima.

⚠️ ADVERTENCIA LEGAL
Esta herramienta es exclusivamente para fines educativos y de investigación legítima.
No debe utilizarse para acosar, doxear, realizar actividades ilegales o violar la privacidad de las personas.
El autor no se responsabiliza del mal uso. El usuario es el único responsable de cumplir con las leyes de su país.

---

🤝 Contribuciones y futuro

Las contribuciones son bienvenidas. Puedes:

· Reportar errores en Issues.
· Ampliar la lista de periódicos.
· Mejorar el detector automático de URLs.
· Añadir nuevas categorías de delitos.
· Optimizar el análisis de conexiones.

---

📜 Licencia

Este proyecto está bajo la licencia MIT. Consulta el archivo LICENSE para más detalles.

---

🙏 Agradecimientos

· BeautifulSoup4 – scraping.
· Flask – interfaz web.
· Inspiración: proyectos OSINT como Sherlock, Maigret.
· Comunidad de investigación OSINT en España.
