# # importacao 
import streamlit as st
import pandas as pd
import numpy as np
import folium
from streamlit_folium import folium_static
import matplotlib.pyplot as plt



## importaçao do csv
################################
df = pd.read_csv("C:/Users/Victor/Desktop/CC/CDS/projetos/python/ProjetoFinal/zomato.csv", encoding="utf-8", engine='python')


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
# print(df_4[['restaurant_name', 'cuisines']].head())


#####################################################################################3


# Título do dashboard
# st.title("Dashboard de Dados")

# Barra de navegação horizontal com st.radio
page = st.radio(
    "Páginas", 
    ("Geral", "País", "Cidade", "Restaurantes", "Culinária"),
    horizontal=True
)


# Filtros na barra lateral
countries = df_4['country'].unique().tolist()
cuisines = df_4['cuisines'].unique().tolist()

selected_countries = st.sidebar.multiselect("Selecione o(s) país(es)", ['Todos'] + countries, default='Todos')
selected_cuisines = st.sidebar.multiselect("Selecione a(s) culinária(s)", ['Todos'] + cuisines, default='Todos')

# Texto no final da barra lateral
st.sidebar.markdown("---")
st.sidebar.write("Projeto por Victor Rabelo de Campos")

# Aplicar filtros apenas se o usuário não selecionar "Todos"
if 'Todos' in selected_countries:
    df_filtered = df_4.copy()
else:
    df_filtered = df_4[df_4['country'].isin(selected_countries)]

if 'Todos' not in selected_cuisines:
    df_filtered = df_filtered[df_filtered['cuisines'].str.contains('|'.join(selected_cuisines), case=False)]


# Renderização das páginas com base na seleção do usuário
if page == "Geral":
    st.title("Análise Geral")
    st.write("Dashboard analisando dados de restaurantes em varias cidades e países.  ")
    st.write("    ")
    st.write("    ")
    st.write("    ")
    # Coloque o conteúdo da página Home aqui
    # Perguntas da página Home com Cards
    col1, col2, col3 = st.columns(3)

    with col1:
        #st.header("Restaurantes Únicos")
        num_unique_restaurants = df_filtered['restaurant_name'].nunique()
        st.metric(label="Número de Restaurantes", value=num_unique_restaurants)

    with col2:
        #st.header("Países Únicos")
        num_unique_countries = df_filtered['country'].nunique()
        st.metric(label="Número de Países", value=num_unique_countries)

    with col3:
        #st.header("Cidades Únicas")
        num_unique_city = df_filtered['city'].nunique()
        st.metric(label="Número de Cidades", value=num_unique_city)

    col4, col5 = st.columns(2)

    with col4:
        #st.header("Total de Avaliações")
        total_aggregate_rating = df_filtered['aggregate_rating'].count()
        st.metric(label="Avaliações Feitas", value=total_aggregate_rating)

    with col5:
        #st.header("Tipos de Culinária")
        total_unique_cuisines = df_filtered["cuisines"].nunique()
        st.metric(label="Tipos de Culinária Registrados", value=total_unique_cuisines)

# Mapa com marcadores de restaurantes
    st.subheader("Mapa de Restaurantes")

    # Verificando se as colunas de latitude e longitude estão presentes no DataFrame
    if 'latitude' in df_filtered.columns and 'longitude' in df_filtered.columns:
        # Criando um DataFrame somente com latitude e longitude
        map_data = df_filtered[['latitude', 'longitude']].dropna()

        # Exibindo o mapa com os restaurantes
        st.map(map_data)
    else:
        st.write("As colunas de latitude e longitude não estão presentes no DataFrame.")

elif page == "País":
    st.title("Análise País")
    # st.write("Página País")
    # Coloque o conteúdo da página País aqui

        # Verifica se o dataframe tem dados após os filtros
    if df_filtered.empty:
        st.warning("Nenhum dado encontrado para os filtros selecionados.")
    else:
        # Pergunta 1: País com mais cidades registradas
        st.header("1. Qual o nome do país que possui mais cidades registradas?")
        country_city_counts = df_filtered.groupby('country')['city'].nunique()

        if not country_city_counts.empty:  # Verifica se não está vazio
            top_5_countries = country_city_counts.sort_values(ascending=False).head(5)

            # Gráfico de barras
            fig, ax = plt.subplots()
            top_5_countries.plot(kind='bar', ax=ax, color='skyblue')
            ax.set_title("Top 5 Países com Mais Cidades Registradas")
            ax.set_xlabel("País")
            ax.set_ylabel("Número de Cidades")
            st.pyplot(fig)

            # Detalhe adicional
            max_cities_country = country_city_counts.idxmax()
            max_cities_count = country_city_counts.max()
            st.write(f"O país com mais cidades registradas é {max_cities_country}, com {max_cities_count} cidades.")
        else:
            st.write("Não há dados suficientes para calcular o país com mais cidades registradas.")

        # Pergunta 2: Top 5 países com mais restaurantes registrados
        st.header("2. Top 5 países com mais restaurantes registrados")
        country_restaurant_counts = df_filtered.groupby('country')['restaurant_name'].nunique()

        if not country_restaurant_counts.empty:  # Verifica se não está vazio
            top_5_countries = country_restaurant_counts.nlargest(5)

            max_restaurants_country = top_5_countries.idxmax()
            max_restaurants_count = top_5_countries.max()
            st.write(f"O país com mais restaurantes registrados é {max_restaurants_country}, com {max_restaurants_count} restaurantes.")

            fig, ax = plt.subplots()
            top_5_countries.plot(kind='bar', ax=ax)
            ax.set_title('Top 5 países com mais restaurantes registrados')
            ax.set_xlabel('País')
            ax.set_ylabel('Número de restaurantes')
            st.pyplot(fig)
        else:
            st.write("Não há dados suficientes para calcular os países com mais restaurantes registrados.")

        # Pergunta 3: Top 5 países com mais restaurantes com nível de preço 4 registrados
        st.header("3. Top 5 países com mais restaurantes com nível de preço 4 registrados")
        df_price_4 = df_filtered[df_filtered['price_range'] == 4]
        country_price_4_counts = df_price_4.groupby('country')['restaurant_name'].nunique()

        if not country_price_4_counts.empty:  # Verifica se não está vazio
            top_5_price_4_countries = country_price_4_counts.nlargest(5)

            max_price_4_country = top_5_price_4_countries.idxmax()
            max_price_4_count = top_5_price_4_countries.max()
            st.write(f"O país com mais restaurantes com nível de preço 4 registrados é {max_price_4_country}, com {max_price_4_count} restaurantes.")

            fig, ax = plt.subplots()
            top_5_price_4_countries.plot(kind='bar', ax=ax, color='skyblue')
            ax.set_title('Top 5 países com mais restaurantes com nível de preço 4')
            ax.set_xlabel('País')
            ax.set_ylabel('Número de restaurantes')
            st.pyplot(fig)
        else:
            st.write("Não há dados suficientes para calcular os países com mais restaurantes com nível de preço 4 registrados.")

        # Criando as colunas para os dados resumidos
        col1, col2, col3, col4 = st.columns(4)

        # Coluna 1 - País com maior quantidade de tipos de culinária distintos
        with col1:
            cuisines_by_country = df_filtered.groupby('country')['cuisines'].nunique()
            if not cuisines_by_country.empty:  # Verifica se não está vazio
                max_cuisines_country = cuisines_by_country.idxmax()
                max_cuisines_count = cuisines_by_country.max()
                st.metric(label="País com mais tipos de culinária", value=max_cuisines_country)
                st.metric(label="Quantidade de tipos", value=max_cuisines_count)
            else:
                st.metric(label="País com mais tipos de culinária", value="N/A")
                st.metric(label="Quantidade de tipos", value="0")

        # Coluna 2 - País com maior quantidade de avaliações
        with col2:
            country_rating_sums = df_filtered.groupby('country')['aggregate_rating'].count()
            if not country_rating_sums.empty:  # Verifica se não está vazio
                max_rating_country = country_rating_sums.idxmax()
                max_rating_sum = country_rating_sums.max()
                st.metric(label="País com mais avaliações", value=max_rating_country)
                st.metric(label="Total de avaliações", value=max_rating_sum)
            else:
                st.metric(label="País com mais avaliações", value="N/A")
                st.metric(label="Total de avaliações", value="0")

        # Coluna 3 - País com maior quantidade de restaurantes que fazem entrega
        with col3:
            df_delivery = df_filtered[df_filtered['has_online_delivery'] == 1]
            country_delivery_counts = df_delivery.groupby('country')['restaurant_name'].nunique()
            if not country_delivery_counts.empty:  # Verifica se não está vazio
                max_delivery_country = country_delivery_counts.idxmax()
                max_delivery_count = country_delivery_counts.max()
                st.metric(label="País com mais entregas", value=max_delivery_country)
                st.metric(label="Restaurantes com entrega", value=max_delivery_count)
            else:
                st.metric(label="País com mais entregas", value="N/A")
                st.metric(label="Restaurantes com entrega", value="0")

        # Coluna 4 - País com maior quantidade de restaurantes que aceitam reservas
        with col4:
            df_reservas = df_filtered[df_filtered['has_table_booking'] == 1]
            country_reservas_counts = df_reservas.groupby('country')['restaurant_name'].nunique()
            if not country_reservas_counts.empty:  # Verifica se não está vazio
                max_reservas_country = country_reservas_counts.idxmax()
                max_reservas_count = country_reservas_counts.max()
                st.metric(label="País com mais reservas", value=max_reservas_country)
                st.metric(label="Restaurantes com reservas", value=max_reservas_count)
            else:
                st.metric(label="País com mais reservas", value="N/A")
                st.metric(label="Restaurantes com reservas", value="0")

        # Pergunta 8: Gráfico de barras do top 5 países com maior média de avaliações registradas
        st.header("8. Qual o nome do país que possui, na média, a maior quantidade de avaliações registrada?")
        country_avg_rating = df_filtered.groupby('country')['aggregate_rating'].count().sort_values(ascending=False).head(5)

        if not country_avg_rating.empty:  # Verifica se não está vazio
            fig, ax = plt.subplots()
            country_avg_rating.plot(kind='bar', ax=ax)
            ax.set_title("Top 5 países com maior média de avaliações registradas")
            ax.set_ylabel("Número de avaliações")
            ax.set_xlabel("País")
            st.pyplot(fig)
        else:
            st.write("Não há dados suficientes para calcular o país com maior média de avaliações.")

        # Pergunta 9: Gráfico de barras do top 5 países com maior nota média registrada
        st.header("9. Qual o nome do país que possui, na média, a maior nota média registrada?")
        country_avg_rating_mean = df_filtered.groupby('country')['aggregate_rating'].mean().sort_values(ascending=False).head(5)

        if not country_avg_rating_mean.empty:  # Verifica se não está vazio
            fig, ax = plt.subplots()
            country_avg_rating_mean.plot(kind='bar', ax=ax)
            ax.set_title("Top 5 países com maior nota média registrada")
            ax.set_ylabel("Nota média")
            ax.set_xlabel("País")
            st.pyplot(fig)
        else:
            st.write("Não há dados suficientes para calcular o país com a maior nota média.")

        # Pergunta 10: Gráfico de barras do top 5 países com menor nota média registrada
        st.header("10. Qual o nome do país que possui, na média, a menor nota média registrada?")
        country_min_avg_rating = df_filtered.groupby('country')['aggregate_rating'].mean().sort_values(ascending=True).head(5)

        if not country_min_avg_rating.empty:  # Verifica se não está vazio
            fig, ax = plt.subplots()
            country_min_avg_rating.plot(kind='bar', ax=ax)
            ax.set_title("Top 5 países com menor nota média registrada")
            ax.set_ylabel("Nota média")
            ax.set_xlabel("País")
            st.pyplot(fig)
        else:
            st.write("Não há dados suficientes para calcular o país com a menor nota média.")

        # Pergunta 11: Gráfico de barras da média de preço de um prato para dois por país (Top 5)
        st.header("11. Qual a média de preço de um prato para dois por país?")
        country_avg_cost_for_two = df_filtered.groupby('country')['average_cost_for_two'].mean().sort_values(ascending=False).head(5)

        if not country_avg_cost_for_two.empty:  # Verifica se não está vazio
            fig, ax = plt.subplots()
            country_avg_cost_for_two.plot(kind='bar', ax=ax)
            ax.set_title("Top 5 países com maior média de preço para dois")
            ax.set_ylabel("Preço médio para dois")
            ax.set_xlabel("País")
            st.pyplot(fig)
        else:
            st.write("Não há dados suficientes para calcular a média de preço de um prato para dois.")

            
elif page == "Cidade":
    st.title("Análise Cidade")
    # st.write("Página Cidade")
    # Coloque o conteúdo da página Cidade aqui
    # Verificação de existência de dados após os filtros
    if df_filtered.empty:
        st.error("Nenhum dado disponível após aplicar os filtros selecionados.")
    else:
        # Dividindo a página em colunas para os cards
        col1, col2 = st.columns(2)
        col3, col4 = st.columns(2)

        # Pergunta 1 - Cidade com mais restaurantes registrados
        with col1:
            st.subheader("Cidade com mais restaurantes registrados")
            restaurants_by_city = df_filtered['city'].value_counts()
            if not restaurants_by_city.empty:
                city_with_most_restaurants = restaurants_by_city.idxmax()
                most_restaurants_count = restaurants_by_city.max()
                st.metric(label="Cidade", value=city_with_most_restaurants,help=f"número de restaurantes = {most_restaurants_count}")
                st.metric(label="Número de Restaurantes", value=most_restaurants_count)
            else:
                st.write("Nenhuma cidade encontrada com restaurantes registrados.")

        # Pergunta 2 - Cidade com mais restaurantes com nota média acima de 4
        with col2:
            st.subheader("Cidade com mais restaurantes com nota média acima de 4")
            high_rated_restaurants = df_filtered[df_filtered['aggregate_rating'] > 4]
            restaurants_by_city_high_ratings = high_rated_restaurants['city'].value_counts()
            if not restaurants_by_city_high_ratings.empty:
                city_with_most_high_rated_restaurants = restaurants_by_city_high_ratings.idxmax()
                most_high_rated_restaurants_count = restaurants_by_city_high_ratings.max()
                st.metric(label="Cidade", value=city_with_most_high_rated_restaurants)
                st.metric(label="Número de Restaurantes", value=most_high_rated_restaurants_count)
            else:
                st.write("Nenhuma cidade encontrada com restaurantes altamente avaliados.")

        # Pergunta 3 - Cidade com mais restaurantes com nota média abaixo de 2.5
        with col3:
            st.subheader("Cidade com mais restaurantes com nota média abaixo de 2.5")
            low_rated_restaurants = df_filtered[df_filtered['aggregate_rating'] < 2.5]
            restaurants_by_city_low_ratings = low_rated_restaurants['city'].value_counts()
            if not restaurants_by_city_low_ratings.empty:
                city_with_most_low_rated_restaurants = restaurants_by_city_low_ratings.idxmax()
                most_low_rated_restaurants_count = restaurants_by_city_low_ratings.max()
                st.metric(label="Cidade", value=city_with_most_low_rated_restaurants)
                st.metric(label="Número de Restaurantes", value=most_low_rated_restaurants_count)
            else:
                st.write("Nenhuma cidade encontrada com restaurantes de baixa avaliação.")

        # Pergunta 4 - Cidade com o maior valor médio de um prato para dois
        with col4:
            st.subheader("Cidade com o maior valor médio de um prato para dois")
            avg_cost_by_city = df_filtered.groupby('city')['average_cost_for_two'].mean()
            if not avg_cost_by_city.empty:
                city_with_highest_avg_cost = avg_cost_by_city.idxmax()
                highest_avg_cost = avg_cost_by_city.max()
                st.metric(label="Cidade", value=city_with_highest_avg_cost)
                st.metric(label="Valor Médio", value=f"{highest_avg_cost:.2f}")
            else:
                st.write("Nenhuma cidade encontrada com valores de pratos disponíveis.")

        # Pergunta 5 - Top 5 cidades com a maior quantidade de tipos de culinária distintas
        st.header("5. Cidades com a Maior Quantidade de Tipos de Culinária Distintas")
        cuisines_by_city = df_filtered.groupby('city')['cuisines'].nunique()
        if not cuisines_by_city.empty:
            top_5_cities = cuisines_by_city.nlargest(5)
            fig, ax = plt.subplots()
            top_5_cities.plot(kind='bar', ax=ax, color='skyblue', edgecolor='black')
            ax.set_title('Top 5 Cidades com a Maior Quantidade de Tipos de Culinária')
            ax.set_xlabel('Cidades')
            ax.set_ylabel('Número de Tipos de Culinária')
            st.pyplot(fig)
        else:
            st.write("Nenhuma cidade encontrada com tipos de culinária distintos.")

        # Pergunta 6 - Cidade com mais restaurantes que fazem reservas
        st.header("6. Qual o nome da cidade que possui a maior quantidade de restaurantes que fazem reservas?")
        restaurants_with_booking = df_filtered[df_filtered['has_table_booking'] == 1]
        restaurants_by_city_with_booking = restaurants_with_booking['city'].value_counts()
        if not restaurants_by_city_with_booking.empty:
            city_with_most_restaurants_with_booking = restaurants_by_city_with_booking.idxmax()
            most_restaurants_with_booking_count = restaurants_by_city_with_booking.max()
            st.write(f"A cidade com mais restaurantes que fazem reservas é {city_with_most_restaurants_with_booking}, com {most_restaurants_with_booking_count} restaurantes.")
        else:
            st.write("Nenhuma cidade encontrada com restaurantes que fazem reservas.")

        # Pergunta 7 - Cidade com mais restaurantes que fazem entregas
        st.header("7. Qual o nome da cidade que possui a maior quantidade de restaurantes que fazem entregas?")
        restaurants_with_delivery = df_filtered[df_filtered['is_delivering_now'] == 1]
        restaurants_by_city_with_delivery = restaurants_with_delivery['city'].value_counts()
        if not restaurants_by_city_with_delivery.empty:
            city_with_most_restaurants_with_delivery = restaurants_by_city_with_delivery.idxmax()
            most_restaurants_with_delivery_count = restaurants_by_city_with_delivery.max()
            st.write(f"A cidade com mais restaurantes que fazem entregas é {city_with_most_restaurants_with_delivery}, com {most_restaurants_with_delivery_count} restaurantes.")
        else:
            st.write("Nenhuma cidade encontrada com restaurantes que fazem entregas.")

        # Pergunta 8 - Cidade com mais restaurantes que aceitam pedidos online
        st.header("8. Qual o nome da cidade que possui a maior quantidade de restaurantes que aceitam pedidos online?")
        restaurants_with_online_orders = df_filtered[df_filtered['has_online_delivery'] == 1]
        restaurants_by_city_with_online_orders = restaurants_with_online_orders['city'].value_counts()
        if not restaurants_by_city_with_online_orders.empty:
            city_with_most_restaurants_with_online_orders = restaurants_by_city_with_online_orders.idxmax()
            most_restaurants_with_online_orders_count = restaurants_by_city_with_online_orders.max()
            st.write(f"A cidade com mais restaurantes que aceitam pedidos online é {city_with_most_restaurants_with_online_orders}, com {most_restaurants_with_online_orders_count} restaurantes.")
        else:
            st.write("Nenhuma cidade encontrada com restaurantes que aceitam pedidos online.")


elif page == "Restaurantes":
    st.title("Análise Restaurantes")
    # st.write("Página Restaurantes")
    # Coloque o conteúdo da página Restaurantes aqui

        # Verificação de existência de dados após os filtros
    if df_filtered.empty:
        st.error("Nenhum dado disponível após aplicar os filtros selecionados.")
    else:
        # 1. Restaurante com a maior quantidade de avaliações
        st.header("1. Top 5 Restaurantes com Maior Quantidade de Avaliações")
        top_restaurants_votes = df_filtered[['restaurant_name', 'votes']].sort_values(by='votes', ascending=False).head(5)
        if not top_restaurants_votes.empty:
            st.bar_chart(data=top_restaurants_votes.set_index('restaurant_name')['votes'], height=300)
        else:
            st.write("Nenhum restaurante encontrado com avaliações registradas.")

        # 2. Restaurante com a maior nota média
        st.header("2. Top 5 Restaurantes com a Maior Nota Média")
        top_restaurants_ratings = df_filtered[['restaurant_name', 'aggregate_rating']].sort_values(by='aggregate_rating', ascending=False).head(5)
        if not top_restaurants_ratings.empty:
            st.bar_chart(data=top_restaurants_ratings.set_index('restaurant_name')['aggregate_rating'], height=300)
        else:
            st.write("Nenhum restaurante encontrado com notas médias registradas.")

        # 3. Restaurante com o maior valor de um prato para duas pessoas
        st.header("3. Top 5 Restaurantes com o Maior Valor de um Prato para Duas Pessoas")
        top_restaurants_cost = df_filtered[['restaurant_name', 'average_cost_for_two']].sort_values(by='average_cost_for_two', ascending=False).head(5)
        if not top_restaurants_cost.empty:
            st.bar_chart(data=top_restaurants_cost.set_index('restaurant_name')['average_cost_for_two'], height=300)
        else:
            st.write("Nenhum restaurante encontrado com valores de prato registrados.")

        # 4. Restaurante de culinária brasileira com a menor média de avaliação
        st.header("4. Qual o nome do restaurante de tipo de culinária brasileira que possui a menor média de avaliação?")
        brazilian_cuisine_restaurants = df_filtered[df_filtered['cuisines'].str.contains('Brazilian', case=False)]
        if not brazilian_cuisine_restaurants.empty:
            restaurant_with_lowest_rating = brazilian_cuisine_restaurants.loc[brazilian_cuisine_restaurants['aggregate_rating'].idxmin()]
            st.write(f"O restaurante de culinária brasileira com a menor média de avaliação é {restaurant_with_lowest_rating['restaurant_name']}, com nota {restaurant_with_lowest_rating['aggregate_rating']}.")
        else:
            st.write("Nenhum restaurante de culinária brasileira encontrado.")

        # 5. Restaurante de culinária brasileira no Brasil com a maior média de avaliação
        st.header("5. Qual o nome do restaurante de tipo de culinária brasileira, e que é do Brasil, que possui a maior média de avaliação?")
        brazilian_cuisine_brazil = df_filtered[(df_filtered['cuisines'].str.contains('Brazilian', case=False)) & (df_filtered['country'] == 'Brazil')]
        if not brazilian_cuisine_brazil.empty:
            restaurant_with_highest_rating = brazilian_cuisine_brazil.loc[brazilian_cuisine_brazil['aggregate_rating'].idxmax()]
            st.write(f"O restaurante de culinária brasileira, localizado no Brasil, com a maior média de avaliação é {restaurant_with_highest_rating['restaurant_name']}, com nota {restaurant_with_highest_rating['aggregate_rating']}.")
        else:
            st.write("Nenhum restaurante de culinária brasileira no Brasil encontrado.")

        # 6. Restaurantes que aceitam pedidos online possuem mais avaliações?
        st.header("6. Os restaurantes que aceitam pedido online são também, na média, os restaurantes que mais possuem avaliações registradas?")
        online_delivery_restaurants = df_filtered[df_filtered['has_online_delivery'] == 1]
        no_online_delivery_restaurants = df_filtered[df_filtered['has_online_delivery'] == 0]
        if not online_delivery_restaurants.empty and not no_online_delivery_restaurants.empty:
            mean_votes_online_delivery = online_delivery_restaurants['votes'].mean()
            mean_votes_no_online_delivery = no_online_delivery_restaurants['votes'].mean()
            st.write(f"Média de avaliações para restaurantes que aceitam pedidos online: {mean_votes_online_delivery:.2f}")
            st.write(f"Média de avaliações para restaurantes que não aceitam pedidos online: {mean_votes_no_online_delivery:.2f}")
            if mean_votes_online_delivery > mean_votes_no_online_delivery:
                st.write("Sim, os restaurantes que aceitam pedidos online possuem, na média, mais avaliações registradas.")
            else:
                st.write("Não, os restaurantes que aceitam pedidos online não possuem, na média, mais avaliações registradas.")
        else:
            st.write("Dados insuficientes para comparar restaurantes com e sem pedidos online.")

        # 7. Restaurantes que fazem reservas possuem maior valor médio de prato?
        st.header("7. Os restaurantes que fazem reservas são também, na média, os restaurantes que possuem o maior valor médio de um prato para duas pessoas?")
        restaurants_with_reservations = df_filtered[df_filtered['has_table_booking'] == 1]
        restaurants_without_reservations = df_filtered[df_filtered['has_table_booking'] == 0]
        if not restaurants_with_reservations.empty and not restaurants_without_reservations.empty:
            mean_cost_with_reservations = restaurants_with_reservations['average_cost_for_two'].mean()
            mean_cost_without_reservations = restaurants_without_reservations['average_cost_for_two'].mean()
            st.write(f"Valor médio de um prato para duas pessoas para restaurantes que aceitam reservas: {mean_cost_with_reservations:.2f}")
            st.write(f"Valor médio de um prato para duas pessoas para restaurantes que não aceitam reservas: {mean_cost_without_reservations:.2f}")
            if mean_cost_with_reservations > mean_cost_without_reservations:
                st.write("Sim, os restaurantes que fazem reservas possuem, na média, o maior valor médio de um prato para duas pessoas.")
            else:
                st.write("Não, os restaurantes que fazem reservas não possuem, na média, o maior valor médio de um prato para duas pessoas.")
        else:
            st.write("Dados insuficientes para comparar restaurantes com e sem reservas.")

        # 8. Comparação entre restaurantes japoneses e churrascarias nos EUA
        st.header("8. Os restaurantes do tipo de culinária japonesa dos Estados Unidos da América possuem um valor médio de prato para duas pessoas maior que as churrascarias americanas (BBQ)?")
        us_restaurants = df_filtered[df_filtered['country'] == 'United States of America']
        japanese_restaurants = us_restaurants[us_restaurants['cuisines'].str.contains('Japanese', case=False)]
        bbq_restaurants = us_restaurants[us_restaurants['cuisines'].str.contains('BBQ', case=False)]
        if not japanese_restaurants.empty and not bbq_restaurants.empty:
            mean_cost_japanese = japanese_restaurants['average_cost_for_two'].mean()
            mean_cost_bbq = bbq_restaurants['average_cost_for_two'].mean()
            st.write(f"Valor médio de um prato para duas pessoas em restaurantes japoneses nos EUA: {mean_cost_japanese:.2f}")
            st.write(f"Valor médio de um prato para duas pessoas em churrascarias (BBQ) nos EUA: {mean_cost_bbq:.2f}")
            if mean_cost_japanese > mean_cost_bbq:
                st.write("Sim, os restaurantes de culinária japonesa nos EUA possuem um valor médio de prato para duas pessoas maior que as churrascarias (BBQ).")
            else:
                st.write("Não, as churrascarias (BBQ) nos EUA possuem um valor médio de prato para duas pessoas maior que os restaurantes de culinária japonesa.")
        else:
            st.write("Dados insuficientes para comparar restaurantes japoneses e churrascarias nos EUA.")

elif page == "Culinária":
    st.title("Análise Culinária")
    # st.write("Página Culinária")
    # Coloque o conteúdo da página Culinária aqui

    
        # Verificação de existência de dados após os filtros
    if df_filtered.empty:
        st.error("Nenhum dado disponível após aplicar os filtros selecionados.")
    else:
            # 1. Restaurante italiano com a maior média de avaliação
            st.header("1. Dos restaurantes que possuem o tipo de culinária italiana, qual o nome do restaurante com a maior média de avaliação?")
            italian_restaurants = df_filtered[df_filtered['cuisines'].str.contains('Italian', case=False)]
            if not italian_restaurants.empty:
                top_italian_restaurant = italian_restaurants.loc[italian_restaurants['aggregate_rating'].idxmax()]
                st.write(f"O restaurante de culinária italiana com a maior média de avaliação é {top_italian_restaurant['restaurant_name']} com uma média de {top_italian_restaurant['aggregate_rating']:.2f}.")
            else:
                st.write("Nenhum restaurante de culinária italiana encontrado.")

            # 2. Restaurante italiano com a menor média de avaliação
            st.header("2. Dos restaurantes que possuem o tipo de culinária italiana, qual o nome do restaurante com a menor média de avaliação?")
            if not italian_restaurants.empty:
                bottom_italian_restaurant = italian_restaurants.loc[italian_restaurants['aggregate_rating'].idxmin()]
                st.write(f"O restaurante de culinária italiana com a menor média de avaliação é {bottom_italian_restaurant['restaurant_name']} com uma média de {bottom_italian_restaurant['aggregate_rating']:.2f}.")
            else:
                st.write("Nenhum restaurante de culinária italiana encontrado.")

            # 3. Restaurante americano com a maior média de avaliação
            st.header("3. Dos restaurantes que possuem o tipo de culinária americana, qual o nome do restaurante com a maior média de avaliação?")
            american_restaurants = df_filtered[df_filtered['cuisines'].str.contains('American', case=False)]
            if not american_restaurants.empty:
                top_american_restaurant = american_restaurants.loc[american_restaurants['aggregate_rating'].idxmax()]
                st.write(f"O restaurante de culinária americana com a maior média de avaliação é {top_american_restaurant['restaurant_name']} com uma média de {top_american_restaurant['aggregate_rating']:.2f}.")
            else:
                st.write("Nenhum restaurante de culinária americana encontrado.")

            # 4. Restaurante americano com a menor média de avaliação
            st.header("4. Dos restaurantes que possuem o tipo de culinária americana, qual o nome do restaurante com a menor média de avaliação?")
            if not american_restaurants.empty:
                bottom_american_restaurant = american_restaurants.loc[american_restaurants['aggregate_rating'].idxmin()]
                st.write(f"O restaurante de culinária americana com a menor média de avaliação é {bottom_american_restaurant['restaurant_name']} com uma média de {bottom_american_restaurant['aggregate_rating']:.2f}.")
            else:
                st.write("Nenhum restaurante de culinária americana encontrado.")

            # 5. Restaurante árabe com a maior média de avaliação
            st.header("5. Dos restaurantes que possuem o tipo de culinária árabe, qual o nome do restaurante com a maior média de avaliação?")
            arabic_restaurants = df_filtered[df_filtered['cuisines'].str.contains('Arabian', case=False)]
            if not arabic_restaurants.empty:
                top_arabic_restaurant = arabic_restaurants.loc[arabic_restaurants['aggregate_rating'].idxmax()]
                st.write(f"O restaurante de culinária árabe com a maior média de avaliação é {top_arabic_restaurant['restaurant_name']} com uma média de {top_arabic_restaurant['aggregate_rating']:.2f}.")
            else:
                st.write("Nenhum restaurante de culinária árabe encontrado.")

            # 6. Restaurante árabe com a menor média de avaliação
            st.header("6. Dos restaurantes que possuem o tipo de culinária árabe, qual o nome do restaurante com a menor média de avaliação?")
            if not arabic_restaurants.empty:
                bottom_arabic_restaurant = arabic_restaurants.loc[arabic_restaurants['aggregate_rating'].idxmin()]
                st.write(f"O restaurante de culinária árabe com a menor média de avaliação é {bottom_arabic_restaurant['restaurant_name']} com uma média de {bottom_arabic_restaurant['aggregate_rating']:.2f}.")
            else:
                st.write("Nenhum restaurante de culinária árabe encontrado.")

            # 7. Restaurante japonês com a maior média de avaliação
            st.header("7. Dos restaurantes que possuem o tipo de culinária japonesa, qual o nome do restaurante com a maior média de avaliação?")
            japanese_restaurants = df_filtered[df_filtered['cuisines'].str.contains('Japanese', case=False)]
            if not japanese_restaurants.empty:
                top_japanese_restaurant = japanese_restaurants.loc[japanese_restaurants['aggregate_rating'].idxmax()]
                st.write(f"O restaurante de culinária japonesa com a maior média de avaliação é {top_japanese_restaurant['restaurant_name']} com uma média de {top_japanese_restaurant['aggregate_rating']:.2f}.")
            else:
                st.write("Nenhum restaurante de culinária japonesa encontrado.")

            # 8. Restaurante japonês com a menor média de avaliação
            st.header("8. Dos restaurantes que possuem o tipo de culinária japonesa, qual o nome do restaurante com a menor média de avaliação?")
            if not japanese_restaurants.empty:
                bottom_japanese_restaurant = japanese_restaurants.loc[japanese_restaurants['aggregate_rating'].idxmin()]
                st.write(f"O restaurante de culinária japonesa com a menor média de avaliação é {bottom_japanese_restaurant['restaurant_name']} com uma média de {bottom_japanese_restaurant['aggregate_rating']:.2f}.")
            else:
                st.write("Nenhum restaurante de culinária japonesa encontrado.")

            # 9. Restaurante de culinária caseira com a maior média de avaliação
            st.header("9. Dos restaurantes que possuem o tipo de culinária caseira, qual o nome do restaurante com a maior média de avaliação?")
            home_cooked_restaurants = df_filtered[df_filtered['cuisines'].str.contains('Home', case=False)]
            if not home_cooked_restaurants.empty:
                top_home_cooked_restaurant = home_cooked_restaurants.loc[home_cooked_restaurants['aggregate_rating'].idxmax()]
                st.write(f"O restaurante de culinária caseira com a maior média de avaliação é {top_home_cooked_restaurant['restaurant_name']} com uma média de {top_home_cooked_restaurant['aggregate_rating']:.2f}.")
            else:
                st.write("Nenhum restaurante de culinária caseira encontrado.")

            # 10. Restaurante de culinária caseira com a menor média de avaliação
            st.header("10. Dos restaurantes que possuem o tipo de culinária caseira, qual o nome do restaurante com a menor média de avaliação?")
            if not home_cooked_restaurants.empty:
                bottom_home_cooked_restaurant = home_cooked_restaurants.loc[home_cooked_restaurants['aggregate_rating'].idxmin()]
                st.write(f"O restaurante de culinária caseira com a menor média de avaliação é {bottom_home_cooked_restaurant['restaurant_name']} com uma média de {bottom_home_cooked_restaurant['aggregate_rating']:.2f}.")
            else:
                st.write("Nenhum restaurante de culinária caseira encontrado.")

                    # 11. Tipo de culinária com maior valor médio de um prato para duas pessoas
            st.header("11. Qual o tipo de culinária que possui o maior valor médio de um prato para duas pessoas?")
            if not df_filtered.empty:
                df_filtered['cuisines'] = df_filtered['cuisines'].apply(lambda x: x.split(",")[0])
                average_cost_by_cuisine = df_filtered.groupby('cuisines')['average_cost_for_two'].mean()
                most_expensive_cuisine = average_cost_by_cuisine.idxmax()
                most_expensive_value = average_cost_by_cuisine.max()
                st.write(f"O tipo de culinária que possui o maior valor médio de um prato para duas pessoas é {most_expensive_cuisine} com um valor médio de {most_expensive_value:.2f}.")
            else:
                st.write("Nenhum dado disponível para essa análise.")

            # 12. Tipo de culinária com a maior nota média
            st.header("12. Qual o tipo de culinária que possui a maior nota média?")
            if not df_filtered.empty:
                average_rating_by_cuisine = df_filtered.groupby('cuisines')['aggregate_rating'].mean()
                highest_rating_cuisine = average_rating_by_cuisine.idxmax()
                highest_rating_value = average_rating_by_cuisine.max()
                st.write(f"O tipo de culinária que possui a maior nota média é {highest_rating_cuisine} com uma nota média de {highest_rating_value:.2f}.")
            else:
                st.write("Nenhum dado disponível para essa análise.")

            # 13. Tipo de culinária com mais restaurantes que aceitam pedidos online e fazem entregas
            st.header("13. Qual o tipo de culinária que possui mais restaurantes que aceitam pedidos online e fazem entregas?")
            online_delivery_restaurants = df_filtered[(df_filtered['has_online_delivery'] == 1) & (df_filtered['has_table_booking'] == 1)]
            if not online_delivery_restaurants.empty:
                online_delivery_restaurants['cuisines'] = online_delivery_restaurants['cuisines'].apply(lambda x: x.split(",")[0])
                cuisine_counts = online_delivery_restaurants['cuisines'].value_counts()
                most_common_cuisine = cuisine_counts.idxmax()
                most_common_cuisine_count = cuisine_counts.max()
                st.write(f"O tipo de culinária que possui mais restaurantes que aceitam pedidos online e fazem entregas é {most_common_cuisine} com {most_common_cuisine_count} restaurantes.")
            else:
                st.write("Nenhum restaurante disponível que aceita pedidos online e faz entregas.")