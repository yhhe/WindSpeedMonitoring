#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul  1 02:15:45 2019

@author: hyh
"""
# plot force
import matplotlib.pyplot as plt
import pandas
import numpy as np
import math

# get frequency distribution 
def frequencyDistribution(data, interval):
    maxV = (int(max(data)/interval) + 1) * interval
    minV = int(min(data)/interval) * interval
    #print(maxV, minV)
    f = np.linspace(minV,maxV,int((maxV-minV)/interval)+1)
    d = np.linspace(0,0,len(f))
    for v in data:
        d[int((v-minV)/interval)] =  d[int((v-minV)/interval)] + 1
    d = d/(interval*len(data))
    for i in range(0,len(f)):
        f[i] = f[i] + interval/2
    return [f,d]

# get the reyleigh distribution
def calStandardLine(sd,data):
    maxV = int(max(data)) + 1
    minV = int(min(data))
    f = np.linspace(minV,maxV,1001)
    d = []
    for i in range(0,len(f)):
        x = f[i]
        d.append(x/(sd**2)*math.exp(-x**2 / (2*(sd**2))))
    d = np.array(d)
    return [f,d]

# estimate the parameter of reyleigh distribution using lease square method
def appxRD(f,d,minsd, maxsd):
    sdt = np.linspace(minsd, maxsd, 300)
    mins = 10000000
    bestsd = minsd
    for sdi in sdt:
        s = 0
        for i in range(0,len(f)):
            x = f[i]
            s = s + (x/(sdi**2)*math.exp(-x**2 / (2*(sdi**2))) - d[i]) **2
        if s < mins:
            mins = s
            bestsd = sdi
    return bestsd


# plot function
def drawTimeSeries(fig, t, data ,subname=''):
    ax = fig.add_subplot(111)
    ax.plot(t,data,label=subname)
    ax.set_title('Time series '+subname)
    ax.set_xlabel('t(h)')
    ax.set_ylabel('Wind Speed(m/s)')
    ax.legend()

def drawFrequencyDistribution(fig, data,subname='', hisbins=16):
    # frequency distribution
    sd = math.sqrt(np.var(data))
    [f_1,d_1] = frequencyDistribution(data, 1)
    [f_2,d_2] = frequencyDistribution(data, 0.5)
#    [f_3,d_3] = frequencyDistribution(data, 0.25)
    [fs,ds] = calStandardLine(sd,data)
    apprSd = appxRD(f_2, d_2, sd/2, sd*3)
    [fa,da] = calStandardLine(apprSd,data)
#    print(apprSd)
#    print(apprSd / sd)
    ax = fig.add_subplot(121)
    ax.set_title('Frequency Distribution '+subname)
    #plt.scatter(f_1,d_1,label='Interval=1')
    ax.scatter(f_2,d_2,label='Interval=0.5')
    #plt.hist(v, 20)
#    plt.scatter(f_3,d_3,label='Interval=0.25')
    ax.plot(fs,ds,label='Reyleigh Distribution')
    #plt.plot(fa,da)
    ax.set_xlabel('v(m/s)')
    ax.set_ylabel('Density Distribution(point)')
    ax.legend()
    ax = fig.add_subplot(122)
    ax.set_title('Frequency Distribution '+subname)
    ax.hist(data,hisbins)
    ax.set_xlabel('v(m/s)')
    ax.set_ylabel('Density Distribution(histogram)')
    ax.legend()

def drawFrequencyRose(fig, data,subname='', dx=10):
    [f_1,d_1] = frequencyDistribution(data, dx)
    if f_1[-1] <= 360:
        f_1=np.append(f_1,f_1[0])
        d_1=np.append(d_1,d_1[0])
    else:
        f_1[-1]=f_1[0]
        d_1[-1]=d_1[0]

    ax = fig.add_subplot(121, polar=True)
    ax.plot(f_1/360*math.pi*2, d_1)
    N = 5
    ax.set_yticklabels([])

    ax = fig.add_subplot(122, polar=True)
    width = dx
    bottom = 0
    bars = ax.bar(f_1/360*math.pi*2,d_1+bottom, width=width/360*2*math.pi, bottom=bottom)
    maxd = max(d_1)
    # Use custom colors and opacity
    for r, bar in zip(d_1,bars):
        bar.set_facecolor(plt.cm.jet(r/maxd/3))
        bar.set_alpha(0.8)
    ax.set_yticklabels([])
    

tr = []
r = []

if True:
    # get data
    f = pandas.read_excel('20170420から20170426.xlsx')
   # i = 0
    #print(f.columns[0])
    #print(f[f.columns[0]])
    #drawTimeSeries(f[f.columns[0]][::30],f[f.columns[1]][::30])
 #   drawTimeSeries(f[f.columns[0]][::30],f[f.columns[2]][::30])
 #   print("mean: ", np.mean(f[f.columns[2]]))
 #   print("sd: ", np.var(f[f.columns[2]])**(1/2))
 #   drawTimeSeries(f[f.columns[0]][::30],f[f.columns[3]][::30])
 #   print("mean: ", np.mean(f[f.columns[3]]))
 #   print("sd: ", np.var(f[f.columns[3]])**(1/2))
#    drawFrequencyDistribution(f[f.columns[2]][::30])
#    drawFrequencyDistribution(f[f.columns[3]][::30])
#    drawFrequencyRose(f[f.columns[1]], 10)

#    for row in f:
#        print(f[row])
#        datas = row.split(',')
#        #print(datas)
#        tr.append(datas[0])
#        if len(datas) > 2 and not i<4 and datas[1]!='':
#            #print(datas[1])
#            r.append(float(datas[1]))
#        i = i+1
#
#    #print(v)
#    print(len(r))
#    r = r[:int(len(r)/1)]
#    # mean velocity
#    meanR = sum(r) /len(r)
#    #standard deviation
#    sd = math.sqrt(np.var(r))
#    print('sd = ', sd)   
#    drawTimeSeries(np.linspace(0,len(r)-1,len(r)),r)
#    [f, d] = frequencyDistribution(r,50)
#    c = []
#    for i in range(1,len(d)+1):
#        c.append(sum(d[:i])*50)
#    [nuA, sigmaA] = apprND(f, d, meanR*0, meanR*2, sd*0, sd*2)
#    [nf, nd, nc] = calNormalDis(r, sd, meanR)
#    [nfa, nda, nca] = calNormalDis(r, sigmaA, nuA)
#    print(sigmaA)
#    plt.subplot()
#    plt.scatter(f, d, label='Density distribution')
#    plt.plot(nf, nd, label='Normal distribution 1')
#    plt.plot(nfa, nda, label='Normal distribution 2')
#    plt.ylim( 0, 0.01)
#    plt.legend()
#    plt.show()
#    plt.subplot()
#    plt.scatter(f, c, label='Cumulative frequency')
#    plt.plot(nf, nc, label='Cumulative frequency 1')
#    plt.plot(nfa, nca, label='Cumulative frequency 2')
#    plt.legend()
#    plt.show()
#    print((meanR, sd))
#    print((nuA, sigmaA))
#    print(f)
#    print(nf)