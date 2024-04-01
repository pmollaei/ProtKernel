# ProtKernel
Here are the necessary information to reproduce the results in the paper titled: ""

** Chignolin **
---
1- Get the protein structure provided for the simulations ("Chignolin.pdb")

2- Retain only the standart residues and remove all added elements for the simulation to the amino acid sequence in the protein structure ("Chignolin_resid2to9.pdb")

3- Load the simulation in VMD and save only the clean sequence ("Chignolin_resid2to9_samples8and9_10000f.dcd")

4- We should now generage the reference protein. Keep in mind that the start residue index in both simulation trajectories and the reference protein should be the same. For example, if you remove the first residue at begining of the sequences in trajectories, the residue IDs start at 2. This should be compatible with the reference protein. That is why you may use the same starting residues as they are in the original structure (in "Chignolin.pdb"), or replace them with random residues. Later, you will remove them and the residue IDs will start at 2 in the reference structure . 
In some cases, the VMD may add extra elements at the end of the residue sequence while generating a new protein ("Generated_Chignolin_VMD.pdb"), remove them ("Generated_Chignolin_ExtraRemoved.pdb").

5- To order atom types in .pdb files, load both reference protein and cleaned simulations files in PyMOL and re-save them ("Generated_Chignolin_ExtraRemoved_OrderedAtoms.pdb", "Chignolin_resid2to9_samples8and9_10000f_OrderedAtoms.pdb")

6- If the residue indices in the cleaned trajectories starts from 2 or higher, now you can remove the extra ones in the generated structure (you can do it using VMD or simply delete them in the text version of .pdb file)

7- Now, we should place the desired reference protein in an appropriate position. 
Load it in VMD, and highlight the origin of space using this command in Tk Console or startup.command: 
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

8- Rotate the protein to align its principal axis to the xyz coordination:
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
<br /> Save this ("Reference_structure.pdb)" and use it as the the reference structure in the "Kernel_analysis.py" code for RMSD measurments.

9- Align the backbone of simulation trajectoris to this reference protein using VMD

10- Save .pdb format of the aligned trajectories

11- You may use the long trajectory for Kernel or split it to single .pdb files using "single_pdb.py" code

12- Measure the Kernel values for different lambda values in each trajectory. Display and save the best Kernel result using "Kernel_analysis.py" code.
