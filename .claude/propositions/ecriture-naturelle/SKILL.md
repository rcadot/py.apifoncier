---
name: ecriture-naturelle
description: "Skill pour relire ou écrire un texte académique en français, sans tics de rédaction typiques des modèles génératifs"
tags: [relecture, redaction, style, francais, academique]
---

## Objectif

Produire ou relire un texte académique en français qui respecte les codes du genre (rigueur, argumentation construite, registre soutenu), sans les tics propres aux modèles génératifs : chiasmes, symétries artificielles, ternaire systématique, vocabulaire lissé.

## Registre académique

- Vocabulaire précis et disciplinaire. Pas de vulgarisation, pas de familiarité.
- Troisième personne ou « on » plutôt que « je », sauf si le genre du texte l'exige explicitement (mémoire, thèse en première personne assumée).
- Syntaxe construite, avec subordination claire. Pas de style haché façon liste de constats juxtaposés.
- Connecteurs logiques marqués et variés : cependant, néanmoins, dès lors, en effet, par conséquent, en revanche, de fait. Un seul connecteur par transition, jamais d'empilement.
- Structure argumentative explicite : problématique posée, développement organisé en parties qui s'enchaînent, conclusion qui répond à la problématique sans la reformuler mot pour mot.
- Références et citations sourcées quand le texte s'appuie sur des travaux existants. Jamais d'attribution inventée.
- Pas d'anecdote personnelle, pas d'apostrophe au lecteur (« vous verrez que »), pas d'exclamation.

## Ponctuation et typographie

- Pas de tirets cadratin : les remplacer par des virgules, des parenthèses ou une nouvelle phrase.
- Pas de point-virgule : couper la phrase ou utiliser une virgule.
- Guillemets français « » pour les citations et les mises en relief.
- Apostrophe droite (') et non l'apostrophe typographique (’).
- Espace insécable avant « : », « ? », « ! » et « % », et à l'intérieur des guillemets « ».
- Nombres avec espace comme séparateur de milliers et virgule décimale, par exemple 9,2 % ou 12 500.

## À éviter systématiquement (tics de LLM)

- Chiasmes et formules à symétrie artificielle (« ce n'est pas X qui compte, c'est Y » et toutes ses variantes).
- Ternaire réflexe : ne pas grouper systématiquement exemples, arguments ou qualificatifs par trois.
- Tournure « pas ceci, plutôt cela » sous toutes ses formes.
- Superlatifs et qualificatifs non étayés par un fait ou une référence.
- Vocabulaire lissé et répétitif que les modèles reproduisent par défaut : robuste, transparent, fluide, incontournable, clé de voûte, employés sans justification précise.
- Transitions creuses : « il est important de noter que », « il convient de », « en conclusion », « dans le monde d'aujourd'hui ».
- Emoji, gras, titres formulés sous forme de question.

### Exemples de réécriture

- Chiasme : « Ce n'est pas la surface qui compte, c'est son usage. » devient « L'usage du sol renseigne davantage que sa surface sur la pression foncière. »
- Ternaire réflexe : « une méthode simple, robuste et reproductible » devient « une méthode reproductible, puisque chaque étape repose sur des données publiques ».
- Transition creuse : « Il est important de noter que les prix ont augmenté. » devient « Les prix ont pourtant augmenté. »
- Qualificatif non étayé : « une hausse considérable » devient « une hausse de 18 % entre 2015 et 2022 ».

## Mise en forme

- Paragraphes rédigés. Pas de listes à puces sauf énumération qui le justifie réellement (critères, étapes d'une méthode).
- Références en note de bas de page ou entre parenthèses selon la convention demandée. Pas de lien hypertexte brut dans le corps du texte.
- Varier la longueur des phrases pour éviter un rythme mécanique, sans pour autant hacher le propos en propositions trop courtes : la syntaxe académique porte des idées complexes, elle peut se permettre des phrases longues bien construites.

## Mode relecture

Quand on donne un texte à relire, procéder ainsi :

- Corriger d'abord la typographie et la ponctuation listées plus haut.
- Repérer et réécrire les chiasmes, les symétries artificielles, les ternaires réflexes et les tournures « pas ceci, plutôt cela ».
- Vérifier le registre : retirer familiarités, anecdotes, apostrophes au lecteur, superlatifs sans appui.
- Vérifier la tenue de l'argumentation : la conclusion répond-elle à la problématique, les parties s'enchaînent-elles avec des connecteurs justifiés plutôt que juxtaposées ?
- Rendre le texte final directement, sans commentaire, sauf demande explicite d'explication des corrections.

## Mode rédaction académique

Quand on demande d'écrire un texte académique, respecter toutes les règles ci-dessus dès le premier jet. Construire d'abord un plan implicite (problématique, axes de développement, conclusion) avant de rédiger, même si ce plan n'apparaît pas explicitement dans le texte rendu. Si un plan est fourni, le suivre tel quel. Rendre uniquement le texte demandé, sans préambule ni méta-commentaire sur la méthode suivie, sauf si l'appelant demande un retour (l'agent `redacteur` ajoute ainsi une section « Points à vérifier »).

Ne jamais inventer un chiffre, une référence ou une attribution : si l'information manque, le signaler.

## Vérification automatique

Sur un texte enregistré dans un fichier, cette commande repère les écarts mécaniques. Chaque occurrence est à examiner, certaines peuvent être légitimes (citation, URL, code).

```bash
LC_ALL=C.UTF-8 grep -nP '—|–|;|’|"|\b([Ii]l est important de noter|[Ii]l convient de|[Ee]n conclusion|dans le monde d.aujourd.hui|robuste|transparent|fluide|incontournable|clé de voûte)\b| [:?!%]|[^\s\x{00A0}\x{202F}][:?!](\s|$)' FICHIER.md
```

## Auto-vérification avant de rendre le texte

- Chaque paragraphe défend une seule idée, reliée à la précédente par un connecteur justifié.
- Aucune énumération par trois sans nécessité, aucun chiasme, aucune tournure « pas ceci, plutôt cela ».
- Chaque chiffre et chaque référence proviennent des sources fournies.
- La conclusion répond à la problématique.
