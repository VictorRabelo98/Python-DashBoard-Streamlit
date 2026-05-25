# Stack e Arquitetura — Zomato Analytics Dashboard

## Visão Geral da Stack

```
┌─────────────────────────────────────────────────┐
│                   USUÁRIO                        │
│              (Browser / Web App)                 │
└─────────────────────┬───────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────┐
│               STREAMLIT (Frontend + Backend)     │
│  • Roteamento de páginas                         │
│  • Componentes interativos (filtros, widgets)    │
│  • Renderização de gráficos e mapas              │
└─────────────────────┬───────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────┐
│           CAMADA DE VISUALIZAÇÃO                 │
│  • Matplotlib — gráficos de barras               │
│  • Folium + streamlit-folium — mapas interativos │
│  • st.metric — cards de KPI                      │
│  • st.bar_chart — gráficos nativos Streamlit     │
└─────────────────────┬───────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────┐
│           CAMADA DE DADOS (Pandas + NumPy)       │
│  • Limpeza: remoção de duplicatas, nulos,        │
│    colunas com valor único                       │
│  • Enriquecimento: mapeamento de códigos,        │
│    criação de colunas derivadas                  │
│  • Filtragem: filtros dinâmicos por país e       │
│    culinária aplicados em tempo real             │
└─────────────────────┬───────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────┐
│              FONTE DE DADOS                      │
│              zomato.csv (~9.500 linhas)          │
└─────────────────────────────────────────────────┘
```

---

## Tecnologias Utilizadas

### Core

| Tecnologia | Versão Recomendada | Função |
|------------|-------------------|--------|
| **Python** | 3.9+ | Linguagem principal |
| **Streamlit** | 1.28+ | Framework de dashboard |
| **Pandas** | 2.0+ | Manipulação de dados |
| **NumPy** | 1.24+ | Operações numéricas |

### Visualização

| Tecnologia | Versão Recomendada | Função |
|------------|-------------------|--------|
| **Matplotlib** | 3.7+ | Gráficos de barras estáticos |
| **Folium** | 0.14+ | Mapas interativos (Leaflet.js) |
| **streamlit-folium** | 0.15+ | Integração Folium + Streamlit |

### Dados

| Arquivo | Formato | Tamanho Aprox. |
|---------|---------|----------------|
| `zomato.csv` | CSV UTF-8 | ~1.5 MB |

---

## Estrutura de Arquivos Recomendada

```
Python-DashBoard-Streamlit/
│
├── ProjetoFinal/
│   ├── zomato.csv              # Dataset original (não modificar)
│   ├── final.py                # Arquivo original (referência histórica)
│   ├── view1.py                # Versão intermediária
│   ├── view2.py                # Versão intermediária com gráficos
│   └── 1.py                    # Exploração inicial
│
├── docs/
│   ├── STORYTELLING.md         # Narrativa do projeto
│   ├── BUSINESS_CONTEXT.md     # Contexto e perguntas de negócio
│   ├── STACK_AND_ARCHITECTURE.md  # Este arquivo
│   ├── DEVELOPMENT_PROCESS.md  # Processo de criação
│   └── CHANGELOG.md            # Melhorias e correções documentadas
│
├── app.py                      # Código corrigido e pronto para produção
├── requirements.txt            # Dependências do projeto
└── README.md                   # Documentação principal
```

---

## Fluxo de Dados

```
zomato.csv
    │
    ▼ pd.read_csv()
DataFrame bruto (~9.500 linhas, 21 colunas)
    │
    ▼ Remover colunas com valor único
DataFrame sem colunas inúteis
    │
    ▼ drop_duplicates()
DataFrame sem linhas repetidas
    │
    ▼ dropna()
DataFrame limpo (~6.000 linhas)
    │
    ▼ Normalizar nomes de colunas
DataFrame com snake_case
    │
    ▼ Enriquecimento (country, color_name, price_type)
DataFrame enriquecido (df_4)
    │
    ▼ Filtros dinâmicos (país, culinária)
df_filtered → Visualizações nas páginas
```

---

## Decisões de Design

### Por que Streamlit?

- **Zero frontend** — o analista de dados escreve apenas Python
- **Hot reload** — mudanças no código refletem imediatamente no browser
- **Componentes prontos** — sidebars, multiselect, metrics, maps sem configuração extra
- **Deploy simples** — Streamlit Cloud com push no GitHub

### Por que Matplotlib ao invés de Plotly?

O projeto usa Matplotlib por ser a escolha original do desenvolvedor e por sua integração direta com pandas (`.plot(kind='bar')`). Plotly ofereceria interatividade adicional nos gráficos, mas exigiria refatoração completa.

### Por que Folium para o mapa?

Folium gera mapas baseados em Leaflet.js com marcadores, popups e layers avançadas. `st.map()` (nativo do Streamlit) é mais simples mas sem customização. A versão final usa `st.map()` pela simplicidade — Folium fica disponível para evolução.

---

## Requirements

```
streamlit>=1.28.0
pandas>=2.0.0
numpy>=1.24.0
matplotlib>=3.7.0
folium>=0.14.0
streamlit-folium>=0.15.0
```

---

## Como Executar

```bash
# Instalar dependências
pip install -r requirements.txt

# Executar o dashboard
streamlit run app.py
```

O dashboard abrirá automaticamente em `http://localhost:8501`.

---

## Considerações de Performance

| Situação | Impacto | Solução |
|----------|---------|---------|
| Leitura do CSV a cada requisição | Lento em produção | Usar `@st.cache_data` |
| Filtros recalculam todo pipeline | Ineficiente | Cache no `df_4` processado |
| Muitos `plt.subplots()` abertos | Vazamento de memória | `plt.close(fig)` após `st.pyplot()` |

A versão corrigida (`app.py`) implementa `@st.cache_data` para carregar e processar os dados apenas uma vez por sessão.
