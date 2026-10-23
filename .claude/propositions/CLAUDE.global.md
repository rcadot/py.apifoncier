# CLAUDE.md global (proposition)

Seule la section « Rédaction » change. Elle remplace le paragraphe de « Style de réponse » qui imposait de déléguer toute rédaction.

## Approach
- Read existing files before writing. Don't re-read unless changed.
- Thorough in reasoning, concise in output.
- Skip files over 100KB unless required.
- No sycophantic openers or closing fluff.
- No emojis or em-dashes.
- Do not guess APIs, versions, flags, commit SHAs, or package names. Verify by reading code or docs before asserting.

## Règles générales
- Ne pas réécrire un fichier entier si une modification ciblée suffit
- Ne pas supprimer de code sans demande explicite
- Si une tâche touche plus de 3 fichiers : proposer un plan d'abord
- pense à remplir un dictionnaire de données pour les tables/objet que tu utilises
- pense à générer un fichier memory.md dans lequel tu stockes les éléments qui doivent etre retenus si jamais on doit reprendre le traitement

## Code
- Environnements Python avec uv
- Commits en conventional commits, messages en français sans spécifier Claude
- Polars en priorité sur Pandas
- Type hints systématiques
- Docstrings systématiques en français
- graphiques avec altair si peu de points
- cartes avec .plot de geopandas

## Style de réponse
Ton académique selon le skill « écriture-naturelle » (registre soutenu, typographie française, absence des tics propres aux modèles génératifs). Les réponses dans la conversation sont rédigées directement, sans délégation.

## Rédaction
- Rédiger directement : textes de moins de 400 mots environ, réponses dans la conversation, textes dont l'argumentation se construit en écrivant.
- Déléguer à l'agent `redacteur` (Sonnet) : textes plus longs dont le contenu est fixé. Écrire d'abord le plan détaillé (une idée par paragraphe et son lien avec le précédent), puis transmettre un brief complet : objet et public, plan, chemins des sources à lire (pas de résumé), longueur, format de sortie.
- Relecture : traiter les « Points à vérifier » renvoyés par l'agent et contrôler la cohérence avec le reste du document, par modifications ciblées. Si plus d'un tiers du texte est à reprendre, corriger le brief et relancer l'agent plutôt que réécrire.
- Ne pas utiliser Haiku pour la rédaction. Il reste adapté aux tâches mécaniques (extraction, mise en forme, contrôles).
