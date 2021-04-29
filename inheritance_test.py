class Data(object):
    
    def __init__(self,name, age):
        self.name=name
        self.age=age

    def showAge(self):
        print('Your age is ',self.age) 
        self.__ImPrivate()

    def updateData(self,newName,newAge):
        self.name=newName
        self.age=newAge     

    def __ImPrivate(self):
        print('I am a private method')    

def main():
    print('Before:')
    objData= Data('Ulyses','32') 
    objData.showAge()   
    objData.updateData('Uly2','31')   
    print('After')
    objData.showAge() 
    






if __name__ == "__main__":
    main()