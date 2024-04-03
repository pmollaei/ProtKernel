# ProtKernel
Here are the necessary files and corresponding descriptions to reproduce the results in the paper titled: ""
<br /> The preprocessig steps are described for Chignolin protein step by step. For other proteins only the filename of each step has been provided. You can refer to the corresponding step's description for Chignolin protein to find how they have been generated.



** Chignolin **
---
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

6- Align backbone of structures in the simulation trajectoris to this reference protein using VMD.

7 Save .pdb format of the aligned trajectories.

8- You may use the long trajectory for Kernel or split it to single .pdb files using "single_pdb.py" code.

9 Measure the Kernel values for different lambda values in each trajectory. Display and save the best Kernel result using "Kernel_analysis.py" code.
