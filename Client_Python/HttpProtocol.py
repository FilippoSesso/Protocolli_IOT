import Package as pk

#variabili globali
LAST_DRONE_DATA={}
TIMER=10

#funzione per eseguire l'invio di dati dopo un intervallo di tempo specificato
def doPolling():
    pk.schedule.every(TIMER).seconds.do(sendSensors)
    while True:
        pk.schedule.run_pending()
        pk.time.sleep(1)

#funzione generica post
def doPost(url,data):
    req = pk.rq.post(url, data=pk.json.dumps(data), headers={'content-type':'application/json'})
    statusCode(req.status_code)
    print(req.json())

#funzione generica ger
def doGet(url):
    req = pk.rq.get(url)
    statusCode(req.status_code)
    return pk.json.loads(req.content)

#funzione di controllo sul codice di risposta del server
def statusCode(code):
    if code == (200 or 201):
        print("Invio Dati....")
    elif code == 400:
        print("Errore Client....")
    elif code == 404:
        print("Errore Server...")
  
#creazione di dreone/i      
def createDrone():
    numDornes=pk.ran.randint(0,10)
    
    modelList=[
                "Potensic Drone T35",
                "Potensic Drone T25",
                "DJI Mavic 2 Pro",
                "DJI Mavic Air",
                "DJI Phantom 4 pro",
                "DJI Mavic Pro",
                "DJI Phantom 4",
                "Parrot ANAFI",
                "DJI Mavic Pro Platinum",
                "DJI SPARK COMBO"
            ]
    
    count=1
    while numDornes>0:
        data={
                "id":f"drone{count}",
                "model":modelList[pk.ran.randint(0,9)]
            }
        doPost("http://10.30.134.11:3000/v1/drones/new",data)
        numDornes-=1
        count+=1

#invio dati registrati dai sensori    
def sendSensors():
    global LAST_DRONE_DATA
    global TIMER
    data={
            "drone":"test",
            "speed":pk.ran.randint(0,100),
            "altitude":pk.ran.randint(0,1000), 
            "battery":pk.ran.randint(0,100),
            "position":{
                "lat":pk.ran.randint(516400146, 630304598),
                "lon":pk.ran.randint(224464416, 341194152)
                }
        }
    if not LAST_DRONE_DATA:
        LAST_DRONE_DATA=data
    elif data['drone']==LAST_DRONE_DATA['drone'] and data['speed']==LAST_DRONE_DATA['speed'] and data['altitude']==LAST_DRONE_DATA['altitude'] and data['battery']==LAST_DRONE_DATA['battery'] and data['position']['lat']==LAST_DRONE_DATA['position']['lat'] and data['position']['lon']==LAST_DRONE_DATA['position']['lon']:
        TIMER=20
    else:TIMER=10
    #print(TIMER)
    doPost("http://10.30.134.11:3000/v1/drones/status",data)

#Accensione o Spegnimento del drone
def changeStatus():
    name='test'
    drone=doGet(f"http://10.30.134.11:3000/v1/drones/{name}/status")
    print(drone)
    drone['state']=not drone['state']
    print(drone)

#ottengo solo il drone corrispondente al nome passato come parametre
def getDroneByName(name):
    drone=doGet(f"http://10.30.134.11:3000/v1/drones/{name}/status")
    return drone

#ottengo tutti i droni presenti nel DB
def getDrones():
    print(doGet("http://10.30.134.11:3000/v1/drones"))
    