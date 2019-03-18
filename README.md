MSIsensor
===========
MSIsensor is a C++ program to detect replication slippage variants at microsatellite regions, and differentiate them as somatic or germline. Given paired tumor and normal sequence data, it builds a distribution for expected (normal) and observed (tumor) lengths of repeated sequence per microsatellite, and compares them using Pearson's Chi-Squared Test. Comprehensive testing indicates MSIsensor is an efficient and effective tool for deriving MSI status from standard tumor-normal paired sequence data. Since there are many users complained that they don't have paired normal sequence data or related normal sequence data can be used to build a paired normal control, we released MSIsensor with version from 0.3. Given tumor only sequence data, it uses comentropy theory and figures out a comentropy value for a distribution per microsatellite. Our test results show that it's performance is comparable with paired tumor and normal sequence data input(figure below). And, We recommend to set different msi score cutoff values for different cancer types. (for example: TCGA UCEC, msi high: msi score >= 13%). We also provide the test results of TCGA and EGA data and illustrate the performance comparison between original tumor/normal paired module and tumor only module. (see AUC figures below)

![](https://github.com/ding-lab/msisensor/blob/master/test/tumor_only_vs_pair.jpg)

MSIsensor_T: msisensor tumor only module; MSIsensor: original tumor/normal paired module.

![](https://github.com/ding-lab/msisensor/blob/master/test/msisensor-tumor-only.png)

If you used this tool for your work, please cite [PMID 24371154](https://www.ncbi.nlm.nih.gov/pubmed/24371154)

Beifang Niu*, Kai Ye*, Qunyuan Zhang, Charles Lu, Mingchao Xie, Michael D. McLellan, Michael C. Wendl and Li Ding#.MSIsensor: microsatellite instability detection using paired tu-mor-normal sequence data. Bioinformatics 30, 1015–1016 (2014).

Tumor only predict(beta)
-------
Prerequisite packages:

    apt-get install gcc g++ make zlib1g-dev libncurses5-dev libncursesw5-dev python python-pip
    pip install numpy scipy xgboost

Build:

    git clone https://github.com/ding-lab/msisensor.git
    cd msisensor
    make

Usage:

    python msisensor.py msi [options]

Options:

    -d   <string>   homopolymer and microsates file
    -t   <string>   tumor bam file
    -o   <string>   output distribution file
    -M   <string>   model folder
    -b   <int>      threads number for parallel computing, default=1

Example:

    python msisensor.py msi -d microsatellites.txt  -t ./171104_E00495_HF5C2CCXY_cancer.dedupped.bam -o ./179001959F2D-179001959F1D_MSI-H_output -b 2 -M ./models/

Output:

    Total sites:  54
    somatic sites:  8
    MSI score:  0.148148148148
    MSI status:  MSS

Contact
-------
If you have any questions, please contact one or more of the following folks:
Beifang Niu <bniu@sccas.cn>
Kai Ye <kaiye@xjtu.edu.cn>
Li Ding <lding@wustl.edu>
Cyriac Kandoth <ckandoth@gmail.com>
