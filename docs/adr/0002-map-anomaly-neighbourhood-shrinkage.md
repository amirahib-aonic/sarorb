# Map Anomaly uses a neighbourhood baseline shrunk toward Borneo

The Anomaly for a whole Area of Interest compares its Harmonized Hotspot Count with the median of the same calendar month in the other years. Per grid cell on the map that fails: at 0.1° only 7% of cells have a non-zero median (under 1% from November to June), so any fire becomes "new fire" and 83% of burning cells were flagged. Harmonization (ADR 0001) cannot fix this, because the problem is a missing history, not a sensor difference.

On the map, each 0.1° cell is instead judged on the 5×5 block of cells around it (about 55 km), and its ratio is shrunk toward the Borneo-wide rate:

```
ratio = (x + μ̄) / (m + μ̄)
```

where x is the block's Harmonized Hotspot Count this month, m is the block's mean for the same calendar month in the other years, and μ̄ is the mean of m over every block in Borneo for that month. A block with little history is pulled toward ×1 instead of toward infinity. The tooltip also says how often the cell itself has burned in that calendar month ("fire here in 9 of 23 Augusts"). This flags about 11% of burning cells, and dropping one more baseline year flips under 3% of flags ([cell-anomaly-analysis.md](../research/cell-anomaly-analysis.md)).

## Considered Options

- **Plain ratio to the cell median**: 83% flagged; a zero median carries no information.
- **Regrid the map to 0.5° cells** with the same shrunk ratio: 12% flagged and simpler to explain, but the map turns blocky and loses where fire is inside each 55 km square.
- **Burn-frequency mask** (only cells that burned in at least a quarter or half of past years): keeps only 19% or 7% of cells at 0.1°.
- **Percentile rank or z-score on log counts**: 43% and 26% flagged, and harder to read than "× normal".
