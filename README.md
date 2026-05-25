# Zomato Analytics Dashboard

Dashboard interativo de análise de dados de restaurantes da plataforma Zomato, construído com Python e Streamlit.

## Visão Geral

Este projeto transforma um dataset bruto com ~9.500 registros de restaurantes em 15 países em um dashboard analítico com 5 perspectivas de negócio: Geral, País, Cidade, Restaurantes e Culinária.

## Stack

| Tecnologia | Uso |
|------------|-----|
| Python 3.9+ | Linguagem principal |
| Streamlit | Framework do dashboard |
| Pandas | Manipulação e análise de dados |
| NumPy | Operações numéricas |
| Matplotlib | Visualização de gráficos |

## Como Executar

```bash
# 1. Clonar o repositório
git clone https://github.com/victorrabelo98/python-dashboard-streamlit.git
cd python-dashboard-streamlit

# 2. Instalar dependências
pip install -r requirements.txt

# 3. Executar o dashboard
streamlit run app.py
```

O dashboard abrirá em `http://localhost:8501`.

## Estrutura do Projeto

```
├── app.py                  # Dashboard corrigido (versão de produção)
├── requirements.txt        # Dependências
├── ProjetoFinal/
│   ├── zomato.csv          # Dataset (não modificar)
│   ├── final.py            # Código original (referência)
│   ├── view1.py            # Versão intermediária
│   └── view2.py            # Versão intermediária com gráficos
└── docs/
    ├── STORYTELLING.md         # Narrativa do projeto
    ├── BUSINESS_CONTEXT.md     # Perguntas de negócio e contexto
    ├── STACK_AND_ARCHITECTURE.md  # Stack e arquitetura
    ├── DEVELOPMENT_PROCESS.md  # Processo de criação
    └── CHANGELOG.md            # Correções documentadas
```

## Funcionalidades

- **Filtros dinâmicos** por país e tipo de culinária
- **Mapa geoespacial** dos restaurantes
- **5 perspectivas analíticas** com 33 perguntas de negócio respondidas
- **Cards de KPI** com métricas principais
- **Gráficos de barras** comparativos

## Documentação

- [Storytelling do Projeto](docs/STORYTELLING.md)
- [Contexto de Negócio](docs/BUSINESS_CONTEXT.md)
- [Stack e Arquitetura](docs/STACK_AND_ARCHITECTURE.md)
- [Processo de Desenvolvimento](docs/DEVELOPMENT_PROCESS.md)
- [Changelog de Correções](docs/CHANGELOG.md)

## Autor

Victor Rabelo de Campos
