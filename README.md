
# Présentation du module

**apifoncier** est un module Python qui propose 
une boîte à outils pour interagir plus facilement avec [l'API
Données foncières du Cerema](https://apidf-preprod.cerema.fr/).

Il permet d'interroger facilement les différentes bases de données 
foncières produites par le Cerema et la DGALN directement en Python. 

# Installation

``` python
pip install apifoncier
```

# Documentation du module

La documentation complète est accessible au lien suivant : [https://rcadot.github.io/py.apifoncier/](https://rcadot.github.io/py.apifoncier/)

Des exemples sous forme de notebook sont également proposées.

# Quickstart

Quelques exemples pour démarrer :

```python
## Récupérer des données de consommation d'espace sur une commune
import apifoncier.ind_conso_espace as conso

df = conso.communes(code_insee='59350')
```

```python
## Récupérer des données de prix sur une commune
import apifoncier.ind_prix as prix

df = prix.communes(code_insee='59350')
```


```python
## Récupérer des transactions issues de DVF+ sur une commune
import apifoncier.dvf_opendata as dvf

df = dvf.mutations(code_insee='59350')
# avec les geometries
gdf = dvf.geomutations(in_bbox=[3, 50, 3.01, 50.01])
```

# Ressources

Pour retrouver toutes les informations sur les données foncières :
[datafoncier.cerema.fr](https://datafoncier.cerema.fr)

Dictionnaire et documentation sur toutes les variables :
[doc-datafoncier.cerema.fr](http://doc-datafoncier.cerema.fr)

[Pour en savoir plus sur l’API données foncières du
cerema.](https://apidf-preprod.cerema.fr/swagger/)
