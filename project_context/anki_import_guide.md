# Guia de Importacao no Anki

## Objetivo

Este guia explica como:

1. localizar a pasta de midia do Anki no computador
2. copiar os audios para o lugar certo
3. importar os CSVs de cards
4. configurar o Anki para revisar de forma eficiente

## Arquivos gerados neste projeto

Arquivos principais:

- `anki_flashcards_import.csv`
- `anki_flashcards_import_en.csv`

Arquivos de revisao manual:

- `anki_flashcards_manual_review.csv`
- `anki_flashcards_manual_review_en.csv`

Pasta de audios:

- `audios/`

## Como achar a pasta do Anki manualmente

Se outra pessoa for fazer isso em outro computador, o jeito mais seguro e:

1. abrir o Anki
2. clicar em `Ferramentas`
3. clicar em `Add-ons` ou `Complementos` se quiser apenas confirmar que o perfil esta aberto
4. voltar
5. clicar em `Ferramentas`
6. clicar em `Ver arquivos` ou `Open Backup/Files` se a interface estiver em ingles
7. abrir a pasta do perfil atual
8. entrar em `collection.media`

Se nao quiser fazer pelo Anki, no Windows normalmente fica em:

- `C:\Users\<SEU_USUARIO>\AppData\Roaming\Anki2\<NOME_DO_PERFIL>\collection.media`

## O que deve ir para a pasta do Anki

Os audios precisam estar dentro de `collection.media`.

Neste projeto, os arquivos de audio ja estao em:

- `audios/`

E o script `generate_anki_cards.py` ja copia automaticamente os audios necessarios para a pasta correta do Anki.

Ele faz isso assim:

1. se a variavel de ambiente `ANKI_MEDIA_DIR` estiver definida, usa esse caminho
2. se nao estiver, tenta descobrir a pasta automaticamente via `%APPDATA%\Anki2`
3. se houver ambiguidade entre perfis, voce precisa definir `ANKI_MEDIA_DIR` manualmente

Entao, neste computador, normalmente nao e preciso mover manualmente nada, desde que o script ja tenha sido executado.

Se alguem for fazer manualmente:

1. abrir a pasta `audios/`
2. copiar os arquivos `.mp3`
3. colar dentro de `collection.media`

## Como importar os cards no Anki

### Passo 1: abrir ou criar o baralho

1. abrir o Anki
2. criar um baralho novo ou escolher um existente
3. deixar esse baralho selecionado

### Passo 2: importar o CSV

Para portugues:

- importar `anki_flashcards_import.csv`

Para ingles:

- importar `anki_flashcards_import_en.csv`

Passos:

1. clicar em `Importar`
2. escolher o arquivo CSV
3. selecionar o baralho correto

### Passo 3: escolher o tipo de nota

O arquivo tem duas colunas:

- coluna 1 = frente
- coluna 2 = verso

O tipo de nota ideal e um tipo simples de dois campos.

Se nao existir:

1. criar um note type simples, por exemplo `Luxemburgues Audio`
2. criar dois campos:
   - `Frente`
   - `Verso`

Na importacao:

1. mapear a primeira coluna para `Frente`
2. mapear a segunda coluna para `Verso`

### Passo 4: evitar duplicatas

Na tela de importacao, confira:

1. que o tipo de nota esta correto
2. que os campos estao mapeados corretamente
3. que o separador de colunas esta como virgula

Se o arquivo ja tiver sido importado antes, o ideal e importar em um baralho de teste primeiro para confirmar o comportamento do Anki com duplicatas.

## Como os cards devem aparecer

### CSV em portugues

Card 1:

- frente: audio
- verso: palavra em luxemburgues
- linha abaixo: traducao em portugues entre parenteses

Card 2:

- frente: primeira traducao em portugues
- verso: palavra em luxemburgues
- linha abaixo: audio

### CSV em ingles

Card 1:

- frente: audio
- verso: palavra em luxemburgues
- linha abaixo: traducao em ingles entre parenteses

Card 2:

- frente: primeira traducao em ingles
- verso: palavra em luxemburgues
- linha abaixo: audio

## Como lidar com os casos incompletos

Nem toda palavra veio com traducao ou audio.

Esses itens nao foram transformados em cards.

Eles estao separados em:

- `anki_flashcards_manual_review.csv`
- `anki_flashcards_manual_review_en.csv`

O ideal e revisar esses arquivos antes de tentar gerar mais cards.

## Configuracao recomendada no Anki

Aqui vai uma configuracao simples e boa para memorizar vocabulario sem exagerar no volume.

### Novos cards por dia

Sugestao inicial:

- `10` a `20` novos cards por dia

Se estiver tranquilo:

- subir para `25`

Se estiver pesado:

- baixar para `5` ou `10`

### Revisoes maximas por dia

Sugestao:

- `9999`

Motivo:

- melhor deixar o limite muito alto para nao acumular revisoes artificiais

### Passos de aprendizado

Sugestao boa para vocabulario:

- `1m 10m 1d`

Ou, se quiser algo mais leve:

- `10m 1d`

### Intervalo de graduacao

Sugestao:

- `3 dias`

### Easy interval

Sugestao:

- `5 a 7 dias`

### Lapses

Sugestao:

- passo de reaprendizagem: `10m`
- leech threshold: `8`

## Melhor estrategia de estudo

Para lembrar de verdade:

1. estudar todos os dias, mesmo pouco
2. nao colocar novos cards demais no inicio
3. ouvir o audio antes de virar o card
4. falar a palavra em voz alta
5. no card de traducao, tentar lembrar a pronuncia antes de revelar

## Ordem recomendada

Uma ordem boa e:

1. importar primeiro o CSV em portugues
2. estudar alguns dias
3. depois importar o CSV em ingles

Motivo:

- isso evita dobrar a carga de revisao logo de cara

## Checklist final

Antes de estudar, confirmar:

1. os audios estao em `collection.media`
2. o CSV correto foi importado
3. os campos frente/verso foram mapeados corretamente
4. o card toca o audio sem erro
5. o baralho esta com limite razoavel de novos cards por dia
