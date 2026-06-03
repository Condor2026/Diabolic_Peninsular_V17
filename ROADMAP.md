# 📍 Roadmap 

DIABOLIC

Este documento describe las direcciones de desarrollo, mejoras planificadas y funcionalidades futuras para **DIABOLIC** (versiones Baleares, Peninsular, Latam, Canarias y Italia).  
La hoja de ruta es orientativa y puede cambiar según las necesidades de la comunidad y los principios éticos del proyecto.

---

## 🟢 Versión actual (5.3 / 1.0)

- ✅ Scraping de 18 periódicos en Baleares y 62 en Península.
- ✅ Rotación de User‑Agent y paginación inteligente (12 formatos).
- ✅ Detector automático de URLs rotas.
- ✅ Clasificación de delitos (12+ tipos, con jerga local).
- ✅ Conexiones entre incidentes (opción 3 del menú).
- ✅ Interfaz web con gráficos y filtros (7/30/90 días).
- ✅ Exportación a JSON y CSV.
- ✅ Menú terminal completo (10 comandos).
- ✅ Código ético, sin almacenamiento de datos personales.
- ✅ Banner con filosofía Spiderman y descripción OSINT.

---

## 🟡 Próximas mejoras (corto plazo – 3 meses)

### 1. Integración con mapas interactivos
- Mostrar los incidentes sobre un mapa real (Leaflet / OpenStreetMap) en la interfaz web.
- Geolocalización aproximada por municipio o coordenadas (usando datos públicos).

### 2. Alertas personalizables
- Sistema de alertas por Telegram, Discord o correo electrónico cuando se detecten patrones anómalos (ej. 5 robos en una misma zona en 24 horas).
- Configuración de umbrales por el usuario.

### 3. Nuevas fuentes de datos
- Añadir RSS de boletines oficiales (ayuntamientos, delegaciones de gobierno).
- Incorporar canales de Twitter/X de policías locales y guardia civil (siempre públicos).

### 4. Mejora en la detección de conexiones
- Expandir la opción 3 con gráficos de red que visualicen relaciones entre incidentes.
- Añadir nivel de confianza (bajo/medio/alto) en los patrones detectados.

### 5. Soporte para más lenguajes
- Internacionalización de la interfaz web (inglés, catalán, etc.).
- Traducción del README y la documentación.

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

### 11. Versión para Canarias
- Adaptación a los periódicos de las islas Canarias (similar a Baleares).

### 12. Colaboración con universidades
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
