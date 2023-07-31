import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from dataclasses import dataclass



@dataclass
class StrainGauge:
    node: int    # node number where strain gauge is attached
    dir_x: float #direction of grid orientation vector - component x
    dir_y: float #direction of grid orientation vector - component y
    dir_z: float #direction of grid orientation vector - component z
    gf: float    #gauge factor
    
@dataclass
class WheatstoneBridge:
    def __post_init__(self):
        self.sg = []

    def addStrainGauge(self,sg):
        self.sg.append(sg)
        self.node_sg = np.zeros(4)
        self.gf_sg = np.zeros(4)
        self.dir_sg = np.zeros((4,3))
    
    def update(self):
        for idx, sg in enumerate(self.sg):
            self.node_sg[idx] = sg.node
            self.gf_sg[idx] = sg.gf
            self.dir_sg[idx][0] = sg.dir_x
            self.dir_sg[idx][1] = sg.dir_y
            self.dir_sg[idx][2] = sg.dir_z
      
    def calculate(self, load_case):
        self.update()
        #
        return voltage_ratio(self.node_sg,self.dir_sg,load_case,self.gf_sg)
    
    def plot3d(self,sglsc=1.0):
        self.update()
        cols=['node','x','y','z']
        df = pd.read_csv('data/nodes.lst', delim_whitespace=True, names=cols)
        fig = plt.figure()
        ax = fig.add_subplot(projection='3d')
        xs = df['x']*np.cos(np.radians(df['y'])) 
        ys = df['z']
        zs = df['x']*np.sin(np.radians(df['y']))
        ax.scatter(xs, ys, zs, marker='o')
        for idx, sg in enumerate(self.sg):
            node_sg = sg.node
            DF = df[df['node']==node_sg]
            x,y,z = DF['x'].iloc[0],DF['y'].iloc[0],DF['z'].iloc[0]
            xn = x * np.cos(np.radians(y))
            yn = z
            zn = x * np.sin(np.radians(y))
            #ax.scatter(xn,yn,zn,color='r')
            ax.text(xn,yn,zn,node_sg,color='r')
            dcx,dcy,dcz = calculate_directions(self.dir_sg, idx)
            dlx=sglsc/2*dcx
            dly=sglsc/2*dcy
            dlz=sglsc/2*dcz
            ax.plot([xn-dly,xn+dly],[yn-dlx,yn+dlx],[zn-dlz,zn+dlz],lw=2,label=f'SG_{idx+1}', color=f'C{idx+1}')
        ax.set_xlim(-20,20)
        ax.set_ylim(-20,20)
        ax.set_zlim(-10,10)
        ax.set_xlabel('Y')
        ax.set_ylabel('X')
        ax.set_zlabel('Z')
        ax.set_aspect('equal')
        ax.view_init(30, 30, 0)
        plt.legend(loc=0)
        plt.show()

def get_node_strains():
    cols=['ilc','node','eps_x','eps_y','eps_z','eps_xy','eps_yz','eps_xz']
    return pd.read_csv('data/strains.lst', delim_whitespace=True, names=cols)

def calculate_directions(dir_sg,isgr):
    nx = dir_sg[isgr][0]
    ny = dir_sg[isgr][1]
    nz = dir_sg[isgr][2]
    size_d_v=np.sqrt(nx**2+ny**2+nz**2)
    dcx=nx/size_d_v
    dcy=ny/size_d_v
    dcz=nz/size_d_v
    return dcx,dcy,dcz

def calculate_sg_strains(node_sg,dir_sg,load_case):
    epsilon= np.zeros(4)
    df = get_node_strains()
    for isgr in range(0,4):
        sg = node_sg[isgr]
        if sg!= 0:
            DF = df[(df['node']==sg)&(df['ilc']==load_case)]
            epelx=DF['eps_x'].iloc[0]
            epely=DF['eps_y'].iloc[0]
            epelz=DF['eps_z'].iloc[0]
            epelxy=DF['eps_xy'].iloc[0]
            epelyz=DF['eps_yz'].iloc[0]
            epelxz=DF['eps_xz'].iloc[0]
            dcx,dcy,dcz = calculate_directions(dir_sg,isgr)
            strain=epelx*dcx**2+epely*dcy**2+epelz*dcz**2 \
                + epelxy*dcx*dcy \
                + epelyz*dcy*dcz \
                + epelxz*dcx*dcz
            epsilon[isgr]=strain
    return epsilon

def voltage_ratio(node_sg,dir_sg,load_case,gf_sg):
    epsilon = calculate_sg_strains(node_sg,dir_sg,load_case)
    v= epsilon[0]*gf_sg[0]-epsilon[1]*gf_sg[1]+epsilon[2]*gf_sg[2]-epsilon[3]*gf_sg[3]
    return v * 0.25

if __name__ == "__main__":
 
    load_case = 1
 
    wb = WheatstoneBridge()
    
    sg1 = StrainGauge(1,1,0,0,2.01)
    wb.addStrainGauge(sg1)
    
    VR = wb.calculate(load_case) # voltage ratio
    
    print(f'Voltage ratio V_OUT/V_EXC for load case {load_case}={VR*1e3:.4f}mV/V')
    
    wb.plot3d()
