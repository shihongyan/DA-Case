import pandas as pd
import matplotlib.pyplot as plt

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

def user_behavior(df):
    '''
    用户消费行为分析
    :param df: 待分析的基础数据
    :return:
    '''
    #将用户根据用户ID分类
    group_user = df.groupby('user_id')
    #判断用户第一次消费和最后一次消费（首购/）
    group_user.month.min().value_counts()
    group_user.month.max().value_counts()
    #用户消费时间分布
    group_user.max().order_dt.value_counts().plot()
    plt.show()


if __name__=='__main__':
   df_b=data_base()
   user_behavior(df_b)