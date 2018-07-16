# -*- coding: utf-8 -*-
"""
Created on Wed Jul  4 17:43:19 2018

@author: Maddox.Meng
"""

from datetime import date
#audit_year = 2017
CY = 2018
NY = CY + 1 #2019
FY = CY + 5 #2023
w7 = date(CY,6,30)
y7 = date(CY,7,31)
z7 = date(CY,9,30)
aa7 = date(NY,6,30)
ab7 = date(FY,6,30)

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
    return date(int(s[0:4]), int(s[4:6]), int(s[6:8]))

#class ColumnCal(object):
#
#    def __init__(self, letter, row):
#        self.letter = letter
#        self.row = row
        
#    B = ColumnCal(B, row['账号'])
'''折人民币金额(测算)=-N*Q'''
#-原币金额*汇率
def cal_base_01(row):
    N = row['原币金额']
    Q = row['汇率']
    return round(-N*Q, 2)

'''diff=S+R'''
#折人民币金额(测算)+折人民币金额
def cal_base_02(row):
    R = row['折人民币金额']
    S = row['折人民币金额(测算)']
    return S+R
    
'''起息日_EY=IF(OR(F=10101),DATE(2017,6,30),F)'''
#F起息日
def cal_base_03(row):
    F = row['起息日']
    if F == '10101' or F == 10101:
        return date(CY,6,30) #date!!!
    #else: return p #int20180101 to date
    else: return int2date(F)

'''到期日_EY=IF(OR(G=10101),DATE(2017,12,31),G)'''
#G到期日
def cal_base_04(row):
    G = row['到期日']
    if G == '10101' or G == 10101:
        return date(CY,12,31) #date!!!
    else: return int2date(G)
    
'''下次付息日=IF(J="按日计息",$W$7,IF(J="按季计息",$Z$7,IF(J="按月计息",$Y$7,IF(J="利随本清",V,0))))'''
#J计息方式 V到期日_EY
def cal_base_05(row):
    J = row['计息方式']
    V = row['到期日_EY']
    if J == "按日计息":
        return date(2017,12,31) #变量
    elif J == "按月计息":
        return date(2018,1,31) #变量
    elif J == "按季计息":
        return date(2018,3,30) #变量
    elif J == "利随本清":
        return date(2018,3,30) #变量
    else: return V

#-------------------------------------------------------------------  
#01--利率风险
#-------------------------------------------------------------------
'''不计息=IF(J="不计息",-R,0)'''
#J计息方式 R折人民币金额
def cal_irr_00_01(row):
    J = row['计息方式']
    R = row['折人民币金额']
    if J == "不计息": return -R
    else: return 0
    
'''三个月内=IF(K=0,IF(V<=$Z$7,-R,0),IF(W<=$Z$7,-R,0))-Y'''
#=IF(V11<=$Z$7, -R11-Y11, 0-Y11)
#K浮动类型 V到期日_EY R折人民币金额 W下次付息日 Y不计息
def cal_irr_01_03(row):
    K = row['浮动类型']
    V = row['到期日_EY']
    R = row['折人民币金额']
    W = row['下次付息日']
    Y = row['IR_不计息']
    if K == 0:
        if V <= z7:
            return -R -Y
        else: return 0
    else:
        if W <= z7:
            return -R -Y
        else: return 0

    
'''三个月至一年=IF(K=0,IF(V<=$AA$7,-R,0),IF(W<=$AA$7,-R,0))-Z-Y'''
#=IF(V11<=$AA$7,-R11-Y11-Z11,0-Y11-Z11)
#K浮动类型 V到期日_EY R折人民币金额 W下次付息日 Y不计息 Z三个月内
def cal_irr_03_12(row):
    K = row['浮动类型']
    V = row['到期日_EY']
    R = row['折人民币金额']
    W = row['下次付息日']
    Y = row['IR_不计息']
    Z = row['IR_三个月内']
    if K == 0:
        if V <= aa7:
            return -R -Y -Z
        else: return 0
    else:
        if W <= aa7:
            return -R -Y -Z
        else: return 0
        
'''一年至五年=IF(K=0,IF(V<=$AB$7,-R,0),IF(W<=$AB$7,-R,0))-Y-Z-AA'''
#K浮动类型 V到期日_EY R折人民币金额 W下次付息日 Y不计息 Z三个月内 AA三个月至一年
def cal_irr_12_60(row):
    K = row['浮动类型']
    V = row['到期日_EY']
    R = row['折人民币金额']
    W = row['下次付息日']
    Y = row['IR_不计息']
    Z = row['IR_三个月内']
    AA = row['IR_三个月至一年']
    if K == 0:
        if V <= ab7:
            return -R -Y -Z -AA
        else: return 0
    else:
        if W <= ab7:
            return -R -Y -Z -AA
        else: return 0

'''五年以上=IF(K=0,IF(V>$AB$7,-R,0),IF(W>$AB$7,-R,0))'''
#K浮动类型 V到期日_EY R折人民币金额 W下次付息日
def cal_irr_60(row):
    K = row['浮动类型']
    V = row['到期日_EY']
    R = row['折人民币金额']
    W = row['下次付息日']
    if K == 0:
        if V > ab7:
            return -R
        else: return 0
    else:
        if W > ab7:
            return -R
        else: return 0
    
'合计=SUM(Y:AC)'
def cal_irr_sum(row):
    Y = row['IR_不计息']
    Z = row['IR_三个月内']
    AA = row['IR_三个月至一年']
    AB = row['IR_一年至五年']
    AC = row['IR_五年以上']
    return Y+Z+AA+AB+AC
 
#-------------------------------------------------------------------
#02--流动性风险 Liquidity risk
#-------------------------------------------------------------------
'''无期限 0'''
def cal_lr_00(row):
    return 0

'''实时偿还 =IF(V<=$AG$7,-R,0)-AF'''
def cal_lr_0X(row):
    V = row['到期日_EY']
    R = row['折人民币金额']
    AF = row['LR_无期限']
    if V <= ag7: return -R-AF
    else: return 0-AF
    
'''一个月内 =IF(V<=$AH$7,-R,0)-AF-AG'''
def cal_lr_01(row):
    V = row['到期日_EY']
    R = row['折人民币金额']
    AF = row['LR_无期限']    
    AG = row['LR_实时偿还']
    if V <= ah7: return -R-AF-AG
    else: return 0-AF-AG
    
'''一个月至三个月 =IF(V<=$AI$7,-R,0)-AF-AG-AH'''
def cal_lr_02(row):
    V = row['到期日_EY']
    R = row['折人民币金额']
    AF = row['LR_无期限']    
    AG = row['LR_实时偿还']
    AH = row['LR_一个月内']
    if V <= ai7: return -R-AF-AG-AH
    else: return 0-AF-AG-AH
    
'''三个月至一年 =IF(V<=$AJ$7,-R,0)-AF-AG-AH-AI'''
def cal_lr_03(row):
    V = row['到期日_EY']
    R = row['折人民币金额']
    AF = row['LR_无期限']    
    AG = row['LR_实时偿还']
    AH = row['LR_一个月内']
    AI = row['LR_一个月至三个月']
    if V <= aj7: return -R-AF-AG-AH-AI
    else: return 0-AF-AG-AH-AI
    
'''一年至五年 =IF(V<=$AK$7,-R,0)-AF-AG-AH-AI-AJ'''
def cal_lr_04(row):
    V = row['到期日_EY']
    R = row['折人民币金额']
    AF = row['LR_无期限']    
    AG = row['LR_实时偿还']
    AH = row['LR_一个月内']
    AI = row['LR_一个月至三个月']
    AJ = row['LR_三个月至一年']
    if V <= ak7: return -R-AF-AG-AH-AI-AJ
    else: return 0-AF-AG-AH-AI-AJ
    
'''五年以上 =IF(V>$AK$7,-R,0)'''
def cal_lr_05(row):
    V = row['到期日_EY']
    R = row['折人民币金额']
    if V > ak7: return -R
    else: return 0
    
'''合计 =SUM(AF:AL)'''
def cal_lr_06(row):
    AF = row['LR_无期限']
    AG = row['LR_实时偿还']
    AH = row['LR_一个月内']
    AI = row['LR_一个月至三个月']
    AJ = row['LR_三个月至一年']
    AK = row['LR_一年至五年']
    AL = row['LR_五年以上']
    return AF+AG+AH+AI+AJ+AK+AL

#-------------------------------------------------------------------
'''03--流动性风险-未折现 Liquidity risk - undiscounted'''
#-------------------------------------------------------------------
'''无期限 0'''
def cal_lrn_00(row):
    return 0
'''实时偿还 =IF(V<=$AP$7,-(R*E/100*(V-U)/365+R),0)-AO'''
def cal_lrn_0X(row):
    V = row['到期日_EY']
    R = row['折人民币金额']
    E = row['利率']
    U = row['起息日_EY']
    AO = row['LRN_无期限']
    if V <= ap7: return -(R*E/100*(V-U).days/365+R)-AO
    else: return 0-AO
    
'''一个月内 =IF(V<=$AQ$7,-(R*E/100*(V-U)/365+R),0)-AP-AO'''
def cal_lrn_01(row):
    V = row['到期日_EY']
    R = row['折人民币金额']
    E = row['利率']
    U = row['起息日_EY']
    AO = row['LRN_无期限']
    AP = row['LRN_实时偿还']
    if V <= aq7: return -(R*E/100*(V-U).days/365+R)-AO-AP
    else: return 0-AO-AP
    
'''一个月至三个月 =IF(V<=$AR$7,-(R*E/100*(V-U)/365+R),0)-AP-AO-AQ'''
def cal_lrn_02(row):
    V = row['到期日_EY']
    R = row['折人民币金额']
    E = row['利率']
    U = row['起息日_EY']
    AO = row['LRN_无期限']
    AP = row['LRN_实时偿还']
    AQ = row['LRN_一个月内']
    if V <= ar7: return -(R*E/100*(V-U).days/365+R)-AO-AP-AQ
    else: return 0-AO-AP-AQ
    
'''三个月至一年 =IF(V<=$AS$7,-(R*E/100*(V-U)/365+R),0)-AP-AO-AQ-AR'''
def cal_lrn_03(row):
    V = row['到期日_EY']
    R = row['折人民币金额']
    E = row['利率']
    U = row['起息日_EY']
    AO = row['LRN_无期限']
    AP = row['LRN_实时偿还']
    AQ = row['LRN_一个月内']
    AR = row['LRN_一个月至三个月']
    if V <= as7: return -(R*E/100*(V-U).days/365+R)-AO-AP-AQ-AR
    else: return 0-AO-AP-AQ-AR
    
'''一年至五年 =IF(V<=$AT$7,-(R*E/100*(V-U)/365+R),0)-AP-AO-AQ-AR-AS'''
def cal_lrn_04(row):
    V = row['到期日_EY']
    R = row['折人民币金额']
    E = row['利率']
    U = row['起息日_EY']
    AO = row['LRN_无期限']
    AP = row['LRN_实时偿还']
    AQ = row['LRN_一个月内']
    AR = row['LRN_一个月至三个月']
    AS = row['LRN_三个月至一年']
    if V <= at7: return -(R*E/100*(V-U).days/365+R)-AO-AP-AQ-AR-AS
    else: return 0-AO-AP-AQ-AR-AS
    
'''五年以上 =IF(V>$AT$7,-(R*E/100*(V-U)/365+R),0)'''
def cal_lrn_05(row):
    V = row['到期日_EY']
    R = row['折人民币金额']
    E = row['利率']
    U = row['起息日_EY']
    if V > at7: return -(R*E/100*(V-U).days/365+R)
    else: return 0
    
'''合计 =SUM(AO:AU)'''
def cal_lrn_06(row):
    AO = row['LRN_无期限']
    AP = row['LRN_实时偿还']
    AQ = row['LRN_一个月内']
    AR = row['LRN_一个月至三个月']
    AS = row['LRN_三个月至一年']
    AT = row['LRN_一年至五年']
    AU = row['LRN_五年以上']
    return AO+AP+AQ+AR+AS+AT+AU

#-------------------------------------------------------------------
#04--应计利息测算 Accrued interest calculation
#-------------------------------------------------------------------
#合计 =-($BE$7-U)/365*E/100*R
def cal_ai_06(row):
    E = row['利率']
    R = row['折人民币金额']
    U = row['起息日_EY']
    return -(be7-U).days/365*E/100*R  
      
#无期限 =IF(AO=0,0,$BE)
def cal_ai_00(row):
    AO = row['LRN_无期限']
    #BE = row['AI_合计']
    E = row['利率']
    R = row['折人民币金额']
    U = row['起息日_EY']
    if AO == 0: return 0
    else: return -(be7-U).days/365*E/100*R  
    
#实时偿还 =IF(AP=0,0,$BE)
def cal_ai_0X(row):
    AP = row['LRN_实时偿还']
    #BE = row['AI_合计']
    E = row['利率']
    R = row['折人民币金额']
    U = row['起息日_EY']
    if AP == 0: return 0
    else: return -(be7-U).days/365*E/100*R    
    
#一个月内 =IF(AQ=0,0,$BE)
def cal_ai_01(row):
    AQ = row['LRN_一个月内']
    #BE = row['AI_合计']
    E = row['利率']
    R = row['折人民币金额']
    U = row['起息日_EY']
    if AQ == 0: return 0
    else: return -(be7-U).days/365*E/100*R    
    
#一个月至三个月 =IF(AR=0,0,$BE)
def cal_ai_02(row):
    AR = row['LRN_一个月至三个月']
    #BE = row['AI_合计']
    E = row['利率']
    R = row['折人民币金额']
    U = row['起息日_EY']
    if AR == 0: return 0
    else: return -(be7-U).days/365*E/100*R      
    
#三个月至一年 =IF(AS=0,0,$BE)
def cal_ai_03(row):
    AS = row['LRN_三个月至一年']
    #BE = row['AI_合计']
    E = row['利率']
    R = row['折人民币金额']
    U = row['起息日_EY']
    if AS == 0: return 0
    else: return -(be7-U).days/365*E/100*R   
    
#一年至五年 =IF(AT=0,0,$BE)
def cal_ai_04(row):
    AT = row['LRN_一年至五年']
    #BE = row['AI_合计']
    E = row['利率']
    R = row['折人民币金额']
    U = row['起息日_EY']
    if AT == 0: return 0
    else: return -(be7-U).days/365*E/100*R  
    
#五年以上 =IF(AU=0,0,$BE)
def cal_ai_05(row):
    AU = row['LRN_五年以上']
    #BE = row['AI_合计']
    E = row['利率']
    R = row['折人民币金额']
    U = row['起息日_EY']
    if AU == 0: return 0
    else: return -(be7-U).days/365*E/100*R  
    
