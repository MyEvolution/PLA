import random
import re
import copy
import plotPLA
#randomly generate an array of datas
def random2DDatas(num):
    result = []
    g1 = [random.random()*20,random.random()*20]
    g2 = [random.random()*20,random.random()*20]
    # 由数据范围内的两个点来确定分割线，保证划分线一定会经过生成的点的范围
    w = [(g1[1] - g2[1])/(g1[0] -g2[0]),-1,g1[1] - (g1[1] - g2[1])/(g1[0] -g2[0])*g1[0]]

    print(w)
    result.append(w)
    for i in range(num):
        x = [random.random()*20,random.random()*20]
        y = w[0]*x[0]+w[1]*x[1]+w[2]
        if y<0:
            x.append(-1)
        elif y>0:
            x.append(1)
        else:continue
        #print(x,y)
        result.append(x)
    return result

def pla(datas):

    size = len(datas)
    if size<=1:
        return;
    err_i = -1

    dms = len(datas[0])
    if dms == 0:
        return;
    para = [0 for x in range(0,dms)]
    run_times = 0
    last_pause = size
    now = 0
    while True:
        #print(run_times)
        run_times= run_times+1
        #for i in range(0, size):
        while now != last_pause:
            p = 0

            now %= size
            for x in range(0, dms - 1):
                p += para[x] * datas[now][x]
            p += para[-1]
            if p <= 0 and datas[now][-1] > 0 or p > 0 and datas[now][-1] < 0:#ignore datas[i][-1] == 0
                #print(p,datas[i][-1])
                err_i = now
                last_pause = err_i
                if last_pause == 0:
                    last_pause = size
                now+=1
                break
            now+=1
        if err_i != -1:
            for x in range(0, dms - 1):
                para[x] += datas[err_i][-1] * datas[err_i][x]  # update the parameters
            para[-1] += datas[err_i][-1]
            err_i = -1;
        else:break;

    return [para,run_times]

def randomIndex(n):
    index = [i for i in range(0,n)]
    def swap(l,x,y):
        l[x] = l[x]+l[y]
        l[y] = l[x] - l[y]
        l[x] = l[x] - l[y]
    for i in range(0,n):
        swap(index,i,int(random.random()*n))
    return index
def plaImproved(datas,n = 1):

    size = len(datas)
    if size<=1:
        return;
    err_i = -1

    dms = len(datas[0])
    if dms == 0:
        return;
    para = [0 for x in range(0,dms)]
    run_times = 0
    index = randomIndex(size)
    last_pause = size
    i = 0
    while True:
        #if run_times>=50:
            #break
        run_times+=1

        #for i in range(0, size):
        while i != last_pause:
            p = 0
            i %= size

            for x in range(0, dms - 1):
                p += para[x] * datas[index[i]][x]
            p += para[-1]
            if p <= 0 and datas[index[i]][-1] > 0 or p > 0 and datas[index[i]][-1] < 0:#ignore datas[i][-1] == 0
                err_i = index[i]
                break;#遇到错误推出循环
            i+=1
        if err_i != -1:
            for x in range(0, dms - 1):#用这个错误来更新参数
                para[x] = para[x]+ n* datas[err_i][-1] * datas[err_i][x]  # update the parameters
            para[-1] += n * datas[err_i][-1]
            last_pause = i
            if last_pause == 0:
                last_pause = size
            i+=1
            err_i = -1;
        else:break;

    return [para,run_times]
def pocket(datas,max_time = 50,greedy = 1):

    size = len(datas)
    last_error = size
    if size<=1:
        return;
    err_i = -1

    dms = len(datas[0])
    if dms == 0:
        return;
    para = [0 for x in range(0,dms)]
    new_para = [0 for x in range(0,dms)]
    new_error = 0
    run_times = 0
    while True:
        index = randomIndex(size)
        if run_times>=max_time:
            break
        run_times+=1

        for i in range(0, size):
            p = 0
            for x in range(0, dms - 1):
                p += new_para[x] * datas[index[i]][x]
            p += new_para[-1]
            if p <= 0 and datas[index[i]][-1] > 0 or p > 0 and datas[index[i]][-1] < 0:#ignore datas[i][-1] == 0
                err_i = index[i]
                break;#遇到错误推出循环
        if err_i != -1:
            for x in range(0, dms - 1):#用这个错误来更新参数
                new_para[x] += datas[err_i][-1] * datas[err_i][x]  # update the parameters
            new_para[-1] +=  datas[err_i][-1]
            for i in range(0, size):
                p = 0
                for x in range(0, dms - 1):
                    p += new_para[x] * datas[i][x]
                p += new_para[-1]
                if p <= 0 and datas[i][-1] > 0 or p > 0 and datas[i][-1] < 0:  # ignore datas[i][-1] == 0
                    new_error+=1#出错了更新错误数目
            if(new_error<last_error):
                para =copy.deepcopy( new_para)#!!!!
                last_error = new_error
                #print(new_error)
            new_error = 0
            err_i = -1;
        else:break;
    if greedy == 0:
        return [new_para,run_times]
    else:return [para,run_times]
def readDataFrom(filename):
    result = []
    separator = re.compile('\t|\b| |\n')

    with open(filename,'r') as f:
        line = f.readline()
        #print(line)
        while line:
            temp = separator.split(line)[0:-1]
            #print(temp)
            abc = [float(x) for x in temp]
            #print(abc)
            result.append(abc)
            #print(result)
            line = f.readline()
    return result
def computeER(para,datas):
    size = len(datas)

    if size <= 1:
        return;
    dms = len(datas[0])
    if dms == 0:
        return;
    count = 0
    for i in range(0, size):
        p = 0
        for x in range(0, dms - 1):
            p += para[x] * datas[i][x]
        p += para[-1]
        #print(datas[i],i)
        if p <= 0 and datas[i][-1] > 0 or p > 0 and datas[i][-1] < 0:#ignore datas[i][-1] == 0
            count=count+1
        #print(count)
    return count/size
if __name__ == "__main__":
    '''all = random2DDatas(100)
    #plotPLA.visualizePLA(all)
    para = plaImproved(all[1:-1])
    plotPLA.visualizePLA(all,para[0])'''
    all = readDataFrom("./hw1_15_train.dat")
    print("15. 修正次数：",pla(all)[1])
    test = readDataFrom('./hw1_18_test.dat')
    para = 0
    for i in range(0,2000):
        para += plaImproved(all)[1]
    print("16. 修正次数：",para/2000)
    para = 0
    for i in range(0,2000):
        para += plaImproved(all,0.5)[1]
    print("17. 修正次数：",para/2000)
    all = readDataFrom("./hw1_18_train.dat")
    error = 0.0
    for i in range(0,2000):
        para = pocket(all)[0]
        error+=computeER(para,all)
    print("18. 平均错误率：",error/2000)

    error = 0.0

    for i in range(0,2000):
        para = pocket(all,greedy=0)[0]
        error+=computeER(para,all)
    print("19. 平均错误率：",error/2000)
    error = 0.0
    for i in range(0,2000):
        para = pocket(all,100)[0]

        error+=computeER(para,all)

    print("20. 平均错误率：",error/2000)





