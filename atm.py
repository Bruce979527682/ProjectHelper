import random
import csv
import time

accounts=[]

def getAccounts():
    with open('accounts.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            try:
                dic = {'Account':row['Account'].strip(),'PIN':row['PIN'].strip(),'Money':float(row['Money'].strip()),'IsLocked':row['IsLocked'].strip().lower()=='true','WrongNum':int(row['WrongNum'].strip())}            
                accounts.append(dic)
            except Exception as e:
                # print(e)
                continue

def writeCsv(filename,row):
    wfile = open(filename, 'a', newline='')
    writer = csv.writer(wfile)    
    writer.writerow(row)

def modify_password():
    getAccounts()
    print("Welcome to Myhome bank!\n")
    count= 1
    global current_account
    while count<=3:
        myaccount= input("Please enter your account number:\n")
        mypassword=input("Please enter your password:\n")
        account_list = list(filter(lambda x: x['Account'] == myaccount, accounts))
        if len(account_list) > 0:
            account = account_list[0]
            current_account = account
            if myaccount== account['Account'] and mypassword==account['PIN'] and account['IsLocked']==False:
                print("Login successful!\n")
                current_account = account
                main_menu()
                break
            else:
                if count==3: 
                    current_account['IsLocked'] = True    
                    current_account['WrongNum'] = 3   
                    saveData()   
                    print("Three times out. Your account was locked, Please callXXXXX or ask bank staff for help!\n")
                else:
                    print("Password wrong, please try again!\n")
                    current_account['WrongNum']+=1
                    count+=1
        else:
            if count==3:
                print("Three times out. Your account was locked, Please callXXXXX or ask bank staff for help!\n")
            else:
                print("Password wrong, please try again!\n")
                count+=1
def saveData():
    csvfile = open('accounts.csv', 'w', newline='')
    writer = csv.DictWriter(csvfile,['Account', 'PIN', 'Money', 'IsLocked', 'WrongNum'])
    writer.writeheader()
    for row in accounts:
        writer.writerow(row)

def main_menu():
    while True:
        print("Welcome to the main menu:\n")
        print("==========================================")
        print("|  Withdraw     :1   |   Balance    :2   |")
        print("=========================================")
        print("|  Deposit      :3   |   Exit       :4   |")
        print("==========================================")
        print("Please chose function:")
        choice= int(input())
        add_money=0
        if choice==1:
            withdraw_money= int(input("Please enter the cash amount:"))
            while True:
                if withdraw_money % 100 ==0:
                    if withdraw_money > current_account['Money']:
                        print("Account balance is not enough!")
                        withdraw_money= int(input("Please enter the cash amount:"))
                    else:
                        if withdraw_money <=3000:
                            current_account['Money']-=withdraw_money
                            writeCsv('records.csv',[current_account['Account'],-withdraw_money, time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())])
                            print("Please take the cash %d dollar. "% withdraw_money)
                            break
                        else:
                            if withdraw_money >= 3000:
                                print("The limit of cash is 3000 dollar!\n")
                                withdraw_money=int(input("Please enter the cash amount:"))
                            elif add_money==10000:
                                print("The cash amount is out of today limit!")
                                break
                            else:
                                print("Today limit is: %d dollar, Please enter the new amount!\n" %(3000-withdraw_money))
                                withdraw_money=int(input("Please enter the amount:"))
                else:
                    withdraw_money= int(input("Please enter a multiple of 100!\n"))
        elif choice== 2:
            print("Account balance is: %d dollar "% current_account['Money'])
        elif choice==3:
            money= int(input("Please put in the cash or check deposit:"))
            while True:
                if money<=10000:
                    current_account['Money']+=money
                    writeCsv('records.csv',[current_account['Account'], money, time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())])
                    print("Succeed! Deposit %d dollar." %money)
                    break
                else:
                    print("Please do not put over 50 bill")
                    money=int(input("Please put in the deposit:"))
        elif choice==4:
            saveData()
            print("Thank you for using the ATM！\n")
            print("See you next time, Have a good day!")
            break

modify_password()
