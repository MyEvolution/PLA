import random
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
    while True:

        run_times+=1
        for i in range(0, size):
            p = 0
            for x in range(0, dms - 1):
                p += para[x] * datas[i][x]
            p += para[-1]
            if p <= 0 and datas[i][-1] > 0 or p >= 0 and datas[i][-1] < 0:#ignore datas[i][-1] == 0
                err_i = i;
                break;
        if err_i != -1:
            for x in range(0, dms - 1):
                para[x] += datas[err_i][-1] * datas[err_i][x]  # update the parameters
            para[-1] += datas[err_i][-1]
            err_i = -1;
        else:break;

    return [para,run_times]
if __name__ == "__main__":
    all = random2DDatas(50)
    #plotPLA.visualizePLA(all)
    para = pla(all[1:-1])
    plotPLA.visualizePLA(all,para[0])
    print("修正次数：",para[1])





