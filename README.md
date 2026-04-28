# B2B Audience Segmentation with K-Means

Pipeline de Machine Learning para segmentação comportamental de audiências B2B em mídia paga.

Identifica automaticamente 3 perfis de contas corporativas e prescreve a estratégia de mídia ideal para cada um, eliminando o desperdício de budget que ocorre quando Google Ads e LinkedIn Ads tratam comportamentos radicalmente diferentes como a mesma audiência.

---

## O problema

Segmentação firmográfica (setor, faturamento, cargo) diz com quem você quer falar. Não diz nada sobre quem vai comprar.

O resultado: budget distribuído igualmente entre empresas com CTR de 18% e empresas com CTR de 0.04%. O algoritmo encontra esse padrão automaticamente nos seus dados.

---

## Os 3 perfis

| Cluster | Perfil | CTR | CPC | Ação |
|---------|--------|-----|-----|------|
| 0 | Alta Performance | ~18.6% | R$38 | Maximizar budget + Lookalike |
| 1 | Alto Custo Estratégico | ~2.15% | R$67 | Remover de paid, nutrir orgânico |
| 2 | Volume Sem Retorno | ~0.04% | R$36 | Excluir ou A/B test 14 dias |

---

## Quickstart

```bash
git clone https://github.com/gluizfernandes/b2b-audience-segmentation
cd b2b-audience-segmentation
pip install -r requirements.txt
jupyter notebook notebooks/b2b_segmentation.ipynb
```

O notebook executa todo o pipeline do zero: geração de dados, pré-processamento, clustering, visualização e inferência em produção.

---

## Estrutura

```
src/
  data_generation.py   Geração do dataset simulado
  preprocessing.py     Agregação, outliers, normalização
  clustering.py        Elbow Method, K-Means, Silhouette Score
  visualization.py     Correlação, cotovelo, scatter de clusters
  inference.py         Serialização e classificação em produção
notebooks/
  b2b_segmentation.ipynb   Pipeline completo e comentado
models/                    Modelos gerados ao rodar o notebook
```

---

## Stack

- Python 3.11+
- scikit-learn — KMeans, StandardScaler, silhouette_score
- pandas, numpy
- matplotlib, seaborn
- joblib — serialização e inferência

---

## Como funciona

**1. Geração dos dados**
Dataset simulado com 8.000 eventos de interação B2B. Reproduzível com `random_state=42`.

**2. Agregação por empresa**
Logs brutos agregados no nível de conta corporativa: CTR, CPC médio, tempo médio de sessão.

**3. Pré-processamento**
Remoção de outliers acima do percentil 99. StandardScaler para normalização de escalas.

**4. Elbow Method**
Testa k de 1 a 10. Inércia cai acentuadamente até k=3. Ganho marginal a partir de k=4.

**5. K-Means com k=3**
Silhouette Score: 0.32. Adequado para dados comportamentais com fronteiras naturalmente difusas.

**6. Deployment**
Modelo serializado com joblib. Script de inferência classifica uma nova conta em milissegundos.

---

## Inferência em produção

```python
from src.inference import load_model, classify_and_act

modelo, scaler = load_model()

nova_empresa = {'ctr': 15.2, 'cpc': 41.0, 'avg_time_site': 2.1}
resultado = classify_and_act(nova_empresa, modelo, scaler, ['ctr', 'cpc', 'avg_time_site'])

print(resultado['cluster'])   # 0
print(resultado['action'])    # Maximizar budget + criar Lookalike Audiences com esse perfil
```

---

## Próximos passos

- Incorporar Lifetime Value (LTV) como variável adicional
- Testar DBSCAN como alternativa que não exige pré-definição de k
- Implementar classificação em streaming com Apache Kafka
- Detecção de anomalias para identificar cliques fraudulentos

---

## Licença

MIT

---

**George Luiz Pereira Fernandes**
[LinkedIn](https://linkedin.com/in/georgeluizfernandes) | [Medium](https://medium.com/@georgeluizfernandes)
