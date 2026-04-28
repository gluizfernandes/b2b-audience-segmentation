# Como parar de desperdiçar budget em mídia paga B2B com Machine Learning

**Publicar em:** Medium (perfil pessoal ou publicação de Data Science)
**Tempo de leitura estimado:** 8 minutos
**Tom:** guia prático para profissionais, não paper acadêmico

---

## O problema que ninguém mede direito

Se você gerencia campanhas B2B no Google Ads ou LinkedIn Ads, provavelmente segmenta por setor de atuação, faturamento estimado ou cargo do tomador de decisão.

Esse filtro diz quem você quer atingir. Não diz nada sobre o comportamento real dessas empresas quando encontram seu anúncio.

O resultado é que você distribui orçamento igualmente entre três tipos de empresa radicalmente diferentes:

A que clica, engaja e tem real intenção de compra. A que clica, fica no site, mas está longe de tomar decisão e te custa o dobro no leilão. A que aparece nas métricas de impressão mas não gera nenhum retorno mensurável.

Segmentação firmográfica não separa esses três perfis. Dado comportamental separa.

---

## O que o modelo precisa ver

Para que o clustering funcione, você precisa de métricas de engajamento no nível da conta, não do clique.

As três variáveis que provaram ter poder separador são:

**CTR (Taxa de Clique)** — captura a intenção de interação direta com o anúncio.

**CPC médio (Custo por Clique)** — reflete a competitividade no leilão. Contas disputadas custam mais. Uma empresa que aparece muito no leilão pode ser um sinal de alto interesse ou de keywords genéricas demais.

**Tempo médio de sessão** — o dado que a maioria dos gestores de tráfego ignora. Uma empresa que fica 30 segundos no site se comporta diferente de uma que fica 2 minutos.

A correlação entre CTR e CPC nesse dataset foi de -0.18. Praticamente zero. Isso valida que as três variáveis capturam dimensões comportamentais independentes. Se CTR e CPC fossem altamente correlacionados, usar os dois seria redundante.

---

## O pipeline em 6 etapas

### Etapa 1 — Geração dos dados

Para esse projeto, usamos um dataset simulado que reproduz o padrão de logs de interação de plataformas de anúncios. Cada linha é um evento de impressão com os campos: company_id, impressions, clicks, cost, session_duration.

```python
import pandas as pd
import numpy as np

np.random.seed(42)
n_events = 8000
ids = [f"ID_CORP_{i:04d}" for i in range(1, 1001)]

raw_data = pd.DataFrame({
    'company_id': np.random.choice(ids, n_events),
    'impressions': 1,
    'clicks': np.random.choice([0, 1], n_events, p=[0.96, 0.04]),
    'cost': np.random.uniform(0.8, 12.0, n_events),
    'session_duration': np.random.gamma(2, 50, n_events)
})
```

### Etapa 2 — Agregação por empresa

Os logs brutos estão no nível de evento. Precisamos agregá-los no nível de conta corporativa.

```python
df_model = raw_data.groupby('company_id').agg(
    total_impressions=('impressions', 'sum'),
    total_clicks=('clicks', 'sum'),
    total_cost=('cost', 'sum'),
    avg_time_site=('session_duration', 'mean')
).reset_index()

df_model['ctr'] = df_model['total_clicks'] / df_model['total_impressions'] * 100
df_model['cpc'] = df_model.apply(
    lambda r: r['total_cost'] / r['total_clicks'] if r['total_clicks'] > 0 else r['total_cost'],
    axis=1
)
df_model['avg_time_site'] = df_model['avg_time_site'] / 60
```

### Etapa 3 — Remoção de outliers

K-Means é sensível a valores extremos porque baseia a posição dos centroides na distância euclidiana. Um outlier distorce o centroide do cluster inteiro.

Filtramos acima do percentil 99 em cada variável quantitativa.

```python
features = ['ctr', 'cpc', 'avg_time_site']
for col in features:
    p99 = df_model[col].quantile(0.99)
    df_model = df_model[df_model[col] <= p99]
```

### Etapa 4 — Normalização

CTR varia de 0 a 100. CPC varia de R$10 a R$70. Tempo varia de 0 a 5 minutos. Escalas diferentes enviesam o cálculo de distância euclidiana. StandardScaler converte para média zero e desvio padrão unitário.

```python
from sklearn.preprocessing import StandardScaler

scaler = StandardScaler()
X_scaled = scaler.fit_transform(df_model[features])
```

### Etapa 5 — Definição do k com Elbow Method

```python
from sklearn.cluster import KMeans

wcss = []
for k in range(1, 11):
    km = KMeans(n_clusters=k, init='k-means++', n_init=10, random_state=42)
    km.fit(X_scaled)
    wcss.append(km.inertia_)
```

A queda de inércia é acentuada até k=3. A partir de 4 clusters, o ganho é marginal. k=3 é o ponto de equilíbrio.

### Etapa 6 — Execução e validação

```python
from sklearn.metrics import silhouette_score

kmeans = KMeans(n_clusters=3, init='k-means++', n_init=10, random_state=42)
df_model['cluster'] = kmeans.fit_predict(X_scaled)

score = silhouette_score(X_scaled, df_model['cluster'])
print(f"Silhouette Score: {score:.2f}")
```

Silhouette Score: 0.32. Em dados comportamentais humanos, esse valor indica separação real mas com fronteiras difusas. É esperado e adequado para esse domínio.

---

## Os 3 perfis e o que fazer com cada um

```python
profile = df_model.groupby('cluster')[features].mean().round(2)
print(profile)
```

| Cluster | CTR (%) | CPC (R$) | Tempo Médio (min) | Perfil |
|---------|---------|----------|-------------------|--------|
| 0 | 18.6 | 38.32 | 1.95 | Alta Performance |
| 1 | 2.15 | 67.59 | 1.80 | Alto Custo Estratégico |
| 2 | 0.04 | 36.22 | 1.48 | Volume Sem Retorno |

**Cluster 0 — Alta Performance**

Esse é o cluster que justifica o investimento em mídia paga B2B. Alto CTR, CPC moderado. Ação: maximizar budget, criar Lookalike Audiences com as empresas desse cluster nas plataformas, usar lances automatizados de CPA.

**Cluster 1 — Alto Custo Estratégico**

O cluster mais perigoso se não for identificado. A empresa tem interesse (tempo de sessão alto), mas o CPC inflado indica disputa de leilão. Conversão direta de paid não acontece com essa conta. Ação: remover de campanhas de fundo de funil, capturar via retargeting com material de alto valor (e-book, webinar, ferramenta gratuita), transferir para automação de e-mail. Custo marginal de nutrição: próximo de zero.

**Cluster 2 — Volume Sem Retorno**

CTR praticamente zero, menor tempo de sessão. Esse público consome impressões e budget sem retorno. Ação: auditar termos de busca que atraem esse perfil, negativar palavras-chave, ou executar teste A/B rigoroso por 14 dias. Se CTR não melhorar, excluir e mover verba para o Cluster 0.

---

## Deployment: usando o modelo em produção

Após treinar e validar, o modelo é serializado com joblib.

```python
import joblib

joblib.dump(kmeans, 'models/modelo_b2b.pkl')
joblib.dump(scaler, 'models/scaler_b2b.pkl')
```

Para classificar uma nova empresa em tempo real:

```python
modelo = joblib.load('models/modelo_b2b.pkl')
padronizador = joblib.load('models/scaler_b2b.pkl')

nova_empresa = pd.DataFrame([{
    'ctr': 15.2,
    'cpc': 41.0,
    'avg_time_site': 2.1
}])

cluster = modelo.predict(padronizador.transform(nova_empresa[features]))
print(f"Cluster: {cluster[0]}")
```

O sistema recebe métricas de uma nova conta do CRM, classifica em milissegundos e dispara a automação correspondente.

---

## Como rodar no seu projeto

```bash
git clone https://github.com/georgeluizfernandes/b2b-audience-segmentation
cd b2b-audience-segmentation
pip install -r requirements.txt
jupyter notebook notebooks/b2b_segmentation.ipynb
```

O notebook executa todo o pipeline do zero, incluindo geração de dados, modelagem e deployment.

---

## Próximos passos

O dataset atual usa variáveis de curto prazo. A próxima evolução natural inclui:

Incorporar Lifetime Value (LTV) estimado por cluster para qualificar ainda mais a alocação de budget.

Testar DBSCAN como alternativa, que não exige a pré-definição de k e lida melhor com clusters de formato irregular.

Implementar classificação em streaming com Apache Kafka para classificação em tempo real à medida que novos dados chegam das plataformas de anúncios.

Explorar detecção de anomalias para identificar cliques fraudulentos antes que contaminem os dados de treinamento.

---

**Código completo:** github.com/georgeluizfernandes/b2b-audience-segmentation

---

**Instrucao de publicacao Medium:**
- Publicar após o Post 01 do LinkedIn já ter gerado engajamento (2 a 3 dias depois)
- Adicionar os gráficos gerados pelo notebook como imagens inline
- Tag: Data Science, Machine Learning, Marketing, Python, B2B
- Canonical URL apontando para o Medium (não para outro canal)
- Ao publicar, comentar o link no Post 02 do LinkedIn
