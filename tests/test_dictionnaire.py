"""Vérifie que le dictionnaire de données reflète le code."""

import importlib.util
from pathlib import Path

SCRIPT = Path(__file__).resolve().parent.parent / "scripts" / "generer_dictionnaire.py"


def test_dictionnaire_donnees_a_jour():
    spec = importlib.util.spec_from_file_location("generer_dictionnaire", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    assert module.TARGET.read_text(encoding="utf-8") == module.render(), (
        "docs/dictionnaire_donnees.rst est obsolète : "
        "lancer `uv run python scripts/generer_dictionnaire.py`."
    )
