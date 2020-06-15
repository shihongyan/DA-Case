import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

#设置title显示中文
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']

def data_base():
    '''
    准备初始数据
    :return:df数据
    '''

    '''
    ⭐sep中的'\s+'表示匹配任意空白符
    user_id:用户id
    order_dt:购买日期
    order_products:购买产品数
    order_amount:购买金额
    '''
    columns = ['user_id','order_dt','order_products','order_amount']
    df = pd.read_table("CDNOW_master.txt",names=columns,sep = '\s+')

    #显示前5行数据
    #df.head()
    #查看数据类型，有哪些异常值需要处理
    #df.info()

    #数据类型转化
    df['order_dt'] = pd.to_datetime(df.order_dt,format = '%Y%m%d')
    #分离出月份
    df['month'] = df.order_dt.values.astype('datetime64[M]')
    return df

def month_analysis(df):
    '''
    分析并绘制图表消费趋势，每月的消费总金额，消费次数，产品购买数量，消费人数
    :param df: 清洗好的数据集
    :return:
    '''

    #计算每月消费总金额
    grouped_month = df.groupby('month')
    order_month_amount = grouped_month.order_amount.sum()

    #绘制折线图,显示每月的消费趋势
    plt.plot(order_month_amount)
    plt.title('每月消费总金额')
    plt.show()

    #统计每月的消费次数
    consumpation_sum=grouped_month.user_id.count()
    plt.plot(consumpation_sum)
    plt.title('每月消费总次数')
    plt.show()

    # 统计每月产品的购买数量
    products_sum = grouped_month.order_products.sum()
    plt.plot(products_sum)
    plt.title('每月产品购买数量')
    plt.show()

def drop_duplicates(df):
    '''
    通过以上图表分析后，需要对数据进行去重（同一人每天买一点.user_id重复，需统计消费人数对比）
    :param df: 待去重数据集
    :return:用户数据去重后的数据集
    '''
    df1=df.groupby('month').user_id.nunique()
    plt.plot(df1)
    plt.title("去重后消费人数")
    plt.show()

def pivot_table(df):
    '''
    以上两个函数均是绘制折线统计图，消费趋势也可以通过数据透视表分析
    :param df: 待分析数据集
    :return:
    '''
    return df.pivot_table(index='month',
                   values=['order_products','order_amount','user_id'],
                   aggfunc={'order_products':'sum','order_amount':'sum','user_id':'count'})

def user_analysis(df):
    '''
    用户个体消费数据分析
    用户消费金额与消费次数的描述统计，散点图
    用户消费金额的分布图（二八法则）
    用户消费次数的分布图
    用户累计消费金额的占比
    :param df: 待分析数据
    :return:
    '''

    #用户消费金额的描述统计
    group_user = df.groupby('user_id')
    print(group_user.sum().describe())

    #用户消费的散点图
    group_r=group_user.sum().query('order_amount<4000')
    group_r.plot.scatter(x = 'order_amount' , y = 'order_products')
    plt.title("用户消费散点图")
    plt.show()

    #用户消费金额的分布图（二八法则）
    group_user.sum().order_amount.plot.hist(bins=20)
    plt.title('用户消费金额分布图')
    plt.show()

    #用户消费次数的分布图（二八准则）
    group_user.sum().query('order_products < 80').order_products.hist(bins = 40)
    plt.title('用户消费次数分布图')
    plt.show()

    #用户累计消费金额占比（百分之多少的用户占了百分之多少的消费额）
    '''
    axis = 0按列计算
    cumsum滚动累计求和
    sort_values 排序，升序
    '''
    user_cumsum = group_user.sum().sort_values('order_amount').apply(lambda x:x.cumsum() / x.sum())
    #user_cumsum.reset_index()在输出表格中加上index索引
    print(user_cumsum)
    user_cumsum.reset_index().order_amount.plot()
    plt.title('用户累计消费金额占比')
    plt.show()

def user_behavior1(df):
    '''
    用户消费行为分析:主要根据用户消费时间进行分析
    :param df: 待分析的基础数据
    :return:
    '''
    #将用户根据用户ID分类
    group_user = df.groupby('user_id')
    #判断用户第一次消费和最后一次消费（首购/）
    first_cus=group_user.month.min().value_counts()
    print(first_cus)
    group_user.month.max().value_counts()
    #用户消费时间分布
    group_user.max().order_dt.value_counts().plot()
    plt.show()
    #客户消费开始时间与截至时间
    user_life = group_user.order_dt.agg(['min','max'])
    print(user_life.head())
    #用户的购买周期
    cycle = (user_life['min'] == user_life['max']).value_counts()
    print(cycle)
def user_behavior2(df):
    '''
    对用户行为进行更深层次的分析
    :param df:
    :return:返回统计用户消费金额，购买数量，消费时间等信息的数据集
    '''
    #统计每个用户消费的总金额，购买产品数，最后一次的消费时间
    user_bht2 = df.pivot_table(index = 'user_id',
                         values = ['order_products','order_amount','order_dt'],
                         aggfunc = {'order_products':'sum','order_amount':'sum','order_dt':'max'})
    print(user_bht2)
    # -(user_bht2.order_dt - user_bht2.order_dt.max())结果为时间类型，将时间格式转化为整数或者浮点数的形式，可以除以单位‘D’，也可以用astype转化
    user_bht2['D'] =-(user_bht2.order_dt - user_bht2.order_dt.max()) / np.timedelta64(1,'D')
    user_bht2.rename(columns={'order_products':'P','order_amount':'A'},inplace=True)
    print(user_bht2.head())
    return user_bht2

def RFM_func(user_bh2):
    level = user_bh2.apply(lambda user_bh2 : '1' if user_bh2 >=0 else '0')
    label = level.D + level.P + level.A
    d = {
        '000':'一般发展客户',
        '001':'重要发展客户',
        '010':'一般保持客户',
        '011':'重要保持客户',
        '100':'一般挽留客户',
        '101':'重要挽留客户',
        '110':'一般价值客户',
        '111':'重点价值客户'
    }
    result = d[label]
    return result

def RFM_show():
    '''
    将用户分类后统计
    :return:
    '''
    df_b = data_base()
    user_bh2 = user_behavior2(df_b)
    #区分每个用户的类型：一般....？重要...？
    user_bh2['label'] = user_bh2[['D', 'P', 'A']].apply(lambda x: x - x.mean()).apply(RFM_func, axis=1)
    print(user_bh2)
    #不同类型的客户产生的消费金额和购买商品数统计
    user_bh3 =user_bh2.groupby('label').sum()
    print(user_bh3)
    #统计不同类型客户的数量
    user_bh4 = user_bh2.groupby('label').count()
    #print(user_bh4)

    #用户生命周期
    pivoted_counts = df_b.pivot_table(index='user_id',
                                      columns='month',
                                      values='order_dt',
                                      aggfunc='count').fillna(0)
    #print(pivoted_counts.head())
    df_purchase = pivoted_counts.applymap(lambda x: 1 if x > 0 else 0)
    print(df_purchase.tail())

if __name__=='__main__':
  RFM_show()