import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import os
import imageio.v2 as imageio
from collections import Counter
from sklearn.linear_model import LinearRegression

#------------------------------
# ANIMATION PLOT
#------------------------------
def animate(networks,pos_type="circular",path="output.gif",plot_every=1):
    layout_fn = {
        "circular": nx.circular_layout,
        "spring": nx.spring_layout,
        "random": nx.random_layout
    }
    file_names = []
    for i, G in enumerate(networks):
        pos = layout_fn[pos_type](G)
        fig, ax = plt.subplots()
        fig.set_size_inches(5, 5)

        tmpx, tmpy = zip(*[pos[n] for n in pos])
        Lxmin, Lxmax = min(tmpx) - 0.2, max(tmpx) + 0.2
        Lymin, Lymax = min(tmpy) - 0.2, max(tmpy) + 0.2

        ax.set_xlim(Lxmin, Lxmax)
        ax.set_ylim(Lymin, Lymax)

        ax.axhline(y=Lymin)
        ax.axvline(x=Lxmin)
        ax.axhline(y=Lymax)
        ax.axvline(x=Lxmax)

        if G.is_directed():
            in_deg = dict(G.in_degree())
            out_deg = dict(G.out_degree())
            node_size = [in_deg[n]*50 for n in G.nodes()]
            node_color = [out_deg[n] for n in G.nodes()]
        else:
            degree = dict(G.degree())
            node_size = [degree[n]*50 for n in G.nodes()]
            node_color = [degree[n] for n in G.nodes()]

        nx.draw(G, pos, ax=ax, with_labels=True,
                node_size=node_size,
                node_color=node_color, 
                cmap = "coolwarm")

        filename = f"tmp-{i+1}.png"
        plt.savefig(filename, bbox_inches='tight')
        plt.close()
        file_names.append(filename)

    images = [imageio.imread(fname) for fname in file_names]
    imageio.mimsave(path, images, duration=.8, loop = 0)
    for fname in file_names:
        os.remove(fname)
    

#------------------------------
# NETWORK CENTRALITY CORRELATION PLOTS
#------------------------------
def plot_centrality_correlation(G,path=""):
    if nx.is_directed(G): 
        df = pd.DataFrame({
            "In Degree Centrality": nx.in_degree_centrality(G),
            "Out Degree Centrality": nx.out_degree_centrality(G),
            "In Closeness Centrality": nx.closeness_centrality(G.reverse(copy=True)),
            "Out Closeness Centrality": nx.closeness_centrality(G),
            "Betweenness Centrality": nx.betweenness_centrality(G.to_undirected()),
        })
    else: 
        df = pd.DataFrame({
            "Degree Centrality": nx.degree_centrality(G),
            "Betweenness Centrality": nx.betweenness_centrality(G),
            "Closeness Centrality": nx.closeness_centrality(G),
        })
    sns.pairplot(df, kind="scatter", diag_kind="hist")   
    plt.show()
    if path != "": 
        plt.savefig(path)  

#------------------------------
# AVERAGE DEGREE
#------------------------------
def ave_degree(G):
    if nx.is_directed(G): 
          print("In Avg Degree: " + str(np.mean(G.in_degree())))
          print("Out Avg Degree: " + str(np.mean(G.out_degree())))
    else: 
        print("Avg Degree: " + str(np.mean(G.degree())))

#------------------------------
# PLOT DEGREE DISTRIBUTION
#------------------------------
def plot_degree_distribution(G,type="in",path="",fit=False):
    if not nx.is_directed(G):
        data=G.degree(); type=""
        degrees = [d for _, d in G.degree()]
    else:
        if(type=="in"):  data=G.in_degree(); degrees = [d for _, d in G.in_degree()]
        if(type=="out"): data=G.out_degree(); degrees = [d for _, d in G.out_degree()]
    
    degree_count = Counter(degrees)
    deg, count = zip(*sorted(degree_count.items()))
    pdf_x = np.array(deg)
    pdf_y = np.array(count) / sum(count)

    sorted_deg = np.sort(degrees)
    cdf_y =  1 - np.arange(1, len(sorted_deg) + 1) / len(sorted_deg)

    fig, ax = plt.subplots(1, 4, figsize=(20, 5))

    ax[0].scatter(pdf_x, pdf_y)
    ax[0].plot(pdf_x, pdf_y)
    ax[0].set_xscale('log')
    ax[0].set_yscale('log')
    ax[0].set_title("PDF (log-log)")
    ax[0].set_xlabel("Out Degree (log)")
    ax[0].set_ylabel("Probability (Log)")

    ax[1].bar(pdf_x, pdf_y, width=0.8, align='center')    
    ax[1].set_title("PDF")
    ax[1].set_xlabel("Out Degree")
    ax[1].set_ylabel("Probability")

    ax[2].plot(sorted_deg, cdf_y)
    ax[2].set_xscale('log')
    ax[2].set_yscale('log')
    ax[2].set_title("cCDF (log-log)")
    ax[2].set_xlabel("Out Degree (log)")
    ax[2].set_ylabel("cCDF (log)")

    ax[3].plot(sorted_deg, cdf_y)
    ax[3].set_title("cCDF")
    ax[3].set_xlabel("Out Degree")
    ax[3].set_ylabel("cCDF")
    if fit:
        x_log = np.log10(pdf_x).reshape(-1, 1)
        y_log = np.log10(pdf_y)
        best_fit = LinearRegression().fit(x_log, y_log)
        pred_pdf = 10**best_fit.predict(np.log10(pdf_x).reshape(-1, 1))
        ax[0].plot(pdf_x, pred_pdf, color='red')

        nonzero_mask = cdf_y > 0
        x_vals = np.array(sorted_deg)[nonzero_mask]
        y_vals = cdf_y[nonzero_mask]
        x_log = np.log10(x_vals).reshape(-1, 1)
        y_log = np.log10(y_vals)
        best_fit = LinearRegression().fit(x_log, y_log)
        pred_ccdf = 10**best_fit.predict(np.log10(sorted_deg).reshape(-1, 1))
        ax[2].plot(sorted_deg, pred_ccdf, color='red')

    if path != "":
        plt.savefig(path)
    plt.show()

#------------------------------
# NETWORK PLOTTING FUNCTION
#------------------------------
def plot_network(G,node_color="degree",layout="random"):
    
    # POSITIONS LAYOUT
    N=len(G.nodes)
    if(layout=="spring"):
        # pos=nx.spring_layout(G,k=50*1./np.sqrt(N),iterations=100)
        pos=nx.spring_layout(G)

    if(layout=="random"):
        pos=nx.random_layout(G)

    #INITALIZE PLOT
    fig, ax = plt.subplots()
    fig.set_size_inches(15, 15)

    # NODE COLORS
    cmap=plt.cm.get_cmap('Greens')

    # DEGREE 
    if node_color=="degree":
            centrality=list(dict(nx.degree(G)).values())
  
    # BETWENNESS 
    if node_color=="betweeness":
            centrality=list(dict(nx.betweenness_centrality(G)).values())
  
    # CLOSENESS
    if node_color=="closeness":
            centrality=list(dict(nx.closeness_centrality(G)).values())

    # NODE SIZE CAN COLOR
    node_colors = [cmap(u/(0.01+max(centrality))) for u in centrality]
    node_sizes = [4000*u/(0.01+max(centrality)) for u in centrality]

    # #PLOT NETWORK
    nx.draw(G,
            with_labels=True,
            edgecolors="black",
            node_color=node_colors,
            node_size=node_sizes,
            font_color='white',
            font_size=18,
            pos=pos
            )

    plt.show()

#------------------------------
# NETWORK SUMMARY FUNCTION
#------------------------------
def network_summary(G):

    def centrality_stats(x):
        x1=dict(x)
        x2=np.array(list(x1.values())); #print(x2)
        print("	min:" ,min(x2))
        print("	mean:" ,np.mean(x2))
        print("	median:" ,np.median(x2))
        # print("	mode:" ,stats.mode(x2)[0][0])
        print("	max:" ,max(x2))
        x=dict(x)
        sort_dict=dict(sorted(x1.items(), key=lambda item: item[1],reverse=True))
        print("	top nodes:",list(sort_dict)[0:6])
        print("	          ",list(sort_dict.values())[0:6])

    try: 
        print("GENERAL")
        print("	number of nodes:",len(list(G.nodes)))
        print("	number of edges:",len(list(G.edges)))

        print("	is_directed:", nx.is_directed(G))
        print("	is_weighted:" ,nx.is_weighted(G))


        if(nx.is_directed(G)):
            print("IN-DEGREE (NORMALIZED)")
            centrality_stats(nx.in_degree_centrality(G))
            print("OUT-DEGREE (NORMALIZED)")
            centrality_stats(nx.out_degree_centrality(G))
        else:
            print("	number_connected_components", nx.number_connected_components(G))
            print("	number of triangle: ",len(nx.triangles(G).keys()))
            print("	density:" ,nx.density(G))
            print("	average_clustering coefficient: ", nx.average_clustering(G))
            print("	degree_assortativity_coefficient: ", nx.degree_assortativity_coefficient(G))
            print("	is_tree:" ,nx.is_tree(G))

            if(nx.is_connected(G)):
                print("	diameter:" ,nx.diameter(G))
                print("	radius:" ,nx.radius(G))
                print("	average_shortest_path_length: ", nx.average_shortest_path_length(G))

            #CENTRALITY 
            print("DEGREE (NORMALIZED)")
            centrality_stats(nx.degree_centrality(G))

            print("CLOSENESS CENTRALITY")
            centrality_stats(nx.closeness_centrality(G))

            print("BETWEEN CENTRALITY")
            centrality_stats(nx.betweenness_centrality(G))
    except:
        print("unable to run")

#------------------------------
# ISOLATE GCC
#------------------------------
def isolate_GCC(G):
    comps = sorted(nx.connected_components (G),key=len, reverse=True) 
    nodes_in_giant_comp = comps[0]
    return nx.subgraph(G, nodes_in_giant_comp)

