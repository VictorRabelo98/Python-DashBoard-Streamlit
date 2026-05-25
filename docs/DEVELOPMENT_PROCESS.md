# Processo de Desenvolvimento — Zomato Analytics Dashboard

## Visão Geral

Este documento descreve o processo de criação do dashboard passo a passo, desde a definição do problema até a entrega da versão funcional.

---

## Etapas do Processo

### 1. Entendimento do Problema (Problem Framing)

**O que foi feito:**
- Leitura do dataset `zomato.csv` para entender estrutura e conteúdo
- Levantamento das perguntas de negócio a responder (33 no total)
- Definição das 5 perspectivas analíticas: Geral, País, Cidade, Restaurante, Culinária
- Escolha da ferramenta: Streamlit por permitir desenvolvimento rápido em Python puro

**Saída:** Lista de perguntas de negócio organizadas por categoria

---

### 2. Exploração dos Dados (EDA — Exploratory Data Analysis)

**Arquivo de referência:** `ProjetoFinal/1.py`

**O que foi feito:**
```python
# Leitura inicial
df = pd.read_csv("zomato.csv")

# Exploração da estrutura
df.head(5)
df.describe(include='all')
df.isnull().sum()
df.duplicated().sum()
df.nunique()
```

**Descobertas:**
| Problema encontrado | Quantidade |
|--------------------|-----------|
| Colunas com valor único | 1 (`Switch to order menu`) |
| Linhas duplicadas | ~60 |
| Valores nulos | Presentes em múltiplas colunas |
| Colunas com nomes mal formatados | Todas (com espaços e parênteses) |
| Códigos sem legenda | `country_code`, `rating_color` |

**Saída:** Diagnóstico completo do dataset, lista de problemas a corrigir

---

### 3. Limpeza de Dados (Data Cleaning)

**Pipeline de limpeza definido:**

```
Passo 1: Remover colunas com valor único (zero variância)
Passo 2: Remover linhas duplicadas
Passo 3: Remover linhas com valores nulos
Passo 4: Normalizar nomes de colunas (snake_case)
```

**Detalhamento de cada passo:**

#### Passo 1 — Colunas com valor único
```python
cols_to_remove = [col for col in df.columns if df[col].nunique() == 1]
df_1 = df.drop(columns=cols_to_remove)
```
*Motivo: Coluna com um único valor não agrega informação analítica.*

#### Passo 2 — Duplicatas
```python
df_2 = df_1.drop_duplicates()
```
*Motivo: Registros duplicados distorcem contagens e médias.*

#### Passo 3 — Nulos
```python
df_3 = df_2.dropna(axis=0, how='any')
```
*Motivo: Linhas incompletas comprometem análises que cruzam múltiplas colunas.*

#### Passo 4 — Normalização de nomes
```python
df_3.columns = (df_3.columns
    .str.strip()
    .str.lower()
    .str.replace(' ', '_')
    .str.replace('(', '')
    .str.replace(')', ''))
```
*Motivo: Colunas com espaços exigem sintaxe `df['coluna com espaco']` em vez de `df.coluna`. snake_case é padrão Python.*

---

### 4. Enriquecimento dos Dados (Feature Engineering)

**Três novas colunas criadas:**

#### `price_type` — Categoria de preço
```python
def create_price_type(price_range):
    mapping = {1: "cheap", 2: "normal", 3: "expensive"}
    return mapping.get(price_range, "gourmet")

df_4['price_type'] = df_4['price_range'].apply(create_price_type)
```

#### `country` — Nome do país
```python
COUNTRIES = {1: "India", 30: "Brazil", 216: "United States of America", ...}

def country_name(country_code):
    return COUNTRIES.get(country_code, "Unknown")

df_4['country'] = df_4['country_code'].apply(country_name)
```

#### `color_name` — Categoria de rating por cor
```python
COLORS = {"3F7E00": "darkgreen", "FFBA00": "red", ...}

def color_name(rating_color):
    return COLORS.get(rating_color, "Unknown")

df_4['color_name'] = df_4['rating_color'].apply(color_name)
```

#### Simplificação da coluna `cuisines`
```python
df_4["cuisines"] = df_4["cuisines"].apply(lambda x: x.split(",")[0])
```
*Motivo: Muitos restaurantes listam múltiplas culinárias. Para análise categórica, o primeiro tipo é o principal.*

---

### 5. Prototipagem do Dashboard (Iterações)

O desenvolvimento passou por 3 versões iterativas:

#### Versão 1 (`view1.py`) — MVP funcional
- Sidebar com selectbox para navegação
- Respostas em texto puro (`st.write()`)
- Sem gráficos
- Sem tratamento de erros (crash se filtro resultar em DataFrame vazio)

#### Versão 2 (`1.py` e `view2.py`) — Cards e gráficos
- Adição de `st.metric()` para KPIs
- Gráficos de barras com Matplotlib
- Navegação horizontal com `st.radio()`
- Tratamento básico de DataFrames vazios

#### Versão Final (`final.py` / `app.py`) — Dashboard completo
- Mapa com `st.map()`
- Tratamento robusto de erros
- Filtros compostos (país + culinária)
- Layout em colunas para melhor organização visual

---

### 6. Identificação e Correção de Erros

Problemas identificados no código original e corrigidos na versão `app.py`:

| # | Problema | Arquivo(s) afetado(s) | Impacto |
|---|---------|----------------------|---------|
| 1 | Caminho absoluto hardcoded (`C:/Users/Victor/...`) | Todos | App não executa em nenhuma outra máquina |
| 2 | `print()` em código Streamlit | Todos | Output vai para terminal, não para o browser |
| 3 | Modificação de `df_filtered` dentro de `elif` | `final.py` L756 | Efeito colateral entre renders |
| 4 | Sem `@st.cache_data` | Todos | CSV relido a cada interação do usuário |
| 5 | `plt.subplots()` sem `plt.close(fig)` | `final.py`, `view2.py` | Vazamento de memória em sessões longas |
| 6 | Filtro de culinária com regex não escapado | Todos | Crash com culinárias contendo `+`, `.`, `(` |
| 7 | Crash quando filtro resulta em df vazio (`view1.py`) | `view1.py` | `idxmax()` em Series vazia lança ValueError |
| 8 | SettingWithCopyWarning no `online_delivery_restaurants` | `view1.py` L512 | Possível modificação silenciosa do df original |
| 9 | Coluna `cuisines` re-split em seção de Culinária | `final.py` L756 | Dado já estava processado, re-split desnecessário |
| 10 | `import folium` e `folium_static` importados mas mapa usa `st.map()` | `final.py` | Dependência desnecessária instalada |

---

### 7. Entrega

**Artefatos gerados:**

| Arquivo | Descrição |
|---------|-----------|
| `app.py` | Código corrigido, pronto para produção |
| `requirements.txt` | Dependências do projeto |
| `docs/STORYTELLING.md` | Narrativa do projeto |
| `docs/BUSINESS_CONTEXT.md` | Perguntas de negócio e contexto |
| `docs/STACK_AND_ARCHITECTURE.md` | Stack técnica e arquitetura |
| `docs/DEVELOPMENT_PROCESS.md` | Este documento |
| `docs/CHANGELOG.md` | Detalhamento das correções |
| `README.md` | Documentação atualizada |
