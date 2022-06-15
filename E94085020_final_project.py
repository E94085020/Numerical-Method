import matplotlib.pyplot as plt
import numpy as np
from deap import algorithms, creator, tools, base
from scipy.stats import bernoulli
import random

def put_in(point_x,point_y,cont,shape):
    y_end=point_y+1
    y_start=y_end-len(shape)
    for i in range(y_start,y_end):
        for j in range(point_x,point_x+len(shape[0])):
            cont[point_y+y_start-i][j]=shape[i-y_start][j-point_x]
            
def remove(cont,shape):
    for i in range(0,len(cont)):
        for j in range(0,len(cont[0])):
            if cont[i][j]==shape[0][0]:
                for a in range(i,i+len(shape)):
                    for b in range(j,j+len(shape)):
                        cont[a][b]=0
                pass
def commute(cont,shape_1,shape_2):
    finded=0
    for i in range(0,len(cont)):
        for j in range(0,len(cont[0])):
            if cont[i][j]==shape_1[0][0]:
                px_1=j
                py_1=i+len(shape_1)-1
                remove(cont,shape_1)
                finded+=1
            if cont[i][j]==shape_2[0][0]:
                px_2=j
                py_2=i+len(shape_2)-1
                remove(cont,shape_2)
                finded+=2
            if finded>=2:
                break
    put_in(px_2,py_2,container_a,shape_1)
    put_in(px_1,py_1,container_a,shape_2)
def find_skyline(cont):
    global skyline_1,x_point,y_point 
    skyline_1=[]
    x_start=0
    y_start=0
    x_end=len(cont[0])
    y_end=len(cont)
    x_point=[]
    y_point=[]
    memo='a'
    '''
    找x軸上的點
    '''
    for i in range(x_start,x_end):
        for j in range(y_start,y_end):
            if memo==cont[j][i] and memo!=0:
                break
            elif memo!=cont[j][i] and cont[j][i]!=0:
                x_point.append(i) 
                memo=cont[j][i]
                break
            elif memo!=cont[j][i] and j==y_end-1:
                x_point.append(i) 
                memo=cont[j][i]
                break
                
    x_point.append(len(cont[0]))
    '''
    找y軸上的點
    直接用x軸的點找
    '''
    for i in range(0, len(x_point)-1):
        for j in range(y_start,y_end):
            #print(x_point)
            if i==0:
                if j==y_end-1:
                    y_point.append(j)
                    skyline_1.append(skyline(x_point[i],x_point[i+1],j))
                    break
                elif cont[j+1][x_point[i]]>0:
                    y_point.append(j)
                    skyline_1.append(skyline(x_point[i],x_point[i+1],j))
                    break      
            elif j==y_end-1 and cont[j][x_point[i]]==0:
                    y_point.append(j)
                   # print('run3')
                    skyline_1.append(skyline(x_point[i],x_point[i+1],j))
            elif cont[j][x_point[i]]>0:
              #  print('run2')
                skyline_1.append(skyline(x_point[i],x_point[i+1],j-1))
                break
def ran_rect(num):
    random.seed(num)
    random.shuffle(rect_group)              
               
def find_rpoint(cont,x,y):
    if cont[y][x]==0:
        for i in range(y,len(cont)):
            if cont[j][x]>0:
                return j-1
                    
class skyline:
    def __init__(self,x1,x2,y):
        self.x1=x1
        self.x2=x2
        self.y=y
        self.L=self.x2-self.x1
def area(cont):
    global w_1,w_2,h
    for i in range(0,len(cont)):
        for j in range(0,len(cont[0])):
            if cont[i][j]>0:
                h=len(cont)-i
                break
        else:
            continue
        break            
    for j in range(0,len(cont[0])):
        for i in range(0,len(cont)):
            if cont[i][j]>0:
                w_1=j
                break
        else:
            continue
        break                
    for j in range(0,len(cont[0])):
        for i in range(0,len(cont)):
            if cont[i][len(cont[0])-1-j]>0:
                w_2=len(cont[0])-j
                break
        else:
            continue
        break   
    return (w_2-w_1)*h

global area_used_per

def rect_area(shape):
    return shape.shape[0]*shape.shape[1]
def rect_unused(group):
    sum=0
    if group==[]:
        return sum
    else:
        for i in range(0,len(group)):
            sum+=rect_area(group[i])
        return sum
def wasted_area(cont,group):
    global area_used_per
    sum_wasted=0
    a_1=area(cont)
    for i in range(len(cont)-h,len(cont)):
        for j in range(w_1,w_2):
            if cont[i][j]==0:
                sum_wasted+=1            
    area_used_per=np.round(100*(a_1-sum_wasted)/a_1,2)            
    return sum_wasted+rect_unused(group)

global w_rect,h_rect
global num_rect,rect_group,group_unused,container_a
rect_group=[]
group_unused=[]
num_rect=1

def  build_rect(h,w):    
     global num_rect,rect_group,group_unused
     rect_group.append(np.full((h,w),num_rect))
     group_unused.append(np.full((h,w),num_rect))
     num_rect+=1
def build_cont(h,w):
    global container_a,rect_group
    #rect_group.clear()
    #print("run_com")
    container_a=np.zeros((h,w))
def check_line(shape,line):
    for i in range(0,len(line)):
        #print(i)
        #print(x_point)
        if len(line)==1:
            return i
        elif i==len(line)-1:
             if line[i].L>=shape.shape[1]:
                return i
             #else i=0
        elif line[i].y>line[i+1].y and line[i].L>=shape.shape[1]:
            if line[i+1].y-line[i].y>shape.shape[0]:
                return i+1
            else: return i   
        
def sec_check(shape,line):
    global sec_line
    sec_line=[]
    memo_h=[]
    for j in range(1,len(line)-1):
        for i in range(0,len(line)-j):
            if line[i+j].x2-line[i].x1>=shape.shape[1]:
                sec_line.append(skyline(line[i].x1,line[i+1].x2,min(line[i].y,line[i+1].y)))
                memo_h.append(abs(line[i].y-line[i+1].y))
                #print('run')
                #print(sec_line[:].y)
    i=0        
    while (i<len(sec_line)):
        #print(i)
        for j in range(0,len(sec_line)):
            if i==j:
                pass
            elif sec_line[i].y<sec_line[j].y:
                sec_line.remove(sec_line[i])
                memo_h.remove(memo_h[i])
                i-=1
                #print("run")
                break
        i+=1        
        if i==len(sec_line)-1:
            break 
            #else:
    #print(memo_h)
    if memo_h==[]:
        return None,None
    else:
        num=memo_h.index(min(memo_h))
        return sec_line[num].x1,sec_line[num].y

def clean_cont():
    global group_unused,container_a
    container_a=np.zeros(container_a.shape)
    group_unused=rect_group.copy()
    
def seq_rect(rect_group):
    global group_unused,container_a
    clean_cont()
    for i in range(0,len(rect_group)):
        #print(i)
        find_skyline(container_a)
        #print(x_point)
        num_line=check_line(rect_group[i],skyline_1)
        #print(num_line)
        if num_line!=None:
            put_in(x_point[num_line],skyline_1[num_line].y,container_a,rect_group[i])
            group_unused.remove(rect_group[i])
        else :
            x,y=sec_check(rect_group[i],skyline_1)
            put_in(x,y,container_a,rect_group[i])
            group_unused.remove(rect_group[i])       



# 解码 - 二进制转换为十进制
def decode(individual):
    # 解码到10进制
    num = int(''.join([str(_) for _ in individual]), 2)
    return num
def eval(individual):
    seed_1=decode(individual)
    # 返回值: 是否满足条件, 目标函数
    ran_rect(seed_1)
    seq_rect(rect_group)
    return wasted_area(container_a,group_unused),

def run_ga():
    random.seed(42)  # 保证结果可以复现
    # 定义问题
    creator.create('FitnessMax', base.Fitness, weights=(-1.0,))  # 单目标优化，最大值问题
    creator.create('Individual', list, fitness=creator.FitnessMax)

    # 生成个体
    gene_size = 26  # 26位编码
    toolbox = base.Toolbox()
    toolbox.register('Binary', bernoulli.rvs, 0.5)
    toolbox.register('Individual', tools.initRepeat, creator.Individual, toolbox.Binary, n=gene_size)


    # 生成初始族群
    pop_size = 100  # 族群中的个体数量
    toolbox.register('Population', tools.initRepeat, list, toolbox.Individual)
    pop = toolbox.Population(n=pop_size)

    # 在工具箱中注册遗传算法需要的工具
    toolbox.register('evaluate', eval)
    toolbox.register('select', tools.selTournament, tournsize=2)  # tournsize=2的锦标赛选择,参数少k
    toolbox.register('mate', tools.cxUniform, indpb=0.5)  # 均匀交叉，参数少ind1,ind2
    toolbox.register('mutate', tools.mutFlipBit, indpb=0.5)  # 位翻转变异

    # 注册计算过程中需要记录的数据
    stats = tools.Statistics(key=lambda ind: ind.fitness.values)
    stats.register('avg', np.mean)
    stats.register('std', np.std)
    stats.register('min', np.min)
    stats.register('max', np.max)

    # 调用DEAP内置算法
    resultPop, logbook = algorithms.eaSimple(pop, toolbox, cxpb=0.5, mutpb=0.2, ngen=50, stats=stats, verbose=False)

def load(cont):
    z=15
    pt_1=np.zeros((len(cont)*z,len(cont[0])*z,3), dtype='uint8')
    for i in range(0,len(cont)):
        for j in range(0,len(cont[0])):
            for k in range(0,z):
                for y in range(0,z):
                    if cont[i][j]==0:
                        pt_1[z*i+k][z*j+y]=[255,255,255]
                    else:
                        pt_1[z*i+k][z*j+y]=[80,(200-(cont[i][j]*15)%150),((cont[i][j]*15)%105+150)]
    return pt_1

def show_rect():
    #for widget in frame3.winfo_children():
     #   widget.destroy()
    list_frame=[frame3,frame5,frame6]    
    global group_unused,img_1
    img_1=[]
    sum=0
    j=0
    k=0
    for i in range(0,len(group_unused)):
        #j=int(i/5)
        #k=int(i%5)
        sum+=group_unused[i].shape[0]
        if (sum*15)+(i*10)>=400:
            k+=1
            j=0
            sum=0
        img_1.append(ImageTk.PhotoImage(Image.fromarray(load(group_unused[i])).convert('RGB')))
        label_4= tk.Label(list_frame[k],image = img_1[i])
        label_4.grid(row=j,column=0,padx=0, pady=10)
        j+=1
     
def Packing():
    for widget in frame4.winfo_children():
        widget.destroy()    
    global container_a,img,area_used_per
    run_ga()
    img=ImageTk.PhotoImage(Image.fromarray(load(container_a)))
    label_4= tk.Label(frame4,image = img)
    label_4.grid(row=0,column=0,padx=0, pady=10)
    label_4=tk.Label(frame4,text='%s%s%s'%('面積使用率為:',area_used_per,'%'),font=('Arial',12))
    label_4.grid(row=1,column=0,padx=0, pady=10)
    show_rect()
    
def build_com():
    build_rect(int(h_r.get("1.0","end").strip()),int(w_r.get("1.0","end").strip()))
    h_r.delete('1.0','end')
    w_r.delete('1.0','end')
    show_rect()
    
def build_cont_button():
    for widget in frame4.winfo_children():
        widget.destroy()     
    global container_a,img,group_unused,rect_group,num_rect
    group_unused=rect_group.copy()
    build_cont(int(h_c.get("1.0","end").strip()),int(w_c.get("1.0","end").strip()))  
    img=ImageTk.PhotoImage(Image.fromarray(load(container_a)))
    label_4= tk.Label(frame4,image = img)
    label_4.grid(row=0,column=0,padx=0, pady=10)
    show_rect()
    
def del_all():
    for widget in frame3.winfo_children():
        widget.destroy()
    for widget in frame5.winfo_children():
        widget.destroy()
    for widget in frame6.winfo_children():
        widget.destroy()        
    global group_unused,rect_group,num_rect
    group_unused.clear()
    rect_group.clear()
    num_rect=1
    
#GUI
import tkinter as tk
from tkinter.ttk import *
from PIL import Image,ImageTk,ImageDraw 
win=tk.Tk()
win.title('2DBP')
win.geometry('800x700')
global img_1
img_1=[]
#frame
frame1 = tk.Frame(win)
frame2 = tk.Frame(win)
frame3 = tk.Frame(win)
frame4 = tk.Frame(win)
frame5 = tk.Frame(win)
frame6 = tk.Frame(win)
frame1.place(x=0, y=0)
frame1.config(height=200, width=500)
frame2.place(x=550, y=0)
frame2.config(height=200, width=300)
frame3.place(x=0, y=200)
frame3.config(height=400, width=133)
frame5.place(x=133, y=200)
frame5.config(height=400, width=133)
frame6.place(x=266, y=200)
frame6.config(height=400, width=133)
frame4.place(x=400, y=200)
frame4.config(height=400, width=400)
#label
label=tk.Label(frame1,text='輸入容器面積(長:高)',font=('Arial',12))
label.grid(row=0,column=0,padx=0, pady=10)
label_2=tk.Label(frame1,text=':',font=('Arial',22))
label_2.grid(row=0,column=2,padx=0, pady=10)
label=tk.Label(frame1,text='加入方格(長:高)',font=('Arial',12))
label.grid(row=1,column=0,padx=0, pady=10)
label_2=tk.Label(frame1,text=':',font=('Arial',22))
label_2.grid(row=1,column=2,padx=0, pady=10)


#text
w_c=tk.Text(frame1,width=10,height=2)
w_c.grid(row=0,column=1,padx=10, pady=10)
h_c=tk.Text(frame1,width=10,height=2)
h_c.grid(row=0,column=3,padx=10, pady=10)
w_r=tk.Text(frame1,width=10,height=2)
w_r.grid(row=1,column=1,padx=10, pady=10)
h_r=tk.Text(frame1,width=10,height=2)
h_r.grid(row=1,column=3,padx=10, pady=10)
button=tk.Button(frame1,text='生成/清空', font=('Arial',16), command=build_cont_button, width=10, height=1)
button.grid(row=0,column=4,padx=10, pady=10)
button=tk.Button(frame1,text='添加方塊', font=('Arial',16), command=build_com, width=10, height=1)
button.grid(row=1,column=4,padx=10, pady=10)
button=tk.Button(frame2,text='裝箱', font=('Arial',16), command=Packing, width=15, height=3)
button.grid(row=1,column=4,padx=10, pady=10)
button=tk.Button(frame1,text='刪除方塊', font=('Arial',16), command=del_all, width=10, height=1)
button.grid(row=2,column=4,padx=5, pady=10)
win.mainloop()    
