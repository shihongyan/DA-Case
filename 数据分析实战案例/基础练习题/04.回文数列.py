import collections

def canPermutePalindrome(s):
    '''
    统计字符串中每个字符的个数，如果有奇数字符>2，或者奇数=1，但是字符串长度为偶数，都不是
    :param s:
    :return: 返回判断结果
    '''
    s = [i for i in s]
    dicts = collections.Counter(s)
    odd = 0
    for i in dicts:
        if dicts[i] % 2 == 1:
            odd += 1
    if odd >= 2 or (odd == 1 and len(s) % 2 == 0):
        return False
    return True
if __name__=='__main__':
    print(canPermutePalindrome('hufheibfowbf'))