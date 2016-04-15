### Run ###

To generate papers_dict.p (used by k-means.py)

> python parseData.py

To generate similarity_Year.txt (used by k-means.py)

> python similarity_year.py

To generate the clusters

> python jaccard-kmeans similarity_Year.txt > output
> python cosine-kmeans similarity_Year.txt > output 
