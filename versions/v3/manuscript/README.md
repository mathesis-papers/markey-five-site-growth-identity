# Markey's growth identity and Shannon's region formulas

Creators: Haobo Ma (ChronoAI Pte Ltd, Singapore), followed by Wenlin Zhang
(National University of Singapore; ChronoAI Pte Ltd, Singapore).

License: Creative Commons Attribution 4.0 International (CC BY 4.0),
https://creativecommons.org/licenses/by/4.0/.

## Statements

The note proves Markey's identity A400701(n) = A374338(n) + 4n + 7 for
every integer n >= 2, using the exact occupied shapes for two through five
consecutive triangular-lattice seeds. It also proves the recorded formulas
and generating functions for A400699 and A400700.

Counting circle--vertex incidences gives Shannon's three A374337 region
formulas and the A374339 edge formula, with their exceptional first value.
The generating function for newly drawn circles belongs to Shannon's
construction, not A264788: their stage-three values are 6 and 4 respectively.
The A265676 relation is an identity for the coefficients of Barker's recorded
rational series; the geometric interpretation of that series is separate.

## Build

Use Tectonic 0.17.0:

```sh
tectonic note.tex
```

For byte-identical PDF timestamps and identifiers, use the fixed source epoch:

```sh
SOURCE_DATE_EPOCH=1794808755 tectonic note.tex
```

Alternatively, use TeX Live:

```sh
pdflatex -interaction=nonstopmode -halt-on-error note.tex
pdflatex -interaction=nonstopmode -halt-on-error note.tex
```

The bibliography is included in `note.tex`; no BibTeX pass is required.
There are no external figures or generated LaTeX inputs.

## Exact finite comparisons

Python 3.9 or later, standard library only:

```sh
python3 verify.py --output verification.json
```

The deterministic output compares simultaneous lattice evolution, exact
shapes and formulas through iteration 60 for four seed sizes; circle--vertex
incidences and region formulas for iterations 1 through 60; newly drawn
circle coefficients through 60; and the petal-series relation for 2 through
60. Boundary-law comparisons use 3 <= A <= 10, 2 <= L-A <= 10, and integer
coordinates in [-3,L+3]. These finite comparisons supplement the written
all-iteration arguments. `source-comparisons.json` gives the ranges of
displayed primary-source terms matching the formulas.

## Lean declaration scope

At revision `2f8421f6b90d37b4815b887f6c60987553831b20`:

- `MarkeyA400701.result` in
  https://github.com/the-omega-institute/trureturing/blob/2f8421f6b90d37b4815b887f6c60987553831b20/D5/S3/StatisticalMechanics/Percolation/MarkeyFiveSiteGrowthDifference.lean
  states the five-site difference for every n > 1 and every pair of distinct
  Euclidean starting points. Its lattice count uses an induced finite window
  with a spare boundary layer, without periodic edges.
- `ShannonA374338.result` in
  https://github.com/the-omega-institute/trureturing/blob/2f8421f6b90d37b4815b887f6c60987553831b20/D5/S3/Geometry/ShannonFixedRadiusCircleVertices.lean
  states the three vertex formulas for every pair of distinct starting points.
- `AxialGrowth.exact_shape` in
  https://github.com/the-omega-institute/trureturing/blob/2f8421f6b90d37b4815b887f6c60987553831b20/D5/S3/StatisticalMechanics/Percolation/TriangularTwoNeighborGrowth.lean
  states the exact shapes for seed sizes 2 and 5 and iterations n >= 2.

The three- and four-site extensions, region and edge counts, added-circle
formula and power-series identities have written proofs in the note. They
are not conclusions of those three declarations.

## Source package

- `note.tex`: main source, references and license.
- `metadata.json`: stable identity, revision, creators, coverage and license.
- `verify.py`: exact finite comparisons.
- `verification.json`: deterministic expected output.
- `source-comparisons.json`: primary-source term ranges.
- `SHA256SUMS`: hashes of the other source-package files.
