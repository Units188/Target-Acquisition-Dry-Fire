#!/bin/bash

# ============================================
# Script de build avec Conda
# Crée l'env conda, installe, et build
# ============================================

echo ""
echo "🎯 Build avec Conda"
echo "======================================================"
echo ""

# Vérifier que conda est installé
if ! command -v conda &> /dev/null; then
    echo "❌ Conda n'est pas installé"
    echo "   Utilisez build_with_venv.sh à la place"
    exit 1
fi

echo "✅ Conda trouvé"

# Nom de l'environnement
ENV_NAME="entrainement_tir"

# Vérifier si l'environnement existe déjà
if conda env list | grep -q "^${ENV_NAME} "; then
    echo ""
    echo "✅ Environnement '$ENV_NAME' trouvé"
else
    echo ""
    echo "📦 Création de l'environnement conda..."
    conda create -n $ENV_NAME python=3.11 -y
    echo "   ✅ Environnement créé"
fi

# Activer l'environnement
echo ""
echo "🔄 Activation de l'environnement..."
source $(conda info --base)/etc/profile.d/conda.sh
conda activate $ENV_NAME

# Vérifier l'activation
if [ "$CONDA_DEFAULT_ENV" != "$ENV_NAME" ]; then
    echo "❌ Impossible d'activer l'environnement"
    exit 1
fi

echo "   ✅ Environnement activé: $CONDA_DEFAULT_ENV"

# Installer PyInstaller
echo ""
echo "📦 Installation de PyInstaller..."
pip install --quiet --upgrade pip
pip install --quiet pyinstaller

# Nettoyer
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
    echo "🗑️  Pour supprimer l'environnement conda :"
    echo "   conda deactivate"
    echo "   conda remove -n $ENV_NAME --all -y"
    echo ""
    echo "======================================================"
    echo ""
    
    # Désactiver
    conda deactivate
    
else
    echo ""
    echo "======================================================"
    echo "❌ BUILD ÉCHOUÉ"
    echo "======================================================"
    echo ""
    echo "Testez le script directement :"
    echo "   conda activate $ENV_NAME"
    echo "   python entrainement_tir_mac.py"
    echo ""
    
    # Désactiver
    conda deactivate
    exit 1
fi
