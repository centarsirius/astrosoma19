"""
Phil Mansfield's code showing how to read the halo MAHs generated by shellfish
March 2019
"""

from __future__ import print_function
from __future__ import division

import sys
import numpy as np
import collections
import struct
import os.path as path


def read_halos(mah_fname):
    """ read_halos reads all the halos in the given mass accretion history
    file. It returns an array of HaloMAH objects. The fields are:
    {
        id : int array
        snapshot_number : int array
        scale_factor : float array
        m200m : float array
        mvir : float array
        m200c : float array
        m500c : float array
        m2500c : float array
    }
    """
    
    fields = np.loadtxt(mah_fname, unpack=True)

    # Find indices of splits between accretion histories.
    idxs = [0]
    snap = fields[1]
    for i in range(len(snap) - 1):
        if snap[i] > snap[i + 1]: idxs.append(1 + i)
    idxs.append(len(snap))

    # Split into individual halos.
    halos = [None] * (len(idxs) - 1)
    for i in range(len(halos)):
        halos[i] = _new_halo(fields, idxs[i], idxs[i+1])
    
    return halos

def _new_halo(fields, lo, hi):
    """_new_halo creates a new Halo corresponding to the index range [lo, hi).
    """
    
    h = collections.namedtuple(
        "HaloMAH", ["id", "snaphot_number", "scale_factor",
                    "m200m", "mvir", "m200c", "m500c", "m2500c"],
    )

    id, snap, scale_factor, m200m, mvir, m200c, m500c, m2500c = fields

    h.id = np.array(id[lo:hi], dtype=int)
    h.snapshot_number = np.array(snap[lo:hi], dtype=int)
    h.scale_factor = scale_factor[lo:hi]
    h.m200m = m200m[lo:hi]
    h.mvir = mvir[lo:hi]
    h.m200c = m200c[lo:hi]
    h.m500c = m500c[lo:hi]
    h.m2500c = m2500c[lo:hi]        
    return h


    
if __name__ == "__main__":
    """
    if len(sys.argv) != 3:
        print("Correct usage: $ read_mah.py MAH_fname")
        exit(1)

    MAH_fname = sys.argv[1]

    halos = read_halos(MAH_fname)
    print("Mass Accretion Histories:")
    print("Mvir      M200m     M200c")
    for i, hd in enumerate(halos): 
        print(i,hd.mvir)
        #print("%.3g  %.3g  %.3g"%(hd.mvir, hd.m200m, hd.m200c))
    """
    print("-----------------------------------------------------------------")

