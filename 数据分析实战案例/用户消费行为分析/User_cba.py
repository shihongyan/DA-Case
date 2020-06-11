import pandas as pd
import matplotlib.pyplot as plt

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

    #设置title显示中文
    plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
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
    通过以上图表分析后，需要对数据进行去重（同一人每天买一点）
    :param df: 待去重数据集
    :return:
    '''
    return df.groupby('month').user_id.nunique()
if __name__=='__main__':
    month_analysis(data_base())