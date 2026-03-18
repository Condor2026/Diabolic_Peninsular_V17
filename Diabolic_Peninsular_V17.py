#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
================================================================================
🔍 DIABOLIC PENINSULAR V17 - OSINT ANALYTICS PLATFORM
================================================================================
📊 Análisis automatizado de patrones delictivos en la España peninsular
================================================================================
🎯 PROPÓSITO:
    Herramienta OSINT de código abierto que monitoriza 62+ periódicos digitales
    para detectar, clasificar y visualizar tendencias delictivas por comunidades
    autónomas (excepto Canarias y Baleares).

⚙️  FUNCIONALIDADES CLAVE:
    • Scraping inteligente con detección automática de URLs
    • Clasificación de delitos (robos, estafas, narcotráfico, violencia...)
    • Detección de patrones y conexiones entre incidentes
    • Visualización web interactiva con gráficos dinámicos
    • Exportación de datos (JSON/CSV)
    • Menú terminal con 10 comandos avanzados

🔐 PRINCIPIOS ÉTICOS:
    • 100% datos públicos (solo noticias digitales)
    • Cero almacenamiento de información personal
    • Transparencia total (código abierto y auditable)
    • Filosofía: "Un gran poder conlleva una gran responsabilidad"

📈 APLICACIONES:
    • Periodismo de datos · Criminología · Prevención ciudadana
    • Asociaciones vecinales · Investigación social

⚖️  LEGALIDAD:
    Cumple con RGPD/LOPDGDD al no tratar datos personales.
    El usuario es el único responsable del uso de la herramienta.

Desarrollado por SpectrumSecurity · https://github.com/Condor2026/Diabolic_Peninsular_V17
================================================================================
"""

import os
import sys
import time
import json
import hashlib
import random
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from flask import Flask, render_template_string, jsonify, request
from collections import defaultdict
import urllib.parse

# ============================================
# COLORES (para terminal)
# ============================================

class Color:
    ROJO = '\033[91m'
    ROJO_OSCURO = '\033[31m'
    VERDE = '\033[92m'
    AMARILLO = '\033[93m'
    AZUL = '\033[94m'
    MAGENTA = '\033[95m'
    CIAN = '\033[96m'
    GRIS = '\033[90m'
    BLANCO = '\033[97m'
    NEGRITA = '\033[1m'
    SUBRAYADO = '\033[4m'
    PARPADEO = '\033[5m'
    RESET = '\033[0m'
    FONDO_ROJO = '\033[41m'
    FONDO_VERDE = '\033[42m'
    FONDO_AMARILLO = '\033[43m'
    FONDO_AZUL = '\033[44m'

def cprint(texto, color=None, negrita=False, subrayado=False, parpadeo=False, fondo=False, fin='\n'):
    colores = {
        'rojo': Color.ROJO, 'rojo_oscuro': Color.ROJO_OSCURO,
        'verde': Color.VERDE, 'amarillo': Color.AMARILLO,
        'azul': Color.AZUL, 'magenta': Color.MAGENTA,
        'cian': Color.CIAN, 'gris': Color.GRIS, 'blanco': Color.BLANCO
    }
    col = colores.get(color, '')
    neg = Color.NEGRITA if negrita else ''
    sub = Color.SUBRAYADO if subrayado else ''
    parp = Color.PARPADEO if parpadeo else ''
    fondo_color = ''
    if fondo:
        if color == 'rojo':
            fondo_color = Color.FONDO_ROJO
        elif color == 'verde':
            fondo_color = Color.FONDO_VERDE
        elif color == 'amarillo':
            fondo_color = Color.FONDO_AMARILLO
        elif color == 'azul':
            fondo_color = Color.FONDO_AZUL
    print(f"{fondo_color}{neg}{sub}{parp}{col}{texto}{Color.RESET}", end=fin)

# ============================================
# CONFIGURACIÓN - Periódicos de la península (ACTUALIZADOS 2026)
# ============================================

VERSION = "1.0"
PUERTO = 5014
ARCHIVO = 'diabolic_peninsular.json'
ARCHIVO_ESTADO = 'estado_periodicos_peninsular.json'
PAGINAS_BUSQUEDA = 10
TIEMPO_ESPERA = 1.5

# Periódicos de la España peninsular - Fuentes verificadas
PERIODICOS_BASE = [
    # NACIONALES (ámbito toda España)
    {'nombre': 'El País', 'url': 'https://elpais.com/noticias/sucesos/', 'base': 'https://elpais.com', 'zona': 'Nacional', 'activo': True},  # ACTUALIZADO
    {'nombre': 'El Mundo', 'url': 'https://www.elmundo.es/sucesos.html', 'base': 'https://www.elmundo.es', 'zona': 'Nacional', 'activo': True},  # ACTUALIZADO
    {'nombre': 'ABC', 'url': 'https://www.abc.es/espana/', 'base': 'https://www.abc.es', 'zona': 'Nacional', 'activo': True},
    {'nombre': 'La Razón', 'url': 'https://www.larazon.es/sucesos/', 'base': 'https://www.larazon.es', 'zona': 'Nacional', 'activo': True},  # ACTUALIZADO
    {'nombre': 'El Periódico', 'url': 'https://www.elperiodico.com/es/sucesos/', 'base': 'https://www.elperiodico.com', 'zona': 'Nacional', 'activo': True},
    {'nombre': '20 Minutos', 'url': 'https://www.20minutos.es/', 'base': 'https://www.20minutos.es', 'zona': 'Nacional', 'activo': True},
    {'nombre': 'El Español', 'url': 'https://www.elespanol.com/', 'base': 'https://www.elespanol.com', 'zona': 'Nacional', 'activo': True},
    {'nombre': 'El Confidencial', 'url': 'https://www.elconfidencial.com/espana/', 'base': 'https://www.elconfidencial.com', 'zona': 'Nacional', 'activo': True},
    {'nombre': 'OK Diario', 'url': 'https://okdiario.com/espana', 'base': 'https://okdiario.com', 'zona': 'Nacional', 'activo': True},
    {'nombre': 'elDiario.es', 'url': 'https://www.eldiario.es/', 'base': 'https://www.eldiario.es', 'zona': 'Nacional', 'activo': True},
    {'nombre': 'Público', 'url': 'https://www.publico.es/', 'base': 'https://www.publico.es', 'zona': 'Nacional', 'activo': True},
    {'nombre': 'Huffington Post', 'url': 'https://www.huffingtonpost.es/', 'base': 'https://www.huffingtonpost.es', 'zona': 'Nacional', 'activo': True},

    # ANDALUCÍA
    {'nombre': 'Diario de Sevilla', 'url': 'https://www.diariodesevilla.es/sucesos/', 'base': 'https://www.diariodesevilla.es', 'zona': 'Andalucía', 'activo': True},
    {'nombre': 'Diario de Cádiz', 'url': 'https://www.diariodecadiz.es/sucesos/', 'base': 'https://www.diariodecadiz.es', 'zona': 'Andalucía', 'activo': True},
    {'nombre': 'Málaga Hoy', 'url': 'https://www.malagahoy.es/sucesos/', 'base': 'https://www.malagahoy.es', 'zona': 'Andalucía', 'activo': True},
    {'nombre': 'Granada Hoy', 'url': 'https://www.granadahoy.com/', 'base': 'https://www.granadahoy.com', 'zona': 'Andalucía', 'activo': True},
    {'nombre': 'Ideal (Granada)', 'url': 'https://www.ideal.es/sucesos/', 'base': 'https://www.ideal.es', 'zona': 'Andalucía', 'activo': True},
    {'nombre': 'Diario Sur (Málaga)', 'url': 'https://www.diariosur.es/sucesos/', 'base': 'https://www.diariosur.es', 'zona': 'Andalucía', 'activo': True},
    {'nombre': 'Córdoba', 'url': 'https://www.diariocordoba.com/', 'base': 'https://www.diariocordoba.com', 'zona': 'Andalucía', 'activo': True},
    {'nombre': 'Huelva Información', 'url': 'https://www.huelvainformacion.es/', 'base': 'https://www.huelvainformacion.es', 'zona': 'Andalucía', 'activo': True},
    {'nombre': 'Diario de Almería', 'url': 'https://www.diariodealmeria.es/', 'base': 'https://www.diariodealmeria.es', 'zona': 'Andalucía', 'activo': True},
    {'nombre': 'Jaén', 'url': 'https://www.diariojaen.es/', 'base': 'https://www.diariojaen.es', 'zona': 'Andalucía', 'activo': True},

    # CATALUÑA
    {'nombre': 'La Vanguardia', 'url': 'https://www.lavanguardia.com/sucesos', 'base': 'https://www.lavanguardia.com', 'zona': 'Cataluña', 'activo': True},
    {'nombre': 'El Periódico (Cataluña)', 'url': 'https://www.elperiodico.com/es/sucesos/', 'base': 'https://www.elperiodico.com', 'zona': 'Cataluña', 'activo': True},
    {'nombre': 'Ara', 'url': 'https://www.ara.cat/societat/', 'base': 'https://www.ara.cat', 'zona': 'Cataluña', 'activo': True},
    {'nombre': 'El Nacional.cat', 'url': 'https://www.elnacional.cat/ca/societat', 'base': 'https://www.elnacional.cat', 'zona': 'Cataluña', 'activo': True},
    {'nombre': 'NacióDigital', 'url': 'https://www.naciodigital.cat/', 'base': 'https://www.naciodigital.cat', 'zona': 'Cataluña', 'activo': True},
    {'nombre': 'Diari de Girona', 'url': 'https://www.diaridegirona.cat/societat/', 'base': 'https://www.diaridegirona.cat', 'zona': 'Cataluña', 'activo': True},
    {'nombre': 'Segre', 'url': 'https://www.segre.com/', 'base': 'https://www.segre.com', 'zona': 'Cataluña', 'activo': True},
    {'nombre': 'Diari de Tarragona', 'url': 'https://www.diaridetarragona.com/', 'base': 'https://www.diaridetarragona.com', 'zona': 'Cataluña', 'activo': True},

    # COMUNIDAD DE MADRID
    {'nombre': 'El Mundo (Madrid)', 'url': 'https://www.elmundo.es/madrid.html', 'base': 'https://www.elmundo.es', 'zona': 'Madrid', 'activo': True},
    {'nombre': 'ABC (Madrid)', 'url': 'https://www.abc.es/espana/madrid/', 'base': 'https://www.abc.es', 'zona': 'Madrid', 'activo': True},
    {'nombre': 'La Razón (Madrid)', 'url': 'https://www.larazon.es/madrid/', 'base': 'https://www.larazon.es', 'zona': 'Madrid', 'activo': True},
    {'nombre': '20 Minutos Madrid', 'url': 'https://www.20minutos.es/madrid/', 'base': 'https://www.20minutos.es', 'zona': 'Madrid', 'activo': True},
    {'nombre': 'Telemadrid', 'url': 'https://www.telemadrid.es/noticias/madrid/', 'base': 'https://www.telemadrid.es', 'zona': 'Madrid', 'activo': True},

    # COMUNIDAD VALENCIANA
    {'nombre': 'Levante-EMV', 'url': 'https://www.levante-emv.com/sucesos/', 'base': 'https://www.levante-emv.com', 'zona': 'Valencia', 'activo': True},
    {'nombre': 'Las Provincias', 'url': 'https://www.lasprovincias.es/sucesos/', 'base': 'https://www.lasprovincias.es', 'zona': 'Valencia', 'activo': True},
    {'nombre': 'Información (Alicante)', 'url': 'https://www.informacion.es/sucesos/', 'base': 'https://www.informacion.es', 'zona': 'Valencia', 'activo': True},
    {'nombre': 'El Periódico Mediterráneo', 'url': 'https://www.elperiodicomediterraneo.com/', 'base': 'https://www.elperiodicomediterraneo.com', 'zona': 'Valencia', 'activo': True},

    # GALICIA
    {'nombre': 'La Voz de Galicia', 'url': 'https://www.lavozdegalicia.es/sucesos', 'base': 'https://www.lavozdegalicia.es', 'zona': 'Galicia', 'activo': True},
    {'nombre': 'Faro de Vigo', 'url': 'https://www.farodevigo.es/sucesos/', 'base': 'https://www.farodevigo.es', 'zona': 'Galicia', 'activo': True},
    {'nombre': 'El Correo Gallego', 'url': 'https://www.elcorreogallego.es/', 'base': 'https://www.elcorreogallego.es', 'zona': 'Galicia', 'activo': True},
    {'nombre': 'Diario de Pontevedra', 'url': 'https://www.diariodepontevedra.es/', 'base': 'https://www.diariodepontevedra.es', 'zona': 'Galicia', 'activo': True},

    # PAÍS VASCO
    {'nombre': 'El Correo', 'url': 'https://www.elcorreo.com/sucesos/', 'base': 'https://www.elcorreo.com', 'zona': 'País Vasco', 'activo': True},
    {'nombre': 'Diario Vasco', 'url': 'https://www.diariovasco.com/sucesos/', 'base': 'https://www.diariovasco.com', 'zona': 'País Vasco', 'activo': True},
    {'nombre': 'Deia', 'url': 'https://www.deia.eus/', 'base': 'https://www.deia.eus', 'zona': 'País Vasco', 'activo': True},

    # CASTILLA Y LEÓN
    {'nombre': 'El Norte de Castilla', 'url': 'https://www.elnortedecastilla.es/sucesos/', 'base': 'https://www.elnortedecastilla.es', 'zona': 'Castilla y León', 'activo': True},
    {'nombre': 'Diario de León', 'url': 'https://www.diariodeleon.es/', 'base': 'https://www.diariodeleon.es', 'zona': 'Castilla y León', 'activo': True},
    {'nombre': 'Diario de Burgos', 'url': 'https://www.diariodeburgos.es/', 'base': 'https://www.diariodeburgos.es', 'zona': 'Castilla y León', 'activo': True},
    {'nombre': 'La Gaceta de Salamanca', 'url': 'https://www.lagacetadesalamanca.es/', 'base': 'https://www.lagacetadesalamanca.es', 'zona': 'Castilla y León', 'activo': True},

    # ARAGÓN
    {'nombre': 'Heraldo de Aragón', 'url': 'https://www.heraldo.es/', 'base': 'https://www.heraldo.es', 'zona': 'Aragón', 'activo': True},
    {'nombre': 'El Periódico de Aragón', 'url': 'https://www.elperiodicodearagon.com/', 'base': 'https://www.elperiodicodearagon.com', 'zona': 'Aragón', 'activo': True},

    # ASTURIAS
    {'nombre': 'La Nueva España', 'url': 'https://www.lne.es/sucesos/', 'base': 'https://www.lne.es', 'zona': 'Asturias', 'activo': True},
    {'nombre': 'El Comercio', 'url': 'https://www.elcomercio.es/sucesos/', 'base': 'https://www.elcomercio.es', 'zona': 'Asturias', 'activo': True},

    # CANTABRIA
    {'nombre': 'El Diario Montañés', 'url': 'https://www.eldiariomontanes.es/sucesos/', 'base': 'https://www.eldiariomontanes.es', 'zona': 'Cantabria', 'activo': True},

    # LA RIOJA
    {'nombre': 'La Rioja', 'url': 'https://www.larioja.com/sucesos/', 'base': 'https://www.larioja.com', 'zona': 'La Rioja', 'activo': True},

    # MURCIA
    {'nombre': 'La Verdad', 'url': 'https://www.laverdad.es/sucesos/', 'base': 'https://www.laverdad.es', 'zona': 'Murcia', 'activo': True},
    {'nombre': 'La Opinión de Murcia', 'url': 'https://www.laopiniondemurcia.es/', 'base': 'https://www.laopiniondemurcia.es', 'zona': 'Murcia', 'activo': True},

    # NAVARRA
    {'nombre': 'Diario de Navarra', 'url': 'https://www.diariodenavarra.es/', 'base': 'https://www.diariodenavarra.es', 'zona': 'Navarra', 'activo': True},
    {'nombre': 'Noticias de Navarra', 'url': 'https://www.noticiasdenavarra.com/', 'base': 'https://www.noticiasdenavarra.com', 'zona': 'Navarra', 'activo': True},

    # EXTREMADURA
    {'nombre': 'Hoy (Extremadura)', 'url': 'https://www.hoy.es/sucesos/', 'base': 'https://www.hoy.es', 'zona': 'Extremadura', 'activo': True},
    {'nombre': 'El Periódico Extremadura', 'url': 'https://www.elperiodicoextremadura.com/', 'base': 'https://www.elperiodicoextremadura.com', 'zona': 'Extremadura', 'activo': True},
]

# Palabras clave de delitos (ampliado)
DELITOS = [
    'robo', 'robos', 'ladrón', 'ladrones', 'detenido', 'detenidos',
    'estafa', 'estafas', 'violencia', 'agresión', 'narcotráfico',
    'droga', 'cocaína', 'marihuana', 'asesinato', 'muerto',
    'homicidio', 'apuñalado', 'tiroteo', 'alunicero', 'butrón',
    'escalo', 'hurtos', 'hurto', 'sustrajo', 'sustrajeron',
    'peta', 'falcon', 'vuelco', 'machada', 'sucesos'
]

TIPOS_DELITO = {
    'robo': {'icono': '💰', 'color': '#8b0000'},
    'violencia': {'icono': '👊', 'color': '#ff0000'},
    'narcotrafico': {'icono': '💊', 'color': '#4b0082'},
    'estafa': {'icono': '📄', 'color': '#8b6b00'},
    'asesinato': {'icono': '💀', 'color': '#000000'},
    'sexual': {'icono': '⚠️', 'color': '#660066'}
}

# Zonas/Comunidades para la península
ZONAS = [
    'Nacional', 'Andalucía', 'Cataluña', 'Madrid', 'Valencia',
    'Galicia', 'País Vasco', 'Castilla y León', 'Aragón', 'Asturias',
    'Cantabria', 'La Rioja', 'Murcia', 'Navarra', 'Extremadura'
]

# ============================================
# DETECTOR AUTOMÁTICO DE URLs (MEJORADO)
# ============================================

class DetectorURLs:
    def __init__(self):
        self.archivo_estado = ARCHIVO_ESTADO
        self.estado = self.cargar_estado()
        self.posibles_paths = [
            'sucesos', 'sucesos/', 'local', 'local/', 'noticias', 'noticias/',
            'sucesos-mallorca', 'category/sucesos/', 'categoria/sucesos/',
            'sucesos.html', 'index.php/sucesos', 'seccion/sucesos',
            'successos', 'successos/', 'categoria/successos/', 'seccio/successos/',
            'tribunales', 'tribunales/', 'justicia', 'justicia/',          # NUEVOS
            'actualidad/sucesos', 'actualidad/sucesos/',                   # NUEVOS
            'espana/sucesos', 'espana/sucesos/'                            # NUEVOS
        ]

    def cargar_estado(self):
        if os.path.exists(self.archivo_estado):
            try:
                with open(self.archivo_estado, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return {}
        return {}

    def guardar_estado(self):
        with open(self.archivo_estado, 'w', encoding='utf-8') as f:
            json.dump(self.estado, f, indent=2)

    def encontrar_url_correcta(self, periodico):
        dominio = periodico['base']
        nombre = periodico['nombre']

        if nombre in self.estado and self.estado[nombre].get('url'):
            url_guardada = self.estado[nombre]['url']
            try:
                r = requests.get(url_guardada, timeout=5, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'})
                if r.status_code == 200:
                    return url_guardada
            except:
                pass

        for path in self.posibles_paths:
            url = f"{dominio}/{path}"
            try:
                r = requests.get(url, timeout=5, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'})
                if r.status_code == 200:
                    soup = BeautifulSoup(r.text, 'html.parser')
                    texto = soup.get_text().lower()
                    if any(d in texto for d in DELITOS) or 'sucesos' in texto:
                        self.estado[nombre] = {'url': url, 'path': path}
                        self.guardar_estado()
                        return url
            except:
                continue
        return None

    def verificar_todos(self, periodicos):
        cprint(f"\n{'='*70}", 'rojo', negrita=True)
        cprint(f"🔍 VERIFICANDO {len(periodicos)} PERIÓDICOS", 'rojo', negrita=True, fondo=True)
        cprint(f"{'='*70}", 'rojo', negrita=True)

        verificados = []
        activos = 0

        for p in periodicos:
            cprint(f"\n📰 {p['nombre']} ", 'amarillo', negrita=True, fin='')

            try:
                r = requests.get(p['url'], timeout=5, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'})
                if r.status_code == 200:
                    p['activo'] = True
                    cprint(f"✅ OK", 'verde')
                    activos += 1
                else:
                    nueva_url = self.encontrar_url_correcta(p)
                    if nueva_url:
                        p['url'] = nueva_url
                        p['activo'] = True
                        cprint(f"✅ NUEVA URL", 'verde')
                        activos += 1
                    else:
                        p['activo'] = False
                        cprint(f"❌ No encontrada", 'rojo')
            except:
                nueva_url = self.encontrar_url_correcta(p)
                if nueva_url:
                    p['url'] = nueva_url
                    p['activo'] = True
                    cprint(f"✅ NUEVA URL", 'verde')
                    activos += 1
                else:
                    p['activo'] = False
                    cprint(f"❌ Error conexión", 'rojo')

            verificados.append(p)
            time.sleep(1)

        cprint(f"\n{'='*70}", 'verde', negrita=True)
        cprint(f"📊 ACTIVOS: {activos} de {len(periodicos)}", 'verde', negrita=True)
        cprint(f"{'='*70}", 'verde', negrita=True)

        return verificados

# ============================================
# GESTOR DE DATOS
# ============================================

class GestorDatos:
    def __init__(self):
        self.archivo = ARCHIVO
        self.datos = self.cargar()
        self.detector = DetectorURLs()

    def cargar(self):
        if os.path.exists(self.archivo):
            try:
                with open(self.archivo, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return {'incidentes': [], 'ultima_actualizacion': None}
        return {'incidentes': [], 'ultima_actualizacion': None}

    def guardar(self):
        self.datos['ultima_actualizacion'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        with open(self.archivo, 'w', encoding='utf-8') as f:
            json.dump(self.datos, f, indent=2, ensure_ascii=False)

    def agregar_incidentes(self, nuevos):
        ids_existentes = {inc['id'] for inc in self.datos['incidentes']}
        contador = 0
        for n in nuevos:
            if n['id'] not in ids_existentes:
                self.datos['incidentes'].append(n)
                contador += 1
        if contador:
            self.guardar()
        return contador

    def detectar_tipo(self, texto):
        texto_lower = texto.lower()
        for tipo, datos in TIPOS_DELITO.items():
            if tipo == 'robo' and any(p in texto_lower for p in ['robo', 'robos', 'ladrón', 'sustrajo', 'alunicero', 'butrón', 'escalo']):
                return tipo
            elif tipo == 'violencia' and any(p in texto_lower for p in ['violencia', 'agresión', 'paliza', 'apuñalado', 'machada']):
                return tipo
            elif tipo == 'narcotrafico' and any(p in texto_lower for p in ['droga', 'cocaína', 'marihuana', 'narcotráfico', 'peta', 'falcon', 'vuelco']):
                return tipo
            elif tipo == 'estafa' and any(p in texto_lower for p in ['estafa', 'estafas', 'timaron']):
                return tipo
            elif tipo == 'asesinato' and any(p in texto_lower for p in ['asesinato', 'muerto', 'homicidio', 'cadáver']):
                return tipo
            elif tipo == 'sexual' and any(p in texto_lower for p in ['sexual', 'violación', 'abusos', 'menores']):
                return tipo
        return 'otro'

    def estadisticas(self, incidentes=None):
        if incidentes is None:
            incidentes = self.datos['incidentes']

        stats = {
            'total': len(incidentes),
            'zonas': defaultdict(int),
            'tipos': defaultdict(int),
            'fuentes': defaultdict(int),
            'municipios': defaultdict(int),
            'ultimos_7dias': 0,
            'ultimos_30dias': 0,
            'ultimos_90dias': 0,
            'tendencia': {}
        }

        hoy = datetime.now()
        hace_7d = (hoy - timedelta(days=7)).strftime('%Y-%m-%d')
        hace_30d = (hoy - timedelta(days=30)).strftime('%Y-%m-%d')
        hace_90d = (hoy - timedelta(days=90)).strftime('%Y-%m-%d')

        for inc in incidentes:
            if inc.get('zona'):
                stats['zonas'][inc['zona']] += 1
            if inc.get('tipo'):
                stats['tipos'][inc['tipo']] += 1
            if inc.get('fuente'):
                stats['fuentes'][inc['fuente']] += 1

            fecha = inc.get('fecha', '')
            if fecha >= hace_7d:
                stats['ultimos_7dias'] += 1
            if fecha >= hace_30d:
                stats['ultimos_30dias'] += 1
            if fecha >= hace_90d:
                stats['ultimos_90dias'] += 1

            if fecha and len(fecha) >= 7:
                mes = fecha[:7]
                stats['tendencia'][mes] = stats['tendencia'].get(mes, 0) + 1

        return stats

    def evolucion_mensual(self):
        meses = {}
        for inc in self.datos['incidentes']:
            if inc.get('fecha') and len(inc['fecha']) >= 7:
                mes = inc['fecha'][:7]
                meses[mes] = meses.get(mes, 0) + 1
        return dict(sorted(meses.items()))

# ============================================
# EXTRACTOR DE NOTICIAS (MEJORADO CON ROTACIÓN DE USER-AGENT Y MÁS FORMATOS)
# ============================================

class ExtractorNoticias:
    def __init__(self, periodicos):
        self.periodicos = periodicos
        self.session = requests.Session()
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/121.0'
        ]
        self.session.headers.update({'User-Agent': random.choice(self.user_agents)})
        self.cache_paginacion = {}

    def _generar_url_pagina(self, url_base, pagina):
        dominio = url_base.split('/')[2] if '//' in url_base else url_base
        if dominio in self.cache_paginacion:
            formato = self.cache_paginacion[dominio]
            return formato.format(pagina=pagina)

        # MÁS FORMATOS DE PAGINACIÓN (AMPLIADO)
        formatos = [
            f"{url_base}pagina/{{pagina}}/",
            f"{url_base}?page={{pagina}}",
            f"{url_base}{{pagina}}/",
            f"{url_base}page/{{pagina}}/",
            f"{url_base}index.php?page={{pagina}}",
            f"{url_base}listado?pag={{pagina}}",
            f"{url_base}?pag={{pagina}}",
            f"{url_base}?p={{pagina}}",
            f"{url_base}pag/{{pagina}}/",               # NUEVO
            f"{url_base}pagina/{{pagina}}",              # NUEVO (sin barra final)
            f"{url_base}?pageNumber={{pagina}}",         # NUEVO
            f"{url_base}?offset={{pagina}}"              # NUEVO
        ]

        for formato in formatos:
            url = formato.format(pagina=pagina)
            try:
                r = self.session.get(url, timeout=5)
                if r.status_code == 200:
                    self.cache_paginacion[dominio] = formato
                    return url
            except:
                continue
        return None

    def buscar_todo(self, paginas=10):
        cprint(f"\n{'='*80}", 'rojo', negrita=True)
        cprint(f"🔥 BÚSQUEDA EN {len(self.periodicos)} PERIÓDICOS", 'rojo', negrita=True, fondo=True)
        cprint(f"{'='*80}", 'rojo', negrita=True)

        todas = []
        total_activos = 0
        self.cache_paginacion = {}

        for periodico in self.periodicos:
            if not periodico.get('activo', True):
                continue

            total_activos += 1
            cprint(f"\n📰 {periodico['nombre']}", 'amarillo', negrita=True)
            cprint(f"   Zona: {periodico['zona']}", 'gris')

            encontrados = 0
            for pagina in range(1, paginas + 1):
                url = self._generar_url_pagina(periodico['url'], pagina)

                if not url:
                    if pagina == 1:
                        cprint(f"   📄 Página {pagina}... ✗ No accesible", 'rojo')
                    else:
                        cprint(f"   📄 Página {pagina}... ✗ No hay más páginas", 'amarillo')
                    break

                try:
                    cprint(f"   📄 Página {pagina}... ", 'gris', fin='')
                    r = self.session.get(url, timeout=8)

                    if r.status_code == 200:
                        soup = BeautifulSoup(r.text, 'html.parser')
                        articulos = []
                        articulos.extend(soup.find_all('article'))
                        articulos.extend(soup.find_all('div', class_=lambda x: x and ('article' in x or 'noticia' in x)))
                        articulos.extend(soup.find_all('h2'))

                        encontrados_pagina = 0
                        for art in articulos[:20]:
                            titulo_elem = art.find(['h2', 'h3']) if art.name != 'h2' else art
                            if not titulo_elem:
                                continue

                            titulo = titulo_elem.get_text().strip()
                            if len(titulo) < 20:
                                continue

                            titulo_lower = titulo.lower()
                            if any(d in titulo_lower for d in DELITOS):
                                zona = periodico['zona']
                                # Intentar detectar si menciona alguna comunidad específica
                                for z in ZONAS:
                                    if z.lower() in titulo_lower and z != 'Nacional':
                                        zona = z
                                        break

                                fecha_elem = art.find('time')
                                fecha = datetime.now().strftime('%Y-%m-%d')
                                if fecha_elem and fecha_elem.get('datetime'):
                                    fecha = fecha_elem.get('datetime')[:10]

                                tipo = gestor.detectar_tipo(titulo)

                                todas.append({
                                    'id': hashlib.md5(titulo.encode()).hexdigest()[:16],
                                    'titulo': titulo[:300],
                                    'fecha': fecha,
                                    'zona': zona,
                                    'tipo': tipo,
                                    'fuente': periodico['nombre']
                                })
                                encontrados_pagina += 1
                                encontrados += 1

                        cprint(f"✓ {encontrados_pagina}", 'verde')
                        if encontrados_pagina == 0 and pagina > 1:
                            break

                    elif r.status_code == 404:
                        cprint(f"✗ No existe (404)", 'amarillo')
                        break
                    else:
                        cprint(f"✗ Error {r.status_code}", 'rojo')

                except Exception as e:
                    cprint(f"✗ Error", 'rojo')

                time.sleep(TIEMPO_ESPERA)
            time.sleep(1)

        unicos = {}
        for n in todas:
            key = hashlib.md5(n['titulo'].encode()).hexdigest()
            if key not in unicos:
                unicos[key] = n

        cprint(f"\n{'='*80}", 'verde', negrita=True)
        cprint(f"📊 TOTAL: {len(unicos)} noticias únicas de {total_activos} periódicos", 'verde', negrita=True)
        cprint(f"{'='*80}", 'verde', negrita=True)

        return list(unicos.values())

# ============================================
# HTML TEMPLATE (interactivo) - Adaptado para península
# ============================================

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>🔥 DIABOLIC PENINSULAR v{{ version }}</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            background: #0a0505;
            color: #fff;
            font-family: 'Segoe UI', Arial;
            padding: 20px;
        }
        .container { max-width: 1400px; margin: 0 auto; }
        .header {
            background: linear-gradient(135deg, #4a0000, #8b0000, #ff0000);
            padding: 40px;
            border-radius: 30px;
            text-align: center;
            margin-bottom: 30px;
            box-shadow: 0 0 40px rgba(255,0,0,0.5);
        }
        .header h1 { font-size: 4em; text-shadow: 3px 3px 0 #4a0000; }
        .version-badge {
            background: black;
            color: #ff0000;
            padding: 5px 20px;
            border-radius: 50px;
            display: inline-block;
            margin-top: 10px;
        }
        .stats-header {
            display: flex;
            justify-content: center;
            gap: 20px;
            margin: 20px 0;
            flex-wrap: wrap;
        }
        .stat-header-item {
            background: rgba(0,0,0,0.7);
            padding: 10px 25px;
            border-radius: 50px;
            border: 1px solid #ff5555;
        }
        .btn {
            background: #8b0000;
            color: white;
            border: none;
            padding: 15px 40px;
            border-radius: 50px;
            font-size: 1.2em;
            cursor: pointer;
            margin: 10px;
            border: 2px solid #ff5555;
        }
        .btn:hover { background: #ff0000; }
        .config-btn {
            background: #2a0a0a;
            color: #ffaa00;
            border: 2px solid #8b0000;
            padding: 12px 25px;
            border-radius: 40px;
            cursor: pointer;
            margin: 10px;
            display: inline-flex;
            align-items: center;
            gap: 10px;
        }
        .config-btn:hover {
            background: #8b0000;
            color: white;
        }
        .filtros {
            display: flex; gap: 10px; justify-content: center; margin: 20px 0; flex-wrap: wrap;
        }
        .filtro-btn {
            background: #1a0a0a; color: white; border: 2px solid #8b0000;
            padding: 10px 20px; border-radius: 30px; text-decoration: none;
        }
        .filtro-btn:hover, .filtro-btn.activo { background: #8b0000; }
        .stats-grid {
            display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px; margin: 30px 0;
        }
        .stat-card {
            background: #1a0a0a; padding: 25px; border-radius: 15px;
            border-left: 8px solid #ff0000; text-align: center;
        }
        .stat-number { font-size: 3em; color: #ff5555; }
        .analysis-section {
            background: #1a0f0f; border-radius: 20px; padding: 25px; margin: 30px 0;
        }
        .section-title {
            color: #ff5555; font-size: 1.8em; margin-bottom: 20px;
            border-bottom: 2px solid #8b0000; padding-bottom: 10px;
        }
        .badge {
            background: #8b0000; color: white; padding: 5px 15px;
            border-radius: 30px; font-size: 0.6em;
        }
        .chart-bar-bg {
            width: 100%; height: 25px; background: #2a1a1a;
            border-radius: 12px; margin: 10px 0; overflow: hidden;
        }
        .chart-bar-fill {
            height: 100%; background: linear-gradient(90deg, #8b0000, #ff0000);
            border-radius: 12px; transition: width 0.5s;
        }
        .chart-label {
            display: flex; justify-content: space-between; color: #ffaa00; margin: 5px 0;
        }
        .incidente-card {
            background: #1a0a0a; margin: 15px 0; padding: 20px;
            border-radius: 12px; border-left: 10px solid #ff0000;
        }
        .incidente-titulo { font-size: 1.2em; font-weight: bold; margin-bottom: 10px; }
        .incidente-meta {
            color: #aaa; display: flex; gap: 20px; flex-wrap: wrap;
        }
        .zona-badge {
            background: #8b0000; color: white; padding: 3px 12px; border-radius: 20px;
        }
        .tipo-badge {
            padding: 3px 12px; border-radius: 20px; font-weight: bold; display: inline-block;
        }
        .footer {
            text-align: center; margin-top: 40px; padding: 20px;
            background: #1a0f0f; border-radius: 15px; color: #8b0000;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>⚡ DIABOLIC PENINSULAR ⚡</h1>
            <div class="version-badge">v{{ version }} · Puerto {{ puerto }}</div>
            <div class="stats-header">
                <div class="stat-header-item">📊 {{ total_incidentes }} incidentes</div>
                <div class="stat-header-item">📰 {{ total_fuentes }} fuentes</div>
                <div class="stat-header-item">🏛️ {{ total_zonas }} comunidades</div>
            </div>
        </div>

        <div style="text-align: center;">
            <form action="/actualizar" method="post" style="display: inline;">
                <button class="btn">🔥 ACTUALIZAR</button>
            </form>
            <a href="/exportar/json" class="config-btn">📥 JSON</a>
            <a href="/exportar/csv" class="config-btn">📥 CSV</a>
        </div>

        <div class="filtros">
            <a href="/" class="filtro-btn {% if filtro == 'todo' %}activo{% endif %}">TODOS</a>
            <a href="/filtro/7d" class="filtro-btn {% if filtro == '7d' %}activo{% endif %}">7 DÍAS</a>
            <a href="/filtro/30d" class="filtro-btn {% if filtro == '30d' %}activo{% endif %}">30 DÍAS</a>
            <a href="/filtro/90d" class="filtro-btn {% if filtro == '90d' %}activo{% endif %}">90 DÍAS</a>
        </div>

        <div class="stats-grid">
            <div class="stat-card">
                <div>TOTAL</div>
                <div class="stat-number">{{ stats.total }}</div>
            </div>
            <div class="stat-card">
                <div>ÚLTIMOS 7d</div>
                <div class="stat-number">{{ stats.ultimos_7dias }}</div>
            </div>
            <div class="stat-card">
                <div>ÚLTIMOS 30d</div>
                <div class="stat-number">{{ stats.ultimos_30dias }}</div>
            </div>
            <div class="stat-card">
                <div>ÚLTIMOS 90d</div>
                <div class="stat-number">{{ stats.ultimos_90dias }}</div>
            </div>
        </div>

        <div class="analysis-section">
            <div class="section-title">📍 POR COMUNIDAD</div>
            {% set total_zonas = stats.zonas.values()|sum %}
            {% for zona, cantidad in stats.zonas.items() %}
            <div class="chart-label">
                <span>{{ zona }}</span>
                <span>{{ cantidad }} ({{ (cantidad / total_zonas * 100)|round(1) }}%)</span>
            </div>
            <div class="chart-bar-bg">
                <div class="chart-bar-fill" style="width: {{ (cantidad / total_zonas * 100) }}%;"></div>
            </div>
            {% endfor %}
        </div>

        <div class="analysis-section">
            <div class="section-title">🔍 POR TIPO</div>
            {% set total_tipos = stats.tipos.values()|sum %}
            {% for tipo, cantidad in stats.tipos.items() %}
            {% set datos = TIPOS_DELITO.get(tipo, {'icono': '❓', 'color': '#666'}) %}
            <div class="chart-label">
                <span><span style="color: {{ datos.color }};">{{ datos.icono }}</span> {{ tipo|upper }}</span>
                <span>{{ cantidad }} ({{ (cantidad / total_tipos * 100)|round(1) }}%)</span>
            </div>
            <div class="chart-bar-bg">
                <div class="chart-bar-fill" style="width: {{ (cantidad / total_tipos * 100) }}%;"></div>
            </div>
            {% endfor %}
        </div>

        <div class="analysis-section">
            <div class="section-title">📰 TODOS LOS INCIDENTES ({{ incidentes|length }})</div>
            {% for inc in incidentes[:20] %}
            {% set tipo_color = TIPOS_DELITO.get(inc.tipo, {'color': '#666'}).color %}
            <div class="incidente-card" style="border-left-color: {{ tipo_color }};">
                <div class="incidente-titulo">{{ inc.titulo }}</div>
                <div class="incidente-meta">
                    <span class="zona-badge">{{ inc.zona or '?' }}</span>
                    <span>📅 {{ inc.fecha }}</span>
                    <span>📰 {{ inc.fuente }}</span>
                </div>
            </div>
            {% endfor %}
        </div>

        <div class="footer">
            <p>🔥 DIABOLIC PENINSULAR v{{ version }} · {{ periodicos_activos }} PERIÓDICOS ACTIVOS · 100% LEGAL</p>
            <p style="font-size:0.8em; color:#666;">"Un gran poder conlleva una gran responsabilidad" - Usa esta herramienta de forma ética.</p>
        </div>
    </div>
</body>
</html>
'''

# ============================================
# FLASK APP
# ============================================

app = Flask(__name__)
gestor = GestorDatos()

@app.route('/')
def home():
    incidentes = gestor.datos['incidentes']
    stats = gestor.estadisticas()
    periodicos_activos = len([p for p in PERIODICOS_BASE if p.get('activo', True)])
    return render_template_string(
        HTML_TEMPLATE,
        version=VERSION,
        puerto=PUERTO,
        stats=stats,
        incidentes=incidentes[::-1],
        total_incidentes=stats['total'],
        total_fuentes=len(stats['fuentes']),
        total_zonas=len(stats['zonas']),
        periodicos_activos=periodicos_activos,
        TIPOS_DELITO=TIPOS_DELITO,
        ZONAS=ZONAS,
        filtro='todo'
    )

@app.route('/filtro/<periodo>')
def filtro(periodo):
    incidentes = gestor.datos['incidentes']
    if periodo == '7d':
        hace = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
        incidentes = [i for i in incidentes if i.get('fecha', '') >= hace]
    elif periodo == '30d':
        hace = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
        incidentes = [i for i in incidentes if i.get('fecha', '') >= hace]
    elif periodo == '90d':
        hace = (datetime.now() - timedelta(days=90)).strftime('%Y-%m-%d')
        incidentes = [i for i in incidentes if i.get('fecha', '') >= hace]
    stats = gestor.estadisticas(incidentes)
    periodicos_activos = len([p for p in PERIODICOS_BASE if p.get('activo', True)])
    return render_template_string(
        HTML_TEMPLATE,
        version=VERSION,
        puerto=PUERTO,
        stats=stats,
        incidentes=incidentes[::-1],
        total_incidentes=stats['total'],
        total_fuentes=len(stats['fuentes']),
        total_zonas=len(stats['zonas']),
        periodicos_activos=periodicos_activos,
        TIPOS_DELITO=TIPOS_DELITO,
        ZONAS=ZONAS,
        filtro=periodo
    )

@app.route('/actualizar', methods=['POST'])
def actualizar():
    cprint(f"\n{'='*80}", 'rojo', negrita=True)
    cprint(f"🔥 ACTUALIZANDO NOTICIAS", 'rojo', negrita=True, fondo=True)
    cprint(f"{'='*80}", 'rojo', negrita=True)

    periodicos = gestor.detector.verificar_todos(PERIODICOS_BASE)
    extractor = ExtractorNoticias(periodicos)
    nuevas = extractor.buscar_todo(paginas=PAGINAS_BUSQUEDA)
    agregadas = gestor.agregar_incidentes(nuevas)

    cprint(f"\n{'='*80}", 'verde', negrita=True)
    cprint(f"✅ {agregadas} NUEVAS NOTICIAS", 'verde', negrita=True, fondo=True)
    cprint(f"{'='*80}", 'verde', negrita=True)

    return home()

@app.route('/exportar/json')
def exportar_json():
    return jsonify(gestor.datos)

@app.route('/exportar/csv')
def exportar_csv():
    import csv
    from io import StringIO
    si = StringIO()
    cw = csv.writer(si)
    cw.writerow(['Título', 'Fecha', 'Zona', 'Tipo', 'Fuente'])
    for inc in gestor.datos['incidentes']:
        cw.writerow([inc['titulo'], inc['fecha'], inc.get('zona',''), inc.get('tipo',''), inc['fuente']])
    return si.getvalue()

# ============================================
# MENÚ TERMINAL
# ============================================

def menu():
    while True:
        print(f"\n{Color.ROJO}{'═'*90}{Color.RESET}")
        print(f"{Color.FONDO_ROJO}{Color.NEGRITA}🔥 DIABOLIC PENINSULAR v{VERSION} - PUERTO {PUERTO}{Color.RESET}")
        print(f"{Color.ROJO}{'═'*90}{Color.RESET}")

        stats = gestor.estadisticas()
        periodicos_activos = len([p for p in PERIODICOS_BASE if p.get('activo', True)])

        print(f"\n{Color.VERDE}📊 ESTADÍSTICAS ACTUALES:{Color.RESET}")
        print(f"   📈 Total: {stats['total']} incidentes")
        if stats['total'] > 0:
            pct_7d = round((stats['ultimos_7dias'] / stats['total'] * 100), 1)
        else:
            pct_7d = 0
        print(f"   ⚡ Últimos 7 días: {stats['ultimos_7dias']} ({pct_7d}% del total)")
        print(f"   🔥 Últimos 30 días: {stats['ultimos_30dias']}")
        print(f"   📆 Últimos 90 días: {stats['ultimos_90dias']}")
        print(f"   🏛️ Comunidades activas: {len(stats['zonas'])}")
        print(f"   📰 Periódicos activos: {periodicos_activos}")
        print(f"   🔍 Tipos detectados: {len(stats['tipos'])}")

        print(f"\n{Color.AMARILLO}📋 COMANDOS COMPLETOS:{Color.RESET}")
        print(f"{Color.ROJO}[1]{Color.RESET} 🔍 Buscar noticias (con detección automática de URLs)")
        print(f"{Color.ROJO}[2]{Color.RESET} 📊 Ver análisis completo")
        print(f"{Color.ROJO}[3]{Color.RESET} 🔗 Ver conexiones entre incidentes")
        print(f"{Color.ROJO}[4]{Color.RESET} 📈 Ver evolución mensual")
        print(f"{Color.ROJO}[5]{Color.RESET} 🌐 Iniciar servidor web")
        print(f"{Color.ROJO}[6]{Color.RESET} 📰 Ver últimos 20 incidentes")
        print(f"{Color.ROJO}[7]{Color.RESET} 📥 Exportar datos (JSON/CSV)")
        print(f"{Color.ROJO}[8]{Color.RESET} 🔍 Verificar periódicos (detector automático)")
        print(f"{Color.ROJO}[9]{Color.RESET} 📊 Ver distribución por tipo")
        print(f"{Color.ROJO}[10]{Color.RESET} 🗑️ Salir")

        op = input(f"\n{Color.ROJO}➤ Opción: {Color.RESET}")

        if op == '1':
            periodicos = gestor.detector.verificar_todos(PERIODICOS_BASE)
            extractor = ExtractorNoticias(periodicos)
            nuevas = extractor.buscar_todo(paginas=PAGINAS_BUSQUEDA)
            agregadas = gestor.agregar_incidentes(nuevas)
            cprint(f"\n✅ {agregadas} nuevas noticias", 'verde', negrita=True)
            input(f"\n{Color.GRIS}Enter para continuar...{Color.RESET}")

        elif op == '2':
            stats = gestor.estadisticas()
            print(f"\n{Color.ROJO}{'═'*70}{Color.RESET}")
            print(f"{Color.AMARILLO}📊 ANÁLISIS COMPLETO{Color.RESET}")
            print(f"{Color.ROJO}{'═'*70}{Color.RESET}")

            print(f"\n{Color.VERDE}📈 TENDENCIAS:{Color.RESET}")
            print(f"   Total histórico: {stats['total']}")
            if stats['total'] > 0:
                pct_7d = round((stats['ultimos_7dias'] / stats['total'] * 100), 1)
                pct_30d = round((stats['ultimos_30dias'] / stats['total'] * 100), 1)
                pct_90d = round((stats['ultimos_90dias'] / stats['total'] * 100), 1)
            else:
                pct_7d = pct_30d = pct_90d = 0
            print(f"   Últimos 7 días: {stats['ultimos_7dias']} ({pct_7d}%)")
            print(f"   Últimos 30 días: {stats['ultimos_30dias']} ({pct_30d}%)")
            print(f"   Últimos 90 días: {stats['ultimos_90dias']} ({pct_90d}%)")

            print(f"\n{Color.VERDE}📍 DISTRIBUCIÓN POR COMUNIDAD:{Color.RESET}")
            for zona, cant in stats['zonas'].items():
                pct = round((cant / stats['total'] * 100), 1) if stats['total'] > 0 else 0
                print(f"   {zona}: {cant} ({pct}%)")

            print(f"\n{Color.VERDE}🔍 DISTRIBUCIÓN POR TIPO:{Color.RESET}")
            for tipo, cant in stats['tipos'].items():
                pct = round((cant / stats['total'] * 100), 1) if stats['total'] > 0 else 0
                print(f"   {tipo}: {cant} ({pct}%)")

            input(f"\n{Color.GRIS}Enter para continuar...{Color.RESET}")

        elif op == '3':
            print(f"\n{Color.ROJO}{'═'*70}{Color.RESET}")
            print(f"{Color.AMARILLO}🔗 CONEXIONES ENTRE INCIDENTES DETECTADAS{Color.RESET}")
            print(f"{Color.ROJO}{'═'*70}{Color.RESET}")

            incidentes = gestor.datos['incidentes'][-100:]
            if len(incidentes) < 5:
                print(f"{Color.GRIS}   Pocos incidentes para detectar patrones. Busca más noticias primero.{Color.RESET}")
                input(f"\n{Color.GRIS}Enter...{Color.RESET}")
                continue

            grupos = defaultdict(list)
            hace_30d = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')

            for inc in incidentes:
                if inc.get('fecha', '') >= hace_30d:
                    clave = (inc.get('tipo', 'otro'), inc.get('zona', 'Desconocida'))
                    grupos[clave].append(inc)

            patrones_mostrados = 0
            for (tipo, zona), lista in grupos.items():
                if len(lista) >= 3:
                    print(f"\n{Color.ROJO}🔥 PATRÓN: {len(lista)} {tipo.upper()} en {zona}{Color.RESET}")
                    for inc in sorted(lista, key=lambda x: x['fecha'], reverse=True)[:3]:
                        print(f"   • {inc['fecha']}: {inc['titulo'][:80]}...")
                    fechas = [inc['fecha'] for inc in lista]
                    dias = (datetime.now() - datetime.strptime(min(fechas), '%Y-%m-%d')).days if fechas else 0
                    if dias > 0:
                        freq = round(len(lista) / dias, 1)
                        print(f"   ⚡ Frecuencia: {freq} incidentes/día")
                    patrones_mostrados += 1

            print(f"\n{Color.AMARILLO}🔍 POSIBLES MISMAS BANDAS (modus operandi){Color.RESET}")
            palabras_modus = ['alunicero', 'butrón', 'escalo', 'tirón', 'violencia', 'estafa']
            for palabra in palabras_modus:
                relacionados = [inc for inc in incidentes if palabra in inc['titulo'].lower()]
                if len(relacionados) >= 2:
                    print(f"\n   {Color.ROJO}• {palabra.upper()}: {len(relacionados)} incidentes{Color.RESET}")
                    for inc in relacionados[:3]:
                        print(f"     - {inc['fecha']} ({inc['zona']}): {inc['titulo'][:60]}...")

            if patrones_mostrados == 0:
                print(f"\n{Color.GRIS}   No se detectaron patrones significativos en los últimos 30 días.{Color.RESET}")

            input(f"\n{Color.GRIS}Enter para continuar...{Color.RESET}")

        elif op == '4':
            evolucion = gestor.evolucion_mensual()
            print(f"\n{Color.ROJO}{'═'*70}{Color.RESET}")
            print(f"{Color.AMARILLO}📈 EVOLUCIÓN MENSUAL{Color.RESET}")
            print(f"{Color.ROJO}{'═'*70}{Color.RESET}")
            for mes, cant in evolucion.items():
                print(f"   {mes}: {cant} incidentes")
            input(f"\n{Color.GRIS}Enter para continuar...{Color.RESET}")

        elif op == '5':
            cprint(f"\n🌐 Servidor web: http://localhost:{PUERTO}", 'verde', negrita=True)
            cprint(f"   Presiona Ctrl+C para volver al menú", 'gris')
            app.run(host='0.0.0.0', port=PUERTO, debug=False)

        elif op == '6':
            incidentes = gestor.datos['incidentes'][-20:][::-1]
            print(f"\n{Color.ROJO}{'═'*70}{Color.RESET}")
            print(f"{Color.AMARILLO}📰 ÚLTIMOS 20 INCIDENTES{Color.RESET}")
            print(f"{Color.ROJO}{'═'*70}{Color.RESET}")
            for i, inc in enumerate(incidentes, 1):
                print(f"\n{Color.ROJO}{i:2d}.{Color.RESET} {inc['titulo'][:100]}...")
                print(f"      {inc['fecha']} | {inc.get('zona', '?')} | {inc['fuente']}")
            input(f"\n{Color.GRIS}Enter para continuar...{Color.RESET}")

        elif op == '7':
            with open('export.json', 'w', encoding='utf-8') as f:
                json.dump(gestor.datos, f, indent=2, ensure_ascii=False)
            with open('export.csv', 'w', encoding='utf-8') as f:
                f.write("Título,Fecha,Zona,Tipo,Fuente\n")
                for inc in gestor.datos['incidentes']:
                    f.write(f"{inc['titulo'][:100].replace(',', ' ')},{inc['fecha']},{inc.get('zona','')},{inc.get('tipo','')},{inc['fuente']}\n")
            cprint(f"\n✅ Exportados export.json y export.csv", 'verde')
            input(f"\n{Color.GRIS}Enter...{Color.RESET}")

        elif op == '8':
            gestor.detector.verificar_todos(PERIODICOS_BASE)
            input(f"\n{Color.GRIS}Enter...{Color.RESET}")

        elif op == '9':
            stats = gestor.estadisticas()
            print(f"\n{Color.ROJO}{'═'*70}{Color.RESET}")
            print(f"{Color.AMARILLO}📊 DISTRIBUCIÓN POR TIPO{Color.RESET}")
            print(f"{Color.ROJO}{'═'*70}{Color.RESET}")
            for tipo, cant in stats['tipos'].items():
                pct = round((cant / stats['total'] * 100), 1) if stats['total'] > 0 else 0
                barra = '█' * int(pct // 2)
                print(f"   {tipo}: {barra} {cant} ({pct}%)")
            input(f"\n{Color.GRIS}Enter...{Color.RESET}")

        elif op == '10':
            cprint(f"\n👋 Hasta pronto, DIABOLIC PENINSULAR se despide", 'rojo', negrita=True)
            break

        else:
            cprint(f"\n❌ Opción no válida", 'rojo')
            time.sleep(1)

# ============================================
# MAIN
# ============================================

if __name__ == '__main__':
    print(f"""
{Color.ROJO}
╔══════════════════════════════════════════════════════════════════╗
║  🔥 DIABOLIC PENINSULAR v{VERSION} - 62+ PERIÓDICOS ACTIVOS 🔥         ║
║  ⚡ España peninsular - OSINT 100% Legal                ⚡       ║
║  Andalucía · Cataluña · Madrid · Valencia · Galicia              ║
║  País Vasco · Castilla · Aragón · Asturias · Cantabria           ║
║  La Rioja · Murcia · Navarra · Extremadura                       ║
║                                         - By                     ║
║                                            •SpectrumSecurity•    ║
╚══════════════════════════════════════════════════════════════════╝
{Color.RESET}""")
    print(f"{Color.GRIS}🕷️  \"Un gran poder conlleva una gran responsabilidad\" - Spiderman{Color.RESET}")
    print(f"{Color.GRIS}⚖️  Uso ético y legal, solo datos públicos.{Color.RESET}")

    stats = gestor.estadisticas()
    print(f"{Color.VERDE}📊 Incidentes en base: {stats['total']}{Color.RESET}")
    print(f"{Color.AMARILLO}⏳ Última actualización: {gestor.datos.get('ultima_actualizacion', 'Nunca')}{Color.RESET}")

    print(f"\n{Color.CIAN}¿Cómo quieres ejecutar?{Color.RESET}")
    print(f"{Color.ROJO}1.{Color.RESET} Modo terminal (10 comandos)")
    print(f"{Color.ROJO}2.{Color.RESET} Modo web directo")

    modo = input(f"\n{Color.ROJO}➤ Elige: {Color.RESET}")

    if modo == '2':
        cprint(f"\n🌐 Servidor web: http://localhost:{PUERTO}", 'verde', negrita=True)
        cprint(f"   Presiona Ctrl+C para detener", 'gris')
        app.run(host='0.0.0.0', port=PUERTO, debug=True)
    else:
        menu()
