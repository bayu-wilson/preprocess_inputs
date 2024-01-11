import numpy as np
from nbodykit.source.catalog import BigFileCatalog
import os
import glob


basepath = "/scratch1/07502/tg868016/training_data/Output_N1360_L100_{}"
#sim_pathlist=[basepath.format("1"),basepath.format("2")] #path to each simulation from which we are extracting styles (scale factor)
sim_pathlist=[basepath.format("2")]
snapshots_per_sim = [glob.glob(path_i+"/PART_*") for path_i in sim_pathlist] #path to each snapshot for each simulation
num_sims = len(snapshots_per_sim)
#style_list = []
for i in range(num_sims):
	print(f"Getting style from sim: {sim_pathlist[i]}")
	style_folder = sim_pathlist[i]+"/style/"
	if not os.path.exists(style_folder):
		os.makedirs(style_folder)
	num_snapshots = len(snapshots_per_sim[i])
	#style_for_sim = []
	for j in range(num_snapshots):
		snapshot = snapshots_per_sim[i][j]
		print(f"Snapshot: {snapshot}")
		f = BigFileCatalog(snapshot, header = 'Header', dataset = '1/')
		#a = f.attrs['Time']
		#a = np.array([allTime[i][j]])
		a = np.array([f.attrs['Time']])
		style_snapshot = style_folder+f"/a_{a[0][0]:.6f}.npy"
		np.save(style_snapshot, a)
		#style_for_sim.append(a)
	#style_list.append(style_for_sim)
	print(" ")

"""

# replace the path with your own path to the style data    
#style_savingpath = '/hildafs/home/xzhangn/xzhangn/sr_pipeline/3.5-training/15_0/map2map/scripts/style/set{}/'
#style_savingpath =
for i in range(num_sims):
    style_folder = style_savingpath.format(i)
    if not os.path.exists(style_folder):
        os.makedirs(style_folder)
    for j in range(num_snapshots):
        path2style = style_folder + 'PART_' +  str(j).rjust(3, '0') + '.npy'
        a = np.array([allTime[i][j]])
        np.save(path2style, a)

"""


"""
glob.glob("/scratch1/07502/tg868016/training_data/Output_N1360_L100_2/PART_*")


# replace the path with your own path to the data
#path = '/hildafs/home/xzhangn/xzhangn/sim_output/dmo-100MPC/15_0/dmo-64/set{}/output/PART_'
basepath="/scratch1/07502/tg868016/training_data/Output_N1360_L100_{}"
pathlist=[basepath.format("1"),basepath.format("2")]


num_sims = 1 # number of different simulations
num_snapshots = 14 # number of snapshots per simulation

for i in range(len(pathlist)):
	for j in range(num_snapshots):
		path2sim = pathlist[i]+"/PART_"+str(j).rjust(3,'0')
		print(path2sim)
# list contain all scale factors
#for i in range(num_sims):
#    temp = []
#    for j in range(num_snapshots):
#        path2sim = path.format(i) + str(j).rjust(3, '0')
#	print(path2sim)
"""
