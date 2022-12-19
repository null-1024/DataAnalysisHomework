import pandas as pd
import pyecharts.options as opts
from pyecharts.charts import Line, Pie, Bar, Timeline
from pyecharts.globals import ThemeType


def analysis1(df):
    """
    计算机专业方向如果想要大概率被录取，需要的各项成绩是多少
    """

    # 1. 筛选数据
    cs = df[(df['录取专业'] == '学硕-计算机科学与技术')
            | (df['录取专业'] == '学硕-软件工程')
            | (df['录取专业'] == '专硕-计算机技术')
            | (df['录取专业'] == '专硕-软件工程')]
    # print(CS)

    # 2. 获取信息
    max_score = list(cs.iloc[:, 7:14].max())
    min_score = list(cs.iloc[:, 7:14].min())
    mean_score = list(
        map(int, cs.iloc[:, 7:14].mean()))  # https://blog.csdn.net/weixin_44739213/article/details/118564022

    # 3. 可视化
    # print(CS.columns[7:14])
    (
        Line(init_opts=opts.InitOpts(theme=ThemeType.LIGHT))
        .add_xaxis(list(cs.columns[7:14]))
        .add_yaxis("max", max_score)
        .add_yaxis("min", min_score)
        .add_yaxis("mean", mean_score)
        .set_global_opts(title_opts=opts.TitleOpts(title="计算机专业方向各项成绩"))
        .render("line_base.html")
    )


def analysis2(df):
    """
    不同专业的招录人数比
    """

    # 1. 获取信息

    foo = dict(df.groupby(['录取专业']).size())
    data = [(i[0], int(i[1])) for i in foo.items()]
    # print(type(data[:2][1][1])) numpy.int64
    # print(type([('专硕-临床医学', 100), ('专硕-会计', 160)][1][1])) int
    # print(data[:2] == [('专硕-临床医学', 100), ('专硕-会计', 160)]) True

    # 2. 可视化
    (
        Pie(init_opts=opts.InitOpts(width="1600px", height="1080px"))
        .add("", data, label_line_opts=opts.PieLabelLineOpts(smooth=False))
        .set_global_opts(title_opts=opts.TitleOpts(title="不同专业的招录人数比"),
                         legend_opts=opts.LegendOpts(type_="scroll", pos_left="80%", orient="vertical"))
        .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))
        .render("pie_base.html")
    )


def analysis3(df):
    """
    录取学生的类型占比(定向和非定向、全日制和非全日制)
    """

    admission_category = df['录取类别']
    academic = df['学习方式']
    flag00 = df[(admission_category == '非定向') | (academic == '非全日制')].shape[0]
    flag01 = df[(admission_category == '非定向') | (academic == '全日制')].shape[0]
    flag10 = df[(admission_category == '定向') | (academic == '非全日制')].shape[0]
    flag11 = df[(admission_category == '定向') | (academic == '全日制')].shape[0]
    (
        Pie(init_opts=opts.InitOpts(theme=ThemeType.LIGHT))
        .add(
            "",
            [("非定向-非全日制", flag00),
             ("非定向-全日制", flag01),
             ("定向-非全日制", flag10),
             ("定向-全日制", flag11)],
            radius=["30%", "75%"],
            center=["25%", "50%"],
            rosetype="radius",
            label_opts=opts.LabelOpts(is_show=False),
        )
        .set_global_opts(title_opts=opts.TitleOpts(title="类型占比"))
        .render("pie_rosetype.html")
    )


def analysis4(df):
    tl = Timeline(init_opts=opts.InitOpts(width="1500px", height="800px"))
    for i in range(7, 14):
        data = df.groupby('录取专业')[df.columns[i]].mean().reset_index() \
            .sort_values(by=df.columns[i], ascending=False).head(20)

        bar = (
            Bar()
            .add_xaxis(list(data.iloc[:, 0]))
            .add_yaxis("top", list(data.iloc[:, 1]))
            .reversal_axis()
            .set_series_opts(label_opts=opts.LabelOpts(position="right"))
            .set_global_opts(title_opts=opts.TitleOpts(f"{df.columns[i]}"))
        )
        tl.add(bar, f"{df.columns[i]}")
    tl.render("timeline_bar.html")


def main():
    # 1. 读取数据
    file = "南京大学2022年硕士研究生统考拟录取名单.xlsx"
    df = pd.read_excel(file, sheet_name="Table 1", index_col=None)
    # print(df)

    # 2. 预处理数据
    if '备注' in df.columns:
        del df['备注']
    # print(df.shape)

    # 3. 分析并可视化展示结果
    analysis1(df)
    analysis2(df)
    analysis3(df)
    analysis4(df)


if __name__ == '__main__':
    main()
