def isUnique(str):
    '''
    1、将字符串转化为list列表
    2、每次记录第一个位置的字母为x，在list中删除第一个位置上的x，判断剩余列表中是否存在，存在则false,反之为true
    :param str:
    :return:
    '''
    str_list=list(str)
    while(len(str_list)!=0):
       x=str_list[0]
       str_list.pop(0)
       if x in str_list:
            return False
    return True

if __name__ == '__main__':
    r = isUnique("iluhwpyk")
    print(r)