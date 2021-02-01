# -*- coding: utf-8 -*-
# @Time    : 2020/11/24 下午4:34
# @Author  : Huting

import pandas as pd


def read_df(df):
    house_dict = {}
    with open('house', 'r') as f:
        lines = f.readlines()
        for line in lines:
            # print(line)
            house_dict = eval(line)
            df = df.append(house_dict, ignore_index=True)
    return df


if __name__ == "__main__":
    my_df = pd.DataFrame(
        columns=['id', 'domain', 'tenant_id', 'name', 'type', 'deal_dt', 'location', 'sub_location', 'area',
                 'class', 'avg_price', 'total_price', 'used_price', 'period', 'change_time', 'introduce',
                 'follower', 'views', 'build_time', 'zhuangxiu', 'show_time', 'years', 'other'])
    house_df = read_df(my_df)
    print(house_df)
    house_df.to_pickle("house_df")
