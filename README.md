# Sistema de Logística de Rotas

Este projeto implementa um sistema de logística de rotas para otimizar o transporte entre cidades.

## Alunos

## Funcionalidades

- Encontrar o menor caminho entre duas cidades.
- Validar regras de negócio para otimizar as rotas.
- Cálculo de custo, distância e tempo estimado para o transporte.

## Tecnologias Utilizadas

- Python
- NetworkX (biblioteca para grafos)
- Geopy (para cálculos de distância geodésica)
- Folium (para visualização em mapas interativos)

## Como Usar

1. **Instalação:**
   Certifique-se de ter o Python e as bibliotecas necessárias instaladas. Você pode instalar as dependências usando:

   ```bash
   pip install networkx geopy folium
   ```
## Execução:

Execute o script Python principal:

```bash
python logistica_rotas.py
```

Entrada de Dados:

Modifique as informações das cidades no script, se necessário.
Defina as rotas e regras de negócio conforme especificado no código.
Resultados:

O script exibirá o menor caminho, custo, distância e tempo estimado.
Um mapa interativo será gerado e salvo como 'caminho.html'.

## Exemplo de Uso
python
Copy code
ponto_partida = "Londrina"
destino = "Foz do Iguaçu"
caminho, custo, distancia, dias, data_chegada = encontrar_menor_caminho_com_regras(ponto_partida, destino)

if caminho is not None:
    print(f"Menor caminho de {ponto_partida} para {destino}: {caminho}")
    print(f"Custo do menor caminho: R${custo:.2f}")
    print(f"Distância total percorrida: {distancia:.2f} km")
    print(f"Tempo estimado de viagem: {int(dias)} dias e {int(horas)} horas")
    print(f"Data e hora de chegada: {data_chegada.strftime('%Y-%m-%d %H:%M:%S')}")
    print("Mapa salvo como 'caminho.html'")
else:
    print("Não foi possível encontrar um caminho válido que satisfaça as regras de negócio.")
    
##Contribuições

Contribuições são bem-vindas! Sinta-se à vontade para abrir problemas (issues) e enviar pull requests.

## Licença
Este projeto está licenciado sob a Licença MIT - consulte o arquivo LICENSE.md para obter detalhes.
