# -*- coding: utf-8 -*-
"""
Created on Tue Jul  3 14:01:51 2018

@author: Maddox.Meng | 孟舸帆 | Meng Gefan
"""

import pandas as pd
from io import StringIO
from GDZC_module import cal1
from GDZC_module import category
from GDZC_module import category_sub
from GDZC_module import removeLineBreak
import re
import datetime

cols = ['账号', '分行', '业务代码', '利率', '起息日', '到期日', '计息标志', '计息方式代码', '浮动类型', '浮动值', 'Field21', 'Field23', '存期', '折人民币余额', '二级科目代码', '二级科目名称', '客户名称', '货币代码', '原币金额', 'Field39', '上次计息日', '维护日期']

p = r'.\吸收存款\step 1\exp_doa_det_deposit_20171231.dat'

#check line break, all 22 "|"
with open(p, 'r', encoding='gb18030', errors='ignore') as f: 
    input = StringIO( f.read().replace('"', '').replace('|+|', '|') )
    
    print ('read csv')
    df = pd.read_csv(input, sep="|", skiprows=0, names=cols, engine='python', index_col=False)
    print ('group')
    dfsum = df.groupby(['二级科目代码'])
    #group出二级科目代码的list
    sujcodes = list(set(df['二级科目代码'].tolist()))
    
    for sujcode in sujcodes:
        dff = df.copy(deep=True)
        #dff = dff.loc[dff['二级科目代码'].isin(sujcode)]
        #TypeError: only list-like objects are allowed to be passed to isin(), you passed a [int]
        #一个数字怎么变成list
        dff = dff[dff['二级科目代码'] == sujcode]
        dff.to_excel('res_%s.xlsx'%sujcode)


#dfsum.to_excel('res_sum.xlsx')