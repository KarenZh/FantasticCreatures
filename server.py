import hug
from hug_middleware_cors import CORSMiddleware
import json
import pyodbc

api = hug.API(__name__)
api.http.add_middleware(CORSMiddleware(api))

def connect():
        server = 'fantastic-creatures.database.windows.net'
        database = 'Fantastic_Creatures'
        username = 'fantastic'
        password = 'creatures123!'
        driver= '{ODBC Driver 13 for SQL Server}'
        cnxn = pyodbc.connect('DRIVER='+driver+';PORT=1433;SERVER='+server+';PORT=1443;DATABASE='+database+';UID='+username+';PWD='+ password)
        return cnxn
        
@hug.get('/getresult')
def getresult(longitude: hug.types.text, latitude: hug.types.text):
    lat = int(round(float(latitude) + 26))
    longt = int(round(float(longitude) - 138))

    lat1 = str(lat + 0.25)
    lat2 = str(lat - 0.25)
    longt1 = str(longt + 0.25)
    longt2 = str(longt - 0.25)



    cnxn = connect()
    cursor = cnxn.cursor()
    creatures_list = []
    description_list = []
    pic_list = []


    if cursor.execute("select * from dbo.ebsnake where (longtitude = ? and latitude = ?) or (longtitude = ? and latitude = ?) or (longtitude = ? and latitude = ?) or (longtitude = ? and latitude = ?)", (longt1, lat1, longt1, lat2, longt2, lat1, longt2, lat2)).rowcount!=0:
        creatures_list.append('Eastern Brown Snakes')
        description_list.append('The eastern brown snake (Pseudonaja textilis), often referred to as the common brown snake, is a species of venomous elapid snake of the genus Pseudonaja. This snake is considered the world\'s second-most venomous land snake It can be aggressive and is responsible for about 60% of snake bite deaths in Australia.')
        pic_list.append('https://c1.staticflickr.com/9/8146/7121195685_4846ff005a_b.jpg')

    if cursor.execute("select * from dbo.bjfish where (longtitude = ? and latitude = ?) or (longtitude = ? and latitude = ?) or (longtitude = ? and latitude = ?) or (longtitude = ? and latitude = ?)", (longt1, lat1, longt1, lat2, longt2, lat1, longt2, lat2)).rowcount!=0:
        creatures_list.append('Box Jellyfish')
        description_list.append('Box jellyfish (class Cubozoa) are cnidarian invertebrates distinguished by their cube-shaped medusae. Some species of box jellyfish produce extremely potent venom: Chironex fleckeri, Carukia barnesi and Malo kingi. Stings from these and a few other species in the class are extremely painful and can be fatal to humans.')
        pic_list.append('https://amindforscience.files.wordpress.com/2014/11/box_jellyfish.jpg')

    if cursor.execute("select * from dbo.croc where (longtitude = ? and latitude = ?) or (longtitude = ? and latitude = ?) or (longtitude = ? and latitude = ?) or (longtitude = ? and latitude = ?)", (longt1, lat1, longt1, lat2, longt2, lat1, longt2, lat2)).rowcount!=0:
        creatures_list.append('Saltwater Crocodile')
        description_list.append('The saltwater crocodile (Crocodylus porosus), also known as the estuarine crocodile, Indo-Pacific crocodile, marine crocodile, sea crocodile or informally as saltie,[2] is the largest of all living reptiles, as well as the largest riparian predator in the world.As its name implies, this species of crocodile can live in marine environments, but usually resides in saline and brackish mangrove swamps, estuaries, deltas, lagoons, and lower stretches of rivers. They have the broadest distribution of any modern crocodile, ranging from the eastern coast of India throughout most of Southeast Asia and northern Australia.')
        pic_list.append('http://cdn.grindtv.com/uploads/2015/07/croc-3--1024x607.jpg')

    num = len(creatures_list)

    if num == 0:
        print (json.dumps({"result":'safe'}))
        return json.dumps({"result":'safe'})

    if num == 1:
        print(json.dumps({"result":'not safe', "num_of_creatures":num, "name1":creatures_list[0], "description1":description_list[0], "pic1":pic_list[0]}))
        return json.dumps({"result":'not safe', "num_of_creatures":num, "name1":creatures_list[0], "description1":description_list[0], "pic1":pic_list[0]})

    if num == 2:
        print(json.dumps({"result":'not safe', "num_of_creatures":num, "name1":creatures_list[0],"name2":creatures_list[1],"description1":description_list[0],"description2":description_list[1],"pic1":pic_list[0],"pic2":pic_list[1]}))
        return json.dumps({"result":'not safe', "num_of_creatures":num, "name1":creatures_list[0],"name2":creatures_list[1],"description1":description_list[0],"description2":description_list[1],"pic1":pic_list[0],"pic2":pic_list[1]})

    if num == 3:
        print(json.dumps({"result":'not safe', "num_of_creatures":num, "name1":creatures_list[0],"name2":creatures_list[1],"name3":creatures_list[2],"description1":description_list[0],"description2":description_list[1], "description3":description_list[2], "pic1":pic_list[0],"pic2":pic_list[1],"pic3":pic_list[2]}))
        return json.dumps({"result":'not safe', "num_of_creatures":num, "name1":creatures_list[0],"name2":creatures_list[1],"name3":creatures_list[2],"description1":description_list[0],"description2":description_list[1], "description3":description_list[2], "pic1":pic_list[0],"pic2":pic_list[1],"pic3":pic_list[2]})

    cnxn.close()

# if __name__ == '__main__':
#     # getresult('138.75','-24.75')
#     getresult('145.75','-16.25')