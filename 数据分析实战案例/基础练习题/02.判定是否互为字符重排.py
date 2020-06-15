def CheckPermutation(str1,str2):
    '''
    复杂版
    :param str1:
    :param str2:
    :return:
    '''
    str2_list=list(str2)
    if len(str1)==len(str2):
        for i in range(len(str1)):
            if(str1[i] in str2_list):
                str2_list.remove(str1[i])
            else:
                return False
        return True
    else:
        return False
    '''
    简化版
    sorted()和sort()的区别
    sort()是应用在list上的方法，对已经存在的列表进行操作，无返回值
    sorted()可以对所有可迭代的对象进行排序操作，返回一个重新排序后的新列表
    :param str1:
    :param str2:
    :return:
    '''
    return sorted(str1)==sorted(str2)

if __name__ == ('__main__'):
    print(CheckPermutation("aafvr","frvaa"))