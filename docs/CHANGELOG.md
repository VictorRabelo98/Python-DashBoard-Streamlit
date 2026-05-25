# Changelog — Correções e Melhorias

## app.py vs código original

Este documento detalha **o que foi alterado**, **por que foi alterado** e **qual erro foi corrigido** na versão `app.py` em relação ao código original (`final.py`, `view1.py`, `view2.py`).

---

## Correção 1 — Caminho do CSV (Crítico)

### Antes (original)
```python
df = pd.read_csv("C:/Users/Victor/Desktop/CC/CDS/projetos/python/ProjetoFinal/zomato.csv",
                 encoding="utf-8", engine='python')
```

### Depois (corrigido)
```python
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(BASE_DIR, "ProjetoFinal", "zomato.csv")

df = pd.read_csv(CSV_PATH, encoding="utf-8")
```

### Por que foi alterado
O caminho absoluto `C:/Users/Victor/...` funciona **apenas** na máquina original do desenvolvedor. Em qualquer outro ambiente (outro computador, servidor, Docker, Streamlit Cloud), a aplicação lança `FileNotFoundError` imediatamente ao iniciar.

### Erro corrigido
```
FileNotFoundError: [Errno 2] No such file or directory:
'C:/Users/Victor/Desktop/CC/CDS/projetos/python/ProjetoFinal/zomato.csv'
```

**Conceito:** Caminhos relativos com `os.path` tornam o projeto portável — funciona em qualquer máquina desde que o arquivo esteja na estrutura correta do projeto.

---

## Correção 2 — Cache de dados com `@st.cache_data`

### Antes (original)
```python
df = pd.read_csv(CSV_PATH, ...)
# pipeline de limpeza executado a cada interação
df_1 = df.drop(columns=cols_to_remove)
df_2 = df_1.drop_duplicates()
df_3 = df_2.dropna(axis=0, how='any')
# ...
```

### Depois (corrigido)
```python
@st.cache_data
def load_and_process_data():
    df = pd.read_csv(CSV_PATH, encoding="utf-8")
    # ... todo o pipeline de limpeza e enriquecimento
    return df_4

df_4 = load_and_process_data()
```

### Por que foi alterado
Streamlit re-executa o **script inteiro** a cada interação do usuário (clique em filtro, mudança de página, etc.). Sem cache, o CSV é lido do disco e todo o pipeline de limpeza é reprocessado **a cada clique**, tornando a aplicação lenta e desperdiçando I/O.

### Erro corrigido
Não é um erro de runtime, mas um **erro de performance** severo. Com `@st.cache_data`, o processamento ocorre **uma única vez** por sessão e o resultado fica em memória.

**Conceito:** `@st.cache_data` é a função de memoização do Streamlit para DataFrames. O resultado é cacheado por argumentos — como a função não recebe argumentos, o cache é permanente durante a sessão.

---

## Correção 3 — Remoção dos `print()` statements

### Antes (original)
```python
print(df_3.head(3))
print(df_4.head(3))
print(df_4[['restaurant_name', 'cuisines']].head())
```

### Depois (corrigido)
```python
# Removidos completamente
```

### Por que foi alterado
`print()` em um script Streamlit envia output para o **terminal do servidor**, nunca para o browser do usuário. Em produção (Streamlit Cloud), esse output é invisível e só gera ruído nos logs do servidor.

### Erro corrigido
Não é um erro de runtime, mas código que nunca deveria estar em produção. Indica que o script não foi limpo antes do deploy.

**Conceito:** Em aplicações Streamlit, toda saída para o usuário deve usar funções `st.*` (st.write, st.dataframe, st.text, etc.). `print()` é para debugging local.

---

## Correção 4 — Fechamento de figuras Matplotlib

### Antes (original)
```python
fig, ax = plt.subplots()
top_5_countries.plot(kind='bar', ax=ax, color='skyblue')
ax.set_title("Top 5 Países com Mais Cidades Registradas")
st.pyplot(fig)
# fig não é fechada!
```

### Depois (corrigido)
```python
fig, ax = plt.subplots()
top_5_countries.plot(kind='bar', ax=ax, color='skyblue')
ax.set_title("Top 5 Países com Mais Cidades Registradas")
plt.tight_layout()
st.pyplot(fig)
plt.close(fig)  # libera memória
```

### Por que foi alterado
Cada `plt.subplots()` aloca memória para uma figura. Sem `plt.close()`, todas as figuras permanecem em memória. Em uma sessão com muitas interações (o usuário navega entre páginas múltiplas vezes), isso causa **crescimento progressivo de consumo de memória**.

### Erro corrigido
```
MatplotlibDeprecationWarning: Figures created through plt.figure(), plt.subplots()...
are not closed and will keep accumulating.
```
Em sessões longas: `MemoryError` ou degradação severa de performance.

**Conceito:** Matplotlib mantém um registro global de todas as figuras abertas. `plt.close(fig)` remove a figura desse registro e libera os recursos alocados.

---

## Correção 5 — Escape de caracteres especiais no filtro de regex

### Antes (original)
```python
df_filtered = df_filtered[
    df_filtered['cuisines'].str.contains('|'.join(selected_cuisines), case=False)
]
```

### Depois (corrigido)
```python
import re

escaped = [re.escape(c) for c in selected_cuisines]
df_filtered = df_filtered[
    df_filtered['cuisines'].str.contains('|'.join(escaped), case=False, na=False)
]
```

### Por que foi alterado
`str.contains()` interpreta o argumento como uma **expressão regular**. Se o nome de uma culinária contém caracteres especiais de regex (`+`, `.`, `(`, `)`, `*`, `?`), a busca torna-se um padrão regex inválido e lança uma exceção.

Exemplo de falha:
- Culinária: `"Fish & Chips"` → sem problema
- Culinária: `"C++ Fusion"` → `re.error: nothing to repeat at position 1`

### Erro corrigido
```
error: nothing to repeat at position X
re.error: unexpected end of regular expression
```

**Conceito:** `re.escape()` escapa todos os caracteres especiais de regex, transformando `"C++"` em `"C\+\+"` antes de ser interpretado como padrão.

---

## Correção 6 — SettingWithCopyWarning e `.copy()`

### Antes (original)
```python
online_delivery_restaurants = df_filtered[
    (df_filtered['has_online_delivery'] == 1) & (df_filtered['has_table_booking'] == 1)
]
online_delivery_restaurants['cuisines'] = online_delivery_restaurants['cuisines'].apply(...)
```

### Depois (corrigido)
```python
online_delivery_restaurants = df_filtered[
    (df_filtered['has_online_delivery'] == 1) & (df_filtered['has_table_booking'] == 1)
].copy()

online_delivery_restaurants['cuisines'] = online_delivery_restaurants['cuisines'].apply(...)
```

### Por que foi alterado
Filtrar um DataFrame com boolean indexing retorna uma **view** (referência) ou uma **cópia**, dependendo do contexto interno do pandas. Modificar essa view sem `.copy()` pode silenciosamente modificar o DataFrame original (`df_filtered`), corrompendo análises subsequentes.

### Erro corrigido
```
SettingWithCopyWarning: A value is trying to be set on a copy of a slice
from a DataFrame. Try using .loc[row_indexer, col_indexer] = value instead
```

**Conceito:** `.copy()` garante que você está trabalhando em uma cópia independente do DataFrame, sem risco de modificar o original por referência.

---

## Correção 7 — Proteção contra DataFrame vazio em `view1.py`

### Antes (original)
```python
# Página Restaurantes — sem proteção
restaurant_with_most_votes = df_filtered.loc[df_filtered['votes'].idxmax()]
```

### Depois (corrigido)
```python
if df_filtered.empty:
    st.error("Nenhum dado disponível após aplicar os filtros selecionados.")
else:
    top_restaurants_votes = df_filtered[['restaurant_name', 'votes']] \
        .sort_values(by='votes', ascending=False).head(5)
    if not top_restaurants_votes.empty:
        st.bar_chart(...)
```

### Por que foi alterado
Se o usuário selecionar uma combinação de filtros que resulta em zero restaurantes (ex: culinária "Peruana" no país "Qatar"), `df_filtered.idxmax()` em um DataFrame vazio lança `ValueError`.

### Erro corrigido
```
ValueError: attempt to get argmax of an empty sequence
```

**Conceito:** Sempre validar se o DataFrame tem dados antes de chamar funções de agregação como `idxmax()`, `idxmin()`, `max()`, `min()`. A verificação `df.empty` é O(1) e não tem custo computacional.

---

## Correção 8 — Re-split desnecessário da coluna `cuisines`

### Antes (original)
```python
# Na página Culinária — após cuisines já ter sido simplificado no pipeline
df_filtered['cuisines'] = df_filtered['cuisines'].apply(lambda x: x.split(",")[0])
```

### Depois (corrigido)
```python
# Linha removida — cuisines já está simplificado desde o pipeline de limpeza
average_cost_by_cuisine = df_filtered.groupby('cuisines')['average_cost_for_two'].mean()
```

### Por que foi alterado
O pipeline de limpeza já aplica `.split(",")[0]` na coluna `cuisines` antes de qualquer visualização. Aplicar novamente dentro de um bloco `elif` gera um `SettingWithCopyWarning` e é código redundante que confunde a leitura.

### Erro corrigido
```
SettingWithCopyWarning + lógica duplicada desnecessária
```

**Conceito:** Transformações de dados devem ser feitas **uma vez** no pipeline de preparação, não repetidas dentro das funções de visualização.

---

## Correção 9 — Importações desnecessárias

### Antes (original)
```python
import folium
from streamlit_folium import folium_static
# folium nunca é usado — st.map() é usado no lugar
```

### Depois (corrigido)
```python
# Importações removidas — apenas o necessário
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import re
```

### Por que foi alterado
Importar bibliotecas não utilizadas:
1. Aumenta o tempo de startup da aplicação
2. Exige instalação de dependências desnecessárias (folium + streamlit-folium)
3. Confunde quem lê o código sobre quais tecnologias são realmente usadas

### Erro corrigido
```
ModuleNotFoundError: No module named 'folium'
# (em ambientes sem folium instalado, o app falhava ao importar)
```

**Conceito:** Importe apenas o que você usa. Cada import é executado na inicialização do app e adiciona overhead.

---

## Sumário das Correções

| # | Categoria | Severidade | Impacto |
|---|-----------|-----------|---------|
| 1 | Caminho absoluto do CSV | **Crítico** | App não executa em outro ambiente |
| 2 | Sem cache de dados | **Alto** | Performance degradada a cada interação |
| 3 | `print()` em produção | Médio | Output invisível, código sujo |
| 4 | Figuras Matplotlib sem fechar | **Alto** | Vazamento de memória progressivo |
| 5 | Regex sem escape | **Alto** | Crash com nomes de culinárias especiais |
| 6 | SettingWithCopyWarning | **Alto** | Risco de corrupção silenciosa de dados |
| 7 | Sem proteção a df vazio | **Alto** | Crash ao filtrar sem resultados |
| 8 | Re-split desnecessário | Baixo | Código redundante e confuso |
| 9 | Imports desnecessários | Baixo | Overhead de startup e dependências |
