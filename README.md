# ProtKernel
Here are the necessary information to reproduce the results in the paper titled: ""

** Chignolin **

1- Get the protein structure provided for the simulations ("Chignolin.pdb")

2- Retain only the standart residues and remove all added elements for the simulation to the amino acid sequence in the protein structure ("Chignolin_resid2to9.pdb")

3- Load the simulation in VMD and save only the clean sequence ("Chignolin_resid2to9_samples8and9_10000f.dcd")

4- Now, we should generage the reference protein. Keep in mind that the start residue index in both simulation trajectories and the reference protein should be the same. For example, if you remove the first residue at begining of the sequences in trajectories, the residue IDs start at 2. This should be compatible with the reference protein. That is why you may use the same starting residues as they are in the original structure (in "Chignolin.pdb"), or replace them with random residues. Later, you will remove them and the residue IDs will start at 2 in the reference structure ("generated_Chignolin_VMD.pdb"). In some cases, the VMD may add extra elements at the end of the residue sequence while generating a new protein, remove them ("Generated_Chignolin_ExtraRemoved.pdb").

clean sequence to generate the reference protein structure usin VMD ("generated_Chignolin_VMD.pdb"). 

5- (If needed) To order atom types in .pdb files, load both reference protein and cleaned simulations files in PyMOL and re-save them
("Generated_Chignolin_ExtraRemoved_OrderedAtoms.pdb", "Chignolin_resid2to9_samples8and9_10000f_OrderedAtoms.pdb")

6- Now, we should place the reference protein in an appropriate position. Load it in VMD, 
