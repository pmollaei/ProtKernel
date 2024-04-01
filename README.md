# ProtKernel
Here are the necessary information to reproduce the results in the paper titled: ""

** Chignolin **

1- Get the protein structure provided for the simulations ("Chignolin.pdb")

2- Retain only the standart residues and remove all added elements for the simulation to the amino acid sequence in the protein structure ("Chignolin_resid2to9.pdb")

3- Load the simulation in VMD and save only the clean sequence ("Chignolin_resid2to9_samples8and9_10000f.dcd")

4- Use the clean sequence to generate the reference protein structure usin VMD ("generated_Chignolin_VMD.pdb"). In some cases, the VMD may add extra elements while generating a new protein, remove them ("Generated_Chignolin_ExtraRemoved.pdb").

5- (If needed) To order atom types in .pdb files, load both reference protein and cleaned simulations files in PyMOL and re-save them ("Generated_Chignolin_ExtraRemoved_OrderedAtoms.pdb", "Chignolin_resid2to9_samples8and9_10000f_OrderedAtoms.pdb")

6- 


The "Chignolin.pdb" is the protein structure provided for simulations in [1]. We used it to generate the basic structure of the protein using VMD ("Chignolin_reference.pdb"). The standard residues have been retained (resid 2 to 9) for our analysis. The generated protein is also rotated to align the principal axis of it with the x,y,z axis.
