import numpy as np
import matplotlib.pyplot as plt

def visualizePLA(all,w = []):
    x = np.linspace(0,20,50)  # 在1到10之间产生50组数据(数据之间呈等差数列)
    y = - all[0][2]/all[0][1]  - all[0][0]/all[0][1]*x

    plt.figure()
    plt.plot(x,y)
    if len(w)!=0:
        z = - w[2] / w[1] - w[0] / w[1] * x
        plt.plot(x,z,color="red",linestyle="--")
    posx = []
    posy = []
    negx = []
    negy = []
    for i in  range(1,len(all)):
        if all[i][-1] == -1:
            negx.append(all[i][0])
            negy.append(all[i][1])
        else:
            posx.append(all[i][0])
            posy.append(all[i][1])
    plt.scatter(negx,negy,marker='x',c='r')
    plt.scatter(posx,posy,marker='o',c='g')
    plt.show()

