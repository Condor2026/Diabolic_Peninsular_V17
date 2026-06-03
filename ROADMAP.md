# 📍 Roadmap 

# 📍 Hoja de ruta de DIABOLIC (Peninsular)

Este documento describe las direcciones de desarrollo, mejoras planificadas y funcionalidades futuras para **DIABOLIC Peninsular** (versión 5.3).  
La hoja de ruta es orientativa y puede cambiar según las necesidades de la comunidad y los principios éticos del proyecto.

---

## 🟢 Versión actual (5.3)

- ✅ Scraping de **62 periódicos de la España peninsular** (nacionales y autonómicos).
- ✅ Rotación de User‑Agent y paginación inteligente (12 formatos).
- ✅ Detector automático de URLs rotas.
- ✅ Clasificación de delitos (12+ tipos, con jerga local: *alunicero, butrón, peta, vuelco, intrusismo turístico…*).
- ✅ Conexiones entre incidentes (opción 3 del menú).
- ✅ Interfaz web con gráficos y filtros (7/30/90 días) por comunidad autónoma.
- ✅ Exportación a JSON y CSV.
- ✅ Menú terminal completo (10 comandos).
- ✅ Código ético, sin almacenamiento de datos personales.
- ✅ Banner con filosofía Spiderman y descripción OSINT.

---

## 🟡 Próximas mejoras (corto plazo – 3 meses)

### 1. Mapas de calor por comunidad
- Visualización geográfica de incidentes sobre mapas de España (Leaflet / OpenStreetMap).
- Geolocalización por comunidad autónoma, provincia y municipio.

### 2. Alertas personalizables
- Sistema de alertas por Telegram, Discord o correo electrónico cuando se detecten patrones anómalos (ej. aumento de estafas en Madrid).
- Configuración de umbrales por el usuario.

### 3. Nuevas fuentes de datos
- Ampliar base de periódicos a **medios locales más pequeños** (prensa comarcal y digital independiente).
- Incorporar boletines oficiales de delegaciones del gobierno y ayuntamientos.
- Agregar canales de Twitter/X de policías locales y guardia civil de cada comunidad.

### 4. Léxico criminal enriquecido
- Expansión del diccionario con jerga delictiva específica de cada región (ej. *"trincheta"* en el sur, *"búho"* en Cataluña, etc.).
- Soporte para delitos emergentes como la **ciberestafa** y la **inteligencia artificial fraudulenta**.

### 5. Mejora en la detección de conexiones
- Expandir la opción 3 con gráficos de red que visualicen relaciones entre incidentes a nivel provincial.
- Añadir nivel de confianza (bajo/medio/alto) en los patrones detectados.

---

## 🟠 Funcionalidades en estudio (medio plazo – 6 meses)

### 6. API pública
- Endpoint REST para consultar incidentes, estadísticas y patrones.
- Documentación Swagger/OpenAPI.

### 7. Instalación mediante Docker
- Contenedor Docker para facilitar el despliegue en servidores.
- Orquestación con docker-compose.

### 8. Análisis predictivo básico
- Modelos de machine learning ligeros para estimar tendencias futuras (con explicabilidad).
- Siempre con datos agregados y sin predecir individuos.

### 9. Integración con herramientas de inteligencia de código abierto
- Exportación directa a Maltego, OpenCTI o MISP.

### 10. Verificación de fuentes
- Mecanismo automático que compruebe la fiabilidad de los periódicos y detecte posibles fake news.

---

## 🔴 Ideas a largo plazo (1 año o más)

### 11. Versión para Canarias y Baleares ya existente
- Mantener la versión peninsular separada, pero permitir una instalación que combine ambas si el usuario lo desea.

### 12. Colaboración con universidades españolas
- Programas de investigación criminológica usando datos anonimizados de DIABOLIC.

### 13. Móvil nativo
- Aplicación Android/iOS que consuma la API pública.

### 14. Comunidad de contribuidores
- Creación de una guía de contribución detallada y un canal de comunicación (Discord/Matrix) para desarrolladores.

---

## 📌 Cómo proponer nuevas ideas

Si quieres sugerir una funcionalidad, reportar un error o participar en el desarrollo, abre un *issue* en el repositorio de GitHub con la etiqueta `enhancement` o `roadmap`.  
Toda contribución debe respetar el [Código de Conducta](CODE_OF_CONDUCT.md) y los principios éticos del proyecto.

---

*Última actualización: marzo 2026*  
**SpectrumSecurity** – *OSINT ético al servicio de la ciudadanía* 🔥
