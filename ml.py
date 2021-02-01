# -*- coding: utf-8 -*-
# @Time    : 2020/12/9 下午8:04
# @Author  : Huting
import datetime
import pandas as pd
import random
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.svm import SVR
from sklearn.metrics import r2_score,mean_absolute_error,mean_squared_error
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import learning_curve
from sklearn.ensemble import RandomForestRegressor
import matplotlib.pyplot as plt


tenant_id_mapping = {
    "天府新区": "tianfuxinqu",
    "成华": "chenghua",
    "武侯": "wuhou",
    "金牛": "jinniu",
    "锦江": "jinjiang",
    "青羊": "qingyang",
    "高新": "gaoxin",
    "高新西": "gaoxinxi"
}
type_mapping = {
    "别墅": "bieshu",
    "商业办公类": "shangye",
    "普通住宅": "zhuzhai",
    "车库": "cheku"
}
zhuangxiu_mapping = {
    "其他":"other",
    "毛坯":"maopi",
    "简":"jianzhuang",
    "精":"jingzhuang"
}
years_mapping = {
    "暂无数据":"other",
    "满两年":"over2years",
    "满五年":"over5years"
}
other_mapping = {
    "非共有":"own",
    "共有":"shared"
}


def svr_func(kernel,X_train_svr,X_test_svr,y_train_svr):
    svr = SVR(kernel=kernel, C=1)
    svr_fit = svr.fit(X_train_svr, y_train_svr.values.ravel())
    y_predict = svr.predict(X_test_svr)
    return svr_fit,y_predict


# MSE，即均方误差
def mse_func(y_test_mse,y_pred):
    return mean_squared_error(scaler_y.inverse_transform(y_test_mse), scaler_y.inverse_transform(y_pred))


# MAE,即平均绝对误差
def mae_func(y_test_mae,y_pred):
    return mean_absolute_error(scaler_y.inverse_transform(y_test_mae), scaler_y.inverse_transform(y_pred))


# 均方根误差（RMSE）
def rmse_func(y_test_rmse,y_pred):
    return np.sqrt(mean_squared_error(scaler_y.inverse_transform(y_test_rmse), scaler_y.inverse_transform(y_pred)))


# 绘制学习曲线,X_curve 为训练集特征值,y_curve为训练集y值,estimator：实现“ fit”和“ predict”方法的对象类型
def draw_learning_curve(estimator,X_curve,y_curve):
    y_curve = y_curve.values.ravel()
    train_size, train_score, test_score = learning_curve(estimator, X_curve, y_curve, cv=10,train_sizes=np.linspace(0.1, 1.0, 5))

    train_scores_mean = np.mean(train_score, axis=1)
    train_scores_std = np.std(train_score, axis=1)
    test_scores_mean = np.mean(test_score, axis=1)
    test_scores_std = np.std(test_score, axis=1)

    plt.fill_between(train_size, train_scores_mean - train_scores_std,train_scores_mean + train_scores_std, alpha=0.1,color="r")
    plt.fill_between(train_size, test_scores_mean - test_scores_std,test_scores_mean + test_scores_std, alpha=0.1, color="g")
    plt.plot(train_size, train_scores_mean, 'o--', color="r",label="Training score")
    plt.plot(train_size, test_scores_mean, 'o-', color="g",label="Cross-validation score")

    plt.grid()
    plt.title('Learn Curve')
    plt.legend(loc="best")
    plt.show()


# 随机选取100个真实值和预测值，进行绘图比较
def draw_y_pred_test(y_tst,y_pred):
    plt.figure(figsize=(10, 7))  # 画布大小
    num = 100
    x = np.arange(1, num + 1)  # 取100个点进行比较
    num_list = np.random.randint(0,len(y_tst),size=100)
    y_tst_new = []
    y_pred_new = []
    for i in num_list:
        y_tst_new.append(y_tst.iloc[i])
        y_pred_new.append(y_pred[i])
    plt.plot(x,y_tst_new, label='target')  # 目标取值
    plt.plot(x,y_pred_new, label='predict')  # 预测取值
    plt.legend(loc='upper right')  # 线条显示位置
    plt.show()


if __name__ == "__main__":

    # 第一步，特征工程，清洗数据

    house_df = pd.read_pickle("house_df").drop_duplicates(subset=['id'])

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
    house_df['zhuangxiu'] = house_df['zhuangxiu'].map(zhuangxiu_mapping)
    house_df['show_time'] = pd.to_datetime(house_df['show_time'].str.strip('挂牌时间'))
    house_df['years'] = house_df['years'].map(years_mapping)
    house_df['other'] = house_df['other'].str.strip('房权所属')
    house_df['other'] = house_df['other'].map(other_mapping)
    house_df['deal_dt_ym'] = house_df['deal_dt'].dt.strftime('%Y%m')
    house_df['used_total_diff_price'] = house_df['used_price'] - house_df['total_price']
    house_df['build_diff'] = ((datetime.datetime.now() - house_df['build_time']) / 365.2425).dt.days

    # 处理时间类型变量
    house_df['deal_year'] = house_df['deal_dt'].dt.year
    house_df['deal_month'] = house_df['deal_dt'].dt.month
    house_df['deal_day'] = house_df['deal_dt'].dt.day
    house_df['show_year'] = house_df['show_time'].dt.year
    house_df['show_month'] = house_df['show_time'].dt.month
    house_df['show_day'] = house_df['show_time'].dt.day

    # 处理重复值
    house_ml = house_df.drop_duplicates()

    # 处理缺失值，凡有缺失值一律删除该行
    house = house_ml[(house_ml['type'] != "cheku") & (house_ml['type'] != "bieshu")].dropna()

    # 处理分类型特征：get_dummies()
    house_dummies = pd.get_dummies(house[['total_price','tenant_id','type','deal_year','deal_month','deal_day','area','class','period','change_time','introduce','follower','views','build_diff','zhuangxiu','show_year','show_month','show_day','other']], drop_first=True)

    # 划分训练集和测试集
    X = house_dummies[house_dummies.columns.difference(['total_price', 'tenant_id','type','zhuangxiu','other'])]
    y = house_dummies[['total_price']]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

    # 数据标准化
    scaler_X = StandardScaler()
    X_train_z = scaler_X.fit_transform(X_train)
    scaler_y = StandardScaler()
    y_train_z = scaler_y.fit_transform(y_train)

    # 用训练集的数据均值、方差归一化测试集，以便数据满足同分布
    X_test_z = scaler_X.fit_transform(X_test)
    y_test_z = scaler_y.fit_transform(y_test)

    # 第二步，模型训练

    # 线性回归预测
    # LR_reg = LinearRegression()
    # LR_reg.fit(X_train,y_train)
    # lr_y_pred = LR_reg.predict(X_test)
    # print('R-squared value of LinearRegression is', r2_score(y_test,lr_y_pred))  # 0.7278125173843732
    # print('the MSE of LinearRegression is', mse_func(y_test, lr_y_pred))  # 18556599.288495883
    # print('the MAE of LinearRegression is',mae_func(y_test,lr_y_pred))  # 2795.5356149250924
    # print('the RMSE of LinearRegression is', rmse_func(y_test, lr_y_pred))  # 4307.737142456104
    # draw_learning_curve(LR_reg,X_train,y_train)  # 学习曲线
    # draw_y_pred_test(y_test,lr_y_pred) # 随机绘制真实值和预测值比较

    # SVF支持向量机
    # 线性核函数 'linear',多项式核函数 'poly',径向基核函数 'rbf'
    svr_model,svr_y_predict = svr_func('linear',X_train,X_test,y_train)
    print('R-squared value of SVR is',r2_score(y_test,svr_y_predict))  # 0.7171193945799677
    print('the MSE of SVR is',mse_func(y_test,svr_y_predict))  # 19285611.486695476
    print('the MAE of SVR is',mae_func(y_test,svr_y_predict))  # 2790.3982283928603
    print('the RMSE of SVR is', rmse_func(y_test, svr_y_predict))  # 4391.538624069641
    draw_learning_curve(svr_model,X_train,y_train)
    draw_y_pred_test(y_test,svr_y_predict)

    # 随机森林
    # rf = RandomForestRegressor()
    # rf.fit(X_train, y_train.values.ravel())
    # rf_y_pred = rf.predict(X_test)
    # print('R-squared value of RandomForestRegressor is', r2_score(y_test,rf_y_pred))  # 0.839083048114967
    # print('the MSE of RandomForestRegressor is', mse_func(y_test, rf_y_pred))  # 10970641.87581887
    # print('the MAE of RandomForestRegressor is',mae_func(y_test,rf_y_pred))  # 2007.173102325804
    # print('the RMSE of RandomForestRegressor is', rmse_func(y_test, rf_y_pred))  # 3312.1959295637794
    # draw_learning_curve(rf,X_train,y_train)
    # draw_y_pred_test(y_test,rf_y_pred)








