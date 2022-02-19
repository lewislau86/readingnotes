from time import time
import numpy as np


#input_data=[1.5,-12.3,3.2,-5.5,23.2,3.2,-1.4,-12.2,34.2,5.4,-7.8,1.1,-4.9]


#input_data = [30,44,80,-82,9,92,-11,-70,-49,96]
#input_data = [-81,84,31,21,-37,8,46,-28,3,67]
input_data = [37,-79,-31,25,98,-53,-51,-87,-87,-50]
def time_costing(func) -> object:
    def core(*args,**kwargs):
        start = time()
        ret = func(*args,**kwargs)
        #print('func :%s \ttime costing:%.16f' % (func.__name__ ,time() - start))
        return ret
    return core

'''
三层循环
将数据分为两段，两段组合就有O(n^2)的复杂度
每次循环都需要计算一次每段数据的和，所以总的复杂度是O(n^3)
'''
@time_costing
def threeloop(input_data):
    max_sum=float('-inf');
    max_list=[]
    for x in range(len(input_data)):
        for y in range(x,len(input_data)):
            seg_sum=0
            for i in input_data[x:y+1]:
                seg_sum+=i
            if seg_sum>=max_sum:
                max_sum=seg_sum
                max_list=input_data[x:y+1]
    return max_sum,max_list

'''
两层循环

'''
@time_costing
def twoloop(input_data):
    max_sum = float('-inf');
    max_list = []
    for x in range(len(input_data)):
        s_max = input_data[x]
        s_sum = input_data[x]
        s_max_list = []
        for y in range(x, len(input_data)):
            if y != x:
                s_sum += input_data[y]
            if s_sum >= s_max:
                s_max = s_sum
                s_max_list = input_data[x:y + 1]
        if s_max >= max_sum:
            max_sum = s_max
            max_list = s_max_list
    return max_sum, max_list

'''
分之算法
'''
@time_costing
def divideConquer(input_data):
    def segment(ls, le, rs, re):
        #print('ls:%d le:%d rs:%d re:%d' % (ls, le, rs, re))
        if le - ls == 1:
            l_max_sum, ls, le = input_data[ls:le][0], ls, le
        else:
            lm = (le - ls) // 2 + ls
            l_max_sum, ls, le = segment(ls, lm, lm, le)

        if re - rs == 1:
            r_max_sum, rs, re = input_data[rs:re][0], rs, re
        else:
            rm = (re - rs) // 2 + rs
            r_max_sum, rs, re = segment(rs, rm, rm, re)
        return merge(l_max_sum, ls, le, r_max_sum, rs, re)

    def merge(l_max_sum, ls, le, r_max_sum, rs, re):
        s_max_sum =0;
        ss, se = 0, re
        # 中间没有间隔
        if le==rs:
            if l_max_sum >= 0 and r_max_sum >= 0:
                s_max_sum = l_max_sum + r_max_sum
                ss, se = ls, re
            else:
                if l_max_sum > r_max_sum:
                    s_max_sum = l_max_sum
                    ss, se = ls, le
                else:
                    s_max_sum = r_max_sum
                    ss, se = rs, re
        else:
            mid_sum = 0
            for i in input_data[ls:re]:
                mid_sum += i
            if l_max_sum >= r_max_sum:
                if mid_sum >= l_max_sum:
                    s_max_sum = mid_sum
                    ss, se = ls, re
                else:
                    s_max_sum = l_max_sum
                    ss, se = ls, le
            else:
                if mid_sum >= r_max_sum:
                    s_max_sum = mid_sum
                    ss, se = ls, re
                else:
                    s_max_sum = r_max_sum
                    ss, se = rs, re
        #print('s_max_sum:%d ss:%d se:%d' % (s_max_sum, ss, se))
        return s_max_sum, ss, se
    N = len(input_data)
    M = (N // 2)
    max_sum, s, e = segment(0, M, M, N)
    return max_sum, input_data[s:e]

@time_costing
def function4(input_data):
    N = len(input_data)

    r_first = False
    r_sum = 0
    r_max = 0
    r_max_index = 0

    l_first = False
    l_sum = 0
    l_max = 0
    l_max_index = 0

    flag = False
    max_item = -1e-10
    max_item_index = 0

    for s in range(N):

        if input_data[s] >= max_item:
            max_item = input_data[s]
            max_item_index = s

            # 正向扫描
        if input_data[s] > 0 and not r_first:
            r_first = True
            flag = True
            r_sum = input_data[s]
            if r_sum >= r_max:
                r_max = r_sum
                r_max_index = s + 1

        if r_first:
            r_sum += input_data[s]
            if r_sum >= r_max:
                r_max = r_sum
                r_max_index = s + 1
            # 优化的地方，当<0时，改变起始点状态，重新累计判断
            if r_sum < 0:
                r_first = False

        # 反向扫描
        if input_data[N - s - 1] > 0 and not l_first:
            l_first = True
            l_sum = input_data[N - s - 1]
            if l_sum >= l_max:
                l_max = l_sum
                l_max_index = N - s - 1

        if l_first:
            l_sum += input_data[N - s - 1]
            if l_sum >= l_max:
                l_max = l_sum
                l_max_index = N - s - 1
            # 优化的地方，当<0时，改变起始点状态，重新累计判断
            if l_sum < 0:
                l_first = False

    if not flag:
        max_sum = max_item
        max_list = input_data[max_item_index, max_item_index + 1]
        return max_sum, max_list
    else:
        max_list = input_data[l_max_index:r_max_index]
        max_sum = 0
        for i in max_list:
            max_sum += i
        return max_sum, max_list

if __name__ == '__main__':
    count =0;
    for i in range(1, 100):
        input_data = np.random.randint(-100, 100, 10)
        max_sum1, max_list1 = threeloop(input_data)
        max_sum2, max_list2 = twoloop(input_data)
        max_sum3, max_list3 = divideConquer(input_data)
        max_sum4, max_list4 = function4(input_data)


        if max_sum1!=max_sum3:
            print(max_sum1, max_sum2, max_sum3, max_sum4)
            print(max_list1,  max_list3 )
            print(input_data)


    #    count+=1

    #print(count)

        #print('sum = %s\n******' % (max_sum ))