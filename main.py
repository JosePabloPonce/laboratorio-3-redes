#Jose Pablo  Ponce 19092
#Gabriel Quiroz 19255
#Alexa Bravo 18331

import slixmpp
from slixmpp.exceptions import IqError, IqTimeout
from aioconsole import ainput
import networkx as nx
import asyncio
import yaml

asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

class Client(slixmpp.ClientXMPP):
    def __init__(self, jid, password, algoritmo, nodo, nodes, names, graph):
        slixmpp.ClientXMPP.__init__(self,jid, password)
        self.algoritmo = algoritmo #algoritmo elegido
        self.names = names #archivo names
        self.graph = graph #informacion del grafo, cantidad de nodos y aristas
        self.nodo = nodo #nodo al cual pertenece
        self.nodes = nodes #nodos a los que se esta dirigido
        self.distancia = 0 #inicializacion de distancia
        self.path = "" #variable para hacer calculos del camino
        
        self.add_event_handler('session_start', self.start)
        self.add_event_handler('message', self.message)
        
    async def start(self, event):
        self.send_presence() 
        await self.get_roster()        
        inicio = ""
        final = ""
        while True:
            to_user = await ainput("Ingresar el usuario al que le enviaras mensaje: ")
            while True:
                mensaje = await ainput("Mensaje: ")
                if (len(mensaje) > 0):
                    if (xmpp.algoritmo == '1'):
                        mensaje = "msg|" + str(xmpp.jid) + "|" + str(to_user) + "|" + str(xmpp.nodo) + "|" + str(mensaje) + "|" + str(self.distancia)
                        for i in xmpp.nodes:
                            xmpp.send_message(mto=xmpp.names[i], mbody=mensaje, mtype='chat' )  
                    elif (xmpp.algoritmo == '2'):

                        for (p, d) in xmpp.graph.nodes(data=True):
                            if (d['jid'] == xmpp.jid):
                                inicio = p
                            if (d['jid'] == to_user):
                                final = p
             
                        self.path=nx.shortest_path(xmpp.graph, inicio, final)
                        print("\nCamino:")
                        print(self.path)
                        self.path.pop(0)
                        mensaje = "msg|" + str(xmpp.jid) + "|" + str(to_user) + "|" + str(xmpp.nodo) + "|" + str(mensaje) + "|" + str(self.distancia) + "|" + ' '.join(self.path)
                        print(mensaje)
                        sendto = self.path[0]
                        mail = ""
                        for (p, d) in xmpp.graph.nodes(data=True):
                            if (p == sendto):
                                mail = d['jid']

                        print("\nReenviando a: "+mail)
                        xmpp.send_message(mto=mail, mbody=mensaje, mtype='chat' )

                    elif (xmpp.algoritmo == '3'):
                        target=[]
                        
                        for x in xmpp.graph.nodes().data():
                            if x[1]["jid"] == to_user:
                                target.append(x)
                        mensaje = "msg|" + str(xmpp.jid) + "|" + str(to_user) + "|" + str(xmpp.nodo) + "|" + str(mensaje) + "|" + str(self.distancia)
                        camino_corto = nx.shortest_path(xmpp.graph, source=xmpp.nodo, target=target[0][0])
                        if len(camino_corto) > 0:
                            xmpp.send_message(mto=xmpp.names[camino_corto[1]], mbody=mensaje, mtype='chat' )
                    else:
                        xmpp.send_message(mto=to_user, mbody=mensaje, mtype='chat' )

    async def message(self, msg):
        if msg['type'] in ('normal', 'chat'):
            await self.ReenviarMensaje(msg['body'])

    async def ReenviarMensaje(self, msg):
        message = msg.split('|')
        if message[0] == 'msg':
            if self.algoritmo == '1':
                print('\nUsando algoritmo de enrutamiento Flooding')
                print('\nReenviando Mensaje')

                if str(message[2]) == str(self.jid):
                    message[3] = message[3] + "," + str(self.nodo)
                    lista = message[3].split(",")
                    message[5] = str(len(lista)-1)
                    print("Mensaje para mi: ", message)
                else:
                    lista = message[3].split(",")
                    if self.nodo not in lista:
                        message[3] = message[3] + "," + str(self.nodo)
                        StrMessage = "|".join(message)
                        for i in self.nodes:
                            self.send_message(mto=self.names[i], mbody=StrMessage, mtype='chat' )  

            elif self.algoritmo == '2':
                print('\nUsando algoritmo de enrutamiento Distance Vector')
                lista = message[6].split(' ')
                if len(lista) > 1:
                    lista.pop(0)
                    sendto = lista[0]
                    message[6] = ' '.join(lista)
                    for (p, d) in xmpp.graph.nodes(data=True):
                        if (p == sendto):
                            jid_receiver = d['jid']
                    print('Reenviando a: ', jid_receiver)

                if message[2] == self.jid:
                    message[3] = message[3] + "," + str(self.nodo)
                    lista = message[3].split(",")
                    message[5] = str(len(lista)-1)
                    print("Mensaje para mi: ", message)
                else:
                    lista = message[3].split(",")
                    if self.nodo not in lista:
                        message[3] = message[3] + "," + str(self.nodo)
                        StrMessage = "|".join(message)
                        self.send_message( mto=jid_receiver,mbody=StrMessage,mtype='chat')  
                        print("Mensaje Enviado")

            elif self.algoritmo == '3':
                print('\nUsando algoritmo de enrutamiento Link State Routing')
                if message[2] == self.jid:
                    message[3] = message[3] + "," + str(self.nodo)
                    lista = message[3].split(",")
                    message[5] = str(len(lista)-1)
                    print("Mensaje para mi: ", message)
                else:
                    lista = message[3].split(",")
                    if self.nodo not in lista:
                        message[3] = message[3] + "," + str(self.nodo)
                        message[5] = str(len(lista)-1)
                        StrMessage = "|".join(message)
                        target = []
                 
                        for x in self.graph.nodes().data():
                            if x[1]["jid"] == message[2]:
                                target.append(x)
                        
                        camino_corto = nx.shortest_path(self.graph, source=self.nodo, target=target[0][0])
                        print('Camino: ', camino_corto)
                        if len(camino_corto) > 0:
                            self.send_message(mto=self.names[camino_corto[1]], mbody=StrMessage, mtype='chat' )  


def Grafo(topo, names):
    G = nx.Graph()
    for key, value in names["config"].items():
        G.add_node(key, jid=value)
        
    for key, value in topo["config"].items():
        for i in value:
            weightA = 1
            G.add_edge(key, i, weight=weightA)
    
    return G
    
if __name__ == "__main__":

    topologia = open("topologia.txt", "r", encoding="utf8")
    nombres = open("nombres.txt", "r", encoding="utf8")
    topoF = yaml.load(topologia.read(), Loader=yaml.FullLoader)
    nombresF = yaml.load( nombres.read(), Loader=yaml.FullLoader)

    jid = input("Usuario: ")
    pswd = input("Contrasena: ")
    print("1. Flooding\n2. Distance Vector Routing\n3. Link State Routing")
    alg = input("Ingresa el algoritmo de enrutamiento a utilizar: ") 


    for key, value in nombresF["config"].items():
            if jid == value:
                nodo = key
                nodes = topoF["config"][key]

    graph = Grafo(topoF, nombresF)
    xmpp = Client(jid, pswd, alg, nodo, nodes, nombresF["config"], graph)
    xmpp.register_plugin('xep_0030') # Service Discovery
    xmpp.register_plugin('xep_0045') # Multi-User Chat
    xmpp.register_plugin('xep_0199') # Ping
    xmpp.connect(disable_starttls=True) 
    xmpp.process(forever=False)