# Politique de sécurité

## Signaler une vulnérabilité

Une vulnérabilité ne doit pas être décrite dans une issue publique. Le signalement se fait de façon privée, au moyen des « Security advisories » GitHub du dépôt [rcadot/py.apifoncier](https://github.com/rcadot/py.apifoncier) (onglet « Security », puis « Report a vulnerability »). Il est utile d'y indiquer la version concernée, les conditions de reproduction et l'impact estimé.

## Bonnes pratiques sur le jeton

Le jeton d'accès donne accès aux données restreintes (Fichiers fonciers, DV3F) au nom de son titulaire. Il doit être traité comme un mot de passe.

On évitera de l'écrire en clair dans un script ou un notebook versionné, y compris dans un dépôt privé. La variable d'environnement `APIFONCIER_TOKEN`, lue par le module lorsque `TOKEN` n'est pas configuré, convient à la plupart des usages. Lorsque le jeton doit être transmis par `configure(TOKEN=...)`, on le lira dans l'environnement avec `os.environ` ou on le saisira à l'exécution avec `getpass`. Les sorties de notebook doivent aussi être vérifiées avant publication. `apifoncier.get_config()` masque le jeton et peut être affiché sans risque.

Si un jeton a été exposé, il faut le considérer comme compromis. Les modalités d'obtention d'un jeton figurent sur [ConsultDF](https://consultdf.cerema.fr/consultdf/services/apidf).

## Garanties offertes par le module

Le jeton n'est envoyé qu'aux endpoints à accès restreint, uniquement en HTTPS et uniquement vers l'hôte configuré dans `BASE_URL`. Dans le cas contraire, le module lève une `InsecureTransportError` sans émettre la requête.

Les liens de pagination `next` qui désignent un autre hôte que celui de la requête initiale sont refusés. Les identifiants insérés dans les chemins d'URL (`idpar`, `idmutation`, `site_id`, codes des indicateurs, etc.) sont contrôlés, car seuls les lettres, les chiffres et les caractères `+ * _ -` sont admis, puis encodés. Une valeur malveillante ne peut donc pas détourner la requête vers une autre ressource.

Ces garanties portent sur le comportement du client. Elles ne couvrent ni la sécurité de l'API distante, ni celle de l'environnement dans lequel le module s'exécute.
