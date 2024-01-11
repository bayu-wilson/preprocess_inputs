# Preprocessing data for AI-assisted SR simulations of reionization

We use [MP-Gadget](https://github.com/MP-Gadget/MP-Gadget) to run cosmological simulation for the LR input. The input and output snapshots are stored in [bigfile](https://github.com/rainwoodman/bigfile) format.

**Step 1** : Run a low-resolution N-body simulation. Our model is trained on LR sets with {Ng_lr=170, Boxsize=100 Mpc/h}. The test LR simulation should in the same resolution. (e.g., {Ng_lr=64, Boxsize=38 Mpc/h}).

**Step 2** : `preproc_chunks.py` convert the snapshot of N-body simulation to a 3D image with 6 channels (3 for displacement and 3 for velocity field). This 3D field is split into 8 chunks due to memory constraints when training the data. The file names for displacement and velocity field chunks are 'disp_a[scale factor]f_chunk[i]' and 'vel_a[scale factor]f_chunk[i]' respectively. The shape is `(Nc/2,Ng/8,Ng/8,Ng/8)` for each of these files. Here `Nc=6` are the normalized displacement + velocity field of tracer particles arranged by their original grid. For usage, check `scripts/HR_preproc.pbs` and `scripts/LR_preproc.pbs` for example job scripts. 


