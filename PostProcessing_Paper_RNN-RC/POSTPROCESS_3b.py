#!/usr/bin/env python
# # -*- coding: utf-8 -*-

"""Created by: Vlachas Pantelis, CSE-lab, ETH Zurich
"""
#!/usr/bin/env python
import pickle
import glob, os
import numpy as np
import argparse

# ADDING PARENT DIRECTORY TO PATH
import os,sys,inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
methods_dir = os.path.dirname(current_dir)+"/Methods"
sys.path.insert(0, methods_dir) 
from Config.global_conf import global_params
global_utils_path = methods_dir + "/Models/Utils"
sys.path.insert(0, global_utils_path) 
from global_utils import *


# PLOTTING
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import re
from Utils.utils import *

font = {'size'   : 16, 'family':'Times New Roman'}
matplotlib.rc('font', **font)
linewidth = 3
markersize = 10
# matplotlib.rc('text', usetex=True)
# matplotlib.rcParams['hatch.color'] = 'white'



# PLOTTING THE NUM OF ACCURATE PREDICTIONS W.R.T. NUMBER OF MODES
# python3 POSTPROCESS_3b.py --system_name Lorenz96_F8GP40R40 --Experiment_Name="Experiment_Daint_Large"
# python3 POSTPROCESS_3b.py --system_name Lorenz96_F10GP40R40 --Experiment_Name="Experiment_Daint_Large"

parser = argparse.ArgumentParser()
parser.add_argument("--system_name", help="system", type=str, required=True)
parser.add_argument("--Experiment_Name", help="Experiment_Name", type=str, required=False, default=None)
args = parser.parse_args()
system_name = args.system_name
Experiment_Name = args.Experiment_Name
# system_name="Lorenz3D"

# Experiment_Name="Experiment_Daint_Large"


if Experiment_Name is None or Experiment_Name=="None" or global_params.cluster == "daint":
    saving_path = global_params.saving_path.format(system_name)
else:
    saving_path = global_params.saving_path.format(Experiment_Name +"/"+system_name)
logfile_path=saving_path+"/Logfiles"
print(system_name)
print(logfile_path)

fig_path = saving_path + "/Total_Results_Figures"
os.makedirs(fig_path, exist_ok=True)

model_test_dict = getAllModelsTestDict(logfile_path)
model_train_dict = getAllModelsTrainDict(logfile_path)


model_names_str = [
"GPU-RNN-gru-RDIM_(.*)-NUM-LAY_1-SIZE-LAY_(.*)-ACT_(.*)-ISH_statefull-SL_(.*)-PL_(.*)-LR_(.*)-DKP_(.*)-ZKP_(.*)-HSPL_(.*)-IPL_(.*)-(.*)WID_0",
"GPU-RNN-gru-RDIM_(.*)-NUM-LAY_2-SIZE-LAY_(.*)-ACT_(.*)-ISH_statefull-SL_(.*)-PL_(.*)-LR_(.*)-DKP_(.*)-ZKP_(.*)-HSPL_(.*)-IPL_(.*)-(.*)WID_0",
"GPU-RNN-gru-RDIM_(.*)-NUM-LAY_3-SIZE-LAY_(.*)-ACT_(.*)-ISH_statefull-SL_(.*)-PL_(.*)-LR_(.*)-DKP_(.*)-ZKP_(.*)-HSPL_(.*)-IPL_(.*)-(.*)WID_0",
"GPU-RNN-lstm-RDIM_(.*)-NUM-LAY_1-SIZE-LAY_(.*)-ACT_(.*)-ISH_statefull-SL_(.*)-PL_(.*)-LR_(.*)-DKP_(.*)-ZKP_(.*)-HSPL_(.*)-IPL_(.*)-(.*)WID_0",
"GPU-RNN-lstm-RDIM_(.*)-NUM-LAY_2-SIZE-LAY_(.*)-ACT_(.*)-ISH_statefull-SL_(.*)-PL_(.*)-LR_(.*)-DKP_(.*)-ZKP_(.*)-HSPL_(.*)-IPL_(.*)-(.*)WID_0",
"GPU-RNN-lstm-RDIM_(.*)-NUM-LAY_3-SIZE-LAY_(.*)-ACT_(.*)-ISH_statefull-SL_(.*)-PL_(.*)-LR_(.*)-DKP_(.*)-ZKP_(.*)-HSPL_(.*)-IPL_(.*)-(.*)WID_0",
]
model_color_str = [
"blue", 
"green",
"red",
"orange",
"blueviolet",
"black",
"cornflowerblue",
]
model_marker_str = [
"s", 
"x", 
"o",
"d",
"*", 
"<",
">",
]
model_marker_width_str = [
3, 
3, 
3,
3,
3, 
3,
3,
]
model_label_str = [
"GRU-L1",
"GRU-L2",
"GRU-L3",
"LSTM-L1",
"LSTM-L2",
"LSTM-L3",
]



if system_name == "Lorenz3D":
    dt=0.01
    lambda1=0.0
elif system_name == "Lorenz96_F8GP40R40":
    dt=0.01
    lambda1=1.68
elif system_name == "Lorenz96_F10GP40R40":
    dt=0.01
    lambda1=2.27
elif system_name == "Lorenz96_F8GP40":
    dt=0.01
    lambda1=1.68



N = len(model_names_str)

# print(ITER)

WDITH=0.14
LENGTH=1.5
widths=0.12

for NUM_ACC_PRED_STR in ["num_accurate_pred_050_avg_TEST"]:
    
    fig, ax = plt.subplots(1)
    ax.yaxis.grid() # horizontal lines
    ax.set_axisbelow(True)

    ITER=0-(N-1)/2
    for MODEL in range(N):
        model_name = model_names_str[MODEL]
        model_color = model_color_str[MODEL]
        model_marker = model_marker_str[MODEL]
        model_markeredgewidth = model_marker_width_str[MODEL]
        model_label = model_label_str[MODEL]

        valid_time_2_rdim = {}
        REGEX = re.compile(model_name)
        for model_name_key in model_test_dict:
            # print(model_name_key)
            model_train = model_train_dict[model_name_key]
            # print(model_train)
            if REGEX.match(model_name_key):
                # print(model_test_dict[model_name_key])
                valid_time = model_test_dict[model_name_key][NUM_ACC_PRED_STR]*dt*lambda1
                mni = model_name_key.find("-RDIM_")
                try:
                    rdim = int(model_name_key[mni+6:mni+8])
                except ValueError:
                    rdim = int(model_name_key[mni+6:mni+7])
                mni = model_name_key.find("-SIZE-LAY_")
                try:
                    model_size = int(model_name_key[mni+10:mni+14])
                except ValueError:
                    model_size = int(model_name_key[mni+10:mni+13])

                if str(rdim) in valid_time_2_rdim:
                    valid_time_2_rdim[str(rdim)].append(valid_time)
                else:
                    valid_time_2_rdim[str(rdim)] = [valid_time]


        if len(valid_time_2_rdim) != 0:
            rdim_vec = []
            valid_time_min_vec = []
            valid_time_max_vec = []
            valid_time_mean_vec = []
            valid_time_all_vec = []
            dictkeys = valid_time_2_rdim.keys()
            dictkeys = [int(key) for key in dictkeys]
            dictkeys = np.sort(dictkeys)
            for intkey in dictkeys:
                rdim = str(intkey)
                valid_time_vec = valid_time_2_rdim[rdim]
                rdim_vec.append(int(rdim))

                valid_time_vec = np.array(valid_time_vec)
                idx = np.argsort(valid_time_vec)
                valid_time_vec = valid_time_vec[idx][::-1]

                PERCENT = 0.9
                # print(len(error_metric_vec))
                valid_time_vec = valid_time_vec[:int(np.ceil(PERCENT*len(valid_time_vec)))]
                valid_time_max = valid_time_vec[0]
                valid_time_min = valid_time_vec[-1]
                valid_time_mean = valid_time_vec.mean()
                valid_time_min_vec.append(valid_time_min)
                valid_time_max_vec.append(valid_time_max)
                valid_time_mean_vec.append(valid_time_mean)
                valid_time_all_vec.append(valid_time_vec)

            valid_time_min_vec=np.array(valid_time_min_vec)
            valid_time_max_vec=np.array(valid_time_max_vec)
            valid_time_mean_vec=np.array(valid_time_mean_vec)
            # print(model_name)
            # print(rdim_vec)
            # print(valid_time_max_vec)
            # print(valid_time_mean_vec)
            # print(valid_time_min_vec)

            # yerr=[]
            # yerr.append(valid_time_mean_vec-valid_time_min_vec)
            # yerr.append(valid_time_max_vec-valid_time_mean_vec)
            # yerr=np.array(yerr)
            # ax.errorbar(np.arange(len(rdim_vec))*LENGTH+ITER*WDITH, valid_time_mean_vec, yerr=yerr, color=model_color, label=model_label+"-"+str(model_size), elinewidth=3, fmt=model_marker,markersize=10, markeredgewidth=model_markeredgewidth, barsabove=True, capsize=8)




            # print(valid_time_vec)
            pos = np.arange(len(rdim_vec))*LENGTH+ITER*WDITH
            pos = list(pos)

            # print(np.shape(valid_time_all_vec))
            # print(np.shape(pos))
            # vp = ax.violinplot(valid_time_all_vec, pos, points=10, widths=widths, showmeans=False, showextrema=True, showmedians=True, bw_method=0.5)

            # vp = ax.violinplot(valid_time_all_vec, pos, points=10, widths=widths, showmeans=True, showextrema=True, showmedians=False, bw_method=0.5)

            vp = ax.violinplot([valid_time_all_vec[0]], [pos[0]], points=10, widths=widths, showmeans=False, showextrema=True, showmedians=True, bw_method=0.5)

            for patch in vp['bodies']:
                patch.set_color(model_color)

            for partname in ('cbars','cmins','cmaxes','cmedians'):
            # for partname in ('cbars','cmins','cmaxes','cmeans'):
                vpi = vp[partname]
                vpi.set_edgecolor(model_color)
                vpi.set_linewidth(2)

            vp = ax.violinplot([valid_time_all_vec[1]], [pos[1]], points=10, widths=widths, showmeans=False, showextrema=True, showmedians=True, bw_method=0.5)

            for patch in vp['bodies']:
                patch.set_color(model_color)
                patch.set_label(model_label)

            for partname in ('cbars','cmins','cmaxes','cmedians'):
            # for partname in ('cbars','cmins','cmaxes','cmeans'):
                vpi = vp[partname]
                vpi.set_edgecolor(model_color)
                vpi.set_linewidth(2)

            # for pc in vp['bodies']:
            #     pc.set_facecolor(model_color)
            #     pc.set_color(model_color)
            #     pc.set_edgecolor(model_color)
            #     pc.set_hatch(model_marker)
            #     pc.set_label(model_label)


            ax.set_xticks(np.arange(len(rdim_vec))*LENGTH)
            ax.set_xticklabels(rdim_vec)
        ITER+=1

    ax.set_xlabel('Reduced order dimension')
    ax.set_ylabel('VPT')
    ax.set_ylim(bottom=0)
    NUM_ACC_PRED_STR_SHORT = "NAP" if NUM_ACC_PRED_STR =="num_accurate_pred_050_avg_TEST" else 0
    fig.savefig(fig_path + '/LAYER_STUDY_VPT_{:}_2_RDIM.pdf'.format(NUM_ACC_PRED_STR_SHORT), bbox_inches='tight')
    lgd = ax.legend(loc="upper left", bbox_to_anchor=(1,1), prop={'size': 24})
    fig.savefig(fig_path + '/LAYER_STUDY_VPT_{:}_2_RDIM_LEGEND.pdf'.format(NUM_ACC_PRED_STR_SHORT), bbox_extra_artists=(lgd,), bbox_inches='tight')
    plt.close()





