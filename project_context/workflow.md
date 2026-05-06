# Workflow Atual

## Objetivo

O script `enrich_lod_csv.py` lê arquivos CSV com palavras em luxemburguês, consulta a API do `lod.lu`, gera um CSV enriquecido com traduções e links de áudio, e baixa os áudios fonte das palavras.

## Estrutura de pastas

- `inputs/`
  - recebe CSVs brutos com uma coluna de palavras
- `outputs/`
  - recebe CSVs enriquecidos com o mesmo nome do arquivo de entrada
- `audios/`
  - recebe os arquivos de áudio fonte baixados do `link audio 1`
  - também recebe os MP3 gerados para o Anki
- `project_context/`
  - documentação persistente do fluxo e das decisões

## Colunas de saída

O CSV gerado contém estas colunas:

- `luxemburgues`
- `portugues`
- `ingles`
- `link audio 1`
- `link audio 2`

## Regra de processamento

Para cada CSV em `inputs/`:

1. verificar se já existe um arquivo com o mesmo nome em `outputs/`
2. se existir, pular o processamento desse CSV
3. se não existir, processar palavra por palavra
4. salvar o CSV enriquecido em `outputs/`

## Barra de progresso

O script usa `tqdm` quando disponível:

- uma barra para arquivos
- uma barra para palavras dentro de cada arquivo

Se `tqdm` não estiver instalado, o script cai no modo texto simples.

## Lógica de consulta

Para cada palavra:

1. chamar `https://lod.lu/api/lb/search?lang=lb&query=<palavra>`
2. escolher o melhor resultado
3. chamar `https://lod.lu/api/lb/entry/<article_id>`
4. extrair:
   - tradução em português a partir de `targetLanguages.pt`
   - tradução em inglês a partir de `targetLanguages.en`
   - `entry.audioFiles.ogg`
   - `entry.audioFiles.aac`

## Lógica de áudio

- baixar o áudio fonte correspondente ao `link audio 1`
- o gerador do Anki converte esse áudio para MP3
- salvar em `audios/`
- nome do arquivo:
  - fonte: `<palavra_sanitizada>__<article_id>.ogg`
  - final Anki: `<palavra_sanitizada>__<article_id>.mp3`
- se o arquivo já existir, não baixar de novo

## Cache atual

Existe cache em memória durante a execução:

- se a mesma palavra aparecer mais de uma vez no mesmo run, ela não é consultada novamente

Ainda não existe cache persistente em arquivo entre execuções.

## Observações importantes

- o script espera que o CSV de entrada tenha cabeçalho
- ele usa a primeira coluna do CSV como fonte das palavras
- se uma palavra falhar na consulta, a linha é gerada com campos vazios, exceto `luxemburgues`
