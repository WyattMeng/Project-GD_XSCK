# -*- coding: utf-8 -*-
"""
Created on Sat Jul  7 17:14:04 2018

@author: Maddox.Meng | 孟舸帆 | Meng Gefan

2018-07-07: Calculate by whole new method -- Numexpr
"""

from datetime import date
#import numpy as np
import numexpr as ne
import pandas as pd
#audit_year = 2017
CY = 2018
NY = CY + 1
FY = CY + 5
w7 = CY*10000+1231
y7 = NY*10000+131
z7 = NY*10000+330
aa7 = NY*10000+1231
ab7 = FY*10000+1231
#w7 = date(CY,12,31)
#y7 = date(NY,1,31)
#z7 = date(NY,3,30)
#aa7 = date(NY,12,31)
#ab7 = date(FY,12,31)

ag7 = w7
ah7 = y7
ai7 = z7
aj7 = aa7
ak7 = ab7

ap7 = w7
aq7 = y7
ar7 = z7
as7 = aa7
at7 = ab7

be7 = w7

def int2date(s):
    s = str(s)
    if len(s) == 8:
        return date(int(s[0:4]), int(s[4:6]), int(s[6:8]))
    else:
        return s
md = {1:31,
      2:28,
      3:31,
      4:30,
      5:31,
      6:30,
      7:31,
      8:31,
      9:30,
      10:31,
      11:30,
      12:31}
def dayscnt(d):
    y = round(d/10000)
    m = round(d/100) - y*100
    d = d - m*100 - y*10000

    ydays = (y-1)//4*(365*3+366) + (y-1)%4*(365)
    
    mdays = 0
    for k in md:
        if k <= m-1:
            mdays += md[k]
    if y%4 == 0 and m > 2:
        mdays + 1
    
    ddays = d
    dayscnt = ydays+mdays+ddays
    return dayscnt

def int2datediff(d1,d2):
    return dayscnt(d1)-dayscnt(d2)

#class ColumnCal(object):
#
#    def __init__(self, letter, row):
#        self.letter = letter
#        self.row = row
        
#    B = ColumnCal(B, df['账号'])
'''折人民币金额(测算)=-N*Q'''
#-原币金额*汇率
def cal_base_01(df):
    N = df['原币金额']
    Q = df['汇率']
    return round(-N*Q, 2)
    #return ne.evaluate('-N*Q')

'''diff=S+R'''
#折人民币金额(测算)+折人民币金额
def cal_base_02(df):
    R = df['折人民币金额']
    S = df['折人民币金额(测算)']
    return ne.evaluate('S+R')
    
'''起息日_EY=IF(OR(F=10101),DATE(2017,6,30),F)'''
#F起息日
def cal_base_03(df):
#    F = df['起息日']
#    if F == '10101' or F == 10101:
#        return date(CY,6,30) #date!!!
#    #else: return p #int20180101 to date
#    else: return int2date(F)
    #F = df['起息日']
    
    df1 = df[df['起息日'].isin(['10101',10101])].copy()
    df2 = df[-df['起息日'].isin(['10101',10101])].copy()
    #df1 = df[(df['起息日'] == '10101') | (df['起息日'] == 10101)]
    
    df1['起息日_EY'] = CY*10000+630
    df2['起息日_EY'] = df2['起息日']

    df=pd.concat([df1,df2])
    df.sort_index(inplace=True)

    return df
'''到期日_EY=IF(OR(G=10101),DATE(2017,12,31),G)'''
#G到期日
def cal_base_04(df):
#    G = df['到期日']
#    if G == '10101' or G == 10101:
#        return date(CY,12,31) #date!!!
#    else: return int2date(G)
    
    df1 = df[df['到期日'].isin(['10101',10101])].copy()
    df2 = df[-df['到期日'].isin(['10101',10101])].copy()
    
    df1['到期日_EY'] = CY*10000+1231
    df2['到期日_EY'] = df2['到期日']

    df=pd.concat([df1,df2])
    df.sort_index(inplace=True)    
    
    return df
    
'''下次付息日=IF(J="按日计息",$W$7,IF(J="按季计息",$Z$7,IF(J="按月计息",$Y$7,IF(J="利随本清",V,0))))'''
#J计息方式 V到期日_EY
def cal_base_05(df):
#    J = df['计息方式']
#    V = df['到期日_EY']
#    if J == "按日计息":
#        return date(2017,12,31) #变量
#    elif J == "按月计息":
#        return date(2018,1,31) #变量
#    elif J == "按季计息":
#        return date(2018,3,30) #变量
#    elif J == "利随本清":
#        return date(2018,3,30) #变量
#    else: return V
    
    df1 = df[df['计息方式'].isin(['按日计息'])].copy()
    df2 = df[df['计息方式'].isin(['按月计息'])].copy()   
    df3 = df[df['计息方式'].isin(['按季计息','利随本清'])].copy()  
    df4 = df[-df['计息方式'].isin(['按日计息','按月计息','按季计息','利随本清'])].copy()

    df1['下次付息日'] = CY*10000+1231
    df2['下次付息日'] = (CY+1)*10000+131
    df3['下次付息日'] = (CY+1)*10000+330
    df4['下次付息日'] = df4['到期日_EY']
    
    df=pd.concat([df1,df2,df3,df4])
    df.sort_index(inplace=True)   
    
    return df
#-------------------------------------------------------------------  
#01--利率风险
#-------------------------------------------------------------------
'''不计息=IF(J="不计息",-R,0)'''
#J计息方式 R折人民币金额
def cal_irr_00_01(df):
#    J = df['计息方式']
    R = df['折人民币金额']
#    if J == "不计息": return -R
#    else: return 0
    
    df1 = df[df['计息方式'].isin(['不计息'])].copy()
    df2 = df[df['计息方式']!='不计息'].copy() 
    df1['IR_不计息'] = -df1['折人民币金额']
    df2['IR_不计息'] = 0  
#    print(df1)
#    print(df2)
    df=pd.concat([df1,df2])
    df.sort_index(inplace=True)      
    return df
'''三个月内=IF(K=0,IF(V<=$Z$7,-R,0),IF(W<=$Z$7,-R,0))-Y'''
#=IF(V11<=$Z$7, -R11-Y11, 0-Y11)
#K浮动类型 V到期日_EY R折人民币金额 W下次付息日 Y不计息
def cal_irr_01_03(df):
    K = df['浮动类型']
    V = df['到期日_EY']
    R = df['折人民币金额']
    W = df['下次付息日']
    Y = df['IR_不计息']
#    if K == 0:
#        if V <= z7:
#            return -R -Y
#        else: return 0
#    else:
#        if W <= z7:
#            return -R -Y
#        else: return 0

    df1 = df[(df['浮动类型']==0) & (df['到期日_EY']<=z7)].copy()
    df2 = df[(df['浮动类型']==0) & (df['到期日_EY']> z7)].copy()   
    df3 = df[(df['浮动类型']!=0) & (df['下次付息日']<=z7)].copy()  
    df4 = df[(df['浮动类型']!=0) & (df['下次付息日']>z7)].copy()
    
    R1 = df1['折人民币金额']
    Y1 = df1['IR_不计息']

    R3 = df3['折人民币金额']
    Y3 = df3['IR_不计息']
    
    df1['IR_三个月内'] = ne.evaluate('-R1-Y1') 
    df2['IR_三个月内'] = 0
    df3['IR_三个月内'] = ne.evaluate('-R3-Y3') 
    df4['IR_三个月内'] = 0 

    df=pd.concat([df1,df2,df3,df4])
    df.sort_index(inplace=True)   
    
    return df
    
'''三个月至一年=IF(K=0,IF(V<=$AA$7,-R,0),IF(W<=$AA$7,-R,0))-Z-Y'''
#=IF(V11<=$AA$7,-R11-Y11-Z11,0-Y11-Z11)
#K浮动类型 V到期日_EY R折人民币金额 W下次付息日 Y不计息 Z三个月内
def cal_irr_03_12(df):
    K = df['浮动类型']
    V = df['到期日_EY']
    R = df['折人民币金额']
    W = df['下次付息日']
    Y = df['IR_不计息']
    Z = df['IR_三个月内']
#    if K == 0:
#        if V <= aa7:
#            return -R -Y -Z
#        else: return 0
#    else:
#        if W <= aa7:
#            return -R -Y -Z
#        else: return 0

    df1 = df[(df['浮动类型']==0) & (df['到期日_EY']<=aa7)].copy()
    df2 = df[(df['浮动类型']==0) & (df['到期日_EY']> aa7)].copy()   
    df3 = df[(df['浮动类型']!=0) & (df['下次付息日']<=aa7)].copy()  
    df4 = df[(df['浮动类型']!=0) & (df['下次付息日']>aa7)].copy()
    
    R1 = df1['折人民币金额']
    Y1 = df1['IR_不计息']
    Z1 = df1['IR_三个月内']
    R3 = df3['折人民币金额']
    Y3 = df3['IR_不计息']
    Z3 = df3['IR_三个月内']
    
    df1['IR_三个月至一年'] = ne.evaluate('-R1-Y1-Z1') 
    df2['IR_三个月至一年'] = 0
    df3['IR_三个月至一年'] = ne.evaluate('-R3-Y3-Z3') 
    df4['IR_三个月至一年'] = 0 

    df=pd.concat([df1,df2,df3,df4])
    df.sort_index(inplace=True)   
    
    return df
        
'''一年至五年=IF(K=0,IF(V<=$AB$7,-R,0),IF(W<=$AB$7,-R,0))-Y-Z-AA'''
#K浮动类型 V到期日_EY R折人民币金额 W下次付息日 Y不计息 Z三个月内 AA三个月至一年
def cal_irr_12_60(df):
    K = df['浮动类型']
    V = df['到期日_EY']
    #R = df['折人民币金额']
    W = df['下次付息日']
    #Y = df['IR_不计息']
    #Z = df['IR_三个月内']
    #AA = df['IR_三个月至一年']
#    if K == 0:
#        if V <= ab7:
#            return -R -Y -Z -AA
#        else: return 0
#    else:
#        if W <= ab7:
#            return -R -Y -Z -AA
#        else: return 0

    df1 = df[((K==0) & (V<=aa7)) | ((K!=0) & (W<=aa7))].copy()
    df2 = df[((K==0) & (V> aa7)) | ((K!=0) & (W> aa7))].copy()

    R1 = df1['折人民币金额']
    Y1 = df1['IR_不计息']
    Z1 = df1['IR_三个月内']
    AA1= df1['IR_三个月至一年']
    
    df1['IR_一年至五年'] = ne.evaluate('-R1-Y1-Z1-AA1') 
    df2['IR_一年至五年'] = 0

    df=pd.concat([df1,df2])
    df.sort_index(inplace=True)
    return df

'''五年以上=IF(K=0,IF(V>$AB$7,-R,0),IF(W>$AB$7,-R,0))'''
#K浮动类型 V到期日_EY R折人民币金额 W下次付息日
def cal_irr_60(df):
    K = df['浮动类型']
    V = df['到期日_EY']
    R = df['折人民币金额']
    W = df['下次付息日']
#    if K == 0:
#        if V > ab7:
#            return -R
#        else: return 0
#    else:
#        if W > ab7:
#            return -R
#        else: return 0
        
    df1 = df[((K==0) & (V> ab7)) | ((K!=0) & (W> aa7))].copy()
    df2 = df[((K==0) & (V<=aa7)) | ((K!=0) & (W<=aa7))].copy()

    R1 = df1['折人民币金额']

    df1['IR_五年以上'] = ne.evaluate('-R1') 
    df2['IR_五年以上'] = 0

    df=pd.concat([df1,df2])
    df.sort_index(inplace=True)
    return df
    
'合计=SUM(Y:AC)'
def cal_irr_sum(df):
    Y = df['IR_不计息']
    Z = df['IR_三个月内']
    AA = df['IR_三个月至一年']
    AB = df['IR_一年至五年']
    AC = df['IR_五年以上']
    return ne.evaluate('Y+Z+AA+AB+AC')
 
#-------------------------------------------------------------------
#02--流动性风险 Liquidity risk
#-------------------------------------------------------------------
'''无期限 0'''
def cal_lr_00(df):
    return ne.evaluate('0')

'''实时偿还 =IF(V<=$AG$7,-R,0)-AF'''
def cal_lr_0X(df):
    V = df['到期日_EY']
    #R = df['折人民币金额']
    #AF = df['LR_无期限']
#    if V <= ag7: return -R-AF
#    else: return 0-AF

    df1 = df[(V<=ag7)].copy()
    df2 = df[-(V<=ag7)].copy()
    R1 = df1['折人民币金额']
    AF1= df1['LR_无期限']
    AF2= df2['LR_无期限']
    df1['LR_实时偿还'] = ne.evaluate('-R1-AF1') 
    df2['LR_实时偿还'] = ne.evaluate(   '-AF2')
    df=pd.concat([df1,df2])
    df.sort_index(inplace=True)
    return df
    
'''一个月内 =IF(V<=$AH$7,-R,0)-AF-AG'''
def cal_lr_01(df):
    V = df['到期日_EY']
#    R = df['折人民币金额']
#    AF = df['LR_无期限']    
#    AG = df['LR_实时偿还']
#    if V <= ah7: return -R-AF-AG
#    else: return 0-AF-AG
    
    df1 = df[(V<=ah7)].copy()
    df2 = df[-(V<=ah7)].copy()
    R1 = df1['折人民币金额']
    AF1= df1['LR_无期限']
    AG1=df1['LR_实时偿还']
    AF2= df2['LR_无期限']
    AG2= df2['LR_实时偿还']
    df1['LR_一个月内'] = ne.evaluate('-R1-AF1-AG1') 
    df2['LR_一个月内'] = ne.evaluate(   '-AF2-AG2')
    df=pd.concat([df1,df2])
    df.sort_index(inplace=True)
    return df
    
'''一个月至三个月 =IF(V<=$AI$7,-R,0)-AF-AG-AH'''
def cal_lr_02(df):
    V = df['到期日_EY']
#    R = df['折人民币金额']
#    AF = df['LR_无期限']    
#    AG = df['LR_实时偿还']
#    AH = df['LR_一个月内']
#    if V <= ai7: return -R-AF-AG-AH
#    else: return 0-AF-AG-AH
    
    df1 = df[(V<=ai7)].copy()
    df2 = df[-(V<=ai7)].copy()
    R1 = df1['折人民币金额']
    AF1= df1['LR_无期限']
    AG1= df1['LR_实时偿还']
    AH1= df1['LR_一个月内']
    AF2= df2['LR_无期限']
    AG2= df2['LR_实时偿还']
    AH2= df2['LR_一个月内']
    df1['LR_一个月至三个月'] = ne.evaluate('-R1-AF1-AG1-AH1') 
    df2['LR_一个月至三个月'] = ne.evaluate(   '-AF2-AG2-AH2') 
    df=pd.concat([df1,df2])
    df.sort_index(inplace=True)
    return df
    
'''三个月至一年 =IF(V<=$AJ$7,-R,0)-AF-AG-AH-AI'''
def cal_lr_03(df):
    V = df['到期日_EY']
#    R = df['折人民币金额']
#    AF = df['LR_无期限']    
#    AG = df['LR_实时偿还']
#    AH = df['LR_一个月内']
#    AI = df['LR_一个月至三个月']
#    if V <= aj7: return -R-AF-AG-AH-AI
#    else: return 0-AF-AG-AH-AI
    
    df1 = df[(V<=aj7)].copy()
    df2 = df[-(V<=aj7)].copy()
    R1 = df1['折人民币金额']
    AF1= df1['LR_无期限']
    AG1= df1['LR_实时偿还']
    AH1= df1['LR_一个月内']
    AI1= df1['LR_一个月至三个月']
    AF2= df2['LR_无期限']
    AG2= df2['LR_实时偿还']
    AH2= df2['LR_一个月内']
    AI2= df2['LR_一个月至三个月']
    df1['LR_三个月至一年'] = ne.evaluate('-R1-AF1-AG1-AH1-AI1') 
    df2['LR_三个月至一年'] = ne.evaluate(   '-AF2-AG2-AH2-AI2') 
    df=pd.concat([df1,df2])
    df.sort_index(inplace=True)
    return df
    
'''一年至五年 =IF(V<=$AK$7,-R,0)-AF-AG-AH-AI-AJ'''
def cal_lr_04(df):
    V = df['到期日_EY']
#    R = df['折人民币金额']
#    AF = df['LR_无期限']    
#    AG = df['LR_实时偿还']
#    AH = df['LR_一个月内']
#    AI = df['LR_一个月至三个月']
#    AJ = df['LR_三个月至一年']
#    if V <= ak7: return -R-AF-AG-AH-AI-AJ
#    else: return 0-AF-AG-AH-AI-AJ
    
    df1 = df[(V<=ak7)].copy()
    df2 = df[-(V<=ak7)].copy()
    R1 = df1['折人民币金额']
    AF1= df1['LR_无期限']
    AG1= df1['LR_实时偿还']
    AH1= df1['LR_一个月内']
    AI1= df1['LR_一个月至三个月']
    AJ1= df1['LR_三个月至一年']
    AF2= df2['LR_无期限']
    AG2= df2['LR_实时偿还']
    AH2= df2['LR_一个月内']
    AI2= df2['LR_一个月至三个月']
    AJ2= df2['LR_三个月至一年']
    df1['LR_一年至五年'] = ne.evaluate('-R1-AF1-AG1-AH1-AI1-AJ1') 
    df2['LR_一年至五年'] = ne.evaluate(   '-AF2-AG2-AH2-AI2-AJ2') 
    df=pd.concat([df1,df2])
    df.sort_index(inplace=True)
    return df
    
'''五年以上 =IF(V>$AK$7,-R,0)'''
def cal_lr_05(df):
    V = df['到期日_EY']
#    R = df['折人民币金额']
#    if V > ak7: return -R
#    else: return 0
    
    df1 = df[(V>ak7)].copy()
    df2 = df[-(V>ak7)].copy()
    R1 = df1['折人民币金额']
    df1['LR_五年以上'] = ne.evaluate('-R1') 
    df2['LR_五年以上'] = 0
    df=pd.concat([df1,df2])
    df.sort_index(inplace=True)
    return df
    
'''合计 =SUM(AF:AL)'''
def cal_lr_06(df):
    AF = df['LR_无期限']
    AG = df['LR_实时偿还']
    AH = df['LR_一个月内']
    AI = df['LR_一个月至三个月']
    AJ = df['LR_三个月至一年']
    AK = df['LR_一年至五年']
    AL = df['LR_五年以上']
    return ne.evaluate('AF+AG+AH+AI+AJ+AK+AL')

#-------------------------------------------------------------------
'''03--流动性风险-未折现 Liquidity risk - undiscounted'''
#-------------------------------------------------------------------
'''无期限 0'''
def cal_lrn_00(df):
    return 0
'''实时偿还 =IF(V<=$AP$7,-(R*E/100*(V-U)/365+R),0)-AO'''
def cal_lrn_0X(df):
    V = df['到期日_EY']
#    R = df['折人民币金额']
#    E = df['利率']
#    U = df['起息日_EY']
#    AO = df['LRN_无期限']
#    if V <= ap7: return -(R*E/100*(V-U).days/365+R)-AO
#    else: return 0-AO
    
    df1 = df[(V<=ap7)].copy()
    df2 = df[-(V<=ap7)].copy()
    R1 = df1['折人民币金额']
    E1 = df1['利率']
    V1 = df1['到期日_EY']
    U1 = df1['起息日_EY']
    AO1= df1['LRN_无期限']
    df1['LR_实时偿还'] = ne.evaluate('-R1-AF1') 
    df2['LR_实时偿还'] = ne.evaluate(   '-AF2')
    df=pd.concat([df1,df2])
    df.sort_index(inplace=True)
    return df
    
'''一个月内 =IF(V<=$AQ$7,-(R*E/100*(V-U)/365+R),0)-AP-AO'''
def cal_lrn_01(df):
    V = df['到期日_EY']
    R = df['折人民币金额']
    E = df['利率']
    U = df['起息日_EY']
    AO = df['LRN_无期限']
    AP = df['LRN_实时偿还']
    if V <= aq7: return -(R*E/100*(V-U).days/365+R)-AO-AP
    else: return 0-AO-AP
    
'''一个月至三个月 =IF(V<=$AR$7,-(R*E/100*(V-U)/365+R),0)-AP-AO-AQ'''
def cal_lrn_02(df):
    V = df['到期日_EY']
    R = df['折人民币金额']
    E = df['利率']
    U = df['起息日_EY']
    AO = df['LRN_无期限']
    AP = df['LRN_实时偿还']
    AQ = df['LRN_一个月内']
    if V <= ar7: return -(R*E/100*(V-U).days/365+R)-AO-AP-AQ
    else: return 0-AO-AP-AQ
    
'''三个月至一年 =IF(V<=$AS$7,-(R*E/100*(V-U)/365+R),0)-AP-AO-AQ-AR'''
def cal_lrn_03(df):
    V = df['到期日_EY']
    R = df['折人民币金额']
    E = df['利率']
    U = df['起息日_EY']
    AO = df['LRN_无期限']
    AP = df['LRN_实时偿还']
    AQ = df['LRN_一个月内']
    AR = df['LRN_一个月至三个月']
    if V <= as7: return -(R*E/100*(V-U).days/365+R)-AO-AP-AQ-AR
    else: return 0-AO-AP-AQ-AR
    
'''一年至五年 =IF(V<=$AT$7,-(R*E/100*(V-U)/365+R),0)-AP-AO-AQ-AR-AS'''
def cal_lrn_04(df):
    V = df['到期日_EY']
    R = df['折人民币金额']
    E = df['利率']
    U = df['起息日_EY']
    AO = df['LRN_无期限']
    AP = df['LRN_实时偿还']
    AQ = df['LRN_一个月内']
    AR = df['LRN_一个月至三个月']
    AS = df['LRN_三个月至一年']
    if V <= at7: return -(R*E/100*(V-U).days/365+R)-AO-AP-AQ-AR-AS
    else: return 0-AO-AP-AQ-AR-AS
    
'''五年以上 =IF(V>$AT$7,-(R*E/100*(V-U)/365+R),0)'''
def cal_lrn_05(df):
    V = df['到期日_EY']
    R = df['折人民币金额']
    E = df['利率']
    U = df['起息日_EY']
    if V > at7: return -(R*E/100*(V-U).days/365+R)
    else: return 0
    
'''合计 =SUM(AO:AU)'''
def cal_lrn_06(df):
    AO = df['LRN_无期限']
    AP = df['LRN_实时偿还']
    AQ = df['LRN_一个月内']
    AR = df['LRN_一个月至三个月']
    AS = df['LRN_三个月至一年']
    AT = df['LRN_一年至五年']
    AU = df['LRN_五年以上']
    return ne.evaluate('AO+AP+AQ+AR+AS+AT+AU')


#-------------------------------------------------------------------
#04--应计利息测算 Accrued interest calculation
#-------------------------------------------------------------------
#合计 =-($BE$7-U)/365*E/100*R
def cal_ai_06(df):
    E = df['利率']
    R = df['折人民币金额']
    U = df['起息日_EY']
    return -(be7-U).days/365*E/100*R  
      
#无期限 =IF(AO=0,0,$BE)
def cal_ai_00(df):
    AO = df['LRN_无期限']
    #BE = df['AI_合计']
    E = df['利率']
    R = df['折人民币金额']
    U = df['起息日_EY']
    if AO == 0: return 0
    else: return -(be7-U).days/365*E/100*R  
    
#实时偿还 =IF(AP=0,0,$BE)
def cal_ai_0X(df):
    AP = df['LRN_实时偿还']
    #BE = df['AI_合计']
    E = df['利率']
    R = df['折人民币金额']
    U = df['起息日_EY']
    if AP == 0: return 0
    else: return -(be7-U).days/365*E/100*R    
    
#一个月内 =IF(AQ=0,0,$BE)
def cal_ai_01(df):
    AQ = df['LRN_一个月内']
    #BE = df['AI_合计']
    E = df['利率']
    R = df['折人民币金额']
    U = df['起息日_EY']
    if AQ == 0: return 0
    else: return -(be7-U).days/365*E/100*R    
    
#一个月至三个月 =IF(AR=0,0,$BE)
def cal_ai_02(df):
    AR = df['LRN_一个月至三个月']
    #BE = df['AI_合计']
    E = df['利率']
    R = df['折人民币金额']
    U = df['起息日_EY']
    if AR == 0: return 0
    else: return -(be7-U).days/365*E/100*R      
    
#三个月至一年 =IF(AS=0,0,$BE)
def cal_ai_03(df):
    AS = df['LRN_三个月至一年']
    #BE = df['AI_合计']
    E = df['利率']
    R = df['折人民币金额']
    U = df['起息日_EY']
    if AS == 0: return 0
    else: return -(be7-U).days/365*E/100*R   
    
#一年至五年 =IF(AT=0,0,$BE)
def cal_ai_04(df):
    AT = df['LRN_一年至五年']
    #BE = df['AI_合计']
    E = df['利率']
    R = df['折人民币金额']
    U = df['起息日_EY']
    if AT == 0: return 0
    else: return -(be7-U).days/365*E/100*R  
    
#五年以上 =IF(AU=0,0,$BE)
def cal_ai_05(df):
    AU = df['LRN_五年以上']
    #BE = df['AI_合计']
    E = df['利率']
    R = df['折人民币金额']
    U = df['起息日_EY']
    if AU == 0: return 0
    else: return -(be7-U).days/365*E/100*R  
    
