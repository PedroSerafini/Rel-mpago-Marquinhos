import networkx as nx
from geopy.distance import geodesic
import folium
from datetime import datetime, timedelta

G = nx.DiGraph()

cidades = {
    "Curitiba": {"endereco": "Endereco1", "latitude": -25.4296, "longitude": -49.2719},
    "Londrina": {"endereco": "Endereco2", "latitude": -23.3105, "longitude": -51.1625},
    "Foz do Iguaçu": {"endereco": "Endereco3", "latitude": -25.5478, "longitude": -54.5882},
    "União da Vitória": {"endereco": "Endereco4", "latitude": -26.2276, "longitude": -51.0870},
    "Joinville": {"endereco": "Endereco5", "latitude": -26.3032, "longitude": -48.8417},
    "Chapecó": {"endereco": "Endereco6", "latitude": -27.1000, "longitude": -52.6158},
    "Porto Alegre": {"endereco": "Endereco7", "latitude": -30.0277, "longitude": -51.2287},
    "Uruguaiana": {"endereco": "Endereco8", "latitude": -29.7617, "longitude": -57.0856},
    "Pelotas": {"endereco": "Endereco9", "latitude": -31.7719, "longitude": -52.3425},
}

for cidade, info in cidades.items():
    G.add_node(cidade, endereco=info["endereco"], latitude=info["latitude"], longitude=info["longitude"])

rotas = [
    ("Curitiba", "Londrina"),
    ("Curitiba", "Joinville"),
    ("Curitiba", "União da Vitória"),
    ("Londrina", "Curitiba"),
    ("Londrina", "Foz do Iguaçu"),
    ("Londrina", "União da Vitória"),
    ("Foz do Iguaçu", "Londrina"),
    ("Foz do Iguaçu", "Chapecó"),
    ("Foz do Iguaçu", "União da Vitória"),
    ("União da Vitória", "Curitiba"),
    ("União da Vitória", "Londrina"),
    ("União da Vitória", "Foz do Iguaçu"),
    ("União da Vitória", "Joinville"),
    ("União da Vitória", "Chapecó"),
    ("Joinville", "Curitiba"),
    ("Joinville", "União da Vitória"),
    ("Joinville", "Chapecó"),
    ("Chapecó", "Foz do Iguaçu"),
    ("Chapecó", "União da Vitória"),
    ("Chapecó", "Joinville"),
    ("Chapecó", "Porto Alegre"),
    ("Chapecó", "Uruguaiana"),
    ("Porto Alegre", "Chapecó"),
    ("Porto Alegre", "Uruguaiana"),
    ("Porto Alegre", "Pelotas"),
    ("Uruguaiana", "Chapecó"),
    ("Uruguaiana", "Porto Alegre"),
    ("Uruguaiana", "Pelotas"),
    ("Pelotas", "Porto Alegre"),
    ("Pelotas", "Uruguaiana"),
]

for origem, destino in rotas:
    G.add_edge(origem, destino)

custo_por_km = 20
distancia_por_dia = 500

def calcular_custo_total(distancia_total):
    custo_total = distancia_total * custo_por_km
    return custo_total

def validar_regras_de_negocio(caminho):
    cidades_a_adicionar = []
    
    if "Foz do Iguaçu" in caminho and "União da Vitória" not in caminho:
        cidades_a_adicionar.append("União da Vitória")
        index_cidade_verificacao = caminho.index("Foz do Iguaçu")
        caminho.insert(index_cidade_verificacao + 1, "União da Vitória")

    if "União da Vitória" in caminho and "Foz do Iguaçu" not in caminho:
        cidades_a_adicionar.append("Foz do Iguaçu")
        index_cidade_verificacao = caminho.index("União da Vitória")
        caminho.insert(index_cidade_verificacao + 1, "Foz do Iguaçu")

    if "Joinville" in caminho and "Chapecó" not in caminho:
        cidades_a_adicionar.append("Chapecó")
        index_cidade_verificacao = caminho.index("Joinville")
        caminho.insert(index_cidade_verificacao + 1, "Chapecó")

    if "Chapecó" in caminho and "Joinville" not in caminho:
        cidades_a_adicionar.append("Joinville")
        index_cidade_verificacao = caminho.index("Joinville")
        caminho.insert(index_cidade_verificacao + 1, cidade)

    return True

def calcular_distancia(caminho):
    distancia_total = 0
    for i in range(len(caminho)-1):
        cidade_atual = caminho[i]
        proxima_cidade = caminho[i+1]
        distancia_total += geodesic(
            (cidades[cidade_atual]["latitude"], cidades[cidade_atual]["longitude"]),
            (cidades[proxima_cidade]["latitude"], cidades[proxima_cidade]["longitude"])
        ).km
    return distancia_total

def calcular_tempo_estimado(distancia_total):
    dias = int(distancia_total // distancia_por_dia)
    horas = int((distancia_total % distancia_por_dia) / 500 * 24)
    return dias, horas

def exibir_mapa(caminho):
    mapa = folium.Map(location=(cidades[caminho[0]]["latitude"], cidades[caminho[0]]["longitude"]), zoom_start=6)
    for cidade in caminho:
        folium.Marker(
            location=(cidades[cidade]["latitude"], cidades[cidade]["longitude"]),
            popup=cidade,
            icon=folium.Icon(color='blue')
        ).add_to(mapa)
    folium.PolyLine([(cidades[cidade]["latitude"], cidades[cidade]["longitude"]) for cidade in caminho], color="red", weight=2.5, opacity=1).add_to(mapa)
    mapa.save('caminho.html')

def encontrar_menor_caminho_com_regras(origem, destino):

    caminho = nx.shortest_path(G, source=origem, target=destino, weight='weight')

    
    if not validar_regras_de_negocio(caminho):
        return None, None, None, None, None
    
    distancia_total = calcular_distancia(caminho)

    custo_total = calcular_custo_total(distancia_total)

    dias, horas = calcular_tempo_estimado(distancia_total)

    exibir_mapa(caminho)

    agora = datetime.now()
    data_chegada = agora + timedelta(days=dias, hours=horas)

    return caminho, custo_total, distancia_total, dias, data_chegada

ponto_partida = "Curitiba"
destino = "Pelotas"
caminho, custo, distancia, dias, data_chegada = encontrar_menor_caminho_com_regras(ponto_partida, destino)

if caminho is not None:
    print(f"Menor caminho de {ponto_partida} para {destino}: {caminho}")
    print(f"Custo do menor caminho: R${custo:.2f}")
    print(f"Distância total percorrida: {distancia:.2f} km")
    print(f"Tempo estimado de viagem: {int(dias)} dias e {int((dias % 1) * 24)} horas")
    print(f"Data e hora de chegada: {data_chegada.strftime('%Y-%m-%d %H:%M:%S')}")
    print("Mapa salvo como 'caminho.html'")
else:
    print("Não foi possível encontrar um caminho válido que satisfaça as regras de negócio.")
