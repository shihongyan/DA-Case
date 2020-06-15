def rotate(matrix):
    '''
    先上下倒序，再对角调换
    :param matrix:
    :return:
    '''
    length = len(matrix)
    # 先在纵向上进行上下翻转
    # 切片会创建新的对象进而开辟新地址
    matrix[:] = matrix[::-1]
    # 然后沿对角线翻转
    for i in range(length):
        for j in range(i):
            matrix[j][i], matrix[i][j] = matrix[i][j], matrix[j][i]

if __name__=='__main__':
   x =[ [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]]
   rotate(x)
   print(x)