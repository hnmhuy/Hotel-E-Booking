import user
import hotel
import bill
import link_data

def CheckLogin_Sever(data, list):
    i=0
    while(i < len(data)):
        account_username = data[i]['username']
        account_password = data[i]['password']
        if(list[1] == account_username and list[2] == account_password ):
            return True
        else:
            i+=1
    return False
