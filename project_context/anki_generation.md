# Geracao de Flashcards Anki

## Objetivo

O script `generate_anki_cards.py` usa os CSVs prontos em `outputs/` para gerar arquivos finais de importacao para o Anki no diretorio principal:

- `anki_flashcards_import.csv`
- `anki_flashcards_import_en.csv`

Esses arquivos sao gerados sem cabecalho.

Tambem sao gerados CSVs de revisao manual:

- `anki_flashcards_manual_review.csv`
- `anki_flashcards_manual_review_en.csv`

## Fontes usadas

- `outputs/*.csv`
- `audios/*.ogg`

## Regra de deduplicacao

Se a mesma palavra em luxemburgues aparecer em mais de um CSV de `outputs/`, apenas a primeira ocorrencia encontrada e usada.

Hoje a deduplicacao e feita por:

- `luxemburgues.casefold()`

## Traducao usada

Mesmo que existam varias traducoes em portugues ou ingles separadas por `;`, o script usa apenas a primeira.

Exemplo:

- `casa; lar; domicilio`
- valor usado: `casa`

## Tipos de card

Cada palavra valida gera exatamente dois cards por idioma exportado.

### Card 1

- frente: audio
- verso: palavra em luxemburgues + traducao entre parenteses

### Card 2

- frente: palavra traduzida
- verso: audio + palavra em luxemburgues

## Regra de elegibilidade

Uma palavra so entra no CSV final do idioma correspondente se tiver:

- palavra em luxemburgues
- primeira traducao do idioma
- arquivo de audio local correspondente

Se faltar traducao ou audio, a palavra nao gera cards.

Mas ela nao some do fluxo:

- vai para o CSV de revisao do idioma
- nao gera cards

## Relacao entre link e arquivo local

Os audios locais foram nomeados com esta convencao:

- `<palavra_sanitizada>__<ARTICLE_ID>.ogg`

Para reencontrar o audio certo, o script usa:

1. a palavra
2. o `link audio 1`
3. o nome do arquivo do link para extrair o `ARTICLE_ID`

## Pasta de midia do Anki

Os audios usados nos cards sao copiados para a pasta `collection.media` do perfil do Anki.

Resolucao atual:

1. se a variavel de ambiente `ANKI_MEDIA_DIR` estiver definida, ela sera usada
2. se nao estiver, o script tenta localizar automaticamente a pasta dentro de `%APPDATA%\Anki2`
3. se houver mais de um perfil e o script nao conseguir decidir, ele pede que `ANKI_MEDIA_DIR` seja definida

Se o arquivo ja existir la, ele nao e copiado de novo.

## Saida final

Os arquivos finais gerados sao:

- `anki_flashcards_import.csv`
- `anki_flashcards_import_en.csv`

Os arquivos auxiliares de revisao sao:

- `anki_flashcards_manual_review.csv`
- `anki_flashcards_manual_review_en.csv`

Formato dos imports:

- sem cabecalho
- duas colunas por linha
- cada linha representa um card
- como cada palavra gera dois cards, o total de linhas e `2 x quantidade_de_palavras_validas`

## CSV de revisao manual

Os CSVs de revisao manual tem cabecalho e registram:

- `luxemburgues`
- `portugues`
- `ingles`
- `link audio 1`
- `link audio 2`
- `motivo`
- `arquivo_origem`

Motivos atuais possiveis:

- `sem_traducao_portugues`
- `sem_traducao_ingles`
- `sem_link_audio_1`
- `audio_nao_encontrado_na_pasta_audios`
