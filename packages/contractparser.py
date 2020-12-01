from pikepdf import Pdf
import tabula
import pandas as pd
class ContractParser:
    def __init__(self,path,password):
        self.path=path
        self.password=password
    def decryptPdf(self): #saves decrypted file as out.pdf 
        with Pdf.open(self.path,self.password) as pdf:
            pdf.save("out.pdf")
    def readFile(self,output):
        self.output=output
        self.DecryptPdf()
        dfs=tabula.read_pdf("out.pdf",pages='all')
        tabula.convert_into("out.pdf", self.output+".csv", output_format="csv", pages='all')
    def makeDF(self):
        return tabula.read_pdf(self.path, pages='all')
    def filterData(self,raw_data):
        self.raw_data=raw_datax
        col=[]
        for i in raw_data.columns:
            col.append(i.replace('\r',''))
        filtered_cont=[]
        data=[raw_data['Security/Contractdescription'],raw_data['Buy(B)/Sell(S)'],raw_data['Quantity'],raw_data['Net Total(BeforeLevies)(Rs)']]
        lenofdata=len(data[0])
        for i in range(lenofdata):
            if(str(data[0][i])=='nan' or data[0][i]=='0'):
                continue
            else:
                filtered_cont.append([str(data[0][i]).replace('\r',''),str(data[1][i]),int(data[2][i]),str(data[3][i])])
        return filtered_cont
    def getInsights(cont):
        trades_taken=0
        gross_profit=0
        trades={}
        cur_name=cont[0][0]
        net_profit=0
        quant=0
        coll_data=[]
        quant_taken=0
        for i in cont:
            if(i[0]!=cur_name):
                trades[cur_name]=(trades_taken,coll_data)
                coll_data=[]
                trades_taken=0
            if(i[3][0]=='('):
                net_profit-=float(i[3][1:-1])
            else:
                net_profit+=float(i[3])
            if(i[1]=='S'):
                quant-=int(i[2])
            else:
                quant_taken+=int(i[2])
                quant+=i[2]
            if(quant==0):
                trades_taken+=1
                coll_data.append([net_profit,quant_taken])
                quant_taken=0
                net_profit=0
                quant=0
            cur_name=i[0]
        return trades