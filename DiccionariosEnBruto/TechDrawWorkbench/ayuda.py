# Copyright (C) 2026 El Equipo del Proyecto DAV
# Universidad Autónoma de Entre Ríos (UADER)
# Bajo la dirección de Guillermo Gerard y Gallo Fabricio David

from Page.ayuda import ayuda as ayuda_page
from Views.ayuda import ayuda as ayuda_views
from Features.ayuda import ayuda as ayuda_features

def ayuda():
    print("==========================================================")
    print("SISTEMA DAV - DICCIONARIO MAESTRO: TECHDRAW WORKBENCH")
    print("==========================================================")
    ayuda_page()
    print("-" * 58)
    ayuda_views()
    print("-" * 58)
    ayuda_features()
    print("==========================================================")