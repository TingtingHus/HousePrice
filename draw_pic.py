# -*- coding: utf-8 -*-
# @Time    : 2020/11/24 下午6:29
# @Author  : Huting
import pandas as pd
from pyecharts.charts import Line, Grid, Bar, Page
from pyecharts import options as opts
from pyecharts.globals import ThemeType
import numpy as np
from pyecharts.render import make_snapshot
from snapshot_selenium import snapshot
import datetime


# 柱状图+两条折线，双y轴
def bar1_mix_line2(x, y_bar_name, y_line1_name,y_line2_name, y_bar_value, y_line1_value, y_line2_value,title,subtitle):
    bar = (
        Bar(init_opts=opts.InitOpts(width="800px", height="400px",theme=ThemeType.LIGHT))
            .add_xaxis(xaxis_data=x)
            .add_yaxis(
                series_name=y_bar_name,
                y_axis=y_bar_value,
                label_opts=opts.LabelOpts(is_show=True),
            )
            .extend_axis(
                yaxis=opts.AxisOpts(
                    name='百分比',
                    type_="value",
                    min_=0,
                    max_=0.5,
                    interval=0.1,
                    axislabel_opts=opts.LabelOpts(formatter="{value}"),
                )
            )
            .set_global_opts(
            tooltip_opts=opts.TooltipOpts(
                is_show=True, trigger="axis", axis_pointer_type="cross"
            ),
            xaxis_opts=opts.AxisOpts(
                type_="category",
                axispointer_opts=opts.AxisPointerOpts(is_show=True, type_="shadow"),
            ),
            yaxis_opts=opts.AxisOpts(
                name=y_bar_name,
                type_="value",
                min_=0,
                max_=15,
                interval=3,
                axislabel_opts=opts.LabelOpts(formatter="{value}"),
                axistick_opts=opts.AxisTickOpts(is_show=True),
                splitline_opts=opts.SplitLineOpts(is_show=True),
            ),
            title_opts=opts.TitleOpts(title=title, subtitle=subtitle),
            legend_opts=opts.LegendOpts(pos_right="20%"),  # 图例的位置
        )
    )

    line = (
        Line()
            .add_xaxis(xaxis_data=x)
            .add_yaxis(
            series_name=y_line1_name,
            yaxis_index=1,
            y_axis=y_line1_value,
            label_opts=opts.LabelOpts(is_show=True),
            z_level=1
        )
            .add_yaxis(
            series_name=y_line2_name,
            yaxis_index=1,
            y_axis=y_line2_value,
            label_opts=opts.LabelOpts(is_show=True),
            z_level=1
        )
    )

    bar.overlap(line)
    return bar


# 单一柱状图
def bar_single(x, y_name, y_bar_value, title, subtitle):
    bar = (
        Bar(init_opts=opts.InitOpts(width='800px', height='400px'))
            .add_xaxis(x)
            .add_yaxis(y_name, y_bar_value, color="#5793f3")
            .set_global_opts(
            title_opts=opts.TitleOpts(title=title, subtitle=subtitle),
            axispointer_opts=opts.AxisPointerOpts(is_show=True, type_="shadow"),
        )
    )
    return bar


def line_two(x, y_line1_name, y2_name, y1_line_value, y2_line_value, title, subtitle):
    line = (
        Line(init_opts=opts.InitOpts(theme=ThemeType.LIGHT))
            .add_xaxis(x)
            .add_yaxis(y_line1_name, y1_line_value)
            .add_yaxis(y2_name, y2_line_value)
            .set_global_opts(title_opts=opts.TitleOpts(title=title, subtitle=subtitle))
            .set_series_opts(
            label_opts=opts.LabelOpts(is_show=True), # 显示标签
            axispointer_opts=opts.AxisPointerOpts(is_show=True, type_="shadow")
            # , markpoint_opts=opts.MarkPointOpts(data=[opts.MarkPointItem(type_="max", name="最大值")])
        )
    )
    return line


# 柱状图和折线图双Y轴,grid网格多图，index传参
def bar1_line1_with_two_axis(x, y_bar, y_line, y_bar_name, y_line_name, sub_title, index, title_left, titel_top):
    bar = (
        Bar(init_opts=opts.InitOpts(width='600px', height='300px'))
            .add_xaxis(x)
            .add_yaxis(
                y_bar_name,
                y_bar,
                xaxis_index=index,  # 需要变动的，图层中第几条X轴
                yaxis_index=index * 2,  # 需要变动的，，图层中第几条Y轴
                color="#5793f3",
            )
            .set_global_opts(
            yaxis_opts=opts.AxisOpts(
                name=y_bar_name,
                min_=0,
                max_=25000,
                position="right",
                grid_index=index,  # 需要变动的 y轴
                axisline_opts=opts.AxisLineOpts(linestyle_opts=opts.LineStyleOpts(color="#5793f3")),
                axislabel_opts=opts.LabelOpts(formatter="{value}"),
            ),
            title_opts=opts.TitleOpts(title=sub_title, pos_left=title_left, pos_top=titel_top),
            tooltip_opts=opts.TooltipOpts(trigger="axis", axis_pointer_type="cross"),
            legend_opts=opts.LegendOpts(pos_left="40%", pos_bottom="0%"),  # 图例的位置
        )
            .extend_axis(
            yaxis=opts.AxisOpts(
                type_="value",
                name=y_line_name,
                min_=0,
                max_=3,
                position="left",
                axisline_opts=opts.AxisLineOpts(linestyle_opts=opts.LineStyleOpts(color="#675bba")),
                axislabel_opts=opts.LabelOpts(formatter="{value}"),
                splitline_opts=opts.SplitLineOpts(is_show=True, linestyle_opts=opts.LineStyleOpts(opacity=1)),
            )
        )
    )
    line = (
        Line()
            .add_xaxis(x)
            .add_yaxis(
                y_line_name,
                y_line,
                xaxis_index=index,  # 需要变动的，图层中第几条X轴
                yaxis_index=index * 2 + 1,  # 需要变动的，图层中第几条Y轴
                color="#675bba",
                label_opts=opts.LabelOpts(is_show=True),
                z_level=1  # z_level将折线图置于直方图之上，控制图表的显示层级,不然会被直方图遮挡
        )
    )
    overlap = bar.overlap(line)
    return overlap


# 各区房价走势及成交价与挂牌价差值走势
def one_domain_bar_line(domain, index, title_left, title_top):
    gap = bar1_line1_with_two_axis(
        x_deal,
        house[house['tenant_id'] == domain].groupby('deal_dt_ym')['avg_price'].mean().astype(int).tolist(),
        house[house['tenant_id'] == domain].groupby('deal_dt_ym')['used_total_diff_price'].mean().round(
            decimals=2).tolist(),
        "成交价(每平米元)",
        "总价差(万元)",
        domain,
        index,
        title_left,
        title_top

    )
    return gap


if __name__ == "__main__":
    # 第一步，获取数据并清洗格式

    # 获取文件DataFrame格式数据
    house_df = pd.read_pickle("house_df").drop_duplicates(subset=['id'])  # 根据id列重复值进行删除
    # 存在重复数据，按id去重（爬取时间差导致房屋部分指标产生变动，如关注人数follower、浏览人数views）
    # house_df = house_orig.drop_duplicates(subset=['id'])  # 这样写会链式赋值的warning

    # 修改部分列数据格式,并转换为数字类型以便后续参与计算
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
    house_df['views'] = house_df['views'].str.strip('浏览（次）').replace('暂无数据', '')  # 本列含空数据''
    house_df['build_time'] = pd.to_datetime(house_df['build_time'].str.strip('建成年代').replace('未知', ''))
    house_df['zhuangxiu'] = house_df['zhuangxiu'].str.strip('装修情况')
    house_df['show_time'] = pd.to_datetime(house_df['show_time'].str.strip('挂牌时间'))
    house_df['other'] = house_df['other'].str.strip('房权所属')
    house_df['deal_dt_ym'] = house_df['deal_dt'].dt.strftime('%Y%m')
    house_df['used_total_diff_price'] = house_df['used_price'] - house_df['total_price']
    # 裁剪数据时间段，剔除车库和别墅
    # house = house_df[house_df['deal_dt'] < '2020-11-01'][house_df['deal_dt'] > '2020-05-31']  # 这样写会warning，因为前后数据类型不同
    house0 = house_df[(house_df['deal_dt'] < '2020-11-01') & (house_df['deal_dt'] > '2020-05-31')]
    house = house0[(house0['type'] != '车库') & (house0['type'] != '别墅')]
    # 提取X轴，本文主要用成交时间作为X轴
    x_deal = house.groupby('deal_dt_ym').deal_dt_ym.unique().str[0].tolist()
    # x_tenant = sorted(house['tenant_id'].unique().tolist())  # 这句和下面这句是等价的
    x_tenant_id = house.sort_values('tenant_id', ascending=False).groupby('tenant_id')['tenant_id'].unique().str[
        0].tolist()

    # 第二步，通过描述性分析展现房价现状

    # 1.各区二手房成交量（折线图堆叠，时间/数量）
    line1 = (
        Line(init_opts=opts.InitOpts(theme=ThemeType.LIGHT))
            .add_xaxis(x_deal)
            .add_yaxis("锦江", house[house['tenant_id'] == '锦江'].groupby(['deal_dt_ym']).count()['id'].tolist())
            .add_yaxis("青羊", house[house['tenant_id'] == '青羊'].groupby(['deal_dt_ym']).count()['id'].tolist())
            .add_yaxis("成华", house[house['tenant_id'] == '成华'].groupby(['deal_dt_ym']).count()['id'].tolist())
            .add_yaxis("武侯", house[house['tenant_id'] == '武侯'].groupby(['deal_dt_ym']).count()['id'].tolist())
            .add_yaxis("金牛", house[house['tenant_id'] == '金牛'].groupby(['deal_dt_ym']).count()['id'].tolist())
            .add_yaxis("高新", house[house['tenant_id'] == '高新'].groupby(['deal_dt_ym']).count()['id'].tolist())
            .add_yaxis("高新西", house[house['tenant_id'] == '高新西'].groupby(['deal_dt_ym']).count()['id'].tolist())
            .add_yaxis("天府新区", house[house['tenant_id'] == '天府新区'].groupby(['deal_dt_ym']).count()['id'].tolist())
            .set_global_opts(title_opts=opts.TitleOpts(title="各区二手房成交量", subtitle="数据截止10月底,其中青羊和成华6月份数据缺失"))
            .set_series_opts(
            label_opts=opts.LabelOpts(is_show=False)
            # ,markpoint_opts=opts.MarkPointOpts(data=[opts.MarkPointItem(type_="max", name="最大值")])
            )
    )
    # 渲染生成图片
    # line1.render("各区二手房成交量.html")
    # make_snapshot(snapshot, line1.render(), "各区二手房成交量.png")

    # 2.各区房价走势及成交价与挂牌价差值走势图（折线图堆叠，时间/房价）
    gap2_1 = one_domain_bar_line("锦江",0,"10%","0%")
    gap2_2 = one_domain_bar_line("青羊",1,"35%","0%")
    gap2_3 = one_domain_bar_line("武侯",2,"60%","0%")
    gap2_4 = one_domain_bar_line("金牛",3,"85%","0%")
    gap2_5 = one_domain_bar_line("成华",4,"10%","50%")
    gap2_6 = one_domain_bar_line("高新",5,"35%","50%")
    gap2_7 = one_domain_bar_line("天府新区",6,"60%","50%")
    gap2_8 = one_domain_bar_line("高新西",7,"85%","50%")

    # # Grid并行多图
    grid = (
        Grid(init_opts=opts.InitOpts(width="1200px", height="600px"))
        .add(gap2_1, grid_opts=opts.GridOpts(pos_left="4%", pos_right="79%", pos_bottom="60%", pos_top="10%"),is_control_axis_index=True)
        .add(gap2_2, grid_opts=opts.GridOpts(pos_left="30%", pos_right="54%", pos_bottom="60%", pos_top="10%"),is_control_axis_index=True)
        .add(gap2_3, grid_opts=opts.GridOpts(pos_left="55%", pos_right="29%", pos_bottom="60%", pos_top="10%"),is_control_axis_index=True)
        .add(gap2_4, grid_opts=opts.GridOpts(pos_left="80%", pos_right="5%", pos_bottom="60%", pos_top="10%"),is_control_axis_index=True)
        .add(gap2_5, grid_opts=opts.GridOpts(pos_left="4%", pos_right="79%", pos_top="60%"),is_control_axis_index=True)
        .add(gap2_6, grid_opts=opts.GridOpts(pos_left="30%", pos_right="54%", pos_top="60%"),is_control_axis_index=True)
        .add(gap2_7, grid_opts=opts.GridOpts(pos_left="55%", pos_right="29%", pos_top="60%"),is_control_axis_index=True)
        .add(gap2_8, grid_opts=opts.GridOpts(pos_left="80%", pos_right="5%", pos_top="60%"),is_control_axis_index=True)
        # .render("各区二手房平均成交价及挂牌价与成交价.html")
    )

    # 4.各区成交二手房平均挂牌天数图（柱状图，时间/天数）
    y_period_mean = house.sort_values('tenant_id', ascending=False).groupby('tenant_id')['period'].mean().round(decimals=2).tolist()
    bar4 = bar_single(x_tenant_id,'平均挂牌时长(天)',y_period_mean,'各区成交二手房平均挂牌天数图','')
    # bar4.render('平均挂牌时长.html')

    # 5.各区成交二手房平均调价次数及平均带看次数（折线图堆叠，时间/天数）
    y_change_time = house.sort_values('tenant_id', ascending=False).groupby('tenant_id')['change_time'].mean().round(
        decimals=2).tolist()
    y_introduce = house.sort_values('tenant_id', ascending=False).groupby('tenant_id')['introduce'].mean().round(
        decimals=2).tolist()
    line5 = line_two(x_tenant_id, '平均调价次数', '平均带看次数', y_change_time, y_introduce, '二手房平均调价次数及平均带看次数', '')
    # line5.render('平均调价次数及平均带看次数.html')

    # 3.房屋建成年限走势图（折线堆叠柱状)
    # 使用apply函数, years字段满足''关键词，则判断这一列赋值为1,否则为0
    house['5years'] = house['years'].apply(lambda x: 1 if '满五年' in x else 0)
    house['2years'] = house['years'].apply(lambda x: 1 if '满两年' in x else 0)
    y_5years_ratio = (house.groupby(['deal_dt_ym'])['5years'].mean()).round(decimals=2).tolist()
    y_2years_ratio = (house.groupby(['deal_dt_ym'])['2years'].mean()).round(decimals=2).tolist()
    house['build_diff'] = (datetime.datetime.now() - house['build_time'])/365.2425
    y_build_diff = house.groupby(['deal_dt_ym'])['build_diff'].apply(lambda g: g.mean(skipna=True)).dt.days.tolist()
    gap3 = bar1_mix_line2(x_deal,'建成年限均值','满两年占比','满五年占比',y_build_diff,y_2years_ratio,y_5years_ratio,'房屋建成年限及满2满5占比走势图','')
    # gap3.render("房屋建成年限走势图.html")


