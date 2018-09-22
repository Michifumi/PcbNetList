# -*- coding: utf-8 -*-
import re

def File_NetOut(f, netno, name, net, total) :
    for i, w in enumerate(net) :
        if i > 0 :
            f.write(', ')
        if (i // 8) > 0 and (i % 8) == 0 :
            f.write('\n')
        f.write(w)
    f.write('\n')
    str = "#####  NET No.{0:6d},   Name:{1:10s},   Parts:{2:6d},   Total:{3:8d}    #####\n".format(netno, name, len(net), total)
    f.write(str)



#************************************************************************************************************************************************
#/TEC      R015(2) C411(2) C308(1) T14(1);
#/S5V      R328(2) C325(2) J3(22) C326(2) R325(2) R323(2) R011(1) C006(2),
#          Q001(2);
#/A5VL     C328(1) C306(2) U301(106) U301(41) U301(70) U301(55) U301(128) C302(2),
#          U301(18) C310(1) C021(1) U301(29) C309(1) U301(107) U301(99) U301(144),
#          U301(113) U301(145) C305(1) U301(81) U301(114) U301(92) C301(1) U301(3),
#          SHORT7(2);
#/RFI      C332(2) U309(2) U301(91);
#
# FORMAT : Calay
def Calay_Read(rfname, wfname = 'NET.TXT') :

    f = open(wfname, 'w')

    netname = []; netlist = []; net = []
    name = ''; n = 0; t = 0
    for line in open(rfname, 'r'):
        f.write(line)
        line = line.replace('\n', '')       #改行削除
        line = line.replace('\r', '')       #改行削除
        #print(line)
        words = re.split(" +", line)        #１行をスペースで分離
        #print(words)
        if n == 0 :                         #ネット名前を記憶
            name = words[0].strip()

        if len(words) > 0 :                 #ネットが存在する時        
            w = words[-1]
            if w == '' :
                EOF = 1
            elif w[-1] == ';' :             #最後の文字が';'の時
                words[-1] = w[:-1]          #';'削除の上、再登録
                for w in words[1:] :        #ネットを記憶
                    w = w.strip()
                    if len(w) > 0 :
                        net.append(w)
                EOF = 1
                #print(name)
                #print(net)
                #print()
            elif w[-1] == ',' :             #最後の文字が','の時
                words[-1] = w[:-1]          #','削除の上、再登録
                for w in words[1:] :	    #ネットを記憶
                    w = w.strip()
                    if len(w) > 0 :
                        net.append(w)
                EOF = 0
            else :
                EOF = 1
        else :
            EOF = 1

        
        if EOF == 1 :
            if name != '' and len(net) > 0 : 
                net.sort()                  #ネットリストの並べ替え
                netname.append(name)
                netlist.append(net)

                t += len(net)
                File_NetOut(f, len(netname), name, net, t)

            net = []; name = ''
            n = 0
        else :
            n += 1

    f.close()
    return (netname, netlist, rfname)

#net1 = Calay_Read('01_calay.net', 'NET1.TXT')
#print(net1[0])            
#print(net1[1])


def Calay_Write(netlist, wfname = 'calay.net') :

    f = open(wfname, 'w')

    name_n = len(netlist[0]); name_n -= 1
    
    for i, (name, net) in enumerate(zip(netlist[0], netlist[1])) :

        net_n = len(net); net_n -= 1
        
        str = '{0:20s}\t'.format(name)
        f.write(str)

        for j, w in enumerate(net) :
            str = '{0:s}'.format(w)
            f.write(str)
            if j >= net_n :
                f.write(";\n")
            elif (j % 8) == 7 :
                f.write(",\n                    \t")
            else :
                f.write(" ")          
           
    f.close()


#Calay_Write(net, 'calay.net')



#************************************************************************************************************************************************
#N220027: U303(21),R371(1),C108(1),R373(1);
#N220028: R373(2),U302(26);
#N220029: U303(20),R370(1);
#SA5V:    R011(2),U401(8),C121(2),U310(5),C412(1),R320(2);
#A5V:     C110(2),U309(5),C324(2),U302(6),C315(1),R012(2),
#         C005(1),R003(1),L001(1),Q001(3);
#S5V:     R328(2),C325(2),C326(2),J3(22),R011(1),Q001(2),C006(2),
#         R323(2),R325(2);
#
# FORMAT : CR-3000, CR-5000PWS, CR-8000(CCF)
def CCF_Read(rfname, wfname = 'NET.TXT') :

    f = open(wfname, 'w')

    netname = []; netlist = []; net = []
    name = ''; n = 0; t = 0
    for line in open(rfname, 'r'):
        f.write(line)
        line = line.replace('\n', '')       #改行削除
        line = line.replace('\r', '')       #改行削除
        #print(line)

        if n == 0 :                         #ネット名前を記憶
            words = line.split(':', 1)
            name = words[0].strip()
            if len(words) > 1 :
                words = (words[1].strip()).split(',')
            else :
                words = []
        else :
            words = (line.strip()).split(',')
        #print(words)           

        if len(words) > 0 :                 #ネットが存在する時
            w = words[-1].strip() 
            if w == '' :                    #最後が''の時
                del words[-1]               #''削除
                for w in words :            #ネットを記憶
                    net.append(w.strip())
                EOF = 0
            elif w[-1] == ';' :             #最後の文字が';'の時
                words[-1] = w[:-1]          #';'削除の上、再登録
                for w in words :            #ネットを記憶
                    w = w.strip()
                    if len(w) > 0 :
                        net.append(w)
                EOF = 1
                #print(name)
                #print(net)
                #print()
            else :
                EOF = 1
        else :
            EOF = 1

        
        if EOF == 1 :
            if name != '' and len(net) > 0 : 
                net.sort()                  #ネットリストの並べ替え
                netname.append(name)
                netlist.append(net)

                t += len(net)
                File_NetOut(f, len(netname), name, net, t)

            net = []; name = ''
            n = 0
        else :
            n += 1

    f.close()
    return (netname, netlist, rfname)


#net2 = CCF_Read('02_ccf.ccf', 'NET2.TXT')
#print(net2[0])            
#print(net2[1])


def CCF_Write(netlist, wfname = 'ccf.net') :

    f = open(wfname, 'w')

    name_n = len(netlist[0]); name_n -= 1
    
    for i, (name, net) in enumerate(zip(netlist[0], netlist[1])) :

        net_n = len(net); net_n -= 1
        
        str = '{0:20s}'.format(name + ":")
        f.write(str)

        for j, w in enumerate(net) :
            str = '{0:s}'.format(w)
            f.write(str)
            if j >= net_n :
                f.write(";\n")
            elif (j % 8) == 7 :
                f.write(",\n                    ")
            else :
                f.write(",")
                       
    f.close()


#CCF_Write(net, 'ccf.net')



#************************************************************************************************************************************************
#1273		[RA21-7,T80-1,U201-97]
#1274		[RA21-6,T81-1,U201-94]
#A3.3V		[C006-2,C302-2,C306-2,C340-2,C341-2,C342-2,R011-1,
#		 T23-1,U301-72,U301-76,U301-85,U301-97,U301-102,
#		 U301-104]
#A5V		[C005-1,C021-1,C110-2,C315-1,C324-2,C325-2,C327-1,
#		 C328-1,C413-1,L002-1,Q001-3,R003-2,R328-2,T82-1,U302-6,
#		 U302-37,U309-5,U318-5]
#
# FORMAT : DK-Σ
def DKS_Read(rfname, wfname = 'NET.TXT') :

    f = open(wfname, 'w')

    netname = []; netlist = []; net = []
    name = ''; n = 0; t = 0
    for line in open(rfname, 'r'):
        f.write(line)
        line = line.replace('\n', '')       #改行削除
        line = line.replace('\r', '')       #改行削除
        #print(line)

        if n == 0 :                         #ネット名前を記憶
            words = line.split('[', 1)
            name = words[0].strip()
            if len(words) > 1 :
                words = (words[1].strip()).split(',')
            else :
                words = []
        else :
            words = (line.strip()).split(',')
        #print(words)           

        if len(words) > 0 :                 #ネットが存在する時
            w = words[-1].strip() 
            if w == '' :                    #最後が''の時
                del words[-1]               #''削除
                for w in words :            #ネットを記憶
                    w = w.strip()
                    if len(w) > 0 :
                	w = w.replace('-', '(', 1) + ')'                   
                        net.append(w)
                EOF = 0
            elif w[-1] == ']' :             #最後の文字が']'の時
                words[-1] = w[:-1]          #']'削除の上、再登録
                for w in words :            #ネットを記憶
                    w = w.strip()                   
                    if len(w) > 0 :
                	w = w.replace('-', '(', 1) + ')'                   
                        net.append(w)
                EOF = 1
                #print(name)
                #print(net)
                #print()
            else :
                EOF = 1
        else :
            EOF = 1

        
        if EOF == 1 :
            if name != '' and len(net) > 0 : 
                net.sort()                  #ネットリストの並べ替え
                netname.append(name)
                netlist.append(net)

                t += len(net)
                File_NetOut(f, len(netname), name, net, t)

            net = []; name = ''
            n = 0
        else :
            n += 1

    f.close()
    return (netname, netlist, rfname)

#net = DKS_Read('03_dks.net', 'NET.TXT')
#print(net[0])            
#print(net[1])


def DKS_Write(netlist, wfname = 'dks.net') :

    f = open(wfname, 'w')

    name_n = len(netlist[0]); name_n -= 1
    
    for i, (name, net) in enumerate(zip(netlist[0], netlist[1])) :

        net_n = len(net); net_n -= 1
        
        str = '{0:20s}['.format(name)
        f.write(str)

        for j, w in enumerate(net) :
            str = '{0:s}'.format((w.replace('(', '-', 1)).rstrip(')') )
            f.write(str)
            if j >= net_n :
                f.write("]\n")
            elif (j % 8) == 7 :
                f.write(",\n                    ")
            else :
                f.write(",")
                       
    f.close()


#DKS_Write(net, 'dks.net')



#************************************************************************************************************************************************
#$NET
#DCIN            ; U101-2, U102-2, U102-3, U103-2, C104-2, C105-2, C106-1,
#                  C108-1, C109-1, C113-1, D105-4, FL101-1, FL101-4, P101-1,
#                  R240-1, R252-2
#VINUPS          ; D105-1, SHORT2-1
#                ; U1-2, U2-1, C1-1, C10-1, C11-2, R11-2
#                ; U1-3, C9-2, R5-2
#                ; U1-5, R3-1, R4-2
#VOUTUPS         ; D105-3, FL103-2, R217-2, SHORT3-1
#$END
#$THM
#$VDD1            ; U4-14, C106-1, C108-1, C113-1, C16-1, FL101-1, FL101-4,
#$                  J101-44B, J101-59A, J3-1, SHORT1-2, SHORT2-1, SHORT3-1
#$END
#
# FORMAT : MM-2
def MM2_Read(rfname, wfname = 'NET.TXT') :

    f = open(wfname, 'w')

    netname = []; netlist = []; net = []
    name = ''; n = 0; t = 0
    for line in open(rfname, 'r'):
        f.write(line)
        line = line.replace('\n', '')       #改行削除
        line = line.replace('\r', '')       #改行削除
        #print(line)

        if n == 0 :                         #ネット名前を記憶
            words = line.split(';', 1)
            name = words[0].strip()
            if name == '' :                 #ネット名前が無い時に'@NET'で始まる名前を自動生成
                name = "@NET{0}".format(len(netname) + 1)
            if len(words) > 1 :
                words = (words[1].strip()).split(',')
            else :
                words = []
        else :                              #前のネットの続き
            if line[0] == '$' :             #'$'で始まる場合、'$'を削除
                line = line[1:]
            words = (line.strip()).split(',')
        #print(words)           
 
        if len(words) > 0 :                 #ネットが存在する時
            w = words[-1] 
            if w == '' :                    #最後が','の時
                del words[-1]               #''削除
                for w in words :            #ネットを記憶
                    w = w.strip()                   
                    if len(w) > 0 :
                	w = w.replace('-', '(', 1) + ')'                   
                        net.append(w)
                EOF = 0
            else :
                for w in words :            #ネットを記憶
                    w = w.strip()                   
                    if len(w) > 0 :
                	w = w.replace('-', '(', 1) + ')'                   
                        net.append(w)
                EOF = 1
                #print(name)
                #print(net)
                #print()
        else :
            EOF = 1

        
        if EOF == 1 :
            if name != '' and len(net) > 0 : 
                net.sort()                  #ネットリストの並べ替え
                netname.append(name)
                netlist.append(net)

                t += len(net)
                File_NetOut(f, len(netname), name, net, t)

            net = []; name = ''
            n = 0
        else :
            n += 1

    f.close()
    return (netname, netlist, rfname)


#net = MM2_Read('04_mm2.net', 'NET.TXT')
#print(net[0])            
#print(net[1])


def MM2_Write(netlist, wfname = 'mm2.net') :

    f = open(wfname, 'w')

    name_n = len(netlist[0]); name_n -= 1

    f.write("$NET\n")   
    for i, (name, net) in enumerate(zip(netlist[0], netlist[1])) :

        net_n = len(net); net_n -= 1
        
        str = '{0:20s}; '.format(name)
        f.write(str)

        for j, w in enumerate(net) :
            str = '{0:s}'.format((w.replace('(', '-', 1)).rstrip(')') )
            f.write(str)
            if j >= net_n :
                f.write("\n")
            elif (j % 8) == 7 :
                f.write(",\n                      ")
            else :
                f.write(", ")

    f.write("$END\n")                      
    f.close()


#MM2_Write(net, 'mm2.net')



#************************************************************************************************************************************************
#$NETS
#LED_RED;  U2.13 Q1.3 R21.2
#N17282026;  C40.2 C39.2 C41.2 C38.2,
#     C37.2 CN3.30 CN3.14 CN3.29,
#     R34.1 C95.1 Q4.3 C96.1,
#     R33.2
#LED_BLUE;  U2.15 R46.2 Q9.2
#N17707156;  CN3.4 U14.C1
#N17706349;  CN3.10 U14.H1
#A19;  U5.H1 U1.C3 U2.66
#$END
#
# FORMAT : Telesis
def Telesis_Read(rfname, wfname = 'NET.TXT') :

    f = open(wfname, 'w')

    netname = []; netlist = []; net = []
    name = ''; n = 0; t = 0; lock = 0
    for line in open(rfname, 'r'):
        f.write(line)
        line = line.replace('\n', '')       #改行削除
        line = line.replace('\r', '')       #改行削除
        #print(line)

        if lock == 0 :                      #読み飛ばし処理
            if line[0:4] == '$NET' :
                lock = 1
            continue

        if n == 0 :                         #ネット名前を記憶
            words = line.split(';', 1)
            name = words[0].strip()
            if name == '' :                 #ネット名前が無い時に'@NET'で始まる名前を自動生成
                name = "@NET{0}".format(len(netname) + 1)
            if len(words) > 1 :
                words = re.split(" +", words[1].strip())      #１行をスペースで分離
            else :
                words = []
        else :                              #前のネットの続き
           words = re.split(" +", line.strip())      #１行をスペースで分離
        #print(words)           
 
        if len(words) > 0 :                 #ネットが存在する時
            w = words[-1] 
            if w[-1] == ',' :               #最後の文字が','の時
                words[-1] = w[:-1]          #','削除の上、再登録
                for w in words :            #ネットを記憶
                    w = w.strip()
                    if len(w) > 0 :
                        w = w.replace('.', '(', 1) + ')'                   
                        net.append(w)
                EOF = 0
            else :
                for w in words :            #ネットを記憶
                    w = (w.strip()).replace('.', '(', 1) + ')'                   
                    net.append(w)
                EOF = 1
                #print(name)
                #print(net)
                #print()
        else :
            EOF = 1

        
        if EOF == 1 :
            if name != '' and len(net) > 0 : 
                net.sort()                  #ネットリストの並べ替え
                netname.append(name)
                netlist.append(net)

                t += len(net)
                File_NetOut(f, len(netname), name, net, t)

            net = []; name = ''
            n = 0
        else :
            n += 1

    f.close()
    return (netname, netlist, rfname)

#net = Telesis_Read('05_telesis.NET', 'NET.TXT')
#print(net[0])            
#print(net[1])


def Telesis_Write(netlist, wfname = 'telesis.net') :

    f = open(wfname, 'w')

    name_n = len(netlist[0]); name_n -= 1

    f.write("$NETS\n")   
    for i, (name, net) in enumerate(zip(netlist[0], netlist[1])) :

        net_n = len(net); net_n -= 1
        
        str = '{0:20s}'.format(name + ';')
        f.write(str)

        for j, w in enumerate(net) :
            str = '{0:s}'.format((w.replace('(', '.', 1)).rstrip(')') )
            f.write(str)
            if j >= net_n :
                f.write("\n")
            elif (j % 8) == 7 :
                f.write(",\n                    ")
            else :
                f.write(" ")

    f.write("$END\n")                      
    f.close()


#Telesis_Write(net, 'telesis.net')



#************************************************************************************************************************************************   
#*SIG #PWRSW
#CN10.1                  U9.54                   RM4.4
#   
#*SIG #RES
#U9.7                    R15.1                   U12.4                   CN4.13
#     
#*SIG 3.3VCPU
#C30.2                   R116.2                  U16.O                   U27.6
#U28.6

#X1               CSTCEV
#X2               C-001R
#*NET*
#*SIG* #BATYENB
#U23.10                U23.13                U11.15
#*SIG* #CHARGE_ON
#Q7.2                  R93.2                 U25.1
#*SIG* 3.3VCPU
#R73.2                 C30.2                 R116.2                R161.2
#U16.3                 U27.6                 U28.6
#*SIG* VALVE_ON
#RM2.3                 Q41.2                 RM3.6
#   
#*END*     OF ASCII OUTPUT FILE

#
# FORMAT : PADS PowerPCB(v2-3)
def PADS_Read(rfname, wfname = 'NET.TXT') :

    f = open(wfname, 'w')

    netname = []; netlist = []; net = []
    name = ''; n = 0; t = 0
    for line in open(rfname, 'r'):
        line = line.replace('\n', '')       #改行削除
        line = line.replace('\r', '')       #改行削除

        words = re.split(" +", line.strip())  #１行をスペースで分離
        if line[0:4] == '*SIG' :            #最初の文字が'*SIG*'の時の処理
            if n == 0 :                     #一番最初のネットは、継続
                EOF = 0
            else :                          #前ネット名前を登録
                name = name1
                EOF = 1
            
            if len(words) > 1 :             #現ネット名前を記憶
                name1 = words[1].strip()
            else :
                name1 = '' 

            n += 1

        elif line[0:4] == '*END' :          #最初の文字が'*END*'の時の処理
            name = name1
            name1 = ''
            EOF = 1
            
        elif n == 0 :
            name = ''; name1 = ''; net = []
            EOF = 1   

        elif len(words) > 0 :
            if name1 != '' and words[0] != '' :
                for w in words :            #ネットを記憶
                    w = w.strip()                   
                    if len(w) > 0 :
                	w = w.replace('.', '(', 1) + ')'                   
                        net.append(w)
                EOF = 0
            else :
                name = name1
                name1 = ''
                EOF = 1
                
        else :
            name = name1
            name1 = ''
            EOF = 1
            
        #print(words)           
        
        if EOF == 1 :                       #前ネットを登録処理
            if name != '' and len(net) > 0 : 
                net.sort()                  #ネットリストの並べ替え
                netname.append(name)
                netlist.append(net)

                t += len(net)
                File_NetOut(f, len(netname), name, net, t)

                #print(name)
                #print(net)
                #print()
                              
            net = []; name = ''
    
        f.write(line); f.write('\n')
        #print(line)

    
    if name1 != '' and len(net) > 0 :       #直前の未登録ネットの登録処理
        net.sort()                          #ネットリストの並べ替え
        netname.append(name1)
        netlist.append(net)

        t += len(net)
        File_NetOut(f, len(netname), name1, net, t)

        #print(name1)
        #print(net)
        #print()

    f.close()
    return (netname, netlist, rfname)


#net = PADS_Read('06_pads.txt', 'NET.TXT')
#print(net[0])            
#print(net[1])


def PADS_Write(netlist, wfname = 'pads.net', rfname = '') :

    f = open(wfname, 'w')

    if rfname != '' :
        import csv
        #Reference, Value, Footprint
      
        data = []
        with open(rfname, 'r') as fcsv:
            reader = csv.reader(fcsv)       # readerオブジェクトを作成
            header = next(reader)           # 最初の一行をヘッダーとして取得
            #print(header)                  # ヘッダーを表示
            if (header[0].strip() == 'Reference') and (header[2].strip() == 'Footprint') :
                # 行ごとのリストを処理する
                for row in reader:
                    data.append(row)        # １行ずつデータ追加

        #print(data)
        
        f.write("*PART*       ITEMS\n")
        for i, w in enumerate(data) :
            f.write('{0:15s}  {1:s}\n'.format( w[0].decode('utf8'),  w[2].decode('utf8') ))
    
    else :
        data = []
        for net in netlist[1] :
            for w in net :
                words = w.split("(")
                if (words[0] in data) == False :
                    data.append(words[0])

        data.sort()
        f.write("*PART*       ITEMS\n")
        for i, w in enumerate(data) :
            f.write('{0:15s}  ""\n'.format( w ))
           

    f.write("*NET*\n")
    name_n = len(netlist[0]); name_n -= 1
    for i, (name, net) in enumerate(zip(netlist[0], netlist[1])) :

        net_n = len(net); net_n -= 1
        
        str = '*SIG* {0:s}\n'.format(name)
        f.write(str)

        for j, w in enumerate(net) :
            str = '{0:10s}'.format((w.replace('(', '.', 1)).rstrip(')') )
            f.write(str)
            if j >= net_n :
                f.write("\n")
            elif (j % 4) == 3 :
                f.write("\n")

    f.write("*END*\n")                      
    f.close()


#PADS_Write(net, 'pads.net')
#PADS_Write(net)



#************************************************************************************************************************************************
#%PART
#2125/0.85       C1
#CES-D50L54      C10
#CSTCR/1.2       X1
#%NET
#N33122                  F1-1 J2-1
#N33120                  J2-2 K1-7 K1-4 R14-1
#*                       J4-2
#N33043                  R1-1 C2-1 C3-2 L1-1
#VOUT                    Q2-6 C8-2 Q2-5 D3-2
#*                       D7-1 Q2-7 Q2-8 C7-1
#*                       J1-1
#N64981                  U4-1 U5-4
#$
#
# FORMAT : Intergraph
def Intergra_Read(rfname, wfname = 'NET.TXT') :

    f = open(wfname, 'w')

    netname = []; netlist = []; net = []
    name = ''; n = 0; t = 0; lock = 0
    for line in open(rfname, 'r'):
        line = line.replace('\n', '')       #改行削除
        line = line.replace('\r', '')       #改行削除

        if lock == 0 :                      #読み飛ばし処理
            if line[0:4] == '%NET' :
                lock = 1
            continue
                
        words = re.split(" +", line)        #１行をスペースで分離
        #print(words)
        if len(words) > 1 :
            if words[0].strip() == '*' :    #前のネットの続き
                for w in words[1:] :        #ネットを記憶
                    w = w.strip()                   
                    if len(w) > 0 :
                	w = w.replace('-', '(', 1) + ')'                   
                        net.append(w)
            else :                          #新しいネット名前
                if n > 0 and name != '' and len(net) > 0 : #前のネットを登録
                    net.sort()              #ネットリストの並べ替え
                    netname.append(name)
                    netlist.append(net)

                    t += len(net)
                    File_NetOut(f, len(netname), name, net, t)

                    #print(name)
                    #print(net)
                    #print()
               
                name = words[0].strip()     #新しいネット名前を記憶
                net = []
                for w in words[1:] :        #新しいネットを記憶
                    w = w.strip()                   
                    if len(w) > 0 :
                	w = w.replace('-', '(', 1) + ')'                   
                        net.append(w)
                    
                n += 1
                
        else :
            if n > 0 and name != '' and len(net) > 0 : 
                net.sort()                  #ネットリストの並べ替え
                netname.append(name)
                netlist.append(net)

                t += len(net)
                File_NetOut(f, len(netname), name, net, t)

                #print(name)
                #print(net)
                #print()

            name = ''; net = []

        f.write(line); f.write('\n')
        #print(line)    

    f.close()
    return (netname, netlist, rfname)


#net = Intergra_Read('07_INTERGRA.NET', 'NET.TXT')
#print(net[0])            
#print(net[1])


def Intergra_Write(netlist, wfname = 'intergra.net', rfname = '') :

    f = open(wfname, 'w')

    
    if rfname != '' :
        import csv
        #Reference, Value, Footprint
     
        data = []
        with open(rfname, 'r') as fcsv:
            reader = csv.reader(fcsv)       # readerオブジェクトを作成
            header = next(reader)           # 最初の一行をヘッダーとして取得
            #print(header)                  # ヘッダーを表示
            if (header[0].strip() == 'Reference') and (header[2].strip() == 'Footprint') :
                # 行ごとのリストを処理する
                for row in reader:
                    data.append(row)        # １行ずつデータ追加

        #print(data)
        
        f.write("%PART\n")
        for i, w in enumerate(data) :
            if len(w[2].decode('utf8')) > 15 :
                f.write('{0:s} {1:s}\n'.format( w[2].decode('utf8'),  w[0].decode('utf8') ))
            else :
                f.write('{0:15s} {1:s}\n'.format( w[2].decode('utf8'),  w[0].decode('utf8') ))
    
    else :
        data = []
        for net in netlist[1] :
            for w in net :
                words = w.split("(")
                if (words[0] in data) == False :
                    data.append(words[0])

        data.sort()
        f.write("%PART\n")
        for i, w in enumerate(data) :
            f.write('""              {0:s}\n'.format( w ))
           
        
    name_n = len(netlist[0]); name_n -= 1
    f.write("%NET\n")   
    for i, (name, net) in enumerate(zip(netlist[0], netlist[1])) :

        net_n = len(net); net_n -= 1
        
        str = '{0:20s}'.format(name)
        f.write(str)

        for j, w in enumerate(net) :
            str = '{0:s}'.format((w.replace('(', '-', 1)).rstrip(')') )
            f.write(str)
            if j >= net_n :
                f.write("\n")
            elif (j % 4) == 3 :
                f.write("\n*                   ")
            else :
                f.write(" ")

    f.write("$\n")                      
    f.close()


#Intergra_Write(net, 'intergra.net')
#Intergra_Write(net)



#Cmp-Mod V01 Created by PcbNew   date = 2017年10月30日 21時24分46秒
#
#BeginCmp
#TimeStamp = 59F71BA6
#Path = /A400
#Reference = BT1;
#ValeurCmp = BT:2;
#IdModule  = Pin_Headers:Pin_Header_Straight_1x02_Pitch2.54mm;
#EndCmp
def Cmp_Read(rfname) :

    data = []
    n = 0; lock = 0
    for line in open(rfname, 'r'):
        #print(line)
        line = line.replace('\n', '')       #改行削除
        line = line.replace('\r', '')       #改行削除
        n += 1
        if n == 1 :                         #ヘッダーチェック
            if line[0:7] != 'Cmp-Mod' :
                break
            else :
                continue
    
        if lock == 0 :                      #「BeginCmp」まで読み飛ばし処理
            if line[0:8] == 'BeginCmp' :
                Ref = ''; Val = ''; Fot = ''; Tim = ''; Pth = ''
                lock = 1
            continue
        else :                              #「EndCmp」までの部品情報を記録
            if line[0:12] == 'Reference = ' and line[-1] == ';' :
                Ref = line[12:-1]
                continue
            elif line[0:12] == 'ValeurCmp = ' and line[-1] == ';' :
                Val = line[12:-1]
                continue
            elif line[0:12] == 'IdModule  = ' and line[-1] == ';' :
                Fot = line[12:-1]
                continue
            elif line[0:6] == 'EndCmp' :
                data.append([Ref, Val, Fot, Tim, Pth])
                lock = 0
                continue
            elif line[0:12] == 'TimeStamp = ' :
                Tim = line[12:]
                continue
            elif line[0:7] == 'Path = ' :
                Pth = line[7:]
		if Pth[0] == '/' :
		    Pth = Pth[1:]
                continue
                  
    return data


#************************************************************************************************************************************************
#(export (version D)
#  (components
#    (comp (ref C1)
#      (value C_Small)
#      (footprint Capacitors_SMD:C_0603_HandSoldering)
#      (libsource (lib device) (part C_Small))
#      (sheetpath (names /) (tstamps /))
#      (tstamp A407))
#    (comp (ref R1)
#      (value R_Small)
#      (footprint Resistors_SMD:R_0603_HandSoldering)
#      (libsource (lib device) (part R_Small))
#      (sheetpath (names /) (tstamps /))
#      (tstamp A4B3))
#    (comp (ref L1)
#      (value L_Small)
#      (footprint Inductors_SMD:L_0603_HandSoldering)
#      (libsource (lib device) (part L_Small))
#      (sheetpath (names /) (tstamps /))
#      (tstamp A53E)))
#  (nets
#    (net (code 1) (name "Net-(L1-Pad1)")
#      (node (ref R1) (pin 1))
#      (node (ref L1) (pin 1)))
#    (net (code 2) (name "Net-(C1-Pad1)")
#      (node (ref C1) (pin 1))
#      (node (ref R1) (pin 2)))
#    (net (code 3) (name "Net-(C1-Pad2)")
#      (node (ref C1) (pin 2))
#      (node (ref L1) (pin 2)))))
#
# FORMAT : KiCAD
def Kicad_Read(rfname, wfname = 'NET.TXT') :

    f = open(wfname, 'w')

    netname = []; netlist = []; net = []
    name = ''; n = 0; t = 0; lock = 0
    for line in open(rfname, 'r'):
        line = line.replace('\n', '')       #改行削除
        line = line.replace('\r', '')       #改行削除
        if lock != 0 :
            f.write(line);  f.write('\n')


        line = line.strip()
        words = re.split(" +", line)        #１行をスペースで分離
        #print(words)

        if len(words) < 1 :                 #読み飛ばし処理
            continue
        
        if lock == 0 :                      #読み飛ばし処理
            if words[0] == '(nets' :
                lock = 1
            else :
                continue

        if len(words) == 5 :
            if words[0] == '(net' and words[1] == '(code' and words[3] == '(name' :
                name = words[4].rstrip(")")    #新しいネット名前を記憶
                name = name.strip('"')
            elif words[0] == '(node' and words[1] == '(ref' and words[3] == '(pin' :
                w = words[2].rstrip(")") + "(" +  words[4].rstrip(")") +")"  #新しいネット名前を記憶
                net.append(w)
                n += 1

                w = words[4].strip()
                if w[-3:] == ')))' :
                    if n > 0 and name != '' and len(net) > 0 : 
                        net.sort()          #ネットリストの並べ替え
                        netname.append(name)
                        netlist.append(net)

                        t += len(net)
                        File_NetOut(f, len(netname), name, net, t)

                        #print(name)
                        #print(net)
                        #print()

                    name = ''; net = []
           
    f.close()
    return (netname, netlist, rfname) 

#net = Kicad_Read('08_Nucleo_EXT.net', 'NET.TXT')
#print(net[0])            
#print(net[1])


def Kicad_Write(netlist, wfname = 'kicad.net', rfname = '') :

    
    f = open(wfname, 'w')
    f.write("(export (version D)\n")

    if rfname != '' :
        import csv
        #Reference, Value, Footprint, Datasheet
        #"C1","C_Small","Capacitors_SMD:C_0603_HandSoldering",""
        #"R1","R_Small","Resistors_SMD:R_0603_HandSoldering",""
        #"L1","L_Small","Inductors_SMD:L_0603_HandSoldering",""
      
        data = []
        with open(rfname, 'r') as fcsv:
            reader = csv.reader(fcsv)       # readerオブジェクトを作成
            header = next(reader)           # 最初の一行をヘッダーとして取得
            #print(header)                  # ヘッダーを表示
            if (header[0].strip() == 'Reference') and (header[1].strip() == 'Value') and (header[2].strip() == 'Footprint') :
                # 行ごとのリストを処理する
                for row in reader:
                    data.append(row)        # １行ずつデータ追加

        #print(data)

        data_n = len(data); data_n -= 1
        for i, w in enumerate(data) :

            f.write("  (components\n")
            f.write('    (comp (ref {0:s})\n'.format( w[0].decode('utf8') ))
            f.write('      (value {0:s})\n'.format( w[1].decode('utf8') ))
            f.write('      (footprint {0:s})\n'.format( w[2].decode('utf8') ))
            f.write('      (libsource (lib device) (part {0:s}))\n'.format( w[1].decode('utf8') ))           
            f.write('      (sheetpath (names /) (tstamps /))\n')            
            f.write('      (tstamp {0:X}))'.format(i + 0xA400))     

            if i >= data_n :
                f.write(")")
                
            f.write("\n")
    
    else :
        data = []
        for net in netlist[1] :
            for w in net :
                words = w.split("(")
                if (words[0] in data) == False :
                    data.append(words[0])

        data.sort()
        data_n = len(data); data_n -= 1
        for i, w in enumerate(data) :

            pin_max = 1
            for net in netlist[1] :
                for w1 in net :
                    words = w1.split("(")
                    if words[0] == w :
                        pin = int(words[1].rstrip(")"))
                        if pin > pin_max :
                            pin_max = pin
            
            f.write("  (components\n")
            f.write('    (comp (ref {0:s})\n'.format(w))
            f.write('      (value "{0:s}:{1:d}")\n'.format(w.rstrip("0123456789"), pin_max))
            if pin_max <= 40 :
                f.write('      (footprint "Pin_Headers:Pin_Header_Straight_1x{0:0>2d}_Pitch2.54mm")\n'.format(pin_max))
            elif pin <= 80 :
                f.write('      (footprint "Pin_Headers:Pin_Header_Straight_2x{0:0>2d}_Pitch2.54mm")\n'.format(pin_max//2))
            else :
                f.write('      (footprint "Pin_Headers:Pin_Header_Straight_2x40_Pitch2.54mm")\n')                
            f.write('      (libsource (lib device) (part ""))\n')           
            f.write('      (sheetpath (names /) (tstamps /))\n')            
            f.write('      (tstamp {0:X}))'.format(i + 0xA400))     

            if i >= data_n :
                f.write(")")
                
            f.write("\n")
            
            
    name_n = len(netlist[0]); name_n -= 1   
    f.write("  (nets\n")
    for i, (name, net) in enumerate(zip(netlist[0], netlist[1])) :

        net_n = len(net); net_n -= 1
        
        str = '    (net (code {0:d}) (name "{1:s}")\n'.format((i + 1), name)
        f.write(str)

        for j, w in enumerate(net) :
            words = w.split('(')
            str = '      (node (ref {0:s}) (pin {1:s}))'.format(words[0], words[1].rstrip(")"))
            f.write(str)
            if j >= net_n :
                f.write(")")
                if i >= name_n :
                    f.write("))")

            f.write("\n")
            
           
    f.close()


#Kicad_Write(net, 'kicad.net')



#************************************************************************************************************************************************
#P  CODE 00
#P  UNITS CUST 0
#P  DIM   N
#317/N023            D1    -1    D0394PA00X+035309Y-027829X0669Y0669R000S0
#317/N027            D1    -2    D0394PA00X+035309Y-028829X0669Y0669R000S0
#317/N027            D2    -1    D0394PA00X+041313Y-022026X0669Y0669R000S0
#317/N028            D2    -2    D0394PA00X+041313Y-023026X0669Y0669R000S0
#317/N007            D3    -1    D0394PA00X+035230Y-031470X0669Y0669R000S0
#317/N009            D3    -2    D0394PA00X+035230Y-032470X0669Y0669R000S0
#317/N009            D4    -1    D0394PA00X+036825Y-031470X0669Y0669R000S0
#317/N014            D4    -2    D0394PA00X+036825Y-032470X0669Y0669R000S0
#317/N014            D5    -1    D0394PA00X+044502Y-022026X0669Y0669R000S0
#317/N009            D5    -2    D0394PA00X+044502Y-023026X0669Y0669R000S0
#317/N009            D6    -1    D0394PA00X+041687Y-025667X0669Y0669R000S0
#317/N022            D6    -2    D0394PA00X+041687Y-026667X0669Y0669R000S0
#317/N011            D7    -1    D0394PA00X+040093Y-027829X0669Y0669R000S0
#317/N007            D7    -2    D0394PA00X+040093Y-028829X0669Y0669R000S0
#317/N022            D8    -1    D0394PA00X+043281Y-025667X0669Y0669R000S0
#317/N011            D8    -2    D0394PA00X+043281Y-026667X0669Y0669R000S0
#317/0               RL    -1    D0394PA00X+038498Y-027829X0669Y0669R000S0
#999
#
# FORMAT : IPC-D-356
def D356_Read(rfname, wfname = 'NET.TXT') :

    f = open(wfname, 'w')

    data = []
    for line in open(rfname, 'r'):
        f.write(line)
 
	if len(line) <= 27 :
	    continue
      
        if line[0] == '3' and line[2] == '7' and line[26] == '-':
            line = line.replace('\n', '')   #改行削除
            line = line.replace('\r', '')   #改行削除
            #print(line)
            name = line[3:17].strip()
            words = line[20:26].strip() + '(' + line[27:31].strip() + ')'
            #print(name, words)
            data.append([name, words])

    netname = []        
    for w in data :
        if (w[0] in netname) == False :     #新しいネット名前を記憶
            netname.append(w[0])

    netlist = [] 
    t = 0       
    for i, name in enumerate(netname) :
        net = []
        for w in data :
            if w[0] == name :               #同一ネット名前ならネットを登録
                net.append(w[1])

        net.sort()                          #ネットリストの並べ替え
        netlist.append(net)
        t += len(net)
        File_NetOut(f, (i + 1), name, net, t)


    f.close()
    return (netname, netlist, rfname)
            
#net = D356_Read('‪LTspice.d356')


#************************************************************************************************************************************************
