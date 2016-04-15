### Run ###

To generate papers_dict.p (used by k-means.py)

> python parseData.py

To generate similarity_Title.txt (used by k-means.py)

> python similarity.py

To generate the clusters using cosine k-means:

> python cosine-kmeans.py data/similarity_Title.txt

To generate the clusters using jaccard k-means:

> python createGraph.py uw
> python jaccard-kmeans.py

To generate the clusters using louvain algorithm:

> python createGraph.py w/uw
> python louvain.py w/uw
