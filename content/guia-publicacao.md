# Guia de Publicação

Ordem e timing para maximizar alcance e autoridade técnica.

---

## Semana 1 — Base técnica

### Dia 1: GitHub

Antes de qualquer post, o repositório precisa estar no ar. É o destino de todos os CTAs.

```bash
cd tcc-b2b-audience-segmentation
git init
git add .
git commit -m "feat: pipeline completo de segmentacao B2B com K-Means"
git branch -M main
git remote add origin https://github.com/georgeluizfernandes/b2b-audience-segmentation.git
git push -u origin main
```

Checklist antes de publicar:
- [ ] README legível no preview do GitHub
- [ ] Notebook executa do zero sem erro
- [ ] requirements.txt completo
- [ ] .gitignore excluindo modelos pesados e .env
- [ ] Link do LinkedIn e Medium no README

### Dia 2 ou 3: Post LinkedIn 01 (negócio)

Arquivo: `content/linkedin/post-01-negocio.md`

Melhor horário: terça ou quarta, entre 8h e 10h.

Após publicar:
- Comentar o link do GitHub como primeiro comentário
- Responder todos os comentários nas primeiras 2 horas (impacto direto no alcance)
- Pedir para 3 a 5 conexões próximas comentarem logo cedo

---

## Semana 2 — Profundidade técnica

### Dia 7 a 9: Artigo Medium

Arquivo: `content/medium/artigo-tecnico.md`

Antes de publicar no Medium:
- Adicionar os gráficos gerados pelo notebook como imagens inline
  - Correlação heatmap (Figura 1)
  - Elbow Method (Figura 2)
  - Scatter dos clusters (Figura 3)
  - Tabela de perfis (Figura 4)
- Tags: Data Science, Machine Learning, Marketing, Python, B2B

Após publicar:
- Comentar link do Medium no Post 01 do LinkedIn
- Compartilhar link no Post 02 do LinkedIn (publicar junto)

### Dia 9 ou 10: Post LinkedIn 02 (técnico)

Arquivo: `content/linkedin/post-02-tecnico.md`

Publicar com imagem do elbow method ou do scatter dos clusters.

---

## Semana 3 — Consolidação

### Dia 14 a 17: Post LinkedIn 03 (persona)

Arquivo: `content/linkedin/post-03-persona.md`

Texto puro, sem imagem. Storytelling performa melhor assim.

Esse post referencia os dados concretos do Cluster 1. Ao responder comentários, linkar para o artigo Medium com o pipeline completo.

---

## Dicas gerais

**GitHub primeiro.** Todos os CTAs apontam para lá. Se o repo não existir no momento do post, o clique não converte.

**Comentar o link, nao colocar no post.** Posts com link externo têm alcance reduzido pelo algoritmo do LinkedIn. Colocar nos comentários mantém o alcance orgânico.

**Responder comentários cedo.** O LinkedIn amplifica posts com engajamento rápido nas primeiras 2 horas.

**Espaçar os posts.** Intervalo mínimo de 3 dias entre posts. Posts muito próximos competem entre si pelo mesmo público.

**Hashtags.** Máximo de 5 hashtags relevantes. Mais que isso reduz distribuição.

**Imagem nos posts técnicos, texto puro nos posts de storytelling.** Carrossel só vale se você tiver o design pronto. Imagem simples do gráfico funciona melhor que carrossel improvisado.
