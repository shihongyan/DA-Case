def replaceSpaces(S,length):
    '''
    复杂版
    :param S:
    :param length:
    :return:
    '''
    # s=list(S)
    # for i in range(length):
    #     if s[i]==' ':
    #         s[i]='%20'
    # return ''.join(s).strip(' ')
    '''
    简化版
    '''
    return S[:length].replace(' ','%20')

if __name__==('__main__'):
    print(replaceSpaces("Mr John Smith    ",13))