# Fome de Dados: A História por Trás do Dashboard Zomato

## O Começo — Uma Plataforma, Milhares de Histórias

Em 2008, a Zomato nasceu em um quarto de escritório em Delhi com um objetivo simples: digitalizar os cardápios de papel espalhados pelos restaurantes da cidade. Uma ideia pequena que virou gigante.

Duas décadas depois, a plataforma conecta **milhões de usuários** a restaurantes em mais de **25 países**. Cada clique, cada avaliação, cada nota deixada por um cliente faminto torna-se um dado. E dados, quando bem tratados, contam histórias poderosas.

Este projeto nasce dessa premissa: **transformar o ruído de milhares de avaliações em inteligência de negócio**.

---

## O Problema — Dados Sem Voz

Imagine ser um empresário do setor gastronômico. Você precisa decidir:

- *Em qual país abrir minha próxima franquia?*
- *Qual culinária tem maior aceitação do público?*
- *Reservas e entregas realmente influenciam a percepção do cliente?*
- *Meu restaurante está na média do mercado ou ficou para trás?*

Sem análise, essas perguntas ficam no campo da intuição. Com análise, viram estratégia.

O dataset da Zomato carrega **mais de 9.500 registros** de restaurantes espalhados por **15 países** e **125 cidades**. Uma mina de ouro — mas bruta, com duplicatas, dados ausentes e colunas sem significado.

O desafio: **extrair ouro do minério**.

---

## A Jornada — Do CSV ao Dashboard

### Fase 1 — O Caos Inicial

O arquivo `zomato.csv` chegou com colunas mal nomeadas (`Switch to order menu`), valores constantes sem utilidade analítica, linhas duplicadas e campos em branco. Um dataset "sujo" como qualquer dataset real.

**Decisões tomadas:**
- Remover colunas com valor único (zero variância = zero informação)
- Eliminar duplicatas exatas
- Descartar linhas com qualquer campo nulo
- Normalizar nomes de colunas para snake_case

### Fase 2 — Enriquecimento

O dataset original codificava países como números inteiros (`30` = Brazil) e cores de rating como hexadecimais (`3F7E00` = darkgreen). Dados legíveis por máquinas, mas invisíveis para humanos.

**Enriquecimento aplicado:**
- Decodificação de `country_code` → nome do país
- Decodificação de `rating_color` → nome da cor
- Categorização de `price_range` → `cheap / normal / expensive / gourmet`
- Simplificação de `cuisines` → apenas o primeiro tipo listado

### Fase 3 — Visualização e Insights

Com o dado limpo e enriquecido, cinco perspectivas analíticas foram construídas:

| Página | Foco |
|--------|------|
| **Geral** | Visão macro: restaurantes, países, cidades, avaliações |
| **País** | Ranking e comparativos globais |
| **Cidade** | Análise urbana e concentração gastronômica |
| **Restaurantes** | Performance individual e comparativa |
| **Culinária** | Preferências por tipo de comida |

---

## Os Insights — O Que os Dados Revelaram

### India domina o mapa

Com **2.489 restaurantes únicos** em **49 cidades**, a Índia é o país com maior presença na plataforma. Não por acaso: a Zomato nasceu lá e o mercado de foodtech indiano cresceu exponencialmente na última década.

### Preço alto não garante nota alta

Restaurantes com `price_range = 4` (gourmet) não necessariamente lideram em avaliação média. A correlação entre preço e satisfação é mais complexa — serviço, localização e expectativa do cliente pesam tanto quanto o cardápio.

### Delivery impulsiona engajamento

Restaurantes que aceitam pedidos online possuem, na média, **significativamente mais avaliações** do que os que operam apenas presencialmente. Mais pedidos = mais oportunidades de feedback = mais visibilidade na plataforma.

### Reservas e valor do ticket

Restaurantes com `has_table_booking = 1` apresentam **ticket médio mais alto**. O serviço de reserva funciona como um indicador de experiência premium — clientes dispostos a reservar estão dispostos a gastar mais.

### Indonesia — a surpresa

Apesar de ter poucos restaurantes no dataset, a Indonésia apresenta a **maior nota média de avaliação**. Poucos dados, alta satisfação — um mercado a observar.

---

## A Solução — Dashboard Interativo

O dashboard foi construído com **Streamlit**, permitindo:

- Filtro por país e culinária em tempo real
- Mapa geoespacial de restaurantes
- Gráficos de barras comparativos
- Cards de métricas para visão rápida
- Navegação entre 5 perspectivas analíticas

### A Proposta de Valor

Em vez de relatórios estáticos que envelhecem antes de serem lidos, o dashboard oferece **exploração dinâmica**: o usuário traz sua própria pergunta e o sistema responde em segundos.

---

## O Que Vem Depois

Com a base analítica estabelecida, as próximas evoluções naturais do projeto incluem:

1. **Análise temporal** — Como as notas evoluem ao longo do tempo?
2. **Segmentação por faixa de preço** — Onde está o sweet spot de preço x avaliação?
3. **Machine Learning** — Prever a nota de um restaurante com base em suas características
4. **Integração com API real** — Dados ao vivo em vez de snapshot estático

---

*"Sem dados, você é apenas mais uma pessoa com uma opinião."*
*— W. Edwards Deming*
