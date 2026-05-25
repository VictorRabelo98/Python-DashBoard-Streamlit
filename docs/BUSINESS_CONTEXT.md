# Contexto de Negócio — Zomato Analytics Dashboard

## Sobre a Zomato

A **Zomato** é uma plataforma global de discovery e delivery de restaurantes fundada em 2008 na Índia. Opera em mais de 25 países conectando usuários a restaurantes por meio de avaliações, cardápios digitais e pedidos online.

O dataset utilizado neste projeto representa um **snapshot histórico** da plataforma com dados de restaurantes em 15 países.

---

## Problema de Negócio

### Contexto

Gestores, investidores e empreendedores do setor gastronômico enfrentam um desafio comum: **tomar decisões estratégicas em um mercado fragmentado e altamente competitivo** sem acesso fácil a dados consolidados.

Perguntas como:

- Onde há maior concentração de restaurantes?
- Qual país tem maior potencial de expansão (poucos restaurantes, alta satisfação)?
- Quais tipos de culinária têm melhor desempenho em avaliações?
- O delivery realmente impacta a percepção do cliente?

...ficam sem resposta quando os dados estão dispersos em planilhas brutas.

### Dor Central

> **Dados brutos existem. Inteligência analítica não.**

O arquivo `zomato.csv` contém informações valiosas, mas em formato inacessível para tomada de decisão: colunas codificadas, dados sujos, sem visualização e sem filtragem interativa.

---

## Objetivo do Projeto

Construir um **dashboard analítico interativo** que:

1. **Limpe e padronize** os dados da Zomato automaticamente
2. **Enriqueça** o dataset com variáveis derivadas (nome do país, categoria de preço, etc.)
3. **Visualize** os dados em múltiplas perspectivas (País, Cidade, Restaurante, Culinária)
4. **Permita filtragem dinâmica** por país e tipo de culinária
5. **Responda perguntas de negócio** de forma visual e interativa

---

## Perguntas de Negócio Respondidas

### Perspectiva Global (Geral)
| # | Pergunta | Tipo de Resposta |
|---|----------|-----------------|
| 1 | Quantos restaurantes únicos estão registrados? | Métrica |
| 2 | Quantos países únicos estão registrados? | Métrica |
| 3 | Quantas cidades únicas estão registradas? | Métrica |
| 4 | Qual o total de avaliações feitas? | Métrica |
| 5 | Qual o total de tipos de culinária registrados? | Métrica |

### Perspectiva País
| # | Pergunta | Tipo de Resposta |
|---|----------|-----------------|
| 1 | Qual país possui mais cidades registradas? | Gráfico + texto |
| 2 | Top 5 países com mais restaurantes registrados | Gráfico |
| 3 | Top 5 países com mais restaurantes gourmet (preço 4) | Gráfico |
| 4 | País com maior diversidade culinária | Métrica |
| 5 | País com mais avaliações | Métrica |
| 6 | País com mais restaurantes com delivery | Métrica |
| 7 | País com mais restaurantes com reservas | Métrica |
| 8 | Top 5 países com maior volume de avaliações | Gráfico |
| 9 | Top 5 países com maior nota média | Gráfico |
| 10 | Top 5 países com menor nota média | Gráfico |
| 11 | Média de preço do prato para dois por país | Gráfico |

### Perspectiva Cidade
| # | Pergunta | Tipo de Resposta |
|---|----------|-----------------|
| 1 | Cidade com mais restaurantes registrados | Card |
| 2 | Cidade com mais restaurantes nota > 4 | Card |
| 3 | Cidade com mais restaurantes nota < 2.5 | Card |
| 4 | Cidade com maior ticket médio | Card |
| 5 | Top 5 cidades com mais tipos de culinária | Gráfico |
| 6 | Cidade com mais restaurantes com reserva | Texto |
| 7 | Cidade com mais restaurantes com delivery | Texto |
| 8 | Cidade com mais pedidos online | Texto |

### Perspectiva Restaurantes
| # | Pergunta | Tipo de Resposta |
|---|----------|-----------------|
| 1 | Top 5 restaurantes com mais avaliações | Gráfico |
| 2 | Top 5 restaurantes com maior nota média | Gráfico |
| 3 | Top 5 restaurantes com maior ticket para dois | Gráfico |
| 4 | Restaurante brasileiro com menor avaliação | Texto |
| 5 | Restaurante brasileiro no Brasil com maior avaliação | Texto |
| 6 | Delivery influencia volume de avaliações? | Comparativo |
| 7 | Reservas influenciam ticket médio? | Comparativo |
| 8 | Japonês vs BBQ nos EUA — qual custa mais? | Comparativo |

### Perspectiva Culinária
| # | Pergunta | Tipo de Resposta |
|---|----------|-----------------|
| 1-2 | Melhor/pior restaurante italiano | Texto |
| 3-4 | Melhor/pior restaurante americano | Texto |
| 5-6 | Melhor/pior restaurante árabe | Texto |
| 7-8 | Melhor/pior restaurante japonês | Texto |
| 9-10 | Melhor/pior restaurante caseiro | Texto |
| 11 | Culinária com maior ticket médio | Texto |
| 12 | Culinária com maior nota média | Texto |
| 13 | Culinária com mais restaurantes com delivery+reserva | Texto |

---

## Métricas-Chave do Dataset (após limpeza)

| Métrica | Valor Aproximado |
|---------|-----------------|
| Restaurantes únicos | ~5.900 |
| Países cobertos | 15 |
| Cidades cobertas | 125 |
| Tipos de culinária | 100+ |
| Avaliações registradas | 28.000+ |

---

## Público-Alvo

| Persona | Uso Principal |
|---------|---------------|
| **Empreendedor gastronômico** | Identificar países/cidades com menor concorrência e alta satisfação |
| **Investidor** | Mapear mercados com potencial de crescimento |
| **Gestor de franquia** | Comparar performance entre unidades em diferentes países |
| **Analista de dados** | Base de estudo para técnicas de EDA e visualização |
| **Estudante de ciência de dados** | Projeto prático de ponta a ponta |

---

## Valor Entregue

```
ANTES: CSV bruto → planilha estática → análise manual demorada
DEPOIS: CSV bruto → pipeline de limpeza automático → dashboard interativo em tempo real
```

O dashboard elimina o trabalho manual de filtragem e agrupamento, reduzindo de **horas para segundos** o tempo necessário para responder uma pergunta de negócio.
