import os
import time
import datetime
import pandas as pd
import numpy as np 
import datetime
import logging

today = datetime.date.today().strftime('%Y%m%d')
outputFileName = "Classification_NONSIM_"+today
outputFileName2 = "Classification_SIM_"+today
outputPath = "customer.attribute"

def mkSubFile(lines,head,srcName,sub):
    [des_filename, extname] = os.path.splitext(srcName)
    [drive_name, folder_name] = os.path.split(srcName)

    filename  = drive_name + '/split_' + folder_name +'_' + str(sub) + extname
    filename1  = drive_name + '/split_' + folder_name +'_' + str(sub) + ".fin"
    #filename1 = "D:\\Classification_SIM_" + today +'_' + str(sub) + extname
    print( 'make file: %s' %filename)    
    fout = open(filename,'w',encoding="utf-8",errors='replace')
    fout1 = open(filename1,'w',encoding="utf-8",errors='replace')
    try:
        fout.writelines([head])
        fout.writelines(lines)
        return sub + 1
    finally:
        fout.close()
        fout1.close()

def splitByLineCount(filename,count):
   # fin = codecs.open(filename,'r',encoding="utf-8",errors='replace')
    fin = open(filename,'r',encoding="utf-8",errors='replace')
    try:
        head = fin.readline()
        buf = []
        sub = 1
        for line in fin:
            buf.append(line)
            if len(buf) == count:
                sub = mkSubFile(buf,head,filename,sub)
                print('sub %d' % sub)
                buf = []
        if len(buf) != 0:
            sub = mkSubFile(buf,head,filename,sub)   
    finally:
        fin.close()

if __name__ == '__main__':
    begin = time.time()
    splitByLineCount(outputPath + '/' + outputFileName2 + ".tab" ,250000)
    splitByLineCount(outputPath +  '/' + outputFileName + ".tab" ,500000)
    end = time.time()
    print('time is %d seconds ' % (end - begin))
    
    