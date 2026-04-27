# FlashcardMaker

Scripts para:

- enriquecer listas de palavras em luxemburguês usando o `lod.lu`
- baixar os áudios correspondentes
- gerar CSVs de importação para flashcards no Anki em português e inglês

## Estrutura

- `enrich_lod_csv.py`
  - processa CSVs em `inputs/`
  - gera CSVs enriquecidos em `outputs/`
  - baixa áudios em `audios/`

- `generate_anki_cards.py`
  - lê os CSVs de `outputs/`
  - gera imports do Anki no diretório principal
  - prepara os áudios para a pasta `collection.media`

- `project_context/`
  - documentação do fluxo

## Configuração

Opcionalmente, defina:

- `ANKI_MEDIA_DIR`

Exemplo:

```powershell
$env:ANKI_MEDIA_DIR="C:\Users\<SEU_USUARIO>\AppData\Roaming\Anki2\<SEU_PERFIL>\collection.media"
```

## Observações

- arquivos gerados e dados locais ficam fora do Git via `.gitignore`
- detalhes do fluxo estão em `project_context/`
