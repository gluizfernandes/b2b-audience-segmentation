# B2B Audience Segmentation

Pipeline de ML open-source para segmentação comportamental de audiencias B2B em midia paga.

Resolve o problema de budget desperdiçado em Google Ads e LinkedIn Ads B2B,
onde a segmentaçãoo firmografica tradicional trata comportamentos radicalmente
diferentes como se fossem a mesma audiência.

## O problema que resolve

Empresas B2B investem em midia paga segmentando por setor e faturamento.
Esse filtro e estatico. Nao captura se a empresa clica, quanto paga por clique,
nem quanto tempo fica no site. O resultado e orcamento distribuido igualmente
entre perfis com ROI completamente diferentes.

## A solucao

K-Means sobre 3 metricas comportamentais (CTR, CPC, avg_time_site) agrupa
automaticamente as contas em 3 personas com estrategias de midia distintas.

## As 3 Personas

| Cluster | Perfil | CTR | CPC | Acao |
|---------|--------|-----|-----|------|
| 0 | Alta Performance | ~18.6% | R$38 | Maximizar budget + Lookalike |
| 1 | Alto Custo Estrategico | 2.15% | R$67 | Remover de paid, nutrir organico |
| 2 | Volume Sem Resposta | 0.04% | R$36 | Excluir ou A/B test 14 dias |

## Stack

- Python 3.11+
- scikit-learn (KMeans, StandardScaler, silhouette_score)
- pandas, numpy
- matplotlib, seaborn
- joblib (serializacao e inferencia)

## Estrutura

```
notebooks/          Notebook completo e executavel
src/                Modulos Python limpos e reutilizaveis
  data_generation.py
  preprocessing.py
  clustering.py
  visualization.py
  inference.py
models/             Modelos serializados (gerados ao rodar o notebook)
```

## Convencoes

- Python 3.11+ com type hints
- Sem dados reais (LGPD) - dataset simulado reproduzivel com seed fixo
- Codigo modular: cada src/ faz uma coisa
- Comentários so onde o motivo não é obvio
- README em portugues, codigo em ingles
