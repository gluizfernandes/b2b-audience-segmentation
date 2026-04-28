# Post LinkedIn 02 — Técnico (para data scientists e analistas)

**Audiência:** data scientists, analistas de dados, engenheiros de ML
**Objetivo:** autoridade técnica + visitas ao GitHub + seguidores da área
**Formato:** post com código e métricas

---

Rodei K-Means em dados de engajamento B2B de mídia paga e o insight mais valioso não veio dos clusters.

Veio da matriz de correlação antes de rodar o modelo.

CTR e CPC têm correlação de -0.18. Quase zero.

Isso significa que o custo por clique não explica o quanto uma empresa clica. São dimensões comportamentais independentes. E é exatamente por isso que o modelo consegue separar perfis que segmentação manual nunca encontraria.

O pipeline tem 5 etapas:

1. Geração de dataset simulado com 8.000 eventos de interação B2B
2. Agregação por empresa: CTR, CPC médio, tempo médio de sessão
3. Remoção de outliers no percentil 99 (K-Means é sensível a valores extremos)
4. StandardScaler para normalizar escalas diferentes
5. Elbow Method para definir k, K-Means com k-means++ para inicialização

Resultado: k=3 foi o ponto de equilíbrio entre variância explicada e parcimônia do modelo.

Silhouette Score de 0.32. Baixo para dados estruturados, adequado para comportamento humano com fronteiras naturalmente difusas.

O que o score confirma: os clusters existem e têm direção coerente, mesmo sem separação perfeita.

Mais importante que o score: a separação vetorial no espaço CTR x tempo de sessão é visível e acionável.

Código completo no GitHub, incluindo módulos de geração de dados, pré-processamento, clustering, visualização e inferência em produção com joblib.

Link nos comentários.

#DataScience #MachineLearning #KMeans #Python #ScikitLearn #B2BMarketing #MLEngineering

---

**Instrucao de publicacao:**
- Postar com imagem do elbow method ou da scatter plot dos clusters
- Comentar link do GitHub logo após
- Esse post tem melhor performance de quarta a quinta, horário comercial
