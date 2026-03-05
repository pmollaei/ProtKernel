"""
Kernel-weighted structural embedding and correlation screening (PDB ensemble)

This script screens a family of analytic kernels defined on atomic Cartesian
coordinates and identifies the kernel that best correlates a 2D PCA embedding
with a structural deviation metric (RMSD to a reference).

Overview
--------
Given:
  1) An ensemble of PDB structures (e.g., frames saved as single-structure PDBs)
  2) A reference structure (PDB)
we compute, for each structure and each lambda triplet (λx, λy, λz) with
λx + λy + λz = 1:

  kernel(atom) = λx * cos(x / r)^2 + λy * cos(y / r)^2 + λz * sin(z / r)^2
  where r = ||(x,y,z)||.

For each (λx, λy, λz), we build a feature matrix:
  rows   = structures in the ensemble
  cols   = kernel values concatenated over atoms (consistent atom ordering assumed)

We then:
  - Embed features with PCA (2 components)
  - Bin PC1 into N sections
  - Randomly sample a fraction of points per bin (stratified sampling)
  - Compute per-bin mean RMSD and quantify how smoothly RMSD changes along PC1

A simple score is used:
  ratio = (|slope| * R^2) / avg_variance
where slope and R^2 come from a linear fit to (bin_index, mean_RMSD),
and avg_variance is the average within-bin RMSD variance.

Outputs
-------
- Prints the best lambda triplet and summary metrics
- Generates:
  1) PCA scatter (PC1 vs PC2) colored by RMSD
  2) Mean RMSD vs PC1-bin index with linear fit and metrics

Notes / Assumptions
-------------------
- Atom ordering must be consistent across PDB files. If not, you should align
  and/or map atoms explicitly (e.g., by residue+atom name) before vectorizing.
- RMSD is computed with MDTraj; by default, it uses the first (and only) frame
  from each PDB file.

Dependencies
------------
biopython, numpy, mdtraj, scikit-learn, matplotlib

Example
-------
python kernel_pca_screen.py \
  --pdb_glob "directory_for_single_pdb_files/*.pdb" \
  --reference_pdb "Reference_Structure.pdb" \
  --intervals 5 \
  --n_sections 100 \
  --sample_frac 0.2 \
  --seed 42
"""

from __future__ import annotations

import argparse
import glob
import math
import random
from dataclasses import dataclass
from typing import Iterable, List, Sequence, Tuple

import mdtraj as md
import numpy as np
from Bio import PDB
from matplotlib.colors import LinearSegmentedColormap
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt


@dataclass(frozen=True)
class KernelScore:
    """Summary metrics for a candidate (λx, λy, λz) kernel."""
    lambdas: Tuple[float, float, float]
    slope: float
    r2: float
    avg_variance: float
    ratio: float


def vector_norm(x: float, y: float, z: float) -> float:
    """Euclidean norm of a 3D vector."""
    return math.sqrt(x * x + y * y + z * z)


def lambda_grid(intervals: int) -> List[Tuple[float, float, float]]:
    """
    Construct lambda triplets (λx, λy, λz) on a uniform grid in [0,1]
    such that λx + λy + λz = 1.
    """
    if intervals < 2:
        raise ValueError("intervals must be >= 2")

    vals = np.linspace(0.0, 1.0, intervals)
    triplets: List[Tuple[float, float, float]] = []
    for lx in vals:
        for ly in vals:
            lz = 1.0 - (lx + ly)
            # Only keep if lz is exactly on-grid (within tolerance) and within [0,1]
            if -1e-9 <= lz <= 1.0 + 1e-9:
                # Snap to grid if close
                lz_snap = float(vals[np.argmin(np.abs(vals - lz))])
                if abs(lz_snap - lz) < 1e-6:
                    triplets.append((float(lx), float(ly), float(lz_snap)))
    # Remove duplicates (can happen due to snapping)
    triplets = sorted(set(triplets))
    return triplets


def compute_kernel_vector(
    pdb_path: str,
    lambdas: Tuple[float, float, float],
    parser: PDB.PDBParser,
) -> np.ndarray:
    """
    Compute the kernel feature vector for a single PDB structure.

    Returns
    -------
    np.ndarray of shape (n_atoms,)
    """
    structure = parser.get_structure(pdb_path, pdb_path)

    lx, ly, lz = lambdas
    values: List[float] = []

    for model in structure:
        for chain in model:
            for residue in chain:
                for atom in residue:
                    x, y, z = atom.get_coord()
                    r = vector_norm(x, y, z)
                    if r == 0.0:
                        # Avoid division-by-zero; define x/r, y/r, z/r = 0
                        xr = yr = zr = 0.0
                    else:
                        xr, yr, zr = x / r, y / r, z / r

                    k = (
                        lx * (math.cos(xr) ** 2)
                        + ly * (math.cos(yr) ** 2)
                        + lz * (math.sin(zr) ** 2)
                    )
                    values.append(k)

    return np.asarray(values, dtype=np.float64)


def rmsd_to_reference(pdb_path: str, ref_traj: md.Trajectory) -> float:
    """
    Compute RMSD(Å) of a PDB structure to a reference structure using MDTraj.
    """
    traj = md.load(pdb_path)
    # md.rmsd returns array of RMSDs for each frame in traj; here it's typically length 1.
    val = float(md.rmsd(traj, ref_traj)[0])
    return val


def stratified_bin_indices(
    pc1: np.ndarray,
    n_sections: int,
) -> List[List[int]]:
    """
    Bin indices by PC1 into `n_sections` equal-width bins.

    Returns a list of lists: bin_indices[bin_id] = [indices in that bin]
    """
    if n_sections < 1:
        raise ValueError("n_sections must be >= 1")

    pc1_min, pc1_max = float(np.min(pc1)), float(np.max(pc1))
    if pc1_max == pc1_min:
        # All points identical in PC1; place everything in one bin.
        return [list(range(len(pc1)))] + [[] for _ in range(n_sections - 1)]

    edges = np.linspace(pc1_min, pc1_max, n_sections + 1)
    bins: List[List[int]] = [[] for _ in range(n_sections)]
    for i, x in enumerate(pc1):
        # Last edge is exclusive; clamp max to last bin
        b = int(np.searchsorted(edges, x, side="right") - 1)
        b = max(0, min(n_sections - 1, b))
        bins[b].append(i)
    return bins


def evaluate_embedding_trend(
    pc1: np.ndarray,
    labels: np.ndarray,
    n_sections: int,
    sample_frac: float,
    seed: int,
) -> Tuple[np.ndarray, KernelScore]:
    """
    Compute per-bin sampled label means along PC1 and fit a linear trend.

    Returns
    -------
    means : np.ndarray
        Mean label per non-empty bin (after sampling).
    score : KernelScore-like tuple without lambdas filled (lambdas set later).
    """
    rng = random.Random(seed)
    bins = stratified_bin_indices(pc1, n_sections)

    sampled_means: List[float] = []
    within_vars: List[float] = []

    for bin_indices in bins:
        if not bin_indices:
            continue

        k = max(1, int(round(len(bin_indices) * sample_frac)))
        sample = rng.sample(bin_indices, k)

        vals = labels[sample]
        sampled_means.append(float(np.mean(vals)))
        within_vars.append(float(np.var(vals)))

    means = np.asarray(sampled_means, dtype=np.float64)

    # Linear trend over bin order (0..len(means)-1)
    x = np.arange(len(means), dtype=np.float64)

    if len(means) < 2:
        slope = 0.0
        r2 = 0.0
    else:
        coeff = np.polyfit(x, means, 1)
        slope = float(abs(coeff[0]))
        pred = np.polyval(coeff, x)
        sst = float(np.sum((means - np.mean(means)) ** 2))
        sse = float(np.sum((means - pred) ** 2))
        r2 = 0.0 if sst == 0.0 else float(1.0 - sse / sst)

    avg_var = float(np.mean(within_vars)) if within_vars else float("inf")
    ratio = 0.0 if (avg_var == 0.0 or not np.isfinite(avg_var)) else float((slope * r2) / avg_var)

    # lambdas will be set by caller
    dummy = KernelScore(lambdas=(0.0, 0.0, 0.0), slope=slope, r2=r2, avg_variance=avg_var, ratio=ratio)
    return means, dummy


def make_custom_jet() -> LinearSegmentedColormap:
    """Jet-like colormap with a fixed resolution."""
    colors = plt.cm.jet(np.linspace(0, 1.0, 500))
    return LinearSegmentedColormap.from_list("custom_jet", colors, 500)


def plot_pca_scatter(
    pc1: np.ndarray,
    pc2: np.ndarray,
    labels: np.ndarray,
    title: str,
) -> None:
    """PC1 vs PC2 scatter colored by RMSD."""
    fig, ax = plt.subplots(figsize=(5, 3), dpi=600)
    for axis in ["top", "bottom", "left", "right"]:
        ax.spines[axis].set_linewidth(1.5)

    cmap = make_custom_jet()
    sc = ax.scatter(pc1, pc2, s=15, c=labels, cmap=cmap, edgecolor="none")

    cbar = plt.colorbar(sc, pad=0.015)
    cbar.ax.tick_params(labelsize=8)
    cbar.set_label("RMSD (Å)", fontsize=11)

    ax.set_title(title, fontsize=7)
    ax.set_xlabel("PC1", fontsize=12)
    ax.set_ylabel("PC2", fontsize=12)

    plt.tight_layout()
    plt.show()


def plot_trend(
    means: np.ndarray,
    score: KernelScore,
    title: str,
) -> None:
    """Plot mean RMSD per bin and a linear fit with metrics."""
    x = np.arange(len(means), dtype=np.float64)
    fig, ax = plt.subplots(figsize=(5, 3), dpi=600)
    for axis in ["top", "bottom", "left", "right"]:
        ax.spines[axis].set_linewidth(1.5)

    ax.scatter(x, means, s=18)
    if len(means) >= 2:
        coeff = np.polyfit(x, means, 1)
        ax.plot(x, np.polyval(coeff, x))

    ax.set_title(title, fontsize=7)
    ax.set_xlabel("PC1 bin index", fontsize=12)
    ax.set_ylabel("Mean RMSD (Å)", fontsize=12)

    txt = f"slope={score.slope:.5f}\nR²={score.r2:.5f}\navg var={score.avg_variance:.5f}\nratio={score.ratio:.5f}"
    ax.text(0.02, 0.98, txt, transform=ax.transAxes, va="top", ha="left", fontsize=8)

    plt.tight_layout()
    plt.show()


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--pdb_glob", required=True, help="Glob for ensemble PDBs (single-structure PDB files).")
    ap.add_argument("--reference_pdb", required=True, help="Reference structure PDB path.")
    ap.add_argument("--intervals", type=int, default=5, help="Grid intervals for lambdas in [0,1].")
    ap.add_argument("--n_sections", type=int, default=100, help="Number of PC1 bins.")
    ap.add_argument("--sample_frac", type=float, default=0.2, help="Fraction sampled per PC1 bin.")
    ap.add_argument("--seed", type=int, default=42, help="Random seed for stratified sampling.")
    ap.add_argument("--scale_labels", type=float, default=1.0, help="Optional multiplicative scale for RMSD labels.")
    args = ap.parse_args()

    pdb_files = sorted(glob.glob(args.pdb_glob))
    if not pdb_files:
        raise FileNotFoundError(f"No files matched: {args.pdb_glob}")

    ref = md.load(args.reference_pdb)

    parser = PDB.PDBParser(QUIET=True)
    lambdas_list = lambda_grid(args.intervals)
    print(f"Found {len(pdb_files)} PDBs")
    print(f"Lambda grid size: {len(lambdas_list)} (intervals={args.intervals})")

    # Precompute RMSD labels once (independent of lambda)
    labels = np.array([rmsd_to_reference(p, ref) for p in pdb_files], dtype=np.float64) * float(args.scale_labels)

    best_score: KernelScore | None = None
    best_pca: np.ndarray | None = None

    pca = PCA(n_components=2)

    for lambdas in lambdas_list:
        # Build feature matrix: (n_structures, n_atoms)
        feat_rows: List[np.ndarray] = []
        for p in pdb_files:
            feat_rows.append(compute_kernel_vector(p, lambdas, parser))

        # Ensure consistent dimensionality
        n_atoms = {row.shape[0] for row in feat_rows}
        if len(n_atoms) != 1:
            raise ValueError(
                "Inconsistent atom counts across PDBs. "
                "Ensure all PDBs share identical atom ordering and content."
            )

        features = np.vstack(feat_rows)  # shape (N, n_atoms)
        emb = pca.fit_transform(features)  # shape (N, 2)
        pc1, pc2 = emb[:, 0], emb[:, 1]

        means, tmp = evaluate_embedding_trend(
            pc1=pc1,
            labels=labels,
            n_sections=args.n_sections,
            sample_frac=args.sample_frac,
            seed=args.seed,
        )

        score = KernelScore(
            lambdas=lambdas,
            slope=tmp.slope,
            r2=tmp.r2,
            avg_variance=tmp.avg_variance,
            ratio=tmp.ratio,
        )

        if best_score is None or score.ratio > best_score.ratio:
            best_score = score
            best_pca = emb

    assert best_score is not None and best_pca is not None

    lx, ly, lz = best_score.lambdas
    title = f"Kernel: {lx:.2f}·cos(x/r)^2 + {ly:.2f}·cos(y/r)^2 + {lz:.2f}·sin(z/r)^2"

    print("\nBest kernel:")
    print(f"  lambdas = {best_score.lambdas}")
    print(f"  slope   = {best_score.slope:.5f}")
    print(f"  R^2     = {best_score.r2:.5f}")
    print(f"  avg var = {best_score.avg_variance:.5f}")
    print(f"  ratio   = {best_score.ratio:.5f}")

    # Recompute bin means for best kernel (for plotting trend)
    pc1 = best_pca[:, 0]
    pc2 = best_pca[:, 1]
    means, _tmp = evaluate_embedding_trend(
        pc1=pc1,
        labels=labels,
        n_sections=args.n_sections,
        sample_frac=args.sample_frac,
        seed=args.seed,
    )

    plot_pca_scatter(pc1, pc2, labels, title=title)
    plot_trend(means, best_score, title=title)


if __name__ == "__main__":
    main()