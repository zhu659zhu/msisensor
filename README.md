MSIsensor_t (MSIsensor for tumor only)
===========
MSIsensor_t is a Python program to detect replication slippage variants at microsatellite regions, and differentiate them as somatic or germline. Given tumor only sequence data, it uses site models trainned by machine learning and figures out a somatic or germline value for a distribution per microsatellite. Our test results show that it's performance is comparable with paired tumor and normal sequence data input. And, We recommend to set 20% as an uniform msi score cutoff values for different cancer types. ( msi high: msi score >= 20%, msi low and mss: msi score <20% ). We also provide the test results of TCGA and EGA data and illustrate the performance comparison between original tumor/normal paired module and tumor only module.
        
                      MSIsensor_AUC   MSIsensor_t_AUC 
TCGA STAD&UCEC&CRC    ---             0.9919
TCGA STAD             0.9999          0.9999      
TCGA UCEC             0.9885          0.9933
TCGA CRC              0.9814          0.9942
EGA  STAD&COAD        1               1
Chinese panel         0.9774          0.994


If you used this tool for your work, please cite [PMID 24371154](https://www.ncbi.nlm.nih.gov/pubmed/24371154)

Beifang Niu*, Kai Ye*, Qunyuan Zhang, Charles Lu, Mingchao Xie, Michael D. McLellan, Michael C. Wendl and Li Ding#.MSIsensor: microsatellite instability detection using paired tu-mor-normal sequence data. Bioinformatics 30, 1015–1016 (2014).

Tumor only predict(beta)
-------
Prerequisite packages:

    apt-get install gcc g++ make zlib1g-dev libncurses5-dev libncursesw5-dev python python-pip
    pip install numpy scipy xgboost

Install:

    git clone https://github.com/zhu659zhu/msisensor.git
    cd msisensor

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
Li Ding <lding@wustl.edu>
