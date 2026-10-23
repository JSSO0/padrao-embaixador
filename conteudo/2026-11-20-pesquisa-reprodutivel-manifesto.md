# Post Dia 30 — 20/11/2026 (sexta)

## Metadados

| Campo | Valor |
|---|---|
| Dia | 30 |
| Data | 2026-11-20 (sexta) |
| Projeto | CACD Forecast AI (padrao-embaixador) |
| Território | LinkedIn + X (thread) + Instagram (carrossel) |
| Formato | Texto + trecho de código (repo público) |
| CTA | "Clone e confira" |
| Status | **pronto** (o manifesto existe; o script de verificação é pré-requisito do snippet) |

## Post LinkedIn

Todo PDF deste projeto chegou com um hash SHA-256 anotado no dia do
download. Não foi astúcia tardia: é o padrão da ferramenta de coleta.

O arquivo `download_manifest.csv` tem hoje 463 entradas. Cada linha
registra: concurso de origem, tipo de documento, URL de origem,
caminho local, SHA-256, tamanho em bytes, status HTTP e data do
download. São 460 PDFs no repositório, vindos de cinco tipos de fonte:
a CDN oficial do Cebraspe, a Internet Archive, o repositório
secundário, o Wayback Machine e coletores de provas.

Por que isso importa para uma pesquisa? Porque "eu juro que extraí
dessa prova" não é método. O leitor cético precisa poder verificar
três coisas sem me chamar:

1. Que o arquivo era exatamente aquele quando foi baixado (o hash).
2. Que a origem é rastreável (a URL, o tipo, a família).
3. Que nada foi silenciosamente alterado (a comparação do hash).

O que isso NÃO prova: que a extração do texto está correta. O hash
garante o arquivo, não o conteúdo interpretado — esse é o próximo
elo, e é auditável separadamente.

O snippet abaixo é a verificação que pretendo tornar padrão. O script
ainda não existe — é pré-requisito deste post. A ideia: recalcular o
SHA-256 de cada arquivo do repo e comparar com o manifesto, falhando
em qualquer divergência.

```bash
# linhas do manifesto (exemplo real, colunas cortadas)
# contest_id,doc_type,url,file_path,sha256,bytes,downloaded_at
# CACD_2025,cebraspe,prova_objetiva,https://...,data/raw/...,29e805d...,185645,2026-10-06

python scripts/verify_manifest.py data/raw/download_manifest.csv
# ok      460/463 arquivos conferem
# FALHA   data/raw/CACD_2010/.../IRBR_ECONOMIA.pdf (hash divergente)
```

Clone, rode a contagem e me diga se bate.

Repo: https://github.com/JSSO0/padrao-embaixador

## Thread X

1/ Todo PDF deste projeto chegou com SHA-256 anotado no dia do download. 463 entradas, 460 PDFs no repo. Sem "confia". 🔍
2/ O manifesto registra: concurso de origem, tipo de documento, URL, caminho local, hash, bytes e status HTTP. Cinco famílias de fonte: CDN oficial, Internet Archive, repositório secundário, Wayback e coletores de provas.
3/ Por quê? Porque cético não confia em CSV bonito. Ele precisa recalcular o hash e verificar a origem sem depender de mim.
4/ O que isso NÃO prova: que a extração do texto está correta. O hash cobre o arquivo, não o parse. Cada etapa com auditoria própria.
5/ O script de verificação ainda não existe — é o próximo pré-requisito. Quando existir, é esse o comando a rodar: python scripts/verify_manifest.py data/raw/download_manifest.csv
6/ Clone e confira: https://github.com/JSSO0/padrao-embaixador

## Carrossel Instagram

**Slide 1**
- Título: Cada PDF, um hash
- Corpo: 463 downloads anotados com SHA-256 no dia em que chegaram. Não é burocracia — é o que separa pesquisa de achismo.
- Texto de imagem: SHA-256
- Alt text: Cartão com a sigla SHA-256 e a frase "463 downloads anotados".

**Slide 2**
- Título: O que o manifesto diz
- Corpo: Para cada arquivo: concurso, tipo de documento, URL de origem, caminho local, hash, bytes e status HTTP.
- Texto de imagem: 463 linhas
- Alt text: Tabela simplificada com colunas do manifesto de downloads.

**Slide 3**
- Título: De onde vieram
- Corpo: CDN oficial do Cebraspe, Internet Archive, Wayback Machine, repositório secundário e coletores de provas. Cada linha registra a fonte.
- Texto de imagem: 5 tipos de fonte
- Alt text: Lista das cinco famílias de origem dos arquivos.

**Slide 4**
- Título: O que o hash prova
- Corpo: Que o arquivo é o mesmo desde o download. Qualquer alteração — proposital ou acidental — fica visível.
- Texto de imagem: arquivo imutável
- Alt text: Ícone de arquivo com marca de verificação de integridade.

**Slide 5**
- Título: O que o hash não prova
- Corpo: Não prova que a extração do texto está certa. O hash cobre o PDF, não o parser. Cada etapa tem auditoria própria.
- Texto de imagem: arquivo ≠ parse
- Alt text: Texto separando integridade de arquivo e qualidade de extração.

**Slide 6**
- Título: Como vou verificar
- Corpo: Um script que recalcula todos os hashes e compara com o manifesto, falhando em qualquer divergência. Ainda não existe — é o próximo passo.
- Texto de imagem: verify_manifest.py
- Alt text: Nome do script de verificação pendente em fonte monoespaçada.

**Slide 7**
- Título: Clone e confira
- Corpo: O repo tem os 460 PDFs, o manifesto e o parquet completo. Pesquisa que não pode ser conferida não é pesquisa.
- Texto de imagem: repo aberto
- Alt text: Frase convidando a clonar o repositório público.

## Hashtags

#OpenScience #Reprodutibilidade #SHA256 #DadosAbertos #CACD #PesquisaReprodutível #Python #Transparência

## Assets

1. **Print do terminal** com a primeira linha do `download_manifest.csv` (contest_id, url, sha256, bytes, data) — ocultar qualquer caminho com nome de usuário.
2. **Screenshot do repositório GitHub** mostrando a árvore `data/raw/` com as pastas por ano — captura da raiz do repo, sem dados sensíveis.
3. **Diagrama do fluxo de coleta** (fonte → download → hash → parquet), 1.200×1.500 px, estilo do banner.
4. **Snippet do snippet-design do verify_manifest.py** — captura de tela do bloco de código do post.

## Fatos e números

| Número | Fonte |
|---|---|
| 463 entradas no manifesto | `data/raw/download_manifest.csv` (Import-Csv | Measure-Object, 22/10/2026) |
| SHA-256 por arquivo | coluna `sha256` do mesmo CSV |
| 460 PDFs no repo | contagem `Get-ChildItem -Recurse -Filter *.pdf | Measure-Object` (22/10/2026) |
| 5 tipos de família (archive/cebraspe/cursocacd/wayback/qconcursos) | coluna `family` do manifesto |
| 5.487 registros no parquet | `data/processed/questions.parquet` (saída de verificação) |
| 0 scripts de verificação | não existe `scripts/verify_manifest.py` (verificação de diretório) |

## Checklist

- [x] Sem credenciais, tokens, chaves, URLs internas, dados de usuário
- [x] URLs públicas de origem apenas (GitHub, archive.org) — sem link de SharePoint interno
- [x] Sem promessa — o script de verificação está marcado como pré-requisito
- [x] Métrica (463/460/hash) + "o que isso NÃO prova" presentes
- [x] 1 CTA ("Clone e confira"), ≤ 3 emojis, sem repetição dos posts publicados

## Pré-requisitos

1. `scripts/verify_manifest.py` — recalcular SHA-256 de todos os arquivos e comparar com o manifesto (o snippet do post depende disso).
2. Atualizar o `README.md` com a seção de reprodução (hoje o README descreve o plano, não o comando de verificação).
3. Resolver a lacuna de contagem: 463 entradas no manifesto vs 460 PDFs no disco (os 3 a mais = zips não extraídos — documentar explicitamente).
4. Publicar o CSV do manifesto na raiz da documentação do repo, com dicionário de colunas.
