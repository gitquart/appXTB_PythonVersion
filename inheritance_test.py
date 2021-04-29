class Data(object):
    
    def __init__(self,name, age):
        self.name=name
        self.age=age

    def suma(self,a,b):
        return a+b    

    def showAge(self):
        print('Your age is ',self.age) 
        self.__ImPrivate()

    def updateData(self,newName,newAge):
        self.name=newName
        self.age=newAge     

    def __ImPrivate(self):
        print('I am a private method') 

class Calc(Data):
    def __init__(self,numA,numB):
        self.num1=numA
        self.num2=numB

    def sumaCalc(self):
        return super(Calc,self).suma(self.num1,self.num2)       
                

def main():
    print('Before:')
    objData= Data('Ulyses','32') 
    objData.showAge()   
    objData.updateData('Uly2','31')   
    print('After')
    objData.showAge() 
    oCalc= Calc(9,6)
    res= oCalc.sumaCalc()
    print(str(res))
    
    






if __name__ == "__main__":
    main()