#!/bin/bash

# ============================================
# Script de build avec environnement virtuel
# Crée l'env, installe les dépendances, et build
# ============================================

echo ""
echo "🎯 Build avec Environnement Virtuel"
echo "======================================================"
echo ""

# Vérifier Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 n'est pas installé"
    exit 1
fi

echo "✅ Python trouvé: $(python3 --version)"

# Créer l'environnement virtuel s'il n'existe pas
if [ ! -d "venv" ]; then
    echo ""
    echo "📦 Création de l'environnement virtuel..."
    python3 -m venv venv
    echo "   ✅ Environnement créé"
else
    echo ""
    echo "✅ Environnement virtuel trouvé"
fi

# Activer l'environnement
echo ""
echo "🔄 Activation de l'environnement virtuel..."
source venv/bin/activate

# Vérifier l'activation
if [ -z "$VIRTUAL_ENV" ]; then
    echo "❌ Impossible d'activer l'environnement virtuel"
    exit 1
fi

echo "   ✅ Environnement activé: $VIRTUAL_ENV"

# Installer PyInstaller
echo ""
echo "📦 Installation de PyInstaller..."
pip install --quiet --upgrade pip
pip install --quiet pyinstaller

# Nettoyer les builds précédents
echo ""
echo "🧹 Nettoyage..."
rm -rf build dist __pycache__ *.pyc

# Builder
echo ""
echo "🔨 Construction de l'application..."
echo "   (Cela peut prendre 1-2 minutes...)"
echo ""

pyinstaller --clean build_mac.spec

# Vérifier le résultat
if [ -d "dist/EntrainementTir.app" ]; then
    echo ""
    echo "======================================================"
    echo "✅ BUILD RÉUSSI !"
    echo "======================================================"
    
    # Supprimer la quarantaine
    echo ""
    echo "🔓 Suppression de la quarantaine macOS..."
    xattr -cr dist/EntrainementTir.app
    
    echo ""
    echo "📱 Application créée :"
    echo "   📂 dist/EntrainementTir.app"
    echo ""
    echo "🚀 Pour lancer :"
    echo "   open dist/EntrainementTir.app"
    echo ""
    echo "💾 Pour installer :"
    echo "   cp -r dist/EntrainementTir.app /Applications/"
    echo ""
    echo "🗑️  Pour nettoyer l'environnement virtuel :"
    echo "   rm -rf venv"
    echo ""
    echo "======================================================"
    echo ""
    
    # Désactiver l'environnement
    deactivate
    
else
    echo ""
    echo "======================================================"
    echo "❌ BUILD ÉCHOUÉ"
    echo "======================================================"
    echo ""
    echo "Testez le script directement :"
    echo "   source venv/bin/activate"
    echo "   python entrainement_tir_mac.py"
    echo ""
    
    # Désactiver l'environnement
    deactivate
    exit 1
fi
