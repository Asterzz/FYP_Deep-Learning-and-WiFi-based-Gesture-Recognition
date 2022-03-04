#coding=utf-8
import string
import numpy as np
import struct
import scipy
from numpy.fft import *
from scipy.fftpack import fftshift
import matplotlib.pyplot as plt


if __name__ == '__main__':


################### configuration ###################
    f=open('1.pcap' ,'rb')
    f.seek(0,0)
    res = []
    NFFT = 256

################### read pcap & parse ###################
    for j in range(281):
        # for j in range(3):
        sss = []
        for i in range(4):
            byte = f.read(1)
            if byte == '':
                break
            else:
                hexstr = "%s" % byte.hex()
                sss.append(hexstr)

        sss.reverse()
        # print(sss)
        sss[0] = '0x' + sss[0]
        sss[1] = '0x' + sss[1]
        sss[2] = '0x' + sss[2]
        sss[3] = '0x' + sss[3]
        s0 = eval(str(sss[0]))  #a1
        s1 = eval(str(sss[1]))  #b2
        s2 = eval(str(sss[2]))  #c3
        s3 = eval(str(sss[3]))  #d4
        s11 = s2 * 16*16 +s3
        s12 = s0* 16*16 +s1
        # s = int(''.join(sss))
        if s11 > 32768:
            s11 = (s11 - 65535) - 1
        if s12 > 32768:
            s12 = (s12 - 65535) - 1
        # print(s11)
        # print(s12)
        res.append([s11, s12])

    Hout = np.array(res[25:])
    cmplx = []
    for i in range(256):
        cmplx.append(Hout[i, 0]+1j*Hout[i, 1])

    # print(cmplx)                          # matlab plot function's input -----> csi
                                            # matlab csireader's csibuffer

################### plot ###################
    csi_buff = fftshift(cmplx)
    csi_phase = np.rad2deg(np.angle(csi_buff))
    csi = cmplx                             # 把plot函数中用到的csi变量单独存一下
                                            # 避免混淆,原cmplx继续保留,貌似matlab代码中直接覆盖了

    for index in range(len(csi_buff)):
        csi = np.abs(csi_buff)
    csi_buff = csi                          # 这里的csi_buff就是csi,不知道为什么matlab要再写一遍

    # print(csi_buff)

    # ax = plt.gca()
    x = [i for i in range(-128, 0, 1)]
    xx = [i for i in range(0, 128, 1)]
    x = x + xx                              # matlab中的x,我省略了nfft计算过程,反正频宽是80

    fig = plt.figure()
    fig.add_subplot(311)
    plt.plot(x, csi, color='blue', linewidth=0.5, linestyle='-')
    plt.title("csi")                        # 设置标题
    # ax.spines['right'].set_color('none')    # right边框属性设置为none 不显示
    # ax.spines['top'].set_color('none')      # top边框属性设置为none 不显示

    fig.add_subplot(312)
    plt.plot(x, csi_phase, color='blue', linewidth=0.5, linestyle='-')

    fig.add_subplot(313)
    csi_mod = np.vstack((csi, csi, csi, csi, csi, csi, csi, csi, csi, csi,
                         csi, csi, csi, csi, csi, csi, csi, csi, csi, csi,
                         csi, csi, csi, csi, csi, csi, csi, csi, csi, csi,
                         csi, csi, csi, csi, csi, csi, csi, csi, csi, csi,
                         csi, csi, csi, csi, csi, csi, csi, csi, csi, csi))
    # csi_mod = np.transpose(csi_mod)
    # ax = plt.axis(0,100,0,100)
    plt.ylim(0, 50)

    plt.imshow(csi_mod)


    plt.pause(1)
    plt.close()



    f.close()


