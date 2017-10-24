# -*- coding: utf-8 -*-
import re
import os
import pcbnew
import PcbNetList as netlist


#今実行しているディレクトリ名を取得
pcb = pcbnew.GetBoard()
pcb_file = pcb.GetFileName()
pcb_dir = os.path.dirname(pcb_file)
#pcb_name =  os.path.basename(pcb_file)
#print("Dir:{0:s}   Name:{1:s}\n").format(pcb_dir, pcb_name)

#作業ディレクトリを記憶
now_dir = os.getcwd() 
#作業ディレクトリを今実行しているディレクトリへ移動
os.chdir(pcb_dir)



#KiCADネットリストを読み込む
net = netlist.Kicad_Read(pcb_file.replace('.kicad_pcb','.net'))

##Calayネットリストを出力する
#netlist.Calay_Write(net)
##CR-500ネットリストを出力する
#netlist.CCF_Write(net)
##DK-Σネットリストを出力する
#netlist.DKS_Write(net)
##MM-2ネットリストを出力する
#netlist.MM2_Write(net)
##Telesisネットリストを出力する
#netlist.Telesis_Write(net)
#PADSネットリストを出力する
netlist.PADS_Write(net)
##Intergraphネットリストを出力する
#netlist.Intergra_Write(net)



#作業ディレクトリを元に戻す
os.chdir(now_dir)

