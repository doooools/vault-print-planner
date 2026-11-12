# Batterie 2 : 28 configurations sur H2S, sans les 10 %

Date : 2026-11-12. Même méthode que `RESULTATS.md` :
- oracle indépendant figé avant la comparaison : `expected2.json` / `expected2.md`, empreintes dans `expected.sha256` ;
- configurations montées en cliquant dans la vraie page : `planner/D*.json` ;
- comparaison brute : `comparison2_raw.md` ;
- imprimante Bambu H2S (340 × 320 × 340), donc aucune pièce n'est limitée par le plateau ;
- les +10 % de rechange du planificateur sont retirés avant de comparer.

Règles que tu as confirmées, appliquées à l'oracle :
- 1 lot de 2 guides + 2 coulisses + 2 butées par F du module ;
- la clé cachée amovible (`Hidden Key Part 2`) : une seule par pile.

## Tableau

Pièces imprimées, oracle → planificateur.

| Id | Configuration | Oracle | Planif. | Verdict | Écart |
|---|---|---|---|---|---|
| D01 | Tiroir S3 2F | 24 | 24 | ✅ | — |
| D02 | Tiroir S5 4F, toit table | 36 | 36 | ✅ | — |
| D03 | Tiroir M3 1F, toit bol | 18 | 18 | ✅ | — |
| D04 | M6 2F : deux 1F, clé cachée, poignée de toit | 36 | 36 | ❌ | 2 `Hidden Key Part 2` au lieu d'1 (F2). Cache de clé : voir Q1 |
| D05 | M7 4F : deux 2F, toit sous-table | 51 | 51 | ✅ | — |
| D06 | L3 1F, toit lourd | 22 | 22 | ✅ | — |
| D07 | L6 2F : deux 1F | 36 | 36 | ✅ | — |
| D08 | L7 4F : 1F+2F+1F, plaque Gridfinity | 63 | 63 | ✅ | — |
| D09 | XL5 1F, toit table | 20 | 20 | ✅ | — |
| D10 | XL6 1F (caisson de tiroir en 2 parties) | 20 | 20 | ✅ | — |
| D11 | XL²4 1F (tiroirs S + M dans une coque) | 32 | 32 | ✅ | — |
| D12 | L²5 2F, toit bol | 48 | 48 | ✅ | — |
| D13 | Caisson L4 1F | 18 | 19 | ❌ | Étiquette en double (F1) |
| D14 | Caisson L5 2F, parois à rainures, toit table | 18 | 19 | ❌ | Étiquette en double (F1) |
| D15 | Caisson XL3 1F étanche | 19 | 19 | ❌ | Étiquette en double (F1). Façade : le planificateur a raison (`XL1F Facade.stl` existe, l'oracle l'avait raté) |
| D16 | Caisson M6 2F | 13 | 14 | ❌ | Étiquette en double (F1) |
| D17 | Caisson S4 4F | 13 | 14 | ❌ | Étiquette en double (F1) |
| D18 | S4 2F + M4 2F côte à côte, toit XL4 | 49 | 49 | ✅ | — |
| D19 | Pile L5 : 2F, 1F, caisson 1F, base + roues + pied + poignée tirable, toit table | 81 | 83 | ❌ | Étiquette en double (F1). Dosserets : voir Q2 |
| D20 | Pile XL3 : base sur roulettes, deux XL3 1F | 40 | 40 | ✅ | — |
| D21 | Deux piles M4 de trois 1F à clé cachée | 102 | 104 | ❌ | 6 `Hidden Key Part 2` au lieu de 2 (F2). Cache de clé : Q1 |
| D22 | S4 1F, séparateurs grille 2 + 1 | 31 | 31 | ✅ | — |
| D23 | S4 2F, plaque Gridfinity à 2 poignées | 25 | 25 | ✅ | — |
| D24 | M5 1F + fixation murale | 20 | 21 | ❌ | 2 pièces murales (« second part ») pour une plaque 1F qui n'a qu'une ouverture (F5) |
| D25 | S3 1F + support IKEA Skådis | 18 | 17 | ❌ | Pas de dosseret, alors que le support se visse dessus (M04 p.15) (F4) |
| D26 | Caisson S3 2F + plaque + 3 séparateurs | 17 | 18 | ❌ | Étiquette en double (F1) |
| D27 | Pile S6 : base + poignée fixe, 2F + 1F | 42 | 43 | ❔ | Dosserets : voir Q2 |
| D28 | Caisson L6 1F | 18 | 19 | ❌ | Étiquette en double (F1) |

Plateaux : aucun problème dans les 52 captures (batteries 1 et 2). Pour chaque fichier, les copies sur les plateaux égalent la quantité de la liste ; tout est dans le plateau, rien ne se chevauche.

## Vérifié dans le manuel

- **Étiquettes des caissons** (M01 p.12) : une seule étiquette par caisson. `Label for Sustainers` sur un 1F, `Label` de tiroir sur un 2F.
- **Pièces murales** (M05) : une « second part » par ouverture trapézoïdale de la plaque. Le 2F en montre 2, la 1F n'a qu'une ouverture.
- **Support pour panneau perforé** (M04 p.15, étape 20) : « attach IKEA or USSA pegboards on backbones », donc un dosseret est nécessaire.
- **Dosserets** (M04 p.7-11) : le dosseret 2F relie la base au premier module ; les suivants relient les modules entre eux, en chevauchant la jonction ; on peut aussi en utiliser des 1F. Le manuel ne donne pas de nombre par module.

## Après correctifs (F1-F5 et cache de clé)

Les 44 configurations des deux batteries ont été rejouées dans la page reconstruite. Les captures d'avant les correctifs sont dans `before_fix/`.

**Batterie 1** — comparée à `expected_corrected.json`, l'oracle figé auquel j'ai appliqué tes deux règles (détail dans `corrections.md`).
- Tout correspond.
- C12 reste à part : le toit lourd découpé y remplace le monobloc, que l'oracle donne lui-même comme alternative.

**Batterie 2** — tout correspond, sauf :
- **D15** : l'oracle se trompait (il n'avait pas vu `XL1F Facade.stl`).
- **D19 et D27** : nombre de dosserets, question Q2 encore ouverte.

**Autres vérifications**
- Design et Print annoncent maintenant le même total pour une coque L² (C13 : 36 et 36).
- Les plateaux sont toujours sans problème (44 captures).
- `node src/validate.js` est propre. Il vérifie aussi les nouvelles règles :
  - une étiquette par caisson ;
  - pas de clé amovible dans un module ;
  - une pièce murale par ouverture ;
  - un dosseret sous chaque support de panneau perforé ;
  - une seule ligne par fichier dans une unité.

| Correctif | Ce qui change | Fichier |
|---|---|---|
| F1 | Une étiquette par caisson : `Label for Sustainers` en 1F, `Label` en 2F/4F | `src/rules.js` |
| F2 | `Hidden Key Part 2` et un `Key Cap` : une fois par pile qui a une serrure cachée. En 3D, la clé n'apparaît plus que dans le module à serrure cachée le plus haut (dans chacun de ses tiroirs). Le cache n'est pas dessiné | `src/rules.js` (`buildHiddenKey`), `src/template.html` |
| F3 | Une ligne par fichier dans une unité : les deux côtés d'un L²/XL² sont fusionnés et perdent l'étiquette « (left) ». Design et Print ajoutent les rechanges sur le même total | `src/rules.js` (`mergeSame`) |
| F4 | Un support de panneau perforé ajoute le dosseret du module si aucun n'est choisi | `src/rules.js`, `src/template.html` |
| F5 | Pièces murales : 1 par plaque 1F/2F, 2 par plaque 4F, ×2 en L et XL (ouvertures comptées sur les plaques) | `src/rules.js` |

## Dosserets : on suit le manuel (Q2)

Le manuel (M04 p.7-15) montre une **colonne** de dosserets au dos de la pile :
- le 1er dosseret, un 2F, relie la base au premier module ;
- les suivants relient les modules entre eux, à cheval sur les jonctions (des 1F sont permis) ;
- la colonne s'arrête sous le module du haut : c'est là que va le verrou de la poignée tirable ;
- les panneaux perforés et la poignée fixe se vissent dessus.

Le planificateur le fait maintenant (`buildBackbones` dans `src/rules.js`) :
- des dosserets 2F sur la hauteur de la base (comptée 1F) et des modules sous celui du haut, plus un 1F si c'est impair, et au moins un 2F au départ de la base ;
- en XL, il n'existe que `XL1F Backbone.stl`, donc la colonne est faite de 1F ;
- un panneau perforé, ou un dosseret choisi dans l'éditeur, prolonge la colonne jusqu'à son niveau.

Avant, il y avait un dosseret par module 1F/2F, et une alerte pour les 4F ; c'est retiré. Les piles déjà enregistrées avec une poignée perdent les dosserets que l'ancienne règle avait cochés d'office ; un fichier de design version 1 aussi.

| Id | Avant | Maintenant |
|---|---|---|
| C10 (base + M4 2F) | M2F | M2F |
| D19 (base + L5 2F + 1F + caisson 1F en haut) | L2F + 2 × L1F | 2 × L2F (comme l'oracle) |
| D25 (S3 1F + Skådis, sans base) | S1F | S1F |
| D27 (base + S6 2F + 1F en haut) | S2F + S1F | S2F + S1F (l'oracle disait 1 × S2F, à faible confiance) |

Après ce changement, les deux batteries correspondent partout, sauf C12 (toit lourd découpé, l'alternative donnée par l'oracle) et D15 (erreur de l'oracle). Les plateaux sont sans problème et `validate.js` est propre (il vérifie aussi la colonne).
