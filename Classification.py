import os
import time
import datetime
import pandas as pd
import numpy as np 
import datetime
import logging

today = datetime.date.today().strftime('%Y%m%d')
i = datetime.datetime.now().strftime('%H%M%S')
today1 = datetime.date.today().strftime('%Y-%m-%d')

inputFileName = "FETNETNONSIM_"+today
inputFileName2 = "MDM_SDP_"+today
outputFileName = "Classification_NONSIM_"+today
outputFileName2 = "Classification_SIM_"+today
inputPath = "customer.attribute/output/"
outputPath = "customer.attribute/"
FORMAT = '%(asctime)s %(levelname)s: %(message)s'
logging.basicConfig(level=logging.DEBUG, filename= outputPath + '/log/Classification_ETL_daily' + today + '.log', filemode='w', format=FORMAT)


df = pd.read_csv(inputPath + inputFileName + '.csv')
df = df.rename(columns={"FETUID":"Key"})
df["CONTRACT_EXPIRY_DT"] = pd.to_datetime(df["CONTRACT_EXPIRY_DT"], errors='coerce')

def CONTRACT_DATE(a): 
    if pd.notnull(a):
            expiry_date = a - datetime.datetime.strptime(today1, '%Y-%m-%d') 
            if  expiry_date.days < 0:
                return "合約已到期"
            elif expiry_date.days >= 0:
                return "小於180天"
            elif expiry_date.days >= 180:
                return "大於180天"
            elif expiry_date.days >= 360:
                return "大於360天"
            elif expiry_date.days > 540:
                 return "大於540天"
    else:
        return 'N/A'
def AGE(a): 
    if pd.notnull(a):
            if  a <= 24:
                return "青春族 <=24歲"
            elif a >= 25 and a <= 34:
                return "上班族 25~34歲"
            elif a >= 35 and a <= 49:
                return "夾心族 35~49歲"
            elif a >= 50 and a <= 100:
                return "樂活族 >=50歲"
            elif a > 100:
                return "異常值大於100歲"
    else:
        return 'N/A'
    
df['CONTRACT_EXPIRY_DT_Group_180'] = df.apply(lambda x: CONTRACT_DATE(x.CONTRACT_EXPIRY_DT), axis = 1) 
df['AGE_Group'] = df.apply(lambda x: AGE(x.AGE), axis = 1) 

df = df.fillna('N/A')
df.to_csv(  outputPath + outputFileName + '.tab' , sep = '\t' ,index=False, encoding='utf8')

logging.info('Classification using NONSIM file translation completed\n')
print("Classification using NONSIM file translation completed")
f=open(outputPath + outputFileName + '.fin',"w")
f.close()
logging.info('NONSIM.fin file created\n')
print("NONSIM.fin file created")


df = pd.read_csv(inputPath + inputFileName2 + '.csv')
df = df.rename(columns={"FETUID":"Key"})
df["CONTRACT_EXPIRY_DT"] = pd.to_datetime(df["CONTRACT_EXPIRY_DT"], errors='coerce')
df['CONTRACT_EXPIRY_DT_Group_180'] = df.apply(lambda x: CONTRACT_DATE(x.CONTRACT_EXPIRY_DT), axis = 1) 
df['AGE_Group'] = df.apply(lambda x: AGE(x.AGE), axis = 1) 


df = df.fillna('N/A')
df.to_csv(outputPath + outputFileName2 + '.tab', sep = '\t' ,index=False, encoding='utf8')
logging.info('Classification using SIM file translation completed\n')
print("Classification using SIM file translation completed")

f=open(outputPath + outputFileName2 + '.fin' ,"w")
f.close()
logging.info('SIM.fin file created\n')
print("SIM.fin file created\n")




def mkSubFile(lines,head,srcName,sub):
    [des_filename, extname] = os.path.splitext(srcName)
    [drive_name, folder_name] = os.path.split(srcName)

    filename  = drive_name + '\split_' + folder_name +'_' + str(sub) + extname
    filename1  = drive_name + '\split_' + folder_name +'_' + str(sub) + ".fin"
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
    splitByLineCount(outputPath + outputFileName2 ,250000)
    splitByLineCount(outputPath + outputFileName,500000)
    end = time.time()
    print('time is %d seconds ' % (end - begin))
    
    