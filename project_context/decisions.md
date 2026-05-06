# Decisions

## Decisões já tomadas

### 1. Separação por pastas

Foi definido que o projeto deve trabalhar com:

- `inputs/` para arquivos brutos
- `outputs/` para arquivos já enriquecidos
- `audios/` para os áudios baixados

Motivo:
- evitar sobrescrever arquivos de origem
- facilitar processamento incremental

### 2. Não reprocessar CSV já consumido

Se um CSV com o mesmo nome já existir em `outputs/`, o script deve ignorar o CSV correspondente em `inputs/`.

Motivo:
- evitar retrabalho
- permitir adicionar novos CSVs ao longo do tempo

### 3. Formato de audio escolhido

Formato atual para os cards do Anki:

- MP3

Motivo:
- compatibilidade ampla com Anki no desktop e celular
- o usuario pediu para usar apenas MP3 nos cards

Observacao:

- o enriquecimento ainda pode baixar audio fonte do `lod.lu`
- o gerador converte para MP3 com `ffmpeg`

### 4. Feedback visual de progresso

Foi pedido explicitamente que o script mostre progresso com `tqdm`.

Motivo:
- o processamento demora
- o usuário quer distinguir se está avançando ou travado

### 5. Fonte de dados

A integração atual depende da API do `lod.lu`, usando:

- `/api/lb/search`
- `/api/lb/entry/<article_id>`

### 6. Escopo do enriquecimento atual

Hoje o script preenche:

- palavra em luxemburguês
- tradução em português
- tradução em inglês
- link do áudio 1
- link do áudio 2

### 7. Contexto do projeto

Foi pedido criar uma pasta com arquivos markdown para documentar o que está sendo feito e facilitar mudanças futuras.

Por isso existe a pasta `project_context/`.

### 8. Geração de cards Anki

Foi decidido criar uma segunda pipeline para gerar cards Anki a partir de `outputs/`.

Regras definidas:

- usar apenas palavras únicas entre todos os CSVs de `outputs`
- usar apenas a primeira tradução em português
- gerar exatamente dois cards por palavra
- copiar os áudios necessários para a pasta `collection.media` do Anki
- gerar um arquivo final sem cabeçalho no diretório principal

### 9. Revisão manual de pendências

Palavras sem tradução em português ou sem áudio não devem gerar cards.

Em vez disso:

- devem ser agrupadas em um CSV separado
- esse CSV serve para revisão manual posterior

## Melhorias futuras prováveis

Itens que podem ser adicionados depois, se necessário:

- cache persistente em arquivo JSON/SQLite
- checkpoint parcial durante a execução
- retomada automática de CSV interrompido
- logs mais detalhados por arquivo
- deduplicação global de downloads de áudio por URL
