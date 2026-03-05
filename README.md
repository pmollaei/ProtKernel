# Pytone code:
Kernel_analysis.py

Input: Folder of single-structure PDBs + reference PDB.
<br /> Output: Best (λx, λy, λz) and plots (PC1/PC2 colored by RMSD + RMSD trend along PC1 bins).
<br /> Reproducibility: Controlled by seed.

---

# Protein Dataset Preparation:

This repository contains the datasets and preprocessing steps required to reproduce the results reported in the paper:
“Efficient Reaction Coordinate Identification for Proteins Using Representation Learning.”

The complete preprocessing workflow is described step-by-step for the Chignolin protein.
For the remaining proteins, only the corresponding filenames for each step are provided.
The same preprocessing procedure used for Chignolin should be applied to these proteins.

** Chignolin Dataset Preparation **

Step 1 — Obtain the Protein Structure
<br /> Download the protein structure used for molecular dynamics simulations.
Files:
Chignolin.pdb
Chignolin.psf

Step 2 — Clean the Protein Sequence
<br /> Retain only the standard residues and remove all additional elements added to the sequence.
Output file:
Chignolin_resid2to9.pdb

Step 3 — Clean Simulation Trajectories
<br /> Load the simulation trajectories into VMD and retain only the cleaned sequence defined in Step 2.
Output file:
Chignolin_resid2to9_samples8and9_10000f.dcd

Step 4 — Generate the Reference Protein Structure
<br /> Create a reference structure ensuring that residue indices match those used in the simulation trajectories.
Important considerations:
<br /> If residues are removed at the beginning of the sequence (e.g., starting at residue 2), the reference structure must use the same indexing.
You may either:
keep the same starting residues as in Chignolin.pdb, or
temporarily add random residues and remove them later.
<br /> During generation in VMD, extra atoms may appear and should be removed.
<br /> Intermediate files:
Generated_Chignolin_VMD.pdb
Generated_Chignolin_RemovedExtra.pdb
<br /> To ensure consistent atom ordering, load both the reference protein and trajectory structures into PyMOL, then resave them.
<br /> Final ordered structures:
Generated_Chignolin_ExtraRemoved_OrderedAtoms.pdb
Chignolin_resid2to9_samples8and9_10000f_OrderedAtoms.pdb
<br /> If the cleaned trajectories start from residue index ≥2, remove the corresponding extra residues from the generated reference structure.

Step 5 — Position the Reference Structure
<br /> Load the structure into VMD and place the protein in a consistent coordinate frame.
<br /> First, display the origin:
<br /> -draw color red
<br /> -draw sphere { 0 0 0 } resolution 16 radius 1.0

Move the geometric center of the protein to the origin:
<br /> -set sel [atomselect top all]
<br /> -set gec [measure center $sel]
<br /> -$gec moveto {0 0 0}
<br /> -$sel moveby [vecscale -1.0 $gec]

Step 6 — Align Principal Axes
<br /> Align the principal axes of the protein with the Cartesian coordinate system.
<br /> -lappend auto_path /directory/la1.0
<br /> -lappend auto_path /directory/orient
<br /> -package require Orient
<br /> -namespace import Orient::orient
<br /> -set sel [atomselect top "all"]
<br /> =set I [draw principalaxes $sel]
<br /> -set A [orient $sel [lindex $I 2] {0 0 1}]
<br /> -$sel move $A
<br /> -set I [draw principalaxes $sel]
<br /> -set A [orient $sel [lindex $I 1] {0 1 0}]
<br /> -$sel move $A
<br /> -set I [draw principalaxes $sel]

Save the final reference structure:
Chignolin_reference.pdb

<br /> This structure is used as the **reference** for RMSD calculations in Kernel_analysis.py.

Step 7 — Align Simulation Trajectories
<br /> Align the backbone atoms of the simulation trajectories to the reference structure using VMD.
Output:
<br /> Chignoline_#15_aligned_to_reference.pdb

Step 8 — Generate Individual Structures
You may either:
<br /> use the full trajectory directly, or
<br /> split the trajectory into individual .pdb files using:
single_pdb.py

Step 9 — Kernel Analysis
<br /> Compute kernel values across structures and identify the optimal kernel parameters.
<br /> Script: Kernel_analysis.py
<br /> **This script evaluates kernel values for different λ combinations, performs PCA analysis, identifies the optimal kernel parameters, and visualizes the resulting reaction coordinate.**

<br />  **Other Protein Systems**

<br /> For the following proteins, the same preprocessing pipeline applies.
<br /> Only the filenames corresponding to each step are provided.


**Fs Peptide**

Step 1: Fspeptide.pdb

Step 2: Fs_resid2to22.pdb

Step 3: Fs_Trajectories_resid2to22.dcd

Step 4:
<br /> Generated_Fs_VMD.pdb
<br /> Generated_Fs_ExtraRemoved.pdb
<br /> Generated_Fs_ExtraRemoved_OrderedAtoms.pdb
<br /> Fs_Trajectories_resid2to22_OrderedAtoms.pdb.zip

Step 5: Fs_reference.pdb

Step 6: Fs_Trajectories_aligned_to_reference.pdb


**Protein B**

Step 1:
<br /> proteinb.pdb
<br /> proteinb.psf

Step 2: proteinb_resid1to45.pdb

Step 3: Proteinb_trajectories_resid1to44.dcd

Step 4:
<br /> Generated_Proteinb_VMD.pdb
<br /> Generated_Proteinb_OrderedAtoms.pdb
<br /> Proteinb_Simulation_resid1to44_OrderedAtoms.pdb.zip

Step 5: Proteinb_reference.pdb

Step 6: Proteinb_aligned_to_reference.pdb


**Trp-Cage**

Step 1:
<br /> Trp_cage.psf
<br /> Trp_cage.pdb

Step 2: Trp_cage_resid3to20.pdb

Step 3: Trp_cage_Trajectories_resid3to20.dcd

Step 4:
<br /> Generated_Trp_cage_VMD.pdb
<br /> Generated_Trp_cage_RemovedExtra.pdb
<br /> Generated_Trp_cage_ExtraRemoved_OrderedAtoms.pdb
<br /> Trp_cage_Trajectories_resid3to20_OrderedAtoms.pdb.zip

Step 5: Trp_cage_reference.pdb

Step 6: Trp_cage_aligned_to_reference.pdb


**NTL9**

Step 1: NTL9.pdb

Step 2:
<br /> NTL9_resid2to38.pdb
<br /> NTL9_Trajectories_resid2to38.dcd

Step 3:
<br /> Generated_NTL9_VMD.pdb
<br /> Generated_NTL9_resid2to38.pdb

Step 4:
<br /> Generated_NTL9_resid2to38_OrderedAtoms.pdb
<br /> NTL9_Trajectories_resid2to38_OrderedAtoms.pdb.zip

Step 5:
<br /> NTL9_reference.pdb

Step 6:
<br /> NTL9_Trajectories_aligned_to_reference.pdb

---
