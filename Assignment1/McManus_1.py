#!/usr/bin/env python
# coding: utf-8

# # Assignment \#1
# ## Kevin McManus, student id: 109702479

# In[1]:


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


# In[13]:


def MyPlot(x,y,title, my_ax=None):
    if my_ax is None:
        fig, ax = plt.subplots( figsize=(8,6))
    else:
        ax = my_ax
        
    ax.plot(x,y)
    ax.set_title(title)
    ax.set_xlabel('Variable X'); ax.set_ylabel('Variable Y')
    return ax
        
def MyErrorPlot(x,y,title, yerror, my_ax=None):
    if my_ax is None:
        fig, ax = plt.subplots( figsize=(8,6))
    else:
        ax = my_ax

    ax.errorbar(x,y, yerr=yerror)
    ax.set_title(title)
    ax.set_xlabel('Variable X'); ax.set_ylabel('Variable Y')
    return ax


