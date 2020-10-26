import hashlib
import base64
from cryptography.fernet import Fernet
from time import sleep
import os

class mainApp():

    def __init__(self,unCleanedFiles=None,typeOfOperation=None,keyCode=None,DEncryptN=False):

        self.keyCode = keyCode
        self.unCleanedFiles = unCleanedFiles
        self.typeOfOperation = typeOfOperation
        self.DEncryptN = DEncryptN
        self.EDcryptor = None
        self.TargetedFiles = None


        if not self.typeOfOperation == None and not self.keyCode == None and not self.keyCode == "" and not self.keyCode == " " and not self.unCleanedFiles == None:
            self.asKey()
            self.Files()

            if self.typeOfOperation =="enc":
                self.Encryptor()
                if self.DEncryptN:
                    self.DEncryptName()
                    
            elif self.typeOfOperation =="dnc":
                self.Decryptor()
                if self.DEncryptN:
                    self.DEncryptName()
                    
        else:
            print('You must have forgot to add some parametre')
        
    
    def asKey(self):
        ##converting a string (paswword) to usable format for the fernet library

        #converting the string (paswword) to bytes for the hashlib
        keyCode = self.keyCode.encode()
        #hashing keyCode that we converted to bytes
        key1 = hashlib.sha3_256(keyCode)
        #converted to a usable key for the fernet
        key_bytes = key1.digest()
        fernet_key = base64.urlsafe_b64encode(key_bytes)
        ##now the password is in good format for the Fernet library to use
        #custom_Encoder is the class that have the Encrypt function & Decrept function that we will use , and we provides it with the key.

        custom_Encoder = Fernet(fernet_key)
        #so we can use it in this Encrypt/Decrypt function in the whole class
        self.EDcryptor = custom_Encoder

    def Encryptor(self):
        ##this function is used to Encrypt only Files in the self.TargetedFiles list


        for oneFile in self.TargetedFiles:
            #we used the open method with mode rb+ to read the bytes of each file in the list
            with open(oneFile,'rb+') as newFile:

                file_bytes_normal = newFile.read()
                #after reading the whole page i used this method to back to the top of page
                newFile.seek(0)
                #calling the encrypt functin that returns the value encrypted !! the value type is byte
                coded = self.Encrypts(file_bytes_normal)
                #OverWritting the file with Encrypted data of its original data
                newFile.write(coded)
                newFile.truncate()

    def Encrypts(self,data):
        ##we used the self.EDcryptor that have Encrypt/Dencrypt functions (that we defined in asKey)
        #its encrypt what we value we give the data (data must be Bytes type)
        return self.EDcryptor.encrypt(data)
        

    def Decrypts(self,data):
        ##we used the self.EDcryptor that have Encrypt/Dencrypt functions (that we defined in asKey)
        #its Decrypt what we value we give the data (data must be Bytes type)

        return self.EDcryptor.decrypt(data)

    def Decryptor(self):
        ## this function only Decrypt Files but its same like the Encrypt function so no need to repeat unessary comments
        #the forTheLoop variable is used for the while loop so it can run , and we can limit the user try chance be return it false after 3 chance
        forTheLoop = True
        #tryNumber is increased every time that the user fails the password , and when its equal 3 the software stops
        tryNumber = 0

        while forTheLoop:

            try:
                for oneFile in self.TargetedFiles:
                    with open(oneFile,'rb+') as newFile:

                        file_bytes_encrypted = newFile.read()
                        
                        newFile.seek(0)
                        decoded = self.Decrypts(file_bytes_encrypted)
                        newFile.write(decoded)
                        newFile.truncate()
                        #we returned false to stop the while loop
                        forTheLoop=False

            except:

                print('the password is wrong try Again')
                #increase the tryNumber value everytime user fails the password , and stop after 3 chances
                tryNumber=tryNumber+1
                if tryNumber<=3:
                    
                    print(f'totatl chances you have left is : {3-tryNumber}')
                    #if the tryNumber is less than 3 or equal 3 , its ask again the user to write the password by recalling the asKey function
                    self.asKey()
                else:
                    #if the user failed all its chances the software stops
                    print('You Used All Your Chances !!!')
                    forTheLoop=False
                

    def DEncryptName(self):
        if self.typeOfOperation == "enc":
            for oneFile in self.TargetedFiles:
                path = oneFile.split('/')[0:-1]
                finalPath = f'{"/".join(path)}'
                fileName = oneFile.split('/')[-1]

                nameCoded = self.Encrypts(fileName.encode())
                os.rename(oneFile,f'{finalPath}/{nameCoded.decode()}')
                
        elif self.typeOfOperation == "dnc":
            for oneFile in self.TargetedFiles:
                path = oneFile.split('/')[0:-1]
                finalPath = f'{"/".join(path)}'
                fileName = oneFile.split('/')[-1]
                print(fileName)
                nameToDecod = self.Decrypts(fileName.encode())
                os.rename(oneFile,f'{finalPath}/{nameToDecod.decode()}')

        


    def Files(self):
        # All_Files = os.listdir()
        All_Files = self.unCleanedFiles
        cleanFiles = []
        for oneFile in All_Files:
            if '.py' in oneFile or '.vscode'==oneFile or "__pycache__" in oneFile :
                continue
            else:
                cleanFiles.append(oneFile)

        self.TargetedFiles = cleanFiles

        