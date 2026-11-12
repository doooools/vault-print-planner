# Batterie de tests : nombre de pièces à imprimer

Date : 2026-11-12, page construite depuis `2c39f57` (branche `claude/ux-redesign-e4f9bf`).

**Méthode**
1. **Oracle indépendant**, figé avant toute comparaison : `expected.json` / `expected.md`.
   - Fait par un agent qui n'avait pas accès au dépôt ni à `_planner/`.
   - Sources : seulement l'arborescence des STL et les 4 manuels PDF (pages rendues et lues).
   - Empreintes dans `expected.sha256`.
2. **Planificateur** utilisé dans la vraie page, comme un utilisateur.
   - Page servie en local, clics sur les vrais contrôles.
   - Le dossier Vault est injecté à la place du sélecteur.
   - Captures dans `planner/*.json` : liste Print, chaque plateau, listes de Design, onglet Matériel.
3. **Plateaux** : `check_plates.py` → `plate_checks.md`.
4. **Comparaison** : `compare.py` → `comparison_raw.md`.
   - Chaque écart a été revérifié dans le manuel ou sur le STL.

Les quantités du planificateur ajoutent volontairement +10 % de rechange (au moins 1) sur les petites pièces : la comparaison se fait sans ces rechanges.

## Tableau

Pièces = nombre de pièces imprimées, sans rechanges. Oracle → planificateur.

| Id | Configuration | Oracle | Planif. | Verdict | Ce qui ne va pas |
|---|---|---|---|---|---|
| C01 | Tiroir S4 1F, toit grille sans poignée | 16 | 16 | ✅ OK | — |
| C02 | Tiroir M4 2F, toit grille + poignée | 21 | 27 | ✅ OK* | 2 guides, 2 coulisses et 2 butées de plus : c'est l'oracle qui se trompe (voir V1) |
| C03 | L5 4F : un 2F + deux 1F | 54 | 60 | ✅ OK* | Même chose (V1). Sur P1S, les 5 pièces trop grandes sont signalées et retirées des plateaux |
| C04 | S4 4F : quatre 1F | 59 | 59 | ✅ OK | — |
| C05 | S3 2F : deux 1F, clé cachée, plaque Gridfinity | 35 | 33 | ❔ À trancher | Cache de clé : planificateur 0, oracle 2 (confiance faible). Aucun manuel ne montre la clé cachée (V2) |
| C06 | Caisson S4 1F + toit grille | 13 | 14 | ❌ KO | Ajoute une étiquette de tiroir `Label.stl` en plus de `Label for Sustainers` (B1) |
| C07 | Caisson M5 2F + toit grille | 13 | 14 | ❌ KO | Ajoute `Label for Sustainers` en plus de `Label.stl` (B1) |
| C08 | Pile S4 : tiroir 1F, tiroir 2F, caisson 1F | 45 | 52 | ❌ KO | 1 étiquette de trop sur le caisson (B1). Les 6 autres viennent de V1 (l'oracle se trompe) |
| C09 | Deux S4 1F côte à côte sous un toit L | 31 | 31 | ✅ OK | Toit L4 posé en diagonale sur P1S. Le format L n'est pas proposé sur P1S (R1) |
| C10 | M4 : base + roues + poignée fixe + poignée tirable, tiroir 2F | 39 | 39 | ✅ OK | Barre de pied cochée par défaut avec les roues, comme dans le manuel |
| C11 | S4 sur base à 4 roulettes, tiroir 1F | 17 | 17 | ✅ OK | Rien d'imprimé pour les roulettes (achetées) |
| C12 | XL3 1F, toit lourd (aussi sur A1 mini) | 23 | 23 | ✅ OK | Seul le toit lourd découpé est proposé (le monobloc ne tient sur aucun plateau). A1 mini et P1S : les 5 grandes pièces sont signalées, comme le prévoit l'oracle |
| C13 | L²4 1F, toit table | 32 | 32 | ⚠️ Compte OK | Design annonce 40 pièces, Print en imprime 36 (B2). Lignes fusionnées nommées « (left) » (B3) |
| C14 | Deux piles : A = C01, B = C07 | 29 | 30 | ❌ KO | Seulement l'étiquette de trop de B (B1). A + B = total, « seulement B » = C07 et « seulement A » = C01 exactement |
| X1 | L5 4F en 1F+1F+2F (ajout) | = C03 | = C03 | ✅ OK | Mêmes pièces que C03 |
| X2 | Deux S4 1F empilés (ajout) | 31 | 31 | ✅ OK | 2 × C01 avec un seul toit |

**Plateaux** : aucun problème dans les 24 captures.
- Pour chaque fichier, le nombre de copies sur les plateaux est égal à la quantité de la liste (rien d'oublié, rien en double).
- Chaque pièce est dans le plateau et hors de la zone interdite du P1S, et aucune pièce n'en chevauche une autre.
- Les pièces trop grandes sont signalées par une alerte rouge dans Print et retirées des plateaux.

## Bugs trouvés (non corrigés)

**B1 — Les caissons reçoivent deux étiquettes.**
- Chaque caisson liste à la fois `Label for Sustainers.stl` et l'étiquette de tiroir `Label.stl`.
- Le manuel 01 p.12 (« Sustainers Naming ») montre une seule étiquette par caisson :
  - `Label for Sustainers` sur la façade 1F ;
  - `Label` sur la façade 2F.
- Code : `src/rules.js` l.276-277.
- Touche C06, C07, C08, C14 : +1 pièce par caisson.

**B2 — Design et Print ne comptent pas les rechanges de la même façon.**
- La liste d'un niveau en Design ajoute la rechange à chaque ligne avant de fusionner. Print fusionne d'abord, puis ajoute la rechange.
- Sur un L² (deux tiroirs dans une coque), Design annonce 40 pièces et Print en imprime 36 :
  - caches de façade, caches de clé et ressorts : 4 au lieu de 3 ;
  - butées : 6 au lieu de 5.
- Sur une pile de 3 niveaux (C08), la somme des listes de niveaux dépasse Print de 4 pièces.
- Ce n'est pas une erreur d'impression, mais les deux listes ne concordent pas.

**B3 — Libellé (cosmétique).** Dans Print, la ligne fusionnée d'un L² s'appelle « Key cap (left) » alors qu'elle compte les deux côtés.

## Vérifications : l'oracle se trompait, ou ce n'est pas tranché

**V1 — Glissières d'un tiroir 2F ou 4F seul : le planificateur a raison** (confirmé par toi : 1 lot par F).
- Le planificateur met 2 guides, 2 coulisses et 2 butées **par niveau de 48 mm**. L'oracle en met 2 par tiroir.
- Mesure sur `S4 Box 2F.stl` : la paroi a un canal de coulisse en T à 13-24 mm **et** à 61-72 mm. Le 1F en a un, le 4F en a quatre.
- Le module 2F a aussi 2 logements de butée par côté.
- Les manuels ne montrent qu'un tiroir 1F.

**V2 — Clé cachée.** Tu as confirmé une seule `Hidden Key Part 2` par pile : le planificateur en met une par tiroir, c'est un bug (voir `RESULTATS2.md`, F2). Le cache de clé reste non tranché.
- Aucune page de manuel ne la montre.
- La manette de `Hidden Key Part 2` mesure 27,7 × 9,8 mm, le logement du cache 27,8 × 9,2 mm.
- Je ne compte pas l'écart comme un bug.

**Accords sur des points incertains** (oracle et planificateur d'accord, à faible confiance) :
- 1 loquet sous un caisson S/M ;
- 2 inserts pour le toit lourd ;
- 1 de chaque accessoire L² ;
- dosseret `M2F Backbone` ajouté par les poignées.

## Remarques (pas des erreurs de quantité)

**R1 — Format L absent sur P1S.** Avec une imprimante 256 × 256, le format L n'est pas proposé, même pour S + S sous un toit L4 dont toutes les pièces tiennent (le toit en diagonale). Pour faire C09 sur P1S, il faut passer par le modèle « Side-by-side S drawers » ou changer d'imprimante.

**R2 — Crémaillères cochées par défaut.** « Geared rails » est coché pour un tiroir seul, alors que le manuel les dit optionnelles (M02 p.4). Les tests les ont décochées.

**R3 — Imprimante changée après coup.** Concevoir en H2S puis passer en P1S fonctionne : les pièces trop grandes sont signalées dans Design et dans Print, et retirées des plateaux.
