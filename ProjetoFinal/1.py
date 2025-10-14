import pandas as pd
import numpy as np





## importaçao do csv
################################
df = pd.read_csv("C:/Users/Victor/Desktop/CC/CDS/projetos/python/ProjetoFinal/zomato.csv", encoding="utf-8", engine='python')

# Ajustar para mostrar todas as colunas
pd.set_option('display.max_columns', None)


#print(df.head(5))


# Identificar colunas com um único valor
cols_to_remove = [col for col in df.columns if df[col].nunique() == 1]

# Remover essas colunas do DataFrame
df_1 = df.drop(columns=cols_to_remove)

# Exibir as colunas removidas
#print("Colunas removidas:", cols_to_remove)

# Exibir o DataFrame após a remoção
#print(df_1)

# Verificar se existem dados duplicados
duplicados = df_1.duplicated()

# Exibir a quantidade de linhas duplicadas
#print(f"Número de linhas duplicadas: {duplicados.sum()}")

# Se desejar, você pode exibir as linhas duplicadas
#if duplicados.sum() > 0:
   # print("Linhas duplicadas:")
    #print(df[duplicados])

# Remover as linhas duplicadas
df_2 = df_1.drop_duplicates()

# Exibir o DataFrame após a remoção das duplicatas
#print(df_2)

# Gerar a tabela de estatística descritiva para todas as colunas (numéricas e não numéricas)
estatisticas_completas = df_2.describe(include='all')

# Exibir a tabela
#print(estatisticas_completas)

df_2.replace(["N/A", "NULL", ""], np.nan)

# Verificar a presença de valores faltantes no DataFrame
#print("Dados faltantes por coluna:")
#print(df_2.isnull().sum())

# Verificar se há valores NaN em todo o DataFrame
#print("\nTotal de valores faltantes no DataFrame:")
#print(df_2.isnull().sum().sum())

# Remover linhas que contêm qualquer valor faltante
df_3 = df_2.dropna(axis=0, how='any')

# Verificar novamente se há dados faltantes
#print("Dados faltantes após remoção de colunas com NaN:")
#print(df_3.isnull().sum())

# Gerar a tabela de estatística descritiva para todas as colunas (numéricas e não numéricas)
estatisticas_completas2 = df_3.describe(include='all')

# Exibir a tabela
#print(estatisticas_completas2)


df_3.columns = df_3.columns.str.strip().str.lower().str.replace(' ', '_').str.replace('(', '').str.replace(')', '')




# Definir a função para criar o tipo de categoria de comida com base no price_range
def create_price_type(price_range):
    if price_range == 1:
        return "cheap"
    elif price_range == 2:
        return "normal"
    elif price_range == 3:
        return "expensive"
    else:
        return "gourmet"

# Supondo que df já esteja carregado e contenha a coluna 'price_range'
# Aplicar a função ao DataFrame para criar uma nova coluna 'price_type'
df_3['price_type'] = df_3['price_range'].apply(create_price_type)

# Exibir o DataFrame com a nova coluna
#print(df_3[['price_range', 'price_type']])

#print(df_3)

df_4 = df_3



COUNTRIES = {
 1: "India",
 14: "Australia",
 30: "Brazil",
 37: "Canada",
 94: "Indonesia",
 148: "New Zeland",
 162: "Philippines",
 166: "Qatar",
 184: "Singapure",
 189: "South Africa",
 191: "Sri Lanka",
 208: "Turkey",
 214: "United Arab Emirates",
 215: "England",
 216: "United States of America",
 }
# Definir a função que retorna o nome do país com base no código
def country_name(country_code):
    return COUNTRIES.get(country_code, "Unknown")

# Aplicar a função ao DataFrame
df_4['country'] = df_4['country_code'].apply(country_name)

#print(df_4.head(3))


COLORS = {
 "3F7E00": "darkgreen",
 "5BA829": "green",
 "9ACD32": "lightgreen",
 "CDD614": "orange",
 "FFBA00": "red",
 "CBCBC8": "darkred",
 "FF7800": "darkred",
 }


# Definir a função que retorna o nome da cor com base no código
def color_name(rating_color):
    return COLORS.get(rating_color, "Unknown")

# Aplicar a função ao DataFrame

df_4['color_name'] = df_4['rating_color'].apply(color_name)

# Exibir as primeiras linhas do DataFrame para verificar o resultado
#print(df_4.head(5))



#################################################################################################### Geral##############################################
# 1. Quantos restaurantes únicos estão registrados? 5914


# Obter a quantidade de nomes de restaurantes únicos
num_unique_restaurants = df_4['restaurant_name'].nunique()

# Exibir o número de restaurantes únicos
#print(f"Número de restaurantes únicos: {num_unique_restaurants}")


# 2. Quantos países únicos estão registrados?15


# Obter a quantidade de países únicos
num_unique_countries = df_4['country'].nunique()

# Exibir o número de países únicos
#print(f"Número de países únicos: {num_unique_countries}")

# 3. Quantas cidades únicas estão registradas? 125

# Obter a quantidade de cidades únicos
num_unique_city = df_4['city'].nunique()

# Exibir o número de países únicos
#print(f"Número de cidades únicas: {num_unique_city}")


# 4. Qual o total de avaliações feitas?28648.0

# Calcular o total de aggregate_rating
total_aggregate_rating = df_4['aggregate_rating'].sum()

# Exibir o total de aggregate_rating
#print(f"Total de aggregate_rating: {total_aggregate_rating}")

# 5. Qual o total de tipos de culinária registrados?  ????



print(df_4.head(5))
###################################################################Pais#######################################################


 ##1. Qual o nome do país que possui mais cidades registradas?
 ##O país com mais cidades registradas é India, com 49 cidades.
 
 # Contar o número de cidades únicas por país
country_city_counts = df_4.groupby('country')['city'].nunique()

# Encontrar o país com o maior número de cidades registradas
max_cities_country = country_city_counts.idxmax()
max_cities_count = country_city_counts.max()

# Exibir o resultado
#print(f"O país com mais cidades registradas é {max_cities_country}, com {max_cities_count} cidades.")
 
### 2. Qual o nome do país que possui mais restaurantes registrados?
 ##O país com mais restaurantes registrados é India, com 2489 restaurantes.
 # Contar o número de restaurantes por país
country_restaurant_counts = df_4.groupby('country')['restaurant_name'].nunique()

# Encontrar o país com o maior número de restaurantes registrados
max_restaurants_country = country_restaurant_counts.idxmax()
max_restaurants_count = country_restaurant_counts.max()

# Exibir o resultado
#print(f"O país com mais restaurantes registrados é {max_restaurants_country}, com {max_restaurants_count} restaurantes.")
 
 ###3. Qual o nome do país que possui mais restaurantes com o nível de preço igual a 4 registrados?
 ##O país com mais restaurantes com nível de preço 4 registrados é United States of America, com 392 restaurantes.
  
  # Filtrar os restaurantes com nível de preço igual a 4
df_price_4 = df_4[df_4['price_range'] == 4]

# Contar o número de restaurantes com nível de preço 4 por país
country_price_4_counts = df_price_4.groupby('country')['restaurant_name'].nunique()

# Encontrar o país com o maior número de restaurantes com nível de preço 4
max_price_4_country = country_price_4_counts.idxmax()
max_price_4_count = country_price_4_counts.max()

# Exibir o resultado
#print(f"O país com mais restaurantes com nível de preço 4 registrados é {max_price_4_country}, com {max_price_4_count} restaurantes.")


  ### 4. Qual o nome do país que possui a maior quantidade de tipos de culinária distintos?
 
 

 ###5. Qual o nome do país que possui a maior quantidade de avaliações feitas?
 ##O país com a maior quantidade de avaliações feitas é India, com um total de 12565.9 avaliações.
 # Somar as avaliações (aggregate_rating) por país
country_rating_sums = df_4.groupby('country')['aggregate_rating'].sum()

# Encontrar o país com a maior quantidade de avaliações feitas
max_rating_country = country_rating_sums.idxmax()
max_rating_sum = country_rating_sums.max()

# Exibir o resultado
##print(f"O país com a maior quantidade de avaliações feitas é {max_rating_country}, com um total de {max_rating_sum} avaliações.")
 
 ###6. Qual o nome do país que possui a maior quantidade de restaurantes que fazem entrega?

 ##O país com mais restaurantes que fazem entrega é India, com 1793 restaurantes.
 
 # Filtrar os restaurantes que fazem entrega (has_online_delivery = 1)
df_delivery = df_4[df_4['has_online_delivery'] == 1]

# Contar o número de restaurantes que fazem entrega por país
country_delivery_counts = df_delivery.groupby('country')['restaurant_name'].nunique()

# Encontrar o país com o maior número de restaurantes que fazem entrega
max_delivery_country = country_delivery_counts.idxmax()
max_delivery_count = country_delivery_counts.max()

# Exibir o resultado
#mprint(f"O país com mais restaurantes que fazem entrega é {max_delivery_country}, com {max_delivery_count} restaurantes.")
 
 ###7. Qual o nome do país que possui a maior quantidade de restaurantes que aceitam reservas?

## O país com mais restaurantes que aceitam reservas é India, com 198 restaurantes.

 # Filtrar os restaurantes que aceitam reservas (has_table_booking = 1)
df_reservas = df_4[df_4['has_table_booking'] == 1]

# Contar o número de restaurantes que aceitam reservas por país
country_reservas_counts = df_reservas.groupby('country')['restaurant_name'].nunique()

# Encontrar o país com o maior número de restaurantes que aceitam reservas
max_reservas_country = country_reservas_counts.idxmax()
max_reservas_count = country_reservas_counts.max()

# Exibir o resultado
#print(f"O país com mais restaurantes que aceitam reservas é {max_reservas_country}, com {max_reservas_count} restaurantes.")
 
 
 ##8. Qual o nome do país que possui, na média, a maior quantidade de avaliações registrada?   ??????????
 ##O país com a maior média de avaliações registradas é Indonesia, com uma média de 4.60 avaliações.

 # Calcular a média das avaliações (aggregate_rating) por país
country_avg_rating = df_4.groupby('country')['aggregate_rating'].mean()

# Encontrar o país com a maior média de avaliações
max_avg_rating_country = country_avg_rating.idxmax()
max_avg_rating = country_avg_rating.max()

# Exibir o resultado
#print(f"O país com a maior média de avaliações registradas é {max_avg_rating_country}, com uma média de {max_avg_rating:.2f} avaliações.")

 ##9. Qual o nome do país que possui, na média, a maior nota média registrada?

 ##O país com a maior nota média registrada é Indonesia, com uma nota média de 4.60.

 # Calcular a média das notas (aggregate_rating) por país
country_avg_rating = df_4.groupby('country')['aggregate_rating'].mean()

# Encontrar o país com a maior nota média
max_avg_rating_country = country_avg_rating.idxmax()
max_avg_rating = country_avg_rating.max()

# Exibir o resultado
print(f"O país com a maior nota média registrada é {max_avg_rating_country}, com uma nota média de {max_avg_rating:.2f}.")
 
 
 ##10. Qual o nome do país que possui, na média, a menor nota média registrada?

##O país com a menor nota média registrada é Brazil, com uma nota média de 3.32.

 # Calcular a média das notas (aggregate_rating) por país
country_avg_rating = df_4.groupby('country')['aggregate_rating'].mean()

# Encontrar o país com a menor nota média
min_avg_rating_country = country_avg_rating.idxmin()
min_avg_rating = country_avg_rating.min()

# Exibir o resultado
##print(f"O país com a menor nota média registrada é {min_avg_rating_country}, com uma nota média de {min_avg_rating:.2f}.")
 
 
 ##11. Qual a média de preço de um prato para dois por país?


'''   ?????????? 
Australia                   138959.783333
Brazil                         138.812500
Canada                          41.861111
England                         43.510000
India                          703.602564
Indonesia                   303000.000000
New Zeland                      62.154812
Philippines                   1227.825000
Qatar                          174.000000
Singapure                      141.437500
South Africa                   339.228324
Sri Lanka                     2579.375000
Turkey                         128.584906
United Arab Emirates           153.716667
United States of America        55.018868
'''

 # Calcular a média do preço para dois por país
country_avg_cost_for_two = df_4.groupby('country')['average_cost_for_two'].mean()

# Exibir o resultado
#print(country_avg_cost_for_two)