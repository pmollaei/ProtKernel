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

proteinb.pdb
proteinb.psf

Step 2

proteinb_resid1to45.pdb

Step 3

Proteinb_trajectories_resid1to44.dcd

Step 4

Generated_Proteinb_VMD.pdb
Generated_Proteinb_OrderedAtoms.pdb
Proteinb_Simulation_resid1to44_OrderedAtoms.pdb.zip

Step 5

Proteinb_reference.pdb

Step 6

Proteinb_aligned_to_reference.pdb
Trp-Cage

Step 1

Trp_cage.psf
Trp_cage.pdb

Step 2

Trp_cage_resid3to20.pdb

Step 3

Trp_cage_Trajectories_resid3to20.dcd

Step 4

Generated_Trp_cage_VMD.pdb
Generated_Trp_cage_RemovedExtra.pdb
Generated_Trp_cage_ExtraRemoved_OrderedAtoms.pdb
Trp_cage_Trajectories_resid3to20_OrderedAtoms.pdb.zip

Step 5

Trp_cage_reference.pdb

Step 6

Trp_cage_aligned_to_reference.pdb
Homeodomain

Step 1

Homeodomain.psf
Homeodomain.pdb

Step 2

Homeodomain_resid3to54.pdb
Homeodomain_Trajectories_resid3to54.dcd

Step 3

Generated_Homeodomain_VMD.pdb
Generated_Homeodomain_resid3to54.pdb

Step 4

Generated_Homeodomain_resid3to54_OrderedAtoms.pdb
Homeodomain_Trajectories_resid3to54_OrderedAtoms.pdb.zip

Step 5

Homeodomain_reference.pdb

Step 6

Homeodomain_Trajectories_aligned_to_reference.pdb
NTL9

Step 1

NTL9.pdb

Step 2

NTL9_resid2to38.pdb
NTL9_Trajectories_resid2to38.dcd

Step 3

Generated_NTL9_VMD.pdb
Generated_NTL9_resid2to38.pdb

Step 4

Generated_NTL9_resid2to38_OrderedAtoms.pdb
NTL9_Trajectories_resid2to38_OrderedAtoms.pdb.zip

Step 5

NTL9_reference.pdb

Step 6

NTL9_Trajectories_aligned_to_reference.pdb




Here are the necessary files and corresponding descriptions to reproduce the results in the paper titled: "Efficient Reaction Coordinate Identification for Proteins Using Representation Learning"
<br /> The preprocessig steps are described for Chignolin protein step by step. For other proteins only the filename of each step has been provided. You can refer to the corresponding step's description for Chignolin protein to find how they have been generated.



** Chignolin **

1- Get the protein structure used for the simulations.
<br /> ("Chignolin.pdb", "Chignolin.psf")

2- Retain only the standart residues and remove all added elements to the protein sequence.
<br /> ("Chignolin_resid2to9.pdb")

3- Load the simulation trajectories in VMD and save only the clean sequence, as step 2. 
<br /> ("Chignolin_resid2to9_samples8and9_10000f.dcd")

4- We should now generage the reference protein. Keep in mind that the start residue index in both simulation trajectories and the reference protein should be the same. For example, if you remove the first residue at begining of the sequences in the trajectories, the residue IDs start at 2. This should be compatible with the reference protein. That is why you may use the same starting residues as they are in the original structure (i.e. in "Chignolin.pdb"), or replace them with random residues. Later, you will remove them and the residue IDs will start at the same index as it is in the trajectories. In some cases, after generating the protein in VMD, extra elements may be added to the protein ("Generated_Chignolin_VMD.pdb"), make sure to remove them 
<br /> ("Generated_Chignolin_RemovedExtra.pdb").
<br /> To order atom types in .pdb files, load both reference protein and cleaned simulations files in PyMOL and re-save them.
<br /> ("Generated_Chignolin_ExtraRemoved_OrderedAtoms.pdb", "Chignolin_resid2to9_samples8and9_10000f_OrderedAtoms.pdb")

<br /> If the residue indices in the cleaned trajectories starts from 2 or higher, now you can remove the extra ones in the generated structure (you can do it using VMD or simply delete them in the text version of .pdb file)

5- Now, we should place the desired reference protein in an appropriate position. 
<br /> Load it in VMD, and highlight the origin of space using this command in Tk Console or startup.command: 
<br /> ...
<br /> draw color red
<br /> draw sphere { 0 0 0 } resolution 16 radius 1.0
<br /> ...
<br /> move the geometric center of protein to the origin using this command (ignore error as “invalid command name <current geometric center>”):
<br /> ...
<br /> set sel [atomselect top all]
<br /> set gec [measure center $sel]
<br /> $gec moveto {0 0 0}
<br /> $sel moveby [vecscale -1.0 $gec]
<br /> ...

<br />- Rotate the protein to align its principal axis to the xyz coordination:
<br /> ...
<br /> lappend auto_path /directory/la1.0
<br /> lappend auto_path /directory/orient
<br /> package require Orient
<br /> namespace import Orient::orient
<br /> set sel [atomselect top "all"]
<br /> set I [draw principalaxes $sel]
<br /> set A [orient $sel [lindex $I 2] {0 0 1}]
<br /> $sel move $A
<br /> set I [draw principalaxes $sel]
<br /> set A [orient $sel [lindex $I 1] {0 1 0}]
<br /> $sel move $A
<br /> set I [draw principalaxes $sel]
<br /> ...
<br /> Save this ("Chignolin_reference.pdb)". You will use it as the the reference structure in "Kernel_analysis.py" code for RMSD measurments.

6- Align backbone of structures in the simulation trajectoris to this reference protein using VMD. Save the aligned trajectories ("Chignoline_#15_aligned_to_reference.pdb").

7- You may use the long trajectory for Kernel or split it to single .pdb files using "single_pdb.py" code.

8- Measure the Kernel values for different lambda values in each trajectory. Display and save the best Kernel result using "Kernel_analysis.py" code.


** Fs peptide **

1- "Fspeptide.pdb"

2- "Fs_resid2to22.pdb"

3- "Fs_Trajectories_resid2to22.dcd"

4- "Generated_Fs_VMD.pdb", "Generated_Fs_ExtraRemoved.pdb", "Generated_Fs_ExtraRemoved_OrderedAtoms.pdb", "Fs_Trajectories_resid2to22_OrderedAtoms.pdb.zip"

5- "Fs_reference.pdb"

6- "Fs_Trajectories_aligned_to_reference.pdb"


** Proteinb **

1- "proteinb.pdb", "proteinb.psf"

2- "proteinb_resid1to45.pdb"

3- "Proteinb_trajectories_resid1to44.dcd"

4- "Generated_Proteinb_VMD.pdb", "Generated_Proteinb_OrderedAtoms.pdb", "Proteinb_Simulation_resid1to44_OrderedAtoms.pdb.zip"

5- "Proteinb_reference.pdb"

6- "Proteinb_aligned_to_reference.pdb"


** Trp-cage **

1- "Trp_cage.psf", "Trp_cage.pdb"

2- "Trp_cage_resid3to20.pdb"

3- "Trp_cage_Trajectories_resid3to20.dcd"

4- "Generated_Trp_cage_VMD.pdb", "Generated_Trp_cage_RemovedExtra.pdb", "Generated_Trp_cage_ExtraRemoved_OrderedAtoms.pdb", "Trp_cage_Trajectories_resid3to20_OrderedAtoms.pdb.zip"

5- "Trp_cage_reference.pdb"

6- "Trp_cage_aligned_to_reference.pdb"


** Homeodomain **

1- "Homeodomain.psf", "Homeodomain.pdb"

2- "Homeodomain_resid3to54.pdb", "Homeodomain_Trajectories_resid3to54.dcd"

3- "Generated_Homeodomain_VMD.pdb", "Generated_Homeodomain_resid3to54.pdb"

4- "Generated_Homeodomain_resid3to54_OrderedAtoms.pdb", "Homeodomain_Trajectories_resid3to54_OrderedAtoms.pdb.zip"

5- "Homeodomain_reference.pdb"

6- "Homeodomain_Trajectories_aligned_to_reference.pdb"


** NTL9 **

1- "NTL9.pdb"

2- "NTL9_resid2to38.pdb", "NTL9_Trajectories_resid2to38.dcd"

3- "Generated_NTL9_VMD.pdb", "Generated_NTL9_resid2to38.pdb"

4- "Generated_NTL9_resid2to38_OrderedAtoms.pdb", "NTL9_Trajectories_resid2to38_OrderedAtoms.pdb.zip"

5- "NTL9_reference.pdb"

6- "NTL9_Trajectories_aligned_to_reference.pdb"

---
