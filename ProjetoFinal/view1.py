# # importacao 

import pandas as pd
import numpy as np
import streamlit as st


## importaçao do csv
################################
df = pd.read_csv('C:/Users/Victor/Desktop/CC/CDS/python/ProjetoFinal/zomato.csv', encoding="utf-8", engine='python')


# Ajustar para mostrar todas as colunas
pd.set_option('display.max_columns', None)


# # Tratamento de dados 


# ### Remover colunas com unico valor 

# Identificar colunas com um único valor
cols_to_remove = [col for col in df.columns if df[col].nunique() == 1]

# Remover essas colunas do DataFrame
df_1 = df.drop(columns=cols_to_remove)

# Exibir as colunas removidas
#print("Colunas removidas:", cols_to_remove)

# Exibir o DataFrame após a remoção
#print(df_1)

# ### dados duplicados


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

##df_1.isna().sum()


# df_2.replace(["N/A", "NULL", ""], np.nan)## essa linha não faz diferenca

# Remover linhas que contêm qualquer valor faltante
df_3 = df_2.dropna(axis=0, how='any')

# ### estatisticas 

# Gerar a tabela de estatística descritiva para todas as colunas (numéricas e não numéricas)
estatisticas_completas2 = df_3.describe(exclude='object')




# ### replace 


df_3.columns = df_3.columns.str.strip().str.lower().str.replace(' ', '_').str.replace('(', '').str.replace(')', '')


# df_3.columns


# ###  criar uma nova coluna 'price_type'


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



# ### PAIS


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


# ### CORES


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


# ### categorizar


# Categorizar os restaurantes por apenas um tipo de culinária (o primeiro da lista)
df_4["cuisines"] = df_4["cuisines"].apply(lambda x: x.split(",")[0])

# Exibir o resultado para verificar a nova categorização
print(df_4[['restaurant_name', 'cuisines']].head())

#####################################################################################################################################################


# Sidebar para seleção de páginas
page = st.sidebar.selectbox("Escolha a página", ["Home", "País", "Cidade", "Restaurantes", "Culinária"])

# Filtros na barra lateral
countries = df_4['country'].unique().tolist()
cuisines = df_4['cuisines'].unique().tolist()

selected_countries = st.sidebar.multiselect("Selecione o(s) país(es)", ['Todos'] + countries, default='Todos')
selected_cuisines = st.sidebar.multiselect("Selecione a(s) culinária(s)", ['Todos'] + cuisines, default='Todos')

# Aplicar filtros apenas se o usuário não selecionar "Todos"
if 'Todos' in selected_countries:
    df_filtered = df_4.copy()
else:
    df_filtered = df_4[df_4['country'].isin(selected_countries)]

if 'Todos' not in selected_cuisines:
    df_filtered = df_filtered[df_filtered['cuisines'].str.contains('|'.join(selected_cuisines), case=False)]

# Página Home
if page == "Home":
    st.title("Dashboard - Home")

    # Perguntas da página Home
    st.header("1. Quantos restaurantes únicos estão registrados?")
    num_unique_restaurants = df_filtered['restaurant_name'].nunique()
    st.write(f"Número de restaurantes únicos: {num_unique_restaurants}")

    st.header("2. Quantos países únicos estão registrados?")
    num_unique_countries = df_filtered['country'].nunique()
    st.write(f"Número de países únicos: {num_unique_countries}")

    st.header("3. Quantas cidades únicas estão registradas?")
    num_unique_city = df_filtered['city'].nunique()
    st.write(f"Número de cidades únicas: {num_unique_city}")

    st.header("4. Qual o total de avaliações feitas?")
    total_aggregate_rating = df_filtered['aggregate_rating'].count()
    st.write(f"Total de avaliações: {total_aggregate_rating}")

    st.header("5. Qual o total de tipos de culinária registrados?")
    total_unique_cuisines = df_filtered["cuisines"].nunique()
    st.write(f"O total de tipos de culinária registrados é: {total_unique_cuisines}")

# Página País
elif page == "País":
    st.title("Dashboard - País")

    # Perguntas da página País
    st.header("1. Qual o nome do país que possui mais cidades registradas?")
    country_city_counts = df_filtered.groupby('country')['city'].nunique()
    max_cities_country = country_city_counts.idxmax()
    max_cities_count = country_city_counts.max()
    st.write(f"O país com mais cidades registradas é {max_cities_country}, com {max_cities_count} cidades.")

    st.header("2. Qual o nome do país que possui mais restaurantes registrados?")
    country_restaurant_counts = df_filtered.groupby('country')['restaurant_name'].nunique()
    max_restaurants_country = country_restaurant_counts.idxmax()
    max_restaurants_count = country_restaurant_counts.max()
    st.write(f"O país com mais restaurantes registrados é {max_restaurants_country}, com {max_restaurants_count} restaurantes.")

    st.header("3. Qual o nome do país que possui mais restaurantes com o nível de preço igual a 4 registrados?")
    df_price_4 = df_filtered[df_filtered['price_range'] == 4]
    country_price_4_counts = df_price_4.groupby('country')['restaurant_name'].nunique()
    max_price_4_country = country_price_4_counts.idxmax()
    max_price_4_count = country_price_4_counts.max()
    st.write(f"O país com mais restaurantes com nível de preço 4 registrados é {max_price_4_country}, com {max_price_4_count} restaurantes.")

    st.header("4. Qual o nome do país que possui a maior quantidade de tipos de culinária distintos?")
    cuisines_by_country = df_filtered.groupby('country')['cuisines'].nunique()
    max_cuisines_country = cuisines_by_country.idxmax()
    max_cuisines_count = cuisines_by_country.max()
    st.write(f"O país com a maior quantidade de tipos de culinária distintos é {max_cuisines_country}, com {max_cuisines_count} tipos de culinária.")

    st.header("5. Qual o nome do país que possui a maior quantidade de avaliações feitas?")
    country_rating_sums = df_filtered.groupby('country')['aggregate_rating'].count()
    max_rating_country = country_rating_sums.idxmax()
    max_rating_sum = country_rating_sums.max()
    st.write(f"O país com a maior quantidade de avaliações feitas é {max_rating_country}, com um total de {max_rating_sum} avaliações.")

    st.header("6. Qual o nome do país que possui a maior quantidade de restaurantes que fazem entrega?")
    df_delivery = df_filtered[df_filtered['has_online_delivery'] == 1]
    country_delivery_counts = df_delivery.groupby('country')['restaurant_name'].nunique()
    max_delivery_country = country_delivery_counts.idxmax()
    max_delivery_count = country_delivery_counts.max()
    st.write(f"O país com mais restaurantes que fazem entrega é {max_delivery_country}, com {max_delivery_count} restaurantes.")

    st.header("7. Qual o nome do país que possui a maior quantidade de restaurantes que aceitam reservas?")
    df_reservas = df_filtered[df_filtered['has_table_booking'] == 1]
    country_reservas_counts = df_reservas.groupby('country')['restaurant_name'].nunique()
    max_reservas_country = country_reservas_counts.idxmax()
    max_reservas_count = country_reservas_counts.max()
    st.write(f"O país com mais restaurantes que aceitam reservas é {max_reservas_country}, com {max_reservas_count} restaurantes.")

    st.header("8. Qual o nome do país que possui, na média, a maior quantidade de avaliações registrada?")
    country_avg_rating = df_filtered.groupby('country')['aggregate_rating'].count()
    max_avg_rating_country = country_avg_rating.idxmax()
    max_avg_rating = country_avg_rating.max()
    st.write(f"O país com a maior média de avaliações registradas é {max_avg_rating_country}, com uma média de {max_avg_rating:.2f} avaliações.")

    st.header("9. Qual o nome do país que possui, na média, a maior nota média registrada?")
    country_avg_rating = df_filtered.groupby('country')['aggregate_rating'].mean()
    max_avg_rating_country = country_avg_rating.idxmax()
    max_avg_rating = country_avg_rating.max()
    st.write(f"O país com a maior nota média registrada é {max_avg_rating_country}, com uma nota média de {max_avg_rating:.2f}.")

    st.header("10. Qual o nome do país que possui, na média, a menor nota média registrada?")
    country_avg_rating = df_filtered.groupby('country')['aggregate_rating'].mean()
    min_avg_rating_country = country_avg_rating.idxmin()
    min_avg_rating = country_avg_rating.min()
    st.write(f"O país com a menor nota média registrada é {min_avg_rating_country}, com uma nota média de {min_avg_rating:.2f}.")

    st.header("11. Qual a média de preço de um prato para dois por país?")
    country_avg_cost_for_two = df_filtered.groupby('country')['average_cost_for_two'].mean()
    st.write(country_avg_cost_for_two)

# Página Cidade
elif page == "Cidade":
    st.title("Dashboard - Cidade")

    # Perguntas da página Cidade
    st.header("1. Qual o nome da cidade que possui mais restaurantes registrados?")
    restaurants_by_city = df_filtered['city'].value_counts()
    city_with_most_restaurants = restaurants_by_city.idxmax()
    most_restaurants_count = restaurants_by_city.max()
    st.write(f"A cidade com mais restaurantes registrados é {city_with_most_restaurants}, com {most_restaurants_count} restaurantes.")

    st.header("2. Qual o nome da cidade que possui mais restaurantes com nota média acima de 4?")
    high_rated_restaurants = df_filtered[df_filtered['aggregate_rating'] > 4]
    restaurants_by_city_high_ratings = high_rated_restaurants['city'].value_counts()
    city_with_most_high_rated_restaurants = restaurants_by_city_high_ratings.idxmax()
    most_high_rated_restaurants_count = restaurants_by_city_high_ratings.max()
    st.write(f"A cidade com mais restaurantes com nota média acima de 4 é {city_with_most_high_rated_restaurants}, com {most_high_rated_restaurants_count} restaurantes.")

    st.header("3. Qual o nome da cidade que possui mais restaurantes com nota média abaixo de 2.5?")
    low_rated_restaurants = df_filtered[df_filtered['aggregate_rating'] < 2.5]
    restaurants_by_city_low_ratings = low_rated_restaurants['city'].value_counts()
    city_with_most_low_rated_restaurants = restaurants_by_city_low_ratings.idxmax()
    most_low_rated_restaurants_count = restaurants_by_city_low_ratings.max()
    st.write(f"A cidade com mais restaurantes com nota média abaixo de 2.5 é {city_with_most_low_rated_restaurants}, com {most_low_rated_restaurants_count} restaurantes.")

    st.header("4. Qual o nome da cidade que possui o maior valor médio de um prato para dois?")
    avg_cost_by_city = df_filtered.groupby('city')['average_cost_for_two'].mean()
    city_with_highest_avg_cost = avg_cost_by_city.idxmax()
    highest_avg_cost = avg_cost_by_city.max()
    st.write(f"A cidade com o maior valor médio de um prato para dois é {city_with_highest_avg_cost}, com um valor médio de {highest_avg_cost:.2f}.")

    st.header("5. Qual o nome da cidade que possui a maior quantidade de tipos de culinária distintas?")
    cuisines_by_city = df_filtered.groupby('city')['cuisines'].nunique()
    city_with_most_cuisines = cuisines_by_city.idxmax()
    most_cuisines_count = cuisines_by_city.max()
    st.write(f"A cidade com a maior quantidade de tipos de culinária distintos é {city_with_most_cuisines}, com {most_cuisines_count} tipos de culinária.")

    st.header("6. Qual o nome da cidade que possui a maior quantidade de restaurantes que fazem reservas?")
    restaurants_with_booking = df_filtered[df_filtered['has_table_booking'] == 1]
    restaurants_by_city_with_booking = restaurants_with_booking['city'].value_counts()
    city_with_most_restaurants_with_booking = restaurants_by_city_with_booking.idxmax()
    most_restaurants_with_booking_count = restaurants_by_city_with_booking.max()
    st.write(f"A cidade com mais restaurantes que fazem reservas é {city_with_most_restaurants_with_booking}, com {most_restaurants_with_booking_count} restaurantes.")

    st.header("7. Qual o nome da cidade que possui a maior quantidade de restaurantes que fazem entregas?")
    restaurants_with_delivery = df_filtered[df_filtered['is_delivering_now'] == 1]
    restaurants_by_city_with_delivery = restaurants_with_delivery['city'].value_counts()
    city_with_most_restaurants_with_delivery = restaurants_by_city_with_delivery.idxmax()
    most_restaurants_with_delivery_count = restaurants_by_city_with_delivery.max()
    st.write(f"A cidade com mais restaurantes que fazem entregas é {city_with_most_restaurants_with_delivery}, com {most_restaurants_with_delivery_count} restaurantes.")

    st.header("8. Qual o nome da cidade que possui a maior quantidade de restaurantes que aceitam pedidos online?")
    restaurants_with_online_orders = df_filtered[df_filtered['has_online_delivery'] == 1]
    restaurants_by_city_with_online_orders = restaurants_with_online_orders['city'].value_counts()
    city_with_most_restaurants_with_online_orders = restaurants_by_city_with_online_orders.idxmax()
    most_restaurants_with_online_orders_count = restaurants_by_city_with_online_orders.max()
    st.write(f"A cidade com mais restaurantes que aceitam pedidos online é {city_with_most_restaurants_with_online_orders}, com {most_restaurants_with_online_orders_count} restaurantes.")

# Página Restaurantes
elif page == "Restaurantes":
    st.title("Dashboard - Restaurantes")

    # Perguntas da página Restaurantes
    st.header("1. Qual o nome do restaurante que possui a maior quantidade de avaliações?")
    restaurant_with_most_votes = df_filtered.loc[df_filtered['votes'].idxmax()]
    st.write(f"O restaurante com a maior quantidade de avaliações é {restaurant_with_most_votes['restaurant_name']}, com {restaurant_with_most_votes['votes']} avaliações.")

    st.header("2. Qual o nome do restaurante com a maior nota média?")
    restaurant_with_highest_rating = df_filtered.loc[df_filtered['aggregate_rating'].idxmax()]
    st.write(f"O restaurante com a maior nota média é {restaurant_with_highest_rating['restaurant_name']}, com nota {restaurant_with_highest_rating['aggregate_rating']}.")

    st.header("3. Qual o nome do restaurante que possui o maior valor de um prato para duas pessoas?")
    restaurant_with_highest_cost = df_filtered.loc[df_filtered['average_cost_for_two'].idxmax()]
    st.write(f"O restaurante com o maior valor de um prato para duas pessoas é {restaurant_with_highest_cost['restaurant_name']}, com o valor de {restaurant_with_highest_cost['average_cost_for_two']}.")

    st.header("4. Qual o nome do restaurante de tipo de culinária brasileira que possui a menor média de avaliação?")
    brazilian_cuisine_restaurants = df_filtered[df_filtered['cuisines'].str.contains('Brazilian', case=False)]
    restaurant_with_lowest_rating = brazilian_cuisine_restaurants.loc[brazilian_cuisine_restaurants['aggregate_rating'].idxmin()]
    st.write(f"O restaurante de culinária brasileira com a menor média de avaliação é {restaurant_with_lowest_rating['restaurant_name']}, com nota {restaurant_with_lowest_rating['aggregate_rating']}.")

    st.header("5. Qual o nome do restaurante de tipo de culinária brasileira, e que é do Brasil, que possui a maior média de avaliação?")
    brazilian_cuisine_brazil = df_filtered[(df_filtered['cuisines'].str.contains('Brazilian', case=False)) & (df_filtered['country'] == 'Brazil')]
    restaurant_with_highest_rating = brazilian_cuisine_brazil.loc[brazilian_cuisine_brazil['aggregate_rating'].idxmax()]
    st.write(f"O restaurante de culinária brasileira, localizado no Brasil, com a maior média de avaliação é {restaurant_with_highest_rating['restaurant_name']}, com nota {restaurant_with_highest_rating['aggregate_rating']}.")

    st.header("6. Os restaurantes que aceitam pedido online são também, na média, os restaurantes que mais possuem avaliações registradas?")
    online_delivery_restaurants = df_filtered[df_filtered['has_online_delivery'] == 1]
    no_online_delivery_restaurants = df_filtered[df_filtered['has_online_delivery'] == 0]
    mean_votes_online_delivery = online_delivery_restaurants['votes'].mean()
    mean_votes_no_online_delivery = no_online_delivery_restaurants['votes'].mean()
    st.write(f"Média de avaliações para restaurantes que aceitam pedidos online: {mean_votes_online_delivery:.2f}")
    st.write(f"Média de avaliações para restaurantes que não aceitam pedidos online: {mean_votes_no_online_delivery:.2f}")
    if mean_votes_online_delivery > mean_votes_no_online_delivery:
        st.write("Sim, os restaurantes que aceitam pedidos online possuem, na média, mais avaliações registradas.")
    else:
        st.write("Não, os restaurantes que aceitam pedidos online não possuem, na média, mais avaliações registradas.")

    st.header("7. Os restaurantes que fazem reservas são também, na média, os restaurantes que possuem o maior valor médio de um prato para duas pessoas?")
    restaurants_with_reservations = df_filtered[df_filtered['has_table_booking'] == 1]
    restaurants_without_reservations = df_filtered[df_filtered['has_table_booking'] == 0]
    mean_cost_with_reservations = restaurants_with_reservations['average_cost_for_two'].mean()
    mean_cost_without_reservations = restaurants_without_reservations['average_cost_for_two'].mean()
    st.write(f"Valor médio de um prato para duas pessoas para restaurantes que aceitam reservas: {mean_cost_with_reservations:.2f}")
    st.write(f"Valor médio de um prato para duas pessoas para restaurantes que não aceitam reservas: {mean_cost_without_reservations:.2f}")
    if mean_cost_with_reservations > mean_cost_without_reservations:
        st.write("Sim, os restaurantes que fazem reservas possuem, na média, o maior valor médio de um prato para duas pessoas.")
    else:
        st.write("Não, os restaurantes que fazem reservas não possuem, na média, o maior valor médio de um prato para duas pessoas.")

    st.header("8. Os restaurantes do tipo de culinária japonesa dos Estados Unidos da América possuem um valor médio de prato para duas pessoas maior que as churrascarias americanas (BBQ)?")
    us_restaurants = df_filtered[df_filtered['country'] == 'United States of America']
    japanese_restaurants = us_restaurants[us_restaurants['cuisines'].str.contains('Japanese', case=False)]
    bbq_restaurants = us_restaurants[us_restaurants['cuisines'].str.contains('BBQ', case=False)]
    mean_cost_japanese = japanese_restaurants['average_cost_for_two'].mean()
    mean_cost_bbq = bbq_restaurants['average_cost_for_two'].mean()
    st.write(f"Valor médio de um prato para duas pessoas em restaurantes japoneses nos EUA: {mean_cost_japanese:.2f}")
    st.write(f"Valor médio de um prato para duas pessoas em churrascarias (BBQ) nos EUA: {mean_cost_bbq:.2f}")
    if mean_cost_japanese > mean_cost_bbq:
        st.write("Sim, os restaurantes de culinária japonesa nos EUA possuem um valor médio de prato para duas pessoas maior que as churrascarias (BBQ).")
    else:
        st.write("Não, as churrascarias (BBQ) nos EUA possuem um valor médio de prato para duas pessoas maior que os restaurantes de culinária japonesa.")


# Página Culinária
elif page == "Culinária":
    st.title("Dashboard - Culinária")

    st.header("1. Dos restaurantes que possuem o tipo de culinária italiana, qual o nome do restaurante com a maior média de avaliação?")
    italian_restaurants = df_filtered[df_filtered['cuisines'].str.contains('Italian', case=False)]
    if not italian_restaurants.empty:
        top_italian_restaurant = italian_restaurants.loc[italian_restaurants['aggregate_rating'].idxmax()]
        st.write(f"O restaurante de culinária italiana com a maior média de avaliação é {top_italian_restaurant['restaurant_name']} com uma média de {top_italian_restaurant['aggregate_rating']:.2f}.")
    else:
        st.write("Nenhum restaurante de culinária italiana encontrado.")

    st.header("2. Dos restaurantes que possuem o tipo de culinária italiana, qual o nome do restaurante com a menor média de avaliação?")
    if not italian_restaurants.empty:
        bottom_italian_restaurant = italian_restaurants.loc[italian_restaurants['aggregate_rating'].idxmin()]
        st.write(f"O restaurante de culinária italiana com a menor média de avaliação é {bottom_italian_restaurant['restaurant_name']} com uma média de {bottom_italian_restaurant['aggregate_rating']:.2f}.")
    else:
        st.write("Nenhum restaurante de culinária italiana encontrado.")

    st.header("3. Dos restaurantes que possuem o tipo de culinária americana, qual o nome do restaurante com a maior média de avaliação?")
    american_restaurants = df_filtered[df_filtered['cuisines'].str.contains('American', case=False)]
    if not american_restaurants.empty:
        top_american_restaurant = american_restaurants.loc[american_restaurants['aggregate_rating'].idxmax()]
        st.write(f"O restaurante de culinária americana com a maior média de avaliação é {top_american_restaurant['restaurant_name']} com uma média de {top_american_restaurant['aggregate_rating']:.2f}.")
    else:
        st.write("Nenhum restaurante de culinária americana encontrado.")

    st.header("4. Dos restaurantes que possuem o tipo de culinária americana, qual o nome do restaurante com a menor média de avaliação?")
    if not american_restaurants.empty:
        bottom_american_restaurant = american_restaurants.loc[american_restaurants['aggregate_rating'].idxmin()]
        st.write(f"O restaurante de culinária americana com a menor média de avaliação é {bottom_american_restaurant['restaurant_name']} com uma média de {bottom_american_restaurant['aggregate_rating']:.2f}.")
    else:
        st.write("Nenhum restaurante de culinária americana encontrado.")

    st.header("5. Dos restaurantes que possuem o tipo de culinária árabe, qual o nome do restaurante com a maior média de avaliação?")
    arabic_restaurants = df_filtered[df_filtered['cuisines'].str.contains('Arabian', case=False)]
    if not arabic_restaurants.empty:
        top_arabic_restaurant = arabic_restaurants.loc[arabic_restaurants['aggregate_rating'].idxmax()]
        st.write(f"O restaurante de culinária árabe com a maior média de avaliação é {top_arabic_restaurant['restaurant_name']} com uma média de {top_arabic_restaurant['aggregate_rating']:.2f}.")
    else:
        st.write("Nenhum restaurante de culinária árabe encontrado.")

    st.header("6. Dos restaurantes que possuem o tipo de culinária árabe, qual o nome do restaurante com a menor média de avaliação?")
    if not arabic_restaurants.empty:
        bottom_arabic_restaurant = arabic_restaurants.loc[arabic_restaurants['aggregate_rating'].idxmin()]
        st.write(f"O restaurante de culinária árabe com a menor média de avaliação é {bottom_arabic_restaurant['restaurant_name']} com uma média de {bottom_arabic_restaurant['aggregate_rating']:.2f}.")
    else:
        st.write("Nenhum restaurante de culinária árabe encontrado.")

    st.header("7. Dos restaurantes que possuem o tipo de culinária japonesa, qual o nome do restaurante com a maior média de avaliação?")
    japanese_restaurants = df_filtered[df_filtered['cuisines'].str.contains('Japanese', case=False)]
    if not japanese_restaurants.empty:
        top_japanese_restaurant = japanese_restaurants.loc[japanese_restaurants['aggregate_rating'].idxmax()]
        st.write(f"O restaurante de culinária japonesa com a maior média de avaliação é {top_japanese_restaurant['restaurant_name']} com uma média de {top_japanese_restaurant['aggregate_rating']:.2f}.")
    else:
        st.write("Nenhum restaurante de culinária japonesa encontrado.")

    st.header("8. Dos restaurantes que possuem o tipo de culinária japonesa, qual o nome do restaurante com a menor média de avaliação?")
    if not japanese_restaurants.empty:
        bottom_japanese_restaurant = japanese_restaurants.loc[japanese_restaurants['aggregate_rating'].idxmin()]
        st.write(f"O restaurante de culinária japonesa com a menor média de avaliação é {bottom_japanese_restaurant['restaurant_name']} com uma média de {bottom_japanese_restaurant['aggregate_rating']:.2f}.")
    else:
        st.write("Nenhum restaurante de culinária japonesa encontrado.")

    st.header("9. Dos restaurantes que possuem o tipo de culinária caseira, qual o nome do restaurante com a maior média de avaliação?")
    home_cooked_restaurants = df_filtered[df_filtered['cuisines'].str.contains('Home', case=False)]
    if not home_cooked_restaurants.empty:
        top_home_cooked_restaurant = home_cooked_restaurants.loc[home_cooked_restaurants['aggregate_rating'].idxmax()]
        st.write(f"O restaurante de culinária caseira com a maior média de avaliação é {top_home_cooked_restaurant['restaurant_name']} com uma média de {top_home_cooked_restaurant['aggregate_rating']:.2f}.")
    else:
        st.write("Nenhum restaurante de culinária caseira encontrado.")

    st.header("10. Dos restaurantes que possuem o tipo de culinária caseira, qual o nome do restaurante com a menor média de avaliação?")
    if not home_cooked_restaurants.empty:
        bottom_home_cooked_restaurant = home_cooked_restaurants.loc[home_cooked_restaurants['aggregate_rating'].idxmin()]
        st.write(f"O restaurante de culinária caseira com a menor média de avaliação é {bottom_home_cooked_restaurant['restaurant_name']} com uma média de {bottom_home_cooked_restaurant['aggregate_rating']:.2f}.")
    else:
        st.write("Nenhum restaurante de culinária caseira encontrado.")

    st.header("11. Qual o tipo de culinária que possui o maior valor médio de um prato para duas pessoas?")
    df_filtered['cuisines'] = df_filtered['cuisines'].apply(lambda x: x.split(",")[0])
    average_cost_by_cuisine = df_filtered.groupby('cuisines')['average_cost_for_two'].mean()
    most_expensive_cuisine = average_cost_by_cuisine.idxmax()
    most_expensive_value = average_cost_by_cuisine.max()
    st.write(f"O tipo de culinária que possui o maior valor médio de um prato para duas pessoas é {most_expensive_cuisine} com um valor médio de {most_expensive_value:.2f}.")

    st.header("12. Qual o tipo de culinária que possui a maior nota média?")
    average_rating_by_cuisine = df_filtered.groupby('cuisines')['aggregate_rating'].mean()
    highest_rating_cuisine = average_rating_by_cuisine.idxmax()
    highest_rating_value = average_rating_by_cuisine.max()
    st.write(f"O tipo de culinária que possui a maior nota média é {highest_rating_cuisine} com uma nota média de {highest_rating_value:.2f}.")

    st.header("13. Qual o tipo de culinária que possui mais restaurantes que aceitam pedidos online e fazem entregas?")
    online_delivery_restaurants = df_filtered[(df_filtered['has_online_delivery'] == 1) & (df_filtered['has_table_booking'] == 1)]
    online_delivery_restaurants['cuisines'] = online_delivery_restaurants['cuisines'].apply(lambda x: x.split(",")[0])
    cuisine_counts = online_delivery_restaurants['cuisines'].value_counts()
    most_common_cuisine = cuisine_counts.idxmax()
    most_common_cuisine_count = cuisine_counts.max()
    st.write(f"O tipo de culinária que possui mais restaurantes que aceitam pedidos online e fazem entregas é {most_common_cuisine} com {most_common_cuisine_count} restaurantes.")        