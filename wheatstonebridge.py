#
# go to the end of this script to put your data in
#

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
    name: str  # name of the bridge for identification
    def __post_init__(self):
        self.sg = []

    @property
    def show_result(self):
        print('\n---------------------------------')
        print(f'{self.name.upper()}')
        for load_case in [1,2,3]:
            self.calculate(load_case)
            print(f'\nLoad case {load_case}:')
            print('\tStrains in microepsilon:')
            print(f'\tEps1={wb.epsilon(load_case)[0]*1e6:.3f}, Eps2={wb.epsilon(load_case)[1]*1e6:.3f}, Eps3={wb.epsilon(load_case)[2]*1e6:.3f}, Eps4={wb.epsilon(load_case)[3]*1e6:.3f}')
            print('')
            print(f'\tVoltage ratio V_OUT/V_EXC for load case {self.LC} = {self.voltage_ratio*1e3:.4f} mV/V')
        
        print('---------------------------------')
        
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
        self.LC = load_case
        self.update()
        #
        self.voltage_ratio = voltage_ratio(self.node_sg,self.dir_sg,load_case,self.gf_sg)
        return self.voltage_ratio
    
    def epsilon(self, lc):
        return calculate_sg_strains(self.node_sg, self.dir_sg, lc)
        
        
    # def plot3d(self,sglsc=1.0):
    #     self.update()
    #     cols=['node','x','y','z']
    #     df = pd.read_csv('data/nodes.lst', delim_whitespace=True, names=cols)
    #     fig = plt.figure()
    #     ax = fig.add_subplot(projection='3d')
    #     xs = df['x']*np.cos(np.radians(df['y'])) 
    #     ys = df['z']
    #     zs = df['x']*np.sin(np.radians(df['y']))
    #     ax.scatter(xs, ys, zs, marker='o')
    #     for idx, sg in enumerate(self.sg):
    #         node_sg = sg.node
    #         DF = df[df['node']==node_sg]
    #         x,y,z = DF['x'].iloc[0],DF['y'].iloc[0],DF['z'].iloc[0]
    #         xn = x * np.cos(np.radians(y))
    #         yn = z
    #         zn = x * np.sin(np.radians(y))
    #         #ax.scatter(xn,yn,zn,color='r')
    #         ax.text(xn,yn,zn,node_sg,color='r')
    #         dcx,dcy,dcz = calculate_directions(self.dir_sg, idx)
    #         dlx=sglsc/2*dcx
    #         dly=sglsc/2*dcy
    #         dlz=sglsc/2*dcz
    #         ax.plot([xn-dly,xn+dly],[yn-dlx,yn+dlx],[zn-dlz,zn+dlz],lw=2,label=f'SG_{idx+1}', color=f'C{idx+1}')
    #     ax.set_xlim(-20,20)
    #     ax.set_ylim(-20,20)
    #     ax.set_zlim(-20,20)
    #     ax.set_xlabel('Y')
    #     ax.set_ylabel('X')
    #     ax.set_zlabel('Z')
    #     ax.set_aspect('equal')
    #     ax.view_init(60,0,90)
    #     plt.legend(loc=0)
    #     plt.show()

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
 
    # FX sensor
    wb = WheatstoneBridge('FX sensor Wheatstone bridge')
    sg1 = StrainGauge(1131, 1,    0,    0, 2.01)
    sg2 = StrainGauge(1131, 0, 0.71,-0.71, 2.01)
    sg3 = StrainGauge(86325,1,    0,    0, 2.01)
    sg4 = StrainGauge(86325,0,-0.71, 0.71, 2.01)
    wb.addStrainGauge(sg1)
    wb.addStrainGauge(sg2)
    wb.addStrainGauge(sg3)
    wb.addStrainGauge(sg4)
    wb.show_result
     # FY sensor
    wb = WheatstoneBridge('FY sensor Wheatstone bridge')
    sg1 = StrainGauge(  970, 0.71, 0.71, 0, 2.01)
    sg2 = StrainGauge(  970, 0.71,-0.71, 0, 2.01)
    sg3 = StrainGauge(58035, 0.71, 0.71, 0, 2.01)
    sg4 = StrainGauge(58035, 0.71,-0.71, 0, 2.01)
    wb.addStrainGauge(sg1)
    wb.addStrainGauge(sg2)
    wb.addStrainGauge(sg3)
    wb.addStrainGauge(sg4)
    wb.show_result
    # FX sensor
    wb = WheatstoneBridge('FZ sensor Wheatstone bridge')
    sg1 = StrainGauge(   34, 0.71, 0, 0.71, 2.01)
    sg2 = StrainGauge(   34, 0.71, 0,-0.71, 2.01)
    sg3 = StrainGauge(29724, 0.71, 0, 0.71, 2.01)
    sg4 = StrainGauge(29724, 0.71, 0,-0.71, 2.01)
    wb.addStrainGauge(sg1)
    wb.addStrainGauge(sg2)
    wb.addStrainGauge(sg3)
    wb.addStrainGauge(sg4)
    wb.show_result
