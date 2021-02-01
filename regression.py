# -*- coding: utf-8 -*-
# @Time    : 2020/12/8 下午6:36
# @Author  : Huting
import datetime
import pandas as pd
from sklearn import linear_model
import numpy as np
import statsmodels.api as sm

tenant_id_mapping = {
    # "天府新区": 1,
    # "成华": 2,
    # "武侯": 3,
    # "金牛": 4,
    # "锦江": 5,
    # "青羊": 6,
    # "高新": 7,
    # "高新西": 8
    "天府新区": 'tianfuxinqu',
    "成华": 'chenghua',
    "武侯": 'wuhou',
    "金牛": 'jinniu',
    "锦江": 'jinjiang',
    "青羊": 'qingyang',
    "高新": 'gaoxin',
    "高新西": 'gaoxinxi'
}
type_mapping = {
    # "别墅": 1,
    # "商业办公类": 2,
    # "普通住宅": 3,
    # "车库": 4
    "别墅": 'bieshu',
    "商业办公类": 'shangye',
    "普通住宅": 'zhuzhai',
    "车库": 'cheku'
}
zhuangxiu_mapping = {
    # "其他":1,
    # "毛坯":2,
    # "简":3,
    # "精":4
    "其他": 'other',
    "毛坯": 'maopi',
    "简": 'jianzhuang',
    "精": 'jingzhuang'
}


# 清洗dataframe，去除空值、无限大、无限小，在本例中未使用
def clean_dataset(df):
    assert isinstance(df, pd.DataFrame), "df needs to be a pd.DataFrame"
    df.dropna(inplace=True)  # df.dropna(axis=0 , inplace=True) #不存在的值，删除整行，默认为0
    indices_to_keep = ~df.isin([np.nan, np.inf, -np.inf]).any(1)
    return df[indices_to_keep].astype(np.float64)


if __name__ == "__main__":
    # 第一步，获取数据并清洗格式

    # 获取文件DataFrame格式数据
    house_df = pd.read_pickle("house_df").drop_duplicates(subset=['id'])  # 根据id列重复值进行删除
    # 存在重复数据，按id去重（爬取时间差导致房屋部分指标产生变动，如关注人数follower、浏览人数views）
    # 修改部分列数据格式,并转换为数字类型以便后续参与计算
    house_df['tenant_id'] = house_df['tenant_id'].map(tenant_id_mapping)
    house_df['type'] = house_df['type'].map(type_mapping)
    house_df['deal_dt'] = pd.to_datetime(house_df['deal_dt'], format='%Y/%m/%d')  # 修改为to_datetime格式
    house_df['area'] = house_df['area'].str[0].str.strip('㎡').astype(float)  # 对某列进行修改
    house_df['class'] = house_df['class'].str[0].str.strip('室').astype(float)
    house_df['avg_price'] = house_df['avg_price'].astype(float)
    house_df['total_price'] = house_df['total_price'].str.strip('万').astype(float)
    house_df['used_price'] = house_df['used_price'].str.strip('挂牌价格（万）').astype(float)
    house_df['period'] = house_df['period'].str.strip('成交周期（天）').astype(float)
    house_df['change_time'] = house_df['change_time'].str.strip('调价（次）').astype(float)
    house_df['introduce'] = house_df['introduce'].str.strip('带看（次）').astype(float)
    house_df['follower'] = house_df['follower'].str.strip('关注（人）').astype(float)
    house_df['views'] = house_df['views'].str.strip('浏览（次）').replace('暂无数据', '').apply(pd.to_numeric, errors='coerce')
    house_df['build_time'] = pd.to_datetime(house_df['build_time'].str.strip('建成年代').replace('未知', ''))
    house_df['zhuangxiu'] = house_df['zhuangxiu'].str.strip('装修情况')
    # house_df['zhuangxiu'] = house_df['zhuangxiu']
    house_df['zhuangxiu'] = house_df['zhuangxiu'].map(zhuangxiu_mapping)
    house_df['show_time'] = pd.to_datetime(house_df['show_time'].str.strip('挂牌时间'))
    house_df['other'] = house_df['other'].str.strip('房权所属')
    house_df['deal_dt_ym'] = house_df['deal_dt'].dt.strftime('%Y%m')
    house_df['used_total_diff_price'] = house_df['used_price'] - house_df['total_price']
    house_df['build_diff'] = ((datetime.datetime.now() - house_df['build_time']) / 365.2425).dt.days
    # 裁剪数据时间段和回归的数据子集，剔除车库和别墅
    house = house_df[(house_df['type'] != 'cheku') & (house_df['type'] != 'bieshu')]

    # 第二步，进行线性回归
    new_house = house[['avg_price','tenant_id', 'type', 'area', 'class', 'period', 'change_time', 'introduce', 'build_diff', 'zhuangxiu']]
    house_lr = new_house.dropna()  # 不存在的值，删除整行

    df_dummy_ref = pd.get_dummies(
        house_lr[['tenant_id', 'type', 'area', 'class', 'period', 'change_time', 'introduce', 'build_diff', 'zhuangxiu']],
        drop_first=True)

    lr = linear_model.LinearRegression()
    predicted = lr.fit(X=df_dummy_ref, y=house_lr['avg_price'])
    values = np.append(predicted.intercept_, predicted.coef_)  # 获取回归系数和截距项（常数项）
    names = np.append('intercept', df_dummy_ref.columns)  # 获取值对应名称
    results = pd.DataFrame(values, index=names, columns=['coef'])  # 把所有项放入一个带标签的DataFrame中
    print(results)
    r2 = lr.score(X=df_dummy_ref, y=house_lr['avg_price'])
    print('R-squared value is {r2}'.format(r2=r2))

    # 第三步，加入政策影响tag，2020年9月14日前成交的二手房tag=0,之后tag=1
    house['tag'] = pd.cut(house['deal_dt'],[house['deal_dt'].min(),pd.to_datetime('2020-09-14'),house['deal_dt'].max()],labels=[0,1])
    new_house_tag = house[['avg_price','tag','tenant_id', 'type', 'area', 'class', 'period', 'change_time', 'introduce', 'build_diff', 'zhuangxiu']]
    house_lr_tag = new_house_tag.dropna()  # 不存在的值，删除整行

    df_dummy_ref_tag = pd.get_dummies(
        house_lr_tag[['tag','tenant_id', 'type', 'area', 'class', 'period', 'change_time', 'introduce', 'build_diff', 'zhuangxiu']],
        drop_first=True)

    lr_tag = linear_model.LinearRegression()
    predicted_tag = lr_tag.fit(X=df_dummy_ref_tag, y=house_lr_tag['avg_price'])
    values_tag = np.append(predicted_tag.intercept_, predicted_tag.coef_)  # 获取回归系数和截距项（常数项）
    names_tag = np.append('intercept', df_dummy_ref_tag.columns)  # 获取值对应名称
    results_tag = pd.DataFrame(values_tag, index=names_tag, columns=['coef'])  # 把所有项放入一个带标签的DataFrame中
    print("增加时间前后变量-------------")
    print(results_tag)
    r2 = lr_tag.score(X=df_dummy_ref_tag, y=house_lr_tag['avg_price'])
    print('R-squared value is {r2}'.format(r2=r2))

    # 查看系数P值显著性
    X2 = sm.add_constant(df_dummy_ref_tag)
    est = sm.OLS(house_lr_tag['avg_price'], X2)
    est2 = est.fit()
    print(est2.summary())