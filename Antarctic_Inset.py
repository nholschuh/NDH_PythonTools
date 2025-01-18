import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

def Antarctic_Inset(xs,ys,c='red',lw=2):

    plt.figure()
    gl = pd.read_table('/mnt/data01/Data/Antarctic_Groundinglines/MODIS_gl_ant/moa_gl.xy',header=None,delimiter=',')
    gl2 = pd.read_table('/mnt/data01/Data/Antarctic_Groundinglines/Ant_w_shelves.xy',header=None,delimiter=',')
    cval1 = 0.8
    cval2 = 0.95
    ds_fac = 10
    plt.fill(gl2[0][::ds_fac],gl2[1][::ds_fac],c=[cval1,cval1,cval1])
    plt.fill(gl[0][::ds_fac],gl[1][::ds_fac],c=[cval2,cval2,cval2])
    plt.plot(gl2[0][::ds_fac],gl2[1][::ds_fac],c=[0.7,0.7,0.7],lw=1.5)
    plt.plot(gl[0][::ds_fac],gl[1][::ds_fac],c=[0.7,0.7,0.7],lw=1.5)

    box = np.array([[xs[0],ys[0]],
                   [xs[1],ys[0]],
                   [xs[1],ys[1]],
                   [xs[0],ys[1]],
                   [xs[0],ys[0]]])
    plt.plot(box[:,0],box[:,1],c=c,lw=lw)


    plt.gca().set_aspect('equal')
    plt.gca().axis('off')


    