
# %% [markdown]
# # importacao 

# %%
import pandas as pd
import numpy as np




# %%
## importaçao do csv
################################
df = pd.read_csv('C:/Users/Victor/Desktop/CC/CDS/python/ProjetoFinal/zomato.csv', encoding="utf-8", engine='python')


# Ajustar para mostrar todas as colunas
pd.set_option('display.max_columns', None)


# %% [markdown]
# # Tratamento de dados 

# %% [markdown]
# ### Remover colunas com unico valor 

# %%
# Identificar colunas com um único valor
cols_to_remove = [col for col in df.columns if df[col].nunique() == 1]

# Remover essas colunas do DataFrame
df_1 = df.drop(columns=cols_to_remove)

# Exibir as colunas removidas
#print("Colunas removidas:", cols_to_remove)

# Exibir o DataFrame após a remoção
#print(df_1)

# %% [markdown]
# ### dados duplicados

# %%

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

# %%
##df_1.isna().sum()

# %%
# df_2.replace(["N/A", "NULL", ""], np.nan)## essa linha não faz diferenca

# Remover linhas que contêm qualquer valor faltante
df_3 = df_2.dropna(axis=0, how='any')

# %% [markdown]
# ### estatisticas 

# %%
# Gerar a tabela de estatística descritiva para todas as colunas (numéricas e não numéricas)
estatisticas_completas2 = df_3.describe(exclude='object')

##?Display(estatisticas_completas2)


# %% [markdown]
# ### replace 

# %%
df_3.columns = df_3.columns.str.strip().str.lower().str.replace(' ', '_').str.replace('(', '').str.replace(')', '')

# %%
# df_3.columns

# %% [markdown]
# ###  criar uma nova coluna 'price_type'

# %%
# Ajustar para mostrar todas as colunas
pd.set_option('display.max_columns', None)



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

print(df_3.head(3))

df_4 = df_3


# %% [markdown]
# ### PAIS

# %%
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


print(df_4.head(3))

# %% [markdown]
# ### CORES

# %%
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

print(df_4.head(3))

# %% [markdown]
# ### categorizar

# %%
# Categorizar os restaurantes por apenas um tipo de culinária (o primeiro da lista)
df_4["cuisines"] = df_4["cuisines"].apply(lambda x: x.split(",")[0])

# Exibir o resultado para verificar a nova categorização
print(df_4[['restaurant_name', 'cuisines']].head())

# %% [markdown]
# # Geral
# 

# %%
# 1. Quantos restaurantes únicos estão registrados? 


# Obter a quantidade de nomes de restaurantes únicos
num_unique_restaurants = df_4['restaurant_name'].nunique()

# Exibir o número de restaurantes únicos
print(f"Número de restaurantes únicos: {num_unique_restaurants}")


# 2. Quantos países únicos estão registrados?15


# Obter a quantidade de países únicos
num_unique_countries = df_4['country'].nunique()

# Exibir o número de países únicos
print(f"Número de países únicos: {num_unique_countries}")

# 3. Quantas cidades únicas estão registradas? 125

# Obter a quantidade de cidades únicos
num_unique_city = df_4['city'].nunique()

# Exibir o número de países únicos
print(f"Número de cidades únicas: {num_unique_city}")


# 4. Qual o total de avaliações feitas?

# Calcular o total de aggregate_rating
total_aggregate_rating = df_4['aggregate_rating'].count()

# Exibir o total de aggregate_rating
print(f"Total de aggregate_rating: {total_aggregate_rating}")

# 5. Qual o total de tipos de culinária registrados?  ????

# Contar o número de tipos de culinária únicos
total_unique_cuisines = df_4["cuisines"].nunique()

# Exibir o resultado
print(f"O total de tipos de culinária registrados é: {total_unique_cuisines}")

# %% [markdown]
# # Pais

# %%
##1. Qual o nome do país que possui mais cidades registradas?

 # Contar o número de cidades únicas por país
country_city_counts = df_4.groupby('country')['city'].nunique()

# Encontrar o país com o maior número de cidades registradas
max_cities_country = country_city_counts.idxmax()
max_cities_count = country_city_counts.max()

# Exibir o resultado
print(f"O país com mais cidades registradas é {max_cities_country}, com {max_cities_count} cidades.")
 
### 2. Qual o nome do país que possui mais restaurantes registrados?

 # Contar o número de restaurantes por país
country_restaurant_counts = df_4.groupby('country')['restaurant_name'].nunique()

# Encontrar o país com o maior número de restaurantes registrados
max_restaurants_country = country_restaurant_counts.idxmax()
max_restaurants_count = country_restaurant_counts.max()

# Exibir o resultado
print(f"O país com mais restaurantes registrados é {max_restaurants_country}, com {max_restaurants_count} restaurantes.")
 
 ###3. Qual o nome do país que possui mais restaurantes com o nível de preço igual a 4 registrados?
 
  
  # Filtrar os restaurantes com nível de preço igual a 4
df_price_4 = df_4[df_4['price_range'] == 4]

# Contar o número de restaurantes com nível de preço 4 por país
country_price_4_counts = df_price_4.groupby('country')['restaurant_name'].nunique()

# Encontrar o país com o maior número de restaurantes com nível de preço 4
max_price_4_country = country_price_4_counts.idxmax()
max_price_4_count = country_price_4_counts.max()

# Exibir o resultado
print(f"O país com mais restaurantes com nível de preço 4 registrados é {max_price_4_country}, com {max_price_4_count} restaurantes.")


  ### 4. Qual o nome do país que possui a maior quantidade de tipos de culinária distintos?
 
  # Contar o número de tipos de culinária distintos por país
cuisines_by_country = df_4.groupby('country')['cuisines'].nunique()

# Encontrar o país com a maior quantidade de tipos de culinária distintos
max_cuisines_country = cuisines_by_country.idxmax()
max_cuisines_count = cuisines_by_country.max()

# Exibir o resultado
print(f"O país com a maior quantidade de tipos de culinária distintos é {max_cuisines_country}, com {max_cuisines_count} tipos de culinária.")
 
 

 ###5. Qual o nome do país que possui a maior quantidade de avaliações feitas?
 
 # Somar as avaliações (aggregate_rating) por país
country_rating_sums = df_4.groupby('country')['aggregate_rating'].count()

# Encontrar o país com a maior quantidade de avaliações feitas
max_rating_country = country_rating_sums.idxmax()
max_rating_sum = country_rating_sums.max()

# Exibir o resultado
print(f"O país com a maior quantidade de avaliações feitas é {max_rating_country}, com um total de {max_rating_sum} avaliações.")
 
 ###6. Qual o nome do país que possui a maior quantidade de restaurantes que fazem entrega?

 
 
 # Filtrar os restaurantes que fazem entrega (has_online_delivery = 1)
df_delivery = df_4[df_4['has_online_delivery'] == 1]

# Contar o número de restaurantes que fazem entrega por país
country_delivery_counts = df_delivery.groupby('country')['restaurant_name'].nunique()

# Encontrar o país com o maior número de restaurantes que fazem entrega
max_delivery_country = country_delivery_counts.idxmax()
max_delivery_count = country_delivery_counts.max()

# Exibir o resultado
print(f"O país com mais restaurantes que fazem entrega é {max_delivery_country}, com {max_delivery_count} restaurantes.")
 
 ###7. Qual o nome do país que possui a maior quantidade de restaurantes que aceitam reservas?



 # Filtrar os restaurantes que aceitam reservas (has_table_booking = 1)
df_reservas = df_4[df_4['has_table_booking'] == 1]

# Contar o número de restaurantes que aceitam reservas por país
country_reservas_counts = df_reservas.groupby('country')['restaurant_name'].nunique()

# Encontrar o país com o maior número de restaurantes que aceitam reservas
max_reservas_country = country_reservas_counts.idxmax()
max_reservas_count = country_reservas_counts.max()

# Exibir o resultado
print(f"O país com mais restaurantes que aceitam reservas é {max_reservas_country}, com {max_reservas_count} restaurantes.")
 
 
 ##8. Qual o nome do país que possui, na média, a maior quantidade de avaliações registrada?   ??????????
 

 # Calcular a média das avaliações (aggregate_rating) por país
country_avg_rating = df_4.groupby('country')['aggregate_rating'].count()

# Encontrar o país com a maior média de avaliações
max_avg_rating_country = country_avg_rating.idxmax()
max_avg_rating = country_avg_rating.max()

# Exibir o resultado
print(f"O país com a maior média de avaliações registradas é {max_avg_rating_country}, com uma média de {max_avg_rating:.2f} avaliações.")

 ##9. Qual o nome do país que possui, na média, a maior nota média registrada?



 # Calcular a média das notas (aggregate_rating) por país
country_avg_rating = df_4.groupby('country')['aggregate_rating'].mean()

# Encontrar o país com a maior nota média
max_avg_rating_country = country_avg_rating.idxmax()
max_avg_rating = country_avg_rating.max()

# Exibir o resultado
print(f"O país com a maior nota média registrada é {max_avg_rating_country}, com uma nota média de {max_avg_rating:.2f}.")
 
 
 ##10. Qual o nome do país que possui, na média, a menor nota média registrada?

#
 # Calcular a média das notas (aggregate_rating) por país
country_avg_rating = df_4.groupby('country')['aggregate_rating'].mean()

# Encontrar o país com a menor nota média
min_avg_rating_country = country_avg_rating.idxmin()
min_avg_rating = country_avg_rating.min()

# Exibir o resultado
print(f"O país com a menor nota média registrada é {min_avg_rating_country}, com uma nota média de {min_avg_rating:.2f}.")
 
 
 ##11. Qual a média de preço de um prato para dois por país?




 # Calcular a média do preço para dois por país
country_avg_cost_for_two = df_4.groupby('country')['average_cost_for_two'].mean()

# Exibir o resultado
print(country_avg_cost_for_two)

# %% [markdown]
# # Cidade
# 

# %%


# Cidade
#  1. Qual o nome da cidade que possui mais restaurantes registrados?

# Contar o número de restaurantes por cidade
restaurants_by_city = df_4['city'].value_counts()

# Encontrar a cidade com o maior número de restaurantes registrados
city_with_most_restaurants = restaurants_by_city.idxmax()
most_restaurants_count = restaurants_by_city.max()

# Exibir o resultado
print(f"A cidade com mais restaurantes registrados é {city_with_most_restaurants}, com {most_restaurants_count} restaurantes.")

#  2. Qual o nome da cidade que possui mais restaurantes com nota média acima de  4?

# Filtrar os restaurantes com nota média acima de 4
high_rated_restaurants = df_4[df_4['aggregate_rating'] > 4]

# Contar o número de restaurantes por cidade entre os restaurantes filtrados
restaurants_by_city_high_ratings = high_rated_restaurants['city'].value_counts()

# Encontrar a cidade com o maior número de restaurantes com nota média acima de 4          
city_with_most_high_rated_restaurants = restaurants_by_city_high_ratings.idxmax()
most_high_rated_restaurants_count = restaurants_by_city_high_ratings.max()

# Exibir o resultado
print(f"A cidade com mais restaurantes com nota média acima de 4 é {city_with_most_high_rated_restaurants},com {most_high_rated_restaurants_count} restaurantes.")

#  3. Qual o nome da cidade que possui mais restaurantes com nota média abaixo de  2.5?

# Filtrar os restaurantes com nota média abaixo de 2.5
low_rated_restaurants = df_4[df_4['aggregate_rating'] < 2.5]

# Contar o número de restaurantes por cidade entre os restaurantes filtrados
restaurants_by_city_low_ratings = low_rated_restaurants['city'].value_counts()

# Encontrar a cidade com o maior número de restaurantes com nota média abaixo de 2.5
city_with_most_low_rated_restaurants = restaurants_by_city_low_ratings.idxmax()
most_low_rated_restaurants_count = restaurants_by_city_low_ratings.max()

# Exibir o resultado
print(f"A cidade com mais restaurantes com nota média abaixo de 2.5 é {city_with_most_low_rated_restaurants}, com {most_low_rated_restaurants_count} restaurantes.")

#  4. Qual o nome da cidade que possui o maior valor médio de um prato para dois?

# Calcular o valor médio de um prato para dois por cidade
avg_cost_by_city = df_4.groupby('city')['average_cost_for_two'].mean()

# Encontrar a cidade com o maior valor médio de um prato para dois
city_with_highest_avg_cost = avg_cost_by_city.idxmax()
highest_avg_cost = avg_cost_by_city.max()

# Exibir o resultado
print(f"A cidade com o maior valor médio de um prato para dois é {city_with_highest_avg_cost}, com um valor médio de {highest_avg_cost:.2f}.")


# 5. Qual o nome da cidade que possui a maior quantidade de tipos de culinária  distintas?

# Contar o número de tipos de culinária distintos por cidade
cuisines_by_city = df_4.groupby('city')['cuisines'].nunique()

# Encontrar a cidade com o maior número de tipos de culinária distintos
city_with_most_cuisines = cuisines_by_city.idxmax()
most_cuisines_count = cuisines_by_city.max()

# Exibir o resultado
print(f"A cidade com a maior quantidade de tipos de culinária distintos é {city_with_most_cuisines}, com {most_cuisines_count} tipos de culinária.")

#  6. Qual o nome da cidade que possui a maior quantidade de restaurantes que fazem  reservas?

# Filtrar os restaurantes que aceitam reservas
restaurants_with_booking = df_4[df_4['has_table_booking'] == 1]

# Contar o número de restaurantes que aceitam reservas por cidade
restaurants_by_city_with_booking = restaurants_with_booking['city'].value_counts()

# Encontrar a cidade com o maior número de restaurantes que aceitam reservas
city_with_most_restaurants_with_booking = restaurants_by_city_with_booking.idxmax()
most_restaurants_with_booking_count = restaurants_by_city_with_booking.max()

# Exibir o resultado
print(f"A cidade com mais restaurantes que fazem reservas é {city_with_most_restaurants_with_booking}, com {most_restaurants_with_booking_count} restaurantes.")

#  7. Qual o nome da cidade que possui a maior quantidade de restaurantes que fazem  entregas?

# Filtrar os restaurantes que fazem entregas
restaurants_with_delivery = df_4[df_4['is_delivering_now'] == 1]

# Contar o número de restaurantes que fazem entregas por cidade
restaurants_by_city_with_delivery = restaurants_with_delivery['city'].value_counts()

# Encontrar a cidade com o maior número de restaurantes que fazem entregas
city_with_most_restaurants_with_delivery = restaurants_by_city_with_delivery.idxmax()
most_restaurants_with_delivery_count = restaurants_by_city_with_delivery.max()

# Exibir o resultado
print(f"A cidade com mais restaurantes que fazem entregas é {city_with_most_restaurants_with_delivery}, com {most_restaurants_with_delivery_count} restaurantes.")



#  8. Qual o nome da cidade que possui a maior quantidade de restaurantes que  aceitam pedidos online?

# Filtrar os restaurantes que aceitam pedidos online
restaurants_with_online_orders = df_4[df_4['has_online_delivery'] == 1]

# Contar o número de restaurantes que aceitam pedidos online por cidade
restaurants_by_city_with_online_orders = restaurants_with_online_orders['city'].value_counts()

# Encontrar a cidade com o maior número de restaurantes que aceitam pedidos online
city_with_most_restaurants_with_online_orders = restaurants_by_city_with_online_orders.idxmax()
most_restaurants_with_online_orders_count = restaurants_by_city_with_online_orders.max()

# Exibir o resultado
print(f"A cidade com mais restaurantes que aceitam pedidos online é {city_with_most_restaurants_with_online_orders}, com {most_restaurants_with_online_orders_count} restaurantes.")

# %% [markdown]
# # Restaurante 

# %%
# Restaurantes
#  1. Qual o nome do restaurante que possui a maior quantidade de avaliações?

# Ordenar os restaurantes pelo número de avaliações (votes) em ordem decrescente
restaurant_with_most_votes = df_4.loc[df_4['votes'].idxmax()]

# Exibir o nome do restaurante e o número de avaliações
print(f"O restaurante com a maior quantidade de avaliações é {restaurant_with_most_votes['restaurant_name']}, com {restaurant_with_most_votes['votes']} avaliações.")


#  2. Qual o nome do restaurante com a maior nota média?

# Ordenar os restaurantes pela maior nota média (aggregate_rating) em ordem decrescente
restaurant_with_highest_rating = df_4.loc[df_4['aggregate_rating'].idxmax()]

# Exibir o nome do restaurante e a nota média
print(f"O restaurante com a maior nota média é {restaurant_with_highest_rating['restaurant_name']}, com nota {restaurant_with_highest_rating['aggregate_rating']}.")



#  3. Qual o nome do restaurante que possui o maior valor de uma prato para duas  pessoas?

# Ordenar os restaurantes pelo maior valor de um prato para duas pessoas (average_cost_for_two) em ordem decrescente
restaurant_with_highest_cost = df_4.loc[df_4['average_cost_for_two'].idxmax()]

# Exibir o nome do restaurante e o valor de um prato para duas pessoas
print(f"O restaurante com o maior valor de um prato para duas pessoas é {restaurant_with_highest_cost['restaurant_name']}, com o valor de {restaurant_with_highest_cost['average_cost_for_two']}.")


#  4. Qual o nome do restaurante de tipo de culinária brasileira que possui a menor  média de avaliação?

# Filtrar os restaurantes de culinária brasileira
brazilian_cuisine_restaurants = df_4[df_4['cuisines'] == 'Brazilian']

# Encontrar o restaurante com a menor média de avaliação (aggregate_rating)
restaurant_with_lowest_rating = brazilian_cuisine_restaurants.loc[brazilian_cuisine_restaurants['aggregate_rating'].idxmin()]

# Exibir o nome do restaurante e a nota média
print(f"O restaurante de culinária brasileira com a menor média de avaliação é {restaurant_with_lowest_rating['restaurant_name']}, com nota {restaurant_with_lowest_rating['aggregate_rating']}.")



#  5. Qual o nome do restaurante de tipo de culinária brasileira, e que é do Brasil, que  possui a maior média de avaliação?

# Filtrar os restaurantes de culinária brasileira localizados no Brasil
brazilian_cuisine_brazil = df_4[(df_4['cuisines'] == 'Brazilian') & (df_4['country'] == 'Brazil')]

# Encontrar o restaurante com a maior média de avaliação (aggregate_rating)
restaurant_with_highest_rating = brazilian_cuisine_brazil.loc[brazilian_cuisine_brazil['aggregate_rating'].idxmax()]

# Exibir o nome do restaurante e a nota média
print(f"O restaurante de culinária brasileira, localizado no Brasil, com a maior média de avaliação é {restaurant_with_highest_rating['restaurant_name']}, com nota {restaurant_with_highest_rating['aggregate_rating']}.")


#  6. Os restaurantes que aceitam pedido online são também, na média, os  restaurantes que mais possuem avaliações registradas?

# Filtrar os restaurantes que aceitam pedidos online (has_online_delivery = 1)
online_delivery_restaurants = df_4[df_4['has_online_delivery'] == 1]

# Filtrar os restaurantes que não aceitam pedidos online (has_online_delivery = 0)
no_online_delivery_restaurants = df_4[df_4['has_online_delivery'] == 0]

# Calcular a média de avaliações (votes) para restaurantes que aceitam pedidos online
mean_votes_online_delivery = online_delivery_restaurants['votes'].mean()

# Calcular a média de avaliações (votes) para restaurantes que não aceitam pedidos online
mean_votes_no_online_delivery = no_online_delivery_restaurants['votes'].mean()

# Exibir os resultados
print(f"Média de avaliações para restaurantes que aceitam pedidos online: {mean_votes_online_delivery:.2f}")
print(f"Média de avaliações para restaurantes que não aceitam pedidos online: {mean_votes_no_online_delivery:.2f}")

# Verificar se a média dos restaurantes que aceitam pedidos online é maior
if mean_votes_online_delivery > mean_votes_no_online_delivery:
    print("Sim, os restaurantes que aceitam pedidos online possuem, na média, mais avaliações registradas.")
else:
    print("Não, os restaurantes que aceitam pedidos online não possuem, na média, mais avaliações registradas.")



#  7. Os restaurantes que fazem reservas são também, na média, os restaurantes que  possuem o maior valor médio de um prato para duas pessoas?

# Filtrar os restaurantes que aceitam reservas (has_table_booking = 1)
restaurants_with_reservations = df_4[df_4['has_table_booking'] == 1]

# Filtrar os restaurantes que não aceitam reservas (has_table_booking = 0)
restaurants_without_reservations = df_4[df_4['has_table_booking'] == 0]

# Calcular o valor médio de um prato para duas pessoas para restaurantes que aceitam reservas
mean_cost_with_reservations = restaurants_with_reservations['average_cost_for_two'].mean()

# Calcular o valor médio de um prato para duas pessoas para restaurantes que não aceitam reservas
mean_cost_without_reservations = restaurants_without_reservations['average_cost_for_two'].mean()

# Exibir os resultados
print(f"Valor médio de um prato para duas pessoas para restaurantes que aceitam reservas: {mean_cost_with_reservations:.2f}")
print(f"Valor médio de um prato para duas pessoas para restaurantes que não aceitam reservas: {mean_cost_without_reservations:.2f}")

# Verificar se os restaurantes que aceitam reservas possuem o maior valor médio
if mean_cost_with_reservations > mean_cost_without_reservations:
    print("Sim, os restaurantes que fazem reservas possuem, na média, o maior valor médio de um prato para duas pessoas.")
else:
    print("Não, os restaurantes que fazem reservas não possuem, na média, o maior valor médio de um prato para duas pessoas.")




#  8. Os restaurantes do tipo de culinária japonesa dos Estados Unidos da América
#   possuem um valor médio de prato para duas pessoas maior que as churrascarias
#  americanas (BBQ)?

# Filtrar os restaurantes localizados nos Estados Unidos da América
us_restaurants = df_4[df_4['country'] == 'United States of America']

# Filtrar os restaurantes de culinária japonesa
japanese_restaurants = us_restaurants[us_restaurants['cuisines'].str.contains('Japanese', case=False)]

# Filtrar as churrascarias (BBQ)
bbq_restaurants = us_restaurants[us_restaurants['cuisines'].str.contains('BBQ', case=False)]

# Calcular o valor médio de um prato para duas pessoas para restaurantes japoneses
mean_cost_japanese = japanese_restaurants['average_cost_for_two'].mean()

# Calcular o valor médio de um prato para duas pessoas para churrascarias (BBQ)
mean_cost_bbq = bbq_restaurants['average_cost_for_two'].mean()

# Exibir os resultados
print(f"Valor médio de um prato para duas pessoas em restaurantes japoneses nos EUA: {mean_cost_japanese:.2f}")
print(f"Valor médio de um prato para duas pessoas em churrascarias (BBQ) nos EUA: {mean_cost_bbq:.2f}")

# Verificar qual tipo de culinária possui o maior valor médio
if mean_cost_japanese > mean_cost_bbq:
    print("Sim, os restaurantes de culinária japonesa nos EUA possuem um valor médio de prato para duas pessoas maior que as churrascarias (BBQ).")
else:
    print("Não, as churrascarias (BBQ) nos EUA possuem um valor médio de prato para duas pessoas maior que os restaurantes de culinária japonesa.")

# %% [markdown]
# # Culinária 
# 
# 

# %%


# Tipos de Culinária
#  1. Dos restaurantes que possuem o tipo de culinária italiana, qual o nome do
#  restaurante com a maior média de avaliação?
# Filtrar os restaurantes que possuem culinária italiana
italian_restaurants = df_4[df_4['cuisines'].str.contains('Italian', case=False)]

# Ordenar os restaurantes pela média de avaliação (aggregate_rating) de forma decrescente
italian_restaurants_sorted = italian_restaurants.sort_values(by='aggregate_rating', ascending=False)

# Selecionar o restaurante com a maior média de avaliação
top_italian_restaurant = italian_restaurants_sorted.iloc[0]

# Exibir o nome do restaurante e sua média de avaliação
print(f"O restaurante de culinária italiana com a maior média de avaliação é {top_italian_restaurant['restaurant_name']} com uma média de {top_italian_restaurant['aggregate_rating']}.")



#  2. Dos restaurantes que possuem o tipo de culinária italiana, qual o nome do
#  restaurante com a menor média de avaliação?


# Filtrar os restaurantes que possuem culinária italiana
italian_restaurants = df_4[df_4['cuisines'].str.contains('Italian', case=False)]

# Ordenar os restaurantes pela média de avaliação (aggregate_rating) de forma crescente
italian_restaurants_sorted = italian_restaurants.sort_values(by='aggregate_rating', ascending=True)

# Selecionar o restaurante com a menor média de avaliação
bottom_italian_restaurant = italian_restaurants_sorted.iloc[0]

# Exibir o nome do restaurante e sua média de avaliação
print(f"O restaurante de culinária italiana com a menor média de avaliação é {bottom_italian_restaurant['restaurant_name']} com uma média de {bottom_italian_restaurant['aggregate_rating']}.")


#  3. Dos restaurantes que possuem o tipo de culinária americana, qual o nome do
#  restaurante com a maior média de avaliação?

# Filtrar os restaurantes que possuem culinária americana
american_restaurants = df_4[df_4['cuisines'].str.contains('American', case=False)]

# Ordenar os restaurantes pela média de avaliação (aggregate_rating) de forma decrescente
american_restaurants_sorted = american_restaurants.sort_values(by='aggregate_rating', ascending=False)

# Selecionar o restaurante com a maior média de avaliação
top_american_restaurant = american_restaurants_sorted.iloc[0]

# Exibir o nome do restaurante e sua média de avaliação
print(f"O restaurante de culinária americana com a maior média de avaliação é {top_american_restaurant['restaurant_name']} com uma média de {top_american_restaurant['aggregate_rating']}.")


#  4. Dos restaurantes que possuem o tipo de culinária americana, qual o nome do
#  restaurante com a menor média de avaliação?

# Filtrar os restaurantes que possuem culinária americana
american_restaurants = df_4[df_4['cuisines'].str.contains('American', case=False)]

# Ordenar os restaurantes pela média de avaliação (aggregate_rating) de forma crescente
american_restaurants_sorted = american_restaurants.sort_values(by='aggregate_rating', ascending=True)

# Selecionar o restaurante com a menor média de avaliação
bottom_american_restaurant = american_restaurants_sorted.iloc[0]

# Exibir o nome do restaurante e sua média de avaliação
print(f"O restaurante de culinária americana com a menor média de avaliação é {bottom_american_restaurant['restaurant_name']} com uma média de {bottom_american_restaurant['aggregate_rating']}.")


#  5. Dos restaurantes que possuem o tipo de culinária árabe, qual o nome do
#  restaurante com a maior média de avaliação?

# Filtrar os restaurantes que possuem culinária árabe
arabic_restaurants = df_4[df_4['cuisines'].str.contains('Arabian', case=False)]

# Ordenar os restaurantes pela média de avaliação (aggregate_rating) de forma decrescente
arabic_restaurants_sorted = arabic_restaurants.sort_values(by='aggregate_rating', ascending=False)

# Selecionar o restaurante com a maior média de avaliação
top_arabic_restaurant = arabic_restaurants_sorted.iloc[0]

# Exibir o nome do restaurante e sua média de avaliação
print(f"O restaurante de culinária árabe com a maior média de avaliação é {top_arabic_restaurant['restaurant_name']} com uma média de {top_arabic_restaurant['aggregate_rating']}.")

#  6. Dos restaurantes que possuem o tipo de culinária árabe, qual o nome do
#  restaurante com a menor média de avaliação?

# Filtrar os restaurantes que possuem culinária árabe (Arabian)
arabic_restaurants = df_4[df_4['cuisines'].str.contains('Arabian', case=False)]

# Ordenar os restaurantes pela média de avaliação (aggregate_rating) de forma crescente
arabic_restaurants_sorted = arabic_restaurants.sort_values(by='aggregate_rating', ascending=True)

# Selecionar o restaurante com a menor média de avaliação
bottom_arabic_restaurant = arabic_restaurants_sorted.iloc[0]

# Exibir o nome do restaurante e sua média de avaliação
print(f"O restaurante de culinária árabe com a menor média de avaliação é {bottom_arabic_restaurant['restaurant_name']} com uma média de {bottom_arabic_restaurant['aggregate_rating']}.")



#  7. Dos restaurantes que possuem o tipo de culinária japonesa, qual o nome do
#  restaurante com a maior média de avaliação?

# Filtrar os restaurantes que possuem culinária japonesa
japanese_restaurants = df_4[df_4['cuisines'].str.contains('Japanese', case=False)]

# Ordenar os restaurantes pela média de avaliação (aggregate_rating) de forma decrescente
japanese_restaurants_sorted = japanese_restaurants.sort_values(by='aggregate_rating', ascending=False)

# Selecionar o restaurante com a maior média de avaliação
top_japanese_restaurant = japanese_restaurants_sorted.iloc[0]

# Exibir o nome do restaurante e sua média de avaliação
print(f"O restaurante de culinária japonesa com a maior média de avaliação é {top_japanese_restaurant['restaurant_name']} com uma média de {top_japanese_restaurant['aggregate_rating']}.")


#  8. Dos restaurantes que possuem o tipo de culinária japonesa, qual o nome do
#  restaurante com a menor média de avaliação?

# Filtrar os restaurantes que possuem culinária japonesa
japanese_restaurants = df_4[df_4['cuisines'].str.contains('Japanese', case=False)]

# Ordenar os restaurantes pela média de avaliação (aggregate_rating) de forma crescente
japanese_restaurants_sorted = japanese_restaurants.sort_values(by='aggregate_rating', ascending=True)

# Selecionar o restaurante com a menor média de avaliação
bottom_japanese_restaurant = japanese_restaurants_sorted.iloc[0]

# Exibir o nome do restaurante e sua média de avaliação
print(f"O restaurante de culinária japonesa com a menor média de avaliação é {bottom_japanese_restaurant['restaurant_name']} com uma média de {bottom_japanese_restaurant['aggregate_rating']}.")



#  9. Dos restaurantes que possuem o tipo de culinária caseira, qual o nome do
#  restaurante com a maior média de avaliação?

# Filtrar os restaurantes que possuem culinária caseira
home_cooked_restaurants = df_4[df_4['cuisines'].str.contains('Home', case=False)]

# Ordenar os restaurantes pela média de avaliação (aggregate_rating) de forma decrescente
home_cooked_restaurants_sorted = home_cooked_restaurants.sort_values(by='aggregate_rating', ascending=False)

# Selecionar o restaurante com a maior média de avaliação
top_home_cooked_restaurant = home_cooked_restaurants_sorted.iloc[0]

# Exibir o nome do restaurante e sua média de avaliação
print(f"O restaurante de culinária caseira com a maior média de avaliação é {top_home_cooked_restaurant['restaurant_name']} com uma média de {top_home_cooked_restaurant['aggregate_rating']}.")





#  10. Dos restaurantes que possuem o tipo de culinária caseira, qual o nome do
#  restaurante com a menor média de avaliação?



# Filtrar os restaurantes que possuem culinária caseira
home_cooked_restaurants = df_4[df_4['cuisines'].str.contains('Home', case=False)]

# Ordenar os restaurantes pela média de avaliação (aggregate_rating) de forma crescente
home_cooked_restaurants_sorted = home_cooked_restaurants.sort_values(by='aggregate_rating', ascending=True)

# Selecionar o restaurante com a menor média de avaliação
bottom_home_cooked_restaurant = home_cooked_restaurants_sorted.iloc[0]

# Exibir o nome do restaurante e sua média de avaliação
print(f"O restaurante de culinária caseira com a menor média de avaliação é {bottom_home_cooked_restaurant['restaurant_name']} com uma média de {bottom_home_cooked_restaurant['aggregate_rating']}.")



#  11. Qual o tipo de culinária que possui o maior valor médio de um prato para duas
#  pessoas?
# Extrair o primeiro tipo de culinária se houver mais de um
df_4['cuisines'] = df_4['cuisines'].apply(lambda x: x.split(",")[0])

# Agrupar o DataFrame pelo tipo de culinária e calcular a média do valor de um prato para duas pessoas
average_cost_by_cuisine = df_4.groupby('cuisines')['average_cost_for_two'].mean()

# Encontrar o tipo de culinária com o maior valor médio
most_expensive_cuisine = average_cost_by_cuisine.idxmax()
most_expensive_value = average_cost_by_cuisine.max()

# Exibir o tipo de culinária e o valor médio
print(f"O tipo de culinária que possui o maior valor médio de um prato para duas pessoas é {most_expensive_cuisine} com um valor médio de {most_expensive_value}.")


#  12. Qual o tipo de culinária que possui a maior nota média?
# Extrair o primeiro tipo de culinária se houver mais de um
df_4['cuisines'] = df_4['cuisines'].apply(lambda x: x.split(",")[0])

# Agrupar o DataFrame pelo tipo de culinária e calcular a média das notas
average_rating_by_cuisine = df_4.groupby('cuisines')['aggregate_rating'].mean()

# Encontrar o tipo de culinária com a maior nota média
highest_rating_cuisine = average_rating_by_cuisine.idxmax()
highest_rating_value = average_rating_by_cuisine.max()

# Exibir o tipo de culinária e a nota média
print(f"O tipo de culinária que possui a maior nota média é {highest_rating_cuisine} com uma nota média de {highest_rating_value:.2f}.")



#  13. Qual o tipo de culinária que possui mais restaurantes que aceitam pedidos
#  online e fazem entregas?

# Filtrar os restaurantes que aceitam pedidos online e fazem entregas
online_delivery_restaurants = df_4[(df_4['has_online_delivery'] == 1) & (df_4['has_table_booking'] == 1)]

# Extrair o primeiro tipo de culinária se houver mais de um
online_delivery_restaurants['cuisines'] = online_delivery_restaurants['cuisines'].apply(lambda x: x.split(",")[0])

# Agrupar o DataFrame pelo tipo de culinária e contar o número de restaurantes
cuisine_counts = online_delivery_restaurants['cuisines'].value_counts()

# Encontrar o tipo de culinária com o maior número de restaurantes
most_common_cuisine = cuisine_counts.idxmax()
most_common_cuisine_count = cuisine_counts.max()

# Exibir o tipo de culinária e o número de restaurantes
print(f"O tipo de culinária que possui mais restaurantes que aceitam pedidos online e fazem entregas é {most_common_cuisine} com {most_common_cuisine_count} restaurantes.")





