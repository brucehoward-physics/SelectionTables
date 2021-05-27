import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

lcs = ['black','blue','green','red']

def getLabels(inDF):
    return np.array(inDF['Sample'])

def makeTableBySample(inDF,cuts=[]):
    if len(cuts)==0:
        print('NO INPUT ROWS GIVEN...')
        return
    labels = getLabels(inDF)
    cells = []
    cells_norm = []
    titles = np.array(inDF.columns)
    row0 = ['Sample']
    for i in range(len(cuts)):
        row0.append(cuts[i])
    cells.append(row0)
    cells_norm.append(row0)
    for i in range(len(labels)):
        label = labels[i]
        ###########################
        # Make the labels nicer...
        label = labels[i]
        if labels[i]=='NueCC':
            label = r'$\nu_e$'+' CC'
        if labels[i]=='NumuCC':
            label = r'$\nu_\mu$'+' CC'
        ###########################
        arr = np.array(inDF[ inDF['Sample']==labels[i] ][cuts])[0]
        arrNorm = 100.*arr/arr[0]
        row = [label]
        rowNorm = [label]
        for j in range(len(cuts)):
            string2append = str(arr[j])
            if arr[j]>100000:
                string2append = str(arr[j]).split('.')[0]
            if j==0:
                row.append(string2append)
                rowNorm.append(string2append)
            else:
                row.append(string2append)
                if arrNorm[j]>=1.:
                    rowNorm.append('{:.2f}'.format(arrNorm[j])+'%')
                else:
                    rowNorm.append('{:.4f}'.format(arrNorm[j])+'%')
        cells.append(row)
        cells_norm.append(rowNorm)
    return cells, cells_norm

def makeTableByCut(inDF,cuts=[]):
    if len(cuts)==0:
        print('NO INPUT ROWS GIVEN...')
        return
    vals = []
    for i in range(len(cuts)):
        vals.append(np.array(inDF[cuts[i]]))
    return vals

def makeSelectionPlot(inDF,cuts=[],signalLabel='NueCC',norm=False,grid=False):
    if len(cuts)==0:
        print('NO INPUT ROWS GIVEN...')
        return
    labels = getLabels(inDF)
    vals = makeTableByCut(inDF=inDF,cuts=cuts)
    sigVal=0.
    for iCut in range(len(cuts)):
        for iLabel in range(len(labels)):
            ###########################
            # Make the labels nicer...
            useLabel = labels[iLabel]
            if labels[iLabel]=='NueCC':
                useLabel = r'$\nu_e$'+' CC'
            if labels[iLabel]=='NumuCC':
                useLabel = r'$\nu_\mu$'+' CC'
            if labels[iLabel]=='Cosmic':
                useLabel = 'Cosm.'
            ###########################
            if iCut==0:
                plt.hist([float(iCut)+0.1],bins=np.linspace(iCut+0.1,iCut+0.9,2),\
                         weights=[np.sum(vals[iCut][iLabel:])/np.sum(vals[iCut])],\
                         color=lcs[iLabel],label=useLabel)
            else:
                plt.hist([float(iCut)+0.1],bins=np.linspace(iCut+0.1,iCut+0.9,2),\
                         weights=[np.sum(vals[iCut][iLabel:]/np.sum(vals[iCut]))],color=lcs[iLabel])
            if labels[iLabel]==signalLabel:
                sigVal=100.*vals[iCut][iLabel]/np.sum(vals[iCut])
                plt.text(x=iCut+0.1,y=1.02,s=useLabel+' = '+'{:.2f}'.format(sigVal)+'%',\
                         fontsize=13,color=lcs[iLabel])
    # Set up plot
    plt.title('Cut visualization + table',fontfamily='serif',fontsize=16)
    plt.legend(fontsize=16)
    plt.xlim(-1,len(cuts))
    plt.ylim(0.,1.06)
    plt.ylabel('Fraction of Selection',fontsize=14)
    plt.xticks([])
    if grid==True:
        plt.grid(axis='y')
    # Add table, see e.g. https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.table.html and demo
    cells, cells_norm = makeTableBySample(inDF=inDF,cuts=cuts)
    if norm==True:
        tbl = plt.table(cellText=cells_norm,cellLoc='center')
    else:
        tbl = plt.table(cellText=cells,cellLoc='center')
    # See https://github.com/matplotlib/matplotlib/issues/12828
    tbl.auto_set_font_size(False)
    tbl.set_fontsize(14)
    # Expand figure, see e.g.
    # https://stackoverflow.com/questions/332289/how-do-you-change-the-size-of-figures-drawn-with-matplotlib
    f = plt.gcf()
    f.set_size_inches(20,10)
    return
