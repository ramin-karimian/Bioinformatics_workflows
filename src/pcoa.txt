import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
plt.rcParams["font.family"] = "Times New Roman"
plt.rcParams['pdf.fonttype'] = 42
import skbio
from scipy.spatial.distance import squareform, pdist
from skbio.stats.distance import permanova , DistanceMatrix
import matplotlib.patches as mpl_patches




def pcoa_plot_data(model,conf,pval):
    plt.clf()
    size= conf['marker_size']
    m = 'o'
    edgecolors =  'skyblue'
    clr = 'white'
    plt.figure(figsize=(conf['figsize']), dpi=conf['dpi'])

    for i in range(len(model.samples['PC1'])):

        plt.scatter(model.samples['PC1'][i],model.samples['PC2'][i],c = clr , s=size,marker = m, edgecolors =edgecolors)

    plt.axis("equal")
    plt.xlabel(f"PC1 ({np.around(model.proportion_explained[0],decimals = 2)})", labelpad = 1,fontsize= conf['fontsize'] )
    plt.ylabel(f"PC2 ({np.around(model.proportion_explained[1],decimals = 2)})", labelpad = 1,fontsize= conf['fontsize'] )
    plt.xticks(fontsize = conf['fontsize']-2)
    plt.yticks(fontsize = conf['fontsize']-2)


    ## pvalue report
    text_legend = []
    text_legend.append("P-value= {}".format(pval,decimals=3))
    handles = [mpl_patches.Rectangle((0, 0), 1, 1, fc="white", ec="white",
                                     lw=0, alpha=0)]
    leg1 = plt.legend(handles, text_legend, loc='upper right', fontsize=conf['fontsize'] -2,
               # prop={'weight':'bold'},shadow=True,
      fancybox=True, framealpha=0.7,
      handlelength=0, handletextpad=0)
    plt.gca().add_artist(leg1)


    # plt.legend(loc='center left',bbox_to_anchor=(1,0.5),fontsize = conf['fontsize']-4)

    plt.savefig(f"pcoa.png",bbox_inches='tight',dpi = conf['dpi'])
    plt.savefig(f"pcoa.pdf",bbox_inches='tight',dpi = conf['dpi'])

    plt.clf()
    plt.close()



def pcoa(df,sampleid_info,conf,name):
    ## df columns are samples and rows are features

    num_dim = conf['num_dim']
    df = df.apply(pd.to_numeric)
    ids = df.columns.values
    distance_matrix = squareform(pdist(df.T.values, 'braycurtis'))

    distance_matrix = np.nan_to_num(distance_matrix,nan=0) ## filing nan with 1

    # pvals = permanova(DistanceMatrix(distance_matrix),[sampleid_info[k] for k in df.columns])['p-value']
    ## You need to change this line, something similar to the line above
    pvals = permanova(DistanceMatrix(distance_matrix),LIST_OF_SAMPLES_GROUP)['p-value']

    model = skbio.stats.ordination.pcoa(distance_matrix,number_of_dimensions=num_dim)

    pcoa_plot_data(model,conf, pvals)

    return  model, ids


if __name__=="__main__":

    conf = {
            'num_dim': 2,
            'dpi': 500,
            'fontsize': 10,
            'figsize': [(2,2),(2.5,2.5)][1], # 2.5 for all
            'marker_size':15
            }

    df = pd.read_csv('datapath')

    sampleid_info  = {'S1':"group1",
                      'S2':'group2',
                      #  ...
                      }

    model , ids = pcoa(df,sampleid_info,conf,name='all')






