"""Génère ``docs/dictionnaire_donnees.rst`` à partir du code du paquet.

Le dictionnaire décrit, pour chaque fonction publique, l'endpoint interrogé,
le mode d'accès, l'objet renvoyé et chacun des paramètres (type et
signification, tirés des annotations et des docstrings).

Usage :
    uv run python scripts/generer_dictionnaire.py          # écrit le fichier
    uv run python scripts/generer_dictionnaire.py --check  # vérifie qu'il est à jour
"""

from __future__ import annotations

import inspect
import re
import sys
from pathlib import Path
from typing import Callable, Dict, List, Tuple

import apifoncier
from apifoncier import (
    cartofriches,
    config,
    dv3f,
    dvf_opendata,
    exceptions,
    ff,
    ind_conso_espace,
    ind_marche,
    ind_prix,
)

TARGET = Path(__file__).resolve().parent.parent / "docs" / "dictionnaire_donnees.rst"

# (module, accès, [(fonction, endpoint)])
CATALOGUE: List[Tuple[object, str, List[Tuple[Callable, str]]]] = [
    (
        cartofriches,
        "libre",
        [
            (cartofriches.friches, "/cartofriches/friches/"),
            (cartofriches.geofriches, "/cartofriches/geofriches/"),
            (cartofriches.friche, "/cartofriches/friches/{site_id}/"),
        ],
    ),
    (
        dvf_opendata,
        "libre",
        [
            (dvf_opendata.mutations, "/dvf_opendata/mutations/"),
            (dvf_opendata.geomutations, "/dvf_opendata/geomutations/"),
            (dvf_opendata.mutation, "/dvf_opendata/mutations/{idmutation}/"),
        ],
    ),
    (
        dv3f,
        "restreint (jeton)",
        [
            (dv3f.mutations, "/dv3f/mutations/"),
            (dv3f.geomutations, "/dv3f/geomutations/"),
            (dv3f.mutation, "/dv3f/mutations/{idmutation}/"),
        ],
    ),
    (
        ff,
        "restreint (jeton)",
        [
            (ff.parcelles, "/ff/parcelles/"),
            (ff.geoparcelles, "/ff/geoparcelles/"),
            (ff.parcelle, "/ff/parcelles/{idpar}/"),
            (ff.tups, "/ff/tups/"),
            (ff.geotups, "/ff/geotups/"),
            (ff.tup, "/ff/tups/{idtup}/"),
            (ff.locaux, "/ff/locaux/"),
            (ff.local, "/ff/locaux/{idlocal}/"),
            (ff.proprios, "/ff/proprios/"),
            (ff.proprio, "/ff/proprios/{idprodroit}/"),
        ],
    ),
    (
        ind_conso_espace,
        "libre",
        [
            (
                ind_conso_espace.communes,
                "/indicateurs/conso_espace/communes/{code_insee}/",
            ),
            (
                ind_conso_espace.departements,
                "/indicateurs/conso_espace/departements/{coddep}/",
            ),
        ],
    ),
    (
        ind_prix,
        "libre",
        [
            (ind_prix.aav, "/indicateurs/dv3f/aav/{periode}/{code_insee}/"),
            (ind_prix.communes, "/indicateurs/dv3f/communes/{periode}/{code_insee}/"),
            (
                ind_prix.departements,
                "/indicateurs/dv3f/departements/{periode}/{coddep}/",
            ),
            (ind_prix.epci, "/indicateurs/dv3f/epci/{periode}/{code_insee}/"),
            (ind_prix.regions, "/indicateurs/dv3f/regions/{periode}/{code_insee}/"),
        ],
    ),
    (
        ind_marche,
        "libre",
        [
            (ind_marche.prix_volume, "/indicateurs/dv3f/prix/{periode}/"),
            (ind_marche.activite, "/indicateurs/dv3f/activite/"),
            (ind_marche.accessibilite, "/indicateurs/dv3f/accessibilite/"),
            (
                ind_marche.valorisation,
                "/indicateurs/dv3f/valorisation/{echelle}/{code_insee}/",
            ),
        ],
    ),
]


def parse_args_section(doc: str) -> Dict[str, str]:
    """Extrait la section ``Args`` d'une docstring Google.

    Args:
        doc: Docstring de la fonction.

    Returns:
        Un dictionnaire ``{paramètre: description}``.
    """
    match = re.search(r"\n\s*Args:\n(.*?)(\n\s*\n\s*[A-Z][a-z]+:\n|\Z)", doc, re.S)
    if not match:
        return {}
    descriptions: Dict[str, str] = {}
    current = None
    for line in match.group(1).splitlines():
        item = re.match(r" {4}(\w+): (.*)", line)
        if item:
            current = item.group(1)
            descriptions[current] = item.group(2).strip()
        elif current and line.strip():
            descriptions[current] += " " + line.strip()
    return descriptions


def type_label(annotation: object) -> str:
    """Rend lisible une annotation de type (forme textuelle).

    Args:
        annotation: Annotation telle que conservée par ``inspect``.

    Returns:
        Le libellé du type.
    """
    text = str(annotation).replace("typing.", "")
    optional = re.fullmatch(r"Optional\[(.*)\]", text)
    if optional:
        text = optional.group(1)
    text = re.sub(r"Union\[(.*)\]", lambda m: m.group(1).replace(", ", " | "), text)
    aliases = {
        "Codes": "str | liste de str",
        "Multi": "str | liste de str",
        "BBox": "liste de 4 float",
        "Point": "liste de 2 float",
        "Table": "DataFrame",
    }
    return aliases.get(text, text)


def returns_label(func: Callable) -> str:
    """Décrit l'objet renvoyé par une fonction.

    Args:
        func: Fonction publique.

    Returns:
        Le libellé de l'objet renvoyé.
    """
    annotation = str(inspect.signature(func).return_annotation)
    if "GeoDataFrame" in annotation:
        return "GeoDataFrame (EPSG:4326), index = identifiant"
    return "DataFrame pandas (ou polars si OUTPUT_FORMAT='polars')"


def escape(text: str) -> str:
    """Neutralise les caractères de balisage RST problématiques en cellule.

    Args:
        text: Texte brut.

    Returns:
        Le texte utilisable dans une ``list-table``.
    """
    return text.replace("|", "\\|")


def render() -> str:
    """Construit le contenu complet du dictionnaire de données.

    Returns:
        Le texte reStructuredText.
    """
    out: List[str] = [
        ".. Fichier généré par scripts/generer_dictionnaire.py : ne pas modifier à la main.",
        "",
        "Dictionnaire de données",
        "=======================",
        "",
        "Ce dictionnaire recense, pour chaque fonction publique du paquet, "
        "l'endpoint de l'API interrogé, le mode d'accès, l'objet renvoyé et les "
        "paramètres acceptés. La signification des champs renvoyés par l'API est "
        "documentée sur `doc-datafoncier.cerema.fr <https://doc-datafoncier.cerema.fr>`_.",
        "",
        "Conventions communes aux endpoints de liste :",
        "",
        "* un paramètre de localisation au moins est requis ; par ordre de priorité "
        "``lon_lat``, ``in_bbox``, ``code_insee``, ``code``, ``coddep`` ;",
        "* les listes de valeurs sont transmises séparées par des virgules ;",
        "* ``page_size`` est fixé par la configuration ``PAGE_SIZE`` et la "
        "pagination est parcourue intégralement.",
        "",
    ]
    for module, access, entries in CATALOGUE:
        name = module.__name__
        title = f"Module ``{name}``"
        out += [title, "-" * len(title), "", f"Accès : {access}.", ""]
        for func, endpoint in entries:
            sub = f"``{func.__name__}``"
            out += [sub, "^" * len(sub), ""]
            out += [
                f"* Endpoint : ``GET {endpoint}``",
                f"* Renvoie : {returns_label(func)}",
                "",
            ]
            descriptions = parse_args_section(inspect.getdoc(func) or "")
            params = inspect.signature(func).parameters
            out += [
                ".. list-table::",
                "   :header-rows: 1",
                "   :widths: 20 20 15 45",
                "",
                "   * - Paramètre",
                "     - Type",
                "     - Défaut",
                "     - Description",
            ]
            for pname, param in params.items():
                default = (
                    "requis"
                    if param.default is inspect.Parameter.empty
                    else repr(param.default)
                )
                out += [
                    f"   * - ``{pname}``",
                    f"     - {escape(type_label(param.annotation))}",
                    f"     - ``{default}``",
                    f"     - {escape(descriptions.get(pname, ''))}",
                ]
            out.append("")
    out += render_config()
    out += render_exceptions()
    return "\n".join(out).rstrip() + "\n"


def render_config() -> List[str]:
    """Décrit les paramètres de configuration.

    Returns:
        Les lignes reStructuredText de la section.
    """
    lines = [
        "Configuration",
        "-------------",
        "",
        "Paramètres modifiables par :func:`apifoncier.configure` "
        "(clés insensibles à la casse).",
        "",
        ".. list-table::",
        "   :header-rows: 1",
        "",
        "   * - Clé",
        "     - Valeur par défaut",
    ]
    for key, value in config.CONFIG_INIT.items():
        lines += [f"   * - ``{key}``", f"     - ``{value!r}``"]
    lines += [
        "",
        "Variables d'environnement : ``APIFONCIER_TOKEN`` (jeton, utilisé si "
        "``TOKEN`` n'est pas configuré) et ``APIFONCIER_BASE_URL``.",
        "",
    ]
    return lines


def render_exceptions() -> List[str]:
    """Décrit la hiérarchie des exceptions.

    Returns:
        Les lignes reStructuredText de la section.
    """
    lines = [
        "Exceptions",
        "----------",
        "",
        ".. list-table::",
        "   :header-rows: 1",
        "",
        "   * - Exception",
        "     - Hérite de",
        "     - Signification",
    ]
    for name in (
        "ApiFoncierError",
        "ValidationError",
        "ApiDFError",
        "AuthenticationError",
        "TokenNotConfigured",
        "InsecureTransportError",
    ):
        cls = getattr(exceptions, name)
        bases = ", ".join(base.__name__ for base in cls.__bases__)
        summary = (inspect.getdoc(cls) or "").splitlines()[0]
        lines += [f"   * - ``{name}``", f"     - ``{bases}``", f"     - {summary}"]
    lines.append("")
    return lines


def main() -> int:
    """Écrit ou vérifie le dictionnaire de données.

    Returns:
        Le code de sortie du programme.
    """
    content = render()
    if "--check" in sys.argv:
        if TARGET.read_text(encoding="utf-8") != content:
            print(f"{TARGET} n'est pas à jour : relancer le script.")
            return 1
        return 0
    TARGET.write_text(content, encoding="utf-8")
    print(f"{TARGET} écrit (apifoncier {apifoncier.__version__}).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
