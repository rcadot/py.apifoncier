# apifoncier

`apifoncier` est un client Python pour l'[API Données foncières du Cerema](https://apidf-preprod.cerema.fr/swagger/). Il donne accès, sous forme de tableaux pandas (ou polars) et de `GeoDataFrame`, aux bases foncières produites par le Cerema et la DGALN : Fichiers fonciers, DV3F, DVF+ en accès libre, Cartofriches, consommation d'espace et indicateurs de marché immobilier.

Les flux Fichiers fonciers et DV3F sont à accès restreint et exigent un jeton. Tous les autres sont librement accessibles.

## Installation

```bash
pip install apifoncier
```

Le format de sortie polars est facultatif et s'installe avec l'extra correspondant :

```bash
pip install "apifoncier[polars]"
```

Le paquet requiert Python 3.9 ou une version ultérieure.

## Démarrage rapide

### Accès libre

Chaque module thématique expose des fonctions qui prennent un code INSEE, une emprise ou un point, et renvoient un tableau. Les fonctions dont le nom commence par `geo` renvoient un `GeoDataFrame`.

```python
import apifoncier.ind_conso_espace as conso
import apifoncier.dvf_opendata as dvf

# Consommation d'espace sur une commune
df = conso.communes(code_insee="59350")

# Mutations DVF+ sur une commune, puis avec leurs géométries
df = dvf.mutations(code_insee="59350")
gdf = dvf.geomutations(in_bbox=[3, 50, 3.01, 50.01])
```

### Accès restreint

Pour les Fichiers fonciers et DV3F, il faut appartenir à une structure publique bénéficiaire et demander un jeton sur [ConsultDF](https://consultdf.cerema.fr/consultdf/services/apidf). Le plus simple est de le fournir par la variable d'environnement `APIFONCIER_TOKEN`, que le module lit lorsque `TOKEN` n'est pas configuré :

```bash
export APIFONCIER_TOKEN="<jeton>"
```

```python
import apifoncier.ff as ff
import apifoncier.dv3f as dv3f

parcelles = ff.parcelles(code_insee="59646")
mutations = dv3f.mutations(code_insee="59646")
```

Le jeton ne doit jamais être écrit en clair dans un script ou un notebook versionné.

## Configuration

La configuration est globale et se modifie avec `apifoncier.configure`. Les clés sont insensibles à la casse, et une clé inconnue ou une valeur invalide lève une `ValidationError`.

```python
import apifoncier

apifoncier.configure(TIMEOUT=30, PAGE_SIZE=200, PROGRESS_BAR=False)
apifoncier.get_config()  # configuration courante, jeton masqué
apifoncier.reset()  # retour aux valeurs par défaut
```

Les clés disponibles sont `BASE_URL`, `TOKEN`, `PROXY`, `PROGRESS_BAR`, `MAX_ATTEMPTS`, `BACKOFF_FACTOR`, `TIMEOUT`, `PAGE_SIZE` et `OUTPUT_FORMAT`. Leurs valeurs par défaut et leur rôle sont décrits dans la [documentation](https://rcadot.github.io/py.apifoncier/). La variable d'environnement `APIFONCIER_BASE_URL` permet de modifier l'URL de l'API sans toucher au code.

## Formats de sortie

Les fonctions renvoient par défaut des `DataFrame` pandas. Avec `OUTPUT_FORMAT="polars"`, elles renvoient des `DataFrame` polars (extra `polars` requis). Les fonctions `geo*` renvoient toujours un `GeoDataFrame` en EPSG:4326, indexé par l'identifiant des entités, y compris lorsque le résultat est vide.

```python
apifoncier.configure(OUTPUT_FORMAT="polars")
```

## Interroger un endpoint sans fonction dédiée

La fonction `apifoncier.get` interroge un endpoint de liste quelconque en bénéficiant de la pagination, des nouvelles tentatives et du contrôle des paramètres de localisation.

```python
apifoncier.get("/cartofriches/friches/", code_insee="59350")
apifoncier.get("/ff/geotups/", geo=True, use_token=True, code_insee="59350")
```

## Sécurité

Le jeton n'est envoyé qu'aux endpoints à accès restreint, uniquement en HTTPS et uniquement vers l'hôte de `BASE_URL`, faute de quoi une `InsecureTransportError` est levée. Les liens de pagination qui désignent un autre hôte sont refusés, et les identifiants insérés dans les chemins d'URL sont contrôlés puis encodés. Pour signaler une vulnérabilité, voir [SECURITY.md](SECURITY.md).

## Développement

Les instructions d'installation de l'environnement, les commandes de test et les conventions de contribution figurent dans [CONTRIBUTING.md](CONTRIBUTING.md). La suite de tests s'exécute hors ligne et ne demande aucun jeton.

## Ressources

La documentation du paquet est publiée à l'adresse <https://rcadot.github.io/py.apifoncier/>. Pour les données elles-mêmes, on se reportera à <https://datafoncier.cerema.fr> et au dictionnaire des variables sur <https://doc-datafoncier.cerema.fr>. La description de l'API se trouve dans son [swagger](https://apidf-preprod.cerema.fr/swagger/).

## Licence

Ce projet est distribué sous licence MIT. Voir le fichier [LICENSE](LICENSE).
