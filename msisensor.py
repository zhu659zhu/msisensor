#!/usr/bin/env python
#----------------------------------
# $Authors: Haidong Zhu & Beifang Niu
# msisensor_t - microsatellite instability detection for tumor only data
# $Date: Fri May 10 11:14:49 CST 2019 $
# $Revision: 0.1 $
# $URL: $
#----------------------------------

# coding: utf-8

import os
import sys
import xgboost
import getopt
import hashlib

site_model_threshold = 0.3
msiscore_threshold = 0.2

rep_start = 1
rep_end = 36

min_rep_coverage = 20


class MSIPredict(object):
    
    def __init__(self):
        pass
    
    def normalization(self, old_list):
        sum_v = sum(old_list)
        if sum_v == 0:
            return
        for i in range(0, len(old_list)):
            old_list[i] = float(old_list[i]) / sum_v

    def load(self, file_name, site_file):
        site_dict = {}
        in_file = open(site_file, "r")
        for l in in_file:
            data = l.strip().split()
            site_dict["_".join(data[:2])] = 1
        feature_dict = {}
        in_file_feature = open(file_name, "r")
        l = in_file_feature.readline()
        while l:
            data = l.strip().split(" ")
            loc = data[0] + "_" + data[1]
            if site_dict.get(loc, 0) == 1:
                l = in_file_feature.readline()
                if l[0] != "T":
                    print "dis file error..."
                    exit()
                feature = l.strip().split(" ")[rep_start: rep_end]
                feature = map(float, feature)
                if sum(feature) < min_rep_coverage:
                    l = in_file_feature.readline()
                    continue
                self.normalization(feature)
                l = in_file_feature.readline()
                feature_dict[loc] = feature
            else:
                l = in_file_feature.readline()
                l = in_file_feature.readline()
        return feature_dict
                
    def predict(self, feature_dict, model_file):
        sta_num = 0
        uns_num = 0
        for site, x_test in feature_dict.items():
            bst = xgboost.Booster()
            m2 = hashlib.md5()
            m2.update(site)
            bst.load_model(model_file + '/%s' % m2.hexdigest())
            dtest = xgboost.DMatrix(x_test)
            y_pred = bst.predict(dtest)
            if y_pred > site_model_threshold:
                uns_num += 1
            else:
                sta_num += 1
        if (uns_num + sta_num) == 0:
            print "Total sites: 0"
            print "MSI status error..."
            exit()
        msiscore = float(uns_num)/(sta_num + uns_num)
        msi_status = "MSI" if float(uns_num)/(sta_num + uns_num) >= msiscore_threshold else "MSS"
        print "Total sites: ", sta_num + uns_num
        print "somatic sites: ", uns_num
        print "MSI score: ", msiscore
        print "MSI status: ", msi_status
        return msi_status
    
    def sample_predict(self, file_name, site_file, model_file):
        tmp_dict = self.load(file_name, site_file)
        return self.predict(tmp_dict, model_file)


if __name__ == '__main__':
    if len(sys.argv) < 4 or sys.argv[1] != "msi":
        print "missing parameter..."
        print "Example:"
        print "python " + sys.argv[0] + " msi -t ./171104_E00495_HF5C2CCXY_cancer.dedupped.bam -o ./179001959F2D-179001959F1D_MSI-H_output -b 2 -M ./models/"
        exit()
    else:
        opts,args = getopt.getopt(sys.argv[2:],'-d:t:o:b:M:',['msi'])
        arg_dict = {}
        for name, value in opts:
            arg_dict[name[1:]] = value
        if not os.path.exists(arg_dict["t"]):
            print "missing bam file..."
            exit()
        if not os.path.exists(arg_dict["t"] + ".bai"):
            print "missing bam index file..."
            exit()
        if arg_dict.get("M", "") == "":
            print "missing model files..."
            exit()
        elif arg_dict.get("o", "") == "":
            print "default file name..."
            arg_dict["o"] = "tmp"
        cmd = sys.argv[0][:-3] if sys.argv[0][:-3][0] == "/" else "./" + sys.argv[0][:-3]
        list_file = "1030c0aa35ca5c263daeae866ad18632"
        if not arg_dict.get("b", ""):
            os.popen(cmd + " msi -d %s -t %s -o %s /dev/null 2>&1" % (arg_dict["M"] + "/" + list_file,arg_dict["t"],arg_dict["o"]))
        else:
            os.popen(cmd + " msi -d %s -t %s -o %s -b %s /dev/null 2>&1" % (arg_dict["M"] + "/" + list_file,arg_dict["t"],arg_dict["o"],arg_dict["b"]))
        mst = MSIPredict()
        mst.sample_predict(arg_dict["o"] + "_dis", arg_dict["M"] + "/" + list_file, arg_dict["M"])


