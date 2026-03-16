#!/bin/bash
# Script de instalación automática para DIABOLIC PENINSULAR

echo "🔥 Instalando DIABOLIC PENINSULAR..."
echo ""

# Actualizar paquetes (para Termux)
if [ -d "/data/data/com.termux" ]; then
    echo "📱 Entorno Termux detectado"
    pkg update && pkg upgrade -y
    pkg install python git -y
else
    echo "💻 Entorno Linux detectado"
    sudo apt update && sudo apt install python3 python3-pip git -y
fi

# Instalar dependencias Python
echo ""
echo "📦 Instalando dependencias..."
pip install flask requests beautifulsoup4

# Clonar repositorio
echo ""
echo "📂 Clonando repositorio..."
git clone https://github.com/Condor2026/Diabolic_Peninsular_V17
cd Diabolic_Peninsular_V17

echo ""
echo "✅ Instalación completada."
echo "🚀 Para ejecutar:"
echo "   python Diabolic_Peninsular_V17.py"
echo ""
echo "📖 Más información en el README.md"
