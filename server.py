import hug
from hug_middleware_cors import CORSMiddleware
import json
import pyodbc

api = hug.API(__name__)
api.http.add_middleware(CORSMiddleware(api))

def connect():
        server = 'src-link.database.windows.net'
        database = ' SrcLink_DB'
        username = 'LinkStart'
        password = 'srclink123!'
        driver= '{ODBC Driver 13 for SQL Server}'
        cnxn = pyodbc.connect('DRIVER='+driver+';PORT=1433;SERVER='+server+';PORT=1443;DATABASE='+database+';UID='+username+';PWD='+ password)
        return cnxn
        
@hug.post('/register')
def register(loginName: hug.types.text, loginPassword: hug.types.text, contactEmail: hug.types.text):

        cnxn = connect()
        cursor = cnxn.cursor()
        cursor.execute("select * from dbo.producer where contact_email = ?" , contactEmail)
        if cursor.rowcount == 0:
                with cursor.execute("insert into dbo.producer(login_name, contact_email, login_password) values (?, ?, ?)", (loginName,contactEmail, loginPassword)):
                        # print(json.dumps({"result": 'OK'}))
                        return json.dumps({"result": 'OK'})
        else:
                # print(json.dumps({"result": 'user already exist'}))
                return json.dumps({"result": 'user already exist'})
        cnxn.close()

@hug.post('/login')
def login(contactEmail: hug.types.text, loginPassword: hug.types.text):

        json_obj1 = json.dumps({u"result": 'failed, login name is incorrect'})
        json_obj2 = json.dumps({u"result": 'failed, password is incorrect'})
        json_obj3 = json.dumps({u"result": 'OK'})

        cnxn = connect()
        cursor = cnxn.cursor()

        if cursor.execute("select * from dbo.producer where contact_email= ?", contactEmail).rowcount == 0:
                # print(json_obj1)
                return json_obj1
        else:
                cursor.execute("select * from dbo.producer where contact_email= ? and login_password=?", (contactEmail,loginPassword))
                if cursor.rowcount == 0:
                        # print(json_obj2)
                        return json_obj2
                else:
                        # print(json_obj3)
                        return json_obj3
        cnxn.close()

@hug.post('/item')
def addItem(productName: hug.types.text, productDescription: hug.types.text, productImg:hug.types.text, contactEmail: hug.types.text):

        productQr = "http://52.243.86.154/"+contactEmail+"/"+productName

        json_obj1 = json.dumps({"result": 'OK'})
        json_obj2 = json.dumps({"result": 'opps, item already exists'})

        cnxn = connect()
        cursor = cnxn.cursor()

        if cursor.execute("select * from dbo.product where contact_email=? and product_name = ?" , (contactEmail,productName)).rowcount == 0:
                with cursor.execute("insert into dbo.product( product_name, product_description, contact_email, product_qr, product_pic) values (?,?,?,?,?)", (productName, productDescription, contactEmail, productQr,productImg)):
                        # print (json_obj1)
                        return json_obj1
        else:
                # print(json_obj2)
                return json_obj2
        cnxn.close()

@hug.get('/item')
def getItem(productQr: hug.types.text):

        cnxn = connect()
        cursor = cnxn.cursor()

        if cursor.execute("select * from dbo.product where product_qr =?", productQr).rowcount == 1:
                row = cursor.fetchone()
                productName = row.product_name
                productDescription = row.product_description
                productImg = row.product_pic
                json_obj = json.dumps({"result": "OK",
                                       "ProductName": productName,
                                       "ProductDescription": productDescription,
                                       "ProductImg": productImg})

                # print (json_obj)
                return json_obj
        else:

                # print (json.dumps({"result": 'item not find'}))
                return json.dumps({"result": 'item not find'})
        cnxn.close()


# if __name__ == '__main__':
#         getItem('http://source_link/1/berryjam')
#         login('hello5@gmail.com','1234')
