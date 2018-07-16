# -*- coding: utf-8 -*-
"""
Created on Sat Jul  7 17:12:29 2018

@author: Maddox.Meng | 孟舸帆 | Meng Gefan

2018-07-07: 
"""

import pandas as pd
import numpy as np
from io import StringIO
from GDZC_module import cal1
from GDZC_module import category
from GDZC_module import category_sub
from GDZC_module import removeLineBreak
import re
import datetime
from XSCK_cal_module_numexpr import cal_base_01
from XSCK_cal_module_numexpr import cal_base_02
from XSCK_cal_module_numexpr import cal_base_03
from XSCK_cal_module_numexpr import cal_base_04
from XSCK_cal_module_numexpr import cal_base_05

from XSCK_cal_module_numexpr import cal_irr_00_01
from XSCK_cal_module_numexpr import cal_irr_01_03
from XSCK_cal_module_numexpr import cal_irr_03_12
from XSCK_cal_module_numexpr import cal_irr_12_60
from XSCK_cal_module_numexpr import cal_irr_60
from XSCK_cal_module_numexpr import cal_irr_sum

from XSCK_cal_module_numexpr import cal_lr_00
from XSCK_cal_module_numexpr import cal_lr_0X
from XSCK_cal_module_numexpr import cal_lr_01
from XSCK_cal_module_numexpr import cal_lr_02
from XSCK_cal_module_numexpr import cal_lr_03
from XSCK_cal_module_numexpr import cal_lr_04
from XSCK_cal_module_numexpr import cal_lr_05
from XSCK_cal_module_numexpr import cal_lr_06

from XSCK_cal_module_numexpr import cal_lrn_00
from XSCK_cal_module_numexpr import cal_lrn_0X
from XSCK_cal_module_numexpr import cal_lrn_01
from XSCK_cal_module_numexpr import cal_lrn_02
from XSCK_cal_module_numexpr import cal_lrn_03
from XSCK_cal_module_numexpr import cal_lrn_04
from XSCK_cal_module_numexpr import cal_lrn_05
from XSCK_cal_module_numexpr import cal_lrn_06
#
#from XSCK_cal_module import cal_ai_00
#from XSCK_cal_module import cal_ai_0X
#from XSCK_cal_module import cal_ai_01
#from XSCK_cal_module import cal_ai_02
#from XSCK_cal_module import cal_ai_03
#from XSCK_cal_module import cal_ai_04
#from XSCK_cal_module import cal_ai_05
#from XSCK_cal_module import cal_ai_06

from XSCK_cal_module_numexpr import int2date
from XSCK_cal_module_numexpr import int2datediff

import time
start_time = time.time()



cols = ['账号', '分行', '业务代码', '利率', '起息日', '到期日', '计息标志', '计息方式代码', '浮动类型', '浮动值', 'Field21', 'Field23', '存期', '折人民币余额', '二级科目代码', '二级科目名称', '客户名称', '货币代码', '原币金额', 'Field39', '上次计息日', '维护日期']
cols = ['账号', '分行', '业务代码', '利率', '起息日', '到期日', '计息标志', '计息方式代码', '浮动类型', '浮动值', 'Field21', 'Field23', '存期', '折人民币金额', '二级科目代码', '二级科目名称', '客户名称', '货币代码', '原币金额', 'Field39', '上次计息日', '维护日期']
cols4wp = ['二级科目代码', '账号', '分行', '业务代码', '利率', '起息日', '到期日', '计息标志', '计息方式代码', '浮动类型', '浮动值', '存期', '原币金额', '货币代码', '折人民币金额']
p = r'.\01.ClientData\exp_doa_det_deposit_20171231_tst.txt'
#p = r'.\01.ClientData\exp_doa_det_deposit_20171231.dat'
'''*********************代码表*********************'''
#=================================================================
codeTable = r'.\01.ClientData\代码表.xlsx'

dfCode01 = pd.read_excel(codeTable,'01_计息方式代码表')
dfCode02 = pd.read_excel(codeTable,'02_货币代码对应表')
dfCode03 = pd.read_excel(codeTable,'03_银行汇率表')

dfCode02 = pd.merge(dfCode02, dfCode03, how='left', on=['货币名称'])
#=================================================================

#check line break, all 22 "|"
with open(p, 'r', encoding='gb18030', errors='ignore') as f: 
    input = StringIO( f.read().replace('"', '').replace('|+|', '|') )
    
    print ('read csv')
    df = pd.read_csv(input, sep="|", skiprows=0, names=cols, engine='python', index_col=False)
    
    #选取WP需要的col, 会比手工wp多一列"二级科目代码", 以group
    df = df[cols4wp]
    # 类型转换
    df[["计息方式代码"]] = df[["计息方式代码"]].astype(str)
    dfCode01[["计息方式代码"]] = dfCode01[["计息方式代码"]].astype(str)
    
    print('left join with 计息方式代码')
    df = pd.merge(df, dfCode01, how='left', on=['计息方式代码'])
    print('left join with 货币代码')
    df = pd.merge(df, dfCode02, how='left', on=['货币代码'])

#    df['折人民币金额(测算)']  = df.apply(lambda row: cal_base_01(row['原币金额'],row['汇率']), axis=1)
#    df['diff']               = df.apply(lambda row: cal_base_02(row['折人民币金额(测算)'],row['折人民币金额']), axis=1)
#    df['起息日_EY']          = df.apply(lambda row: cal_base_03(row['起息日']), axis=1)
#    df['到期日_EY']          = df.apply(lambda row: cal_base_04(row['到期日']), axis=1)
#    df['下次付息日']          = df.apply(lambda row: cal_base_05(row['计息方式'],row['到期日_EY']), axis=1)
    
    print('calculating base')
    df['折人民币金额(测算)']  = cal_base_01(df)
    print("--- %s seconds ---" % (time.time() - start_time))
    df['diff']               = cal_base_02(df)
    print("--- %s seconds ---" % (time.time() - start_time))
    df = cal_base_03(df)
    #df['起息日2_EY'] =  int2date(df['起息日_EY'].values)#
    print("--- %s seconds ---" % (time.time() - start_time))
    df = cal_base_04(df)
    #df['到期日2_EY'] =  int2date(df['到期日_EY'])
    print("--- %s seconds ---" % (time.time() - start_time))
    df = cal_base_05(df)
    print("--- %s seconds ---" % (time.time() - start_time))
#    df['起息日_EY']          = df.apply(lambda row: cal_base_03(row), axis=1) 
#    df['到期日_EY']          = df.apply(lambda row: cal_base_04(row), axis=1)
#    df['下次付息日']         = df.apply(lambda row: cal_base_05(row), axis=1)
    
    df['datediff'] =  int2datediff(df['到期日_EY'], df['起息日_EY'])
    
    
    df['blk1'] = np.nan
    print("--- %s seconds ---" % (time.time() - start_time))
    print('calculating IR')
#    df['IR_不计息']          = df.apply(lambda row: cal_irr_00_01(row), axis=1)
#    df['IR_三个月内']        = df.apply(lambda row: cal_irr_01_03(row), axis=1)
#    df['IR_三个月至一年']     = df.apply(lambda row: cal_irr_03_12(row), axis=1)
#    df['IR_一年至五年']       = df.apply(lambda row: cal_irr_12_60(row), axis=1)
#    df['IR_五年以上']         = df.apply(lambda row: cal_irr_60(row), axis=1)  
#    df['IR_合计']            = df.apply(lambda row: c(row), axis=1) 
    df = cal_irr_00_01(df)
    print("--- %s seconds ---" % (time.time() - start_time))
    df = cal_irr_01_03(df)
    print("--- %s seconds ---" % (time.time() - start_time))
    df = cal_irr_03_12(df)
    print("--- %s seconds ---" % (time.time() - start_time))
    df = cal_irr_12_60(df)
    print("--- %s seconds ---" % (time.time() - start_time))
    df = cal_irr_60(df)
    print("--- %s seconds ---" % (time.time() - start_time))
    df['IR_合计'] = cal_irr_sum(df)
    print("--- %s seconds ---" % (time.time() - start_time))
    
    df['blk2'] = np.nan
    print('calculating LR')
#    df['LR_无期限']          = df.apply(lambda row: cal_lr_00(row), axis=1)
#    df['LR_实时偿还']        = df.apply(lambda row: cal_lr_0X(row), axis=1)
#    df['LR_一个月内']        = df.apply(lambda row: cal_lr_01(row), axis=1)
#    df['LR_一个月至三个月']   = df.apply(lambda row: cal_lr_02(row), axis=1)
#    df['LR_三个月至一年']     = df.apply(lambda row: cal_lr_03(row), axis=1)  
#    df['LR_一年至五年']       = df.apply(lambda row: cal_lr_04(row), axis=1)  
#    df['LR_五年以上']         = df.apply(lambda row: cal_lr_05(row), axis=1) 
#    df['LR_合计']            = df.apply(lambda row: cal_lr_06(row), axis=1) 
    df['LR_无期限'] = 0
    print("--- %s seconds ---" % (time.time() - start_time))
    df = cal_lr_0X(df)
    print("--- %s seconds ---" % (time.time() - start_time))
    df = cal_lr_01(df)
    print("--- %s seconds ---" % (time.time() - start_time))
    df = cal_lr_02(df)
    print("--- %s seconds ---" % (time.time() - start_time))
    df = cal_lr_03(df)
    print("--- %s seconds ---" % (time.time() - start_time))
    df = cal_lr_04(df)
    print("--- %s seconds ---" % (time.time() - start_time))
    df = cal_lr_05(df)
    print("--- %s seconds ---" % (time.time() - start_time))
    df['IR_合计'] = cal_lr_06(df)
    print("--- %s seconds ---" % (time.time() - start_time))    

    df['blk3'] = np.nan
    print('calculating LRN')
#    df['LRN_无期限']          = df.apply(lambda row: cal_lrn_00(row), axis=1)
#    df['LRN_实时偿还']        = df.apply(lambda row: cal_lrn_0X(row), axis=1)
#    df['LRN_一个月内']        = df.apply(lambda row: cal_lrn_01(row), axis=1)
#    df['LRN_一个月至三个月']   = df.apply(lambda row: cal_lrn_02(row), axis=1)
#    df['LRN_三个月至一年']     = df.apply(lambda row: cal_lrn_03(row), axis=1)  
#    df['LRN_一年至五年']       = df.apply(lambda row: cal_lrn_04(row), axis=1)  
#    df['LRN_五年以上']         = df.apply(lambda row: cal_lrn_05(row), axis=1) 
#    df['LRN_合计']            = df.apply(lambda row: cal_lrn_06(row), axis=1)
#    df['blk4'] = np.nan 
#    print('calculating AI')
#    df['AI_无期限']          = df.apply(lambda row: cal_ai_00(row), axis=1)
#    df['AI_实时偿还']        = df.apply(lambda row: cal_ai_0X(row), axis=1)
#    df['AI_一个月内']        = df.apply(lambda row: cal_ai_01(row), axis=1)
#    df['AI_一个月至三个月']   = df.apply(lambda row: cal_ai_02(row), axis=1)
#    df['AI_三个月至一年']     = df.apply(lambda row: cal_ai_03(row), axis=1)  
#    df['AI_一年至五年']       = df.apply(lambda row: cal_ai_04(row), axis=1)  
#    df['AI_五年以上']         = df.apply(lambda row: cal_ai_05(row), axis=1) 
#    df['AI_合计']            = df.apply(lambda row: cal_ai_06(row), axis=1) 
        
    #df.to_excel('xxxxx.xlsx')
    
    #group出二级科目代码的list
    sujcodes = list(set(df['二级科目代码'].tolist()))
    
    for sujcode in sujcodes:
        print('Exporting subject code:%s'%str(sujcode))
        dff = df.copy(deep=True)
        dff = dff[dff['二级科目代码'] == sujcode]
        dff.to_excel(r'.\result20180707_02\res_%s.xlsx'%sujcode, index=False)


print("--- %s seconds ---" % (time.time() - start_time))

