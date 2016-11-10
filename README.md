# Community Detection from Research Articles

The task is to detect research papers which belong to a common field of research.

The project contains following folders:
* aan :
  * This folder consists of the AAN (ACL Anthology Network) dataset. We worked on the 2013 release of the dataset.

* aan_small :
  * This folder consists of a subset of the AAN dataset. It contains approximately 2000 nodes.

* algorithms:
  * This folder contains the code for the different algorithms used.
    * Cosine-kmeans
    * Jaccard-kmeans
    * Louvain
    * Newman-girvan
    * Newman-girvan-v2 (not used to generate the outputs)

* metrics:
  * This folder contains code for different metrics used to construct the network.
    * authorCitation
      * This metric uses the author citation network to detect communities. We have used louvain and newman-girvan algorithms for this.
      * How to run: Refer Community-Detection/metrics/authorCitation/README.md
    * paperCitaion
      * This metric uses the paper citation network to detect communities. We have used louvain and newman-girvan algorithms for this.
      * How to run: Refer Community-Detection/metrics/paperCitation/README.md
    * title
      * This folder contains the code for running K-means algorithm (using Jaccard and Cosine) on the title metric.
      * How to run: Refer Community-Detection/metrics/title/README.md
    * year
      * This folder contains the code for running K-means algorithm (using Jaccard and Cosine) on the year metric.
      * How to run: Refer Community-Detection/metrics/year/README.md

* outputs
  * This folder contains the outputs for various algorithms run on different metrics along with their respective graphs.
  
* CommunityDetectionReport.pdf: Project report
