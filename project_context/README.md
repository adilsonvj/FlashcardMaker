# FlashcardMaker Context

Este diretório guarda contexto operacional do projeto para futuras sessões.

Objetivo:
- registrar o que o script faz hoje
- documentar a estrutura de pastas
- anotar decisões já tomadas
- facilitar mudanças futuras sem precisar redescobrir tudo

Arquivos atuais:
- `workflow.md`: fluxo atual do enriquecimento dos CSVs
- `decisions.md`: decisões importantes e combinados já definidos
- `anki_generation.md`: geração do CSV de importação do Anki
- `anki_import_guide.md`: passo a passo para copiar áudios, achar a pasta do Anki e importar os cards

Como usar este diretório:
- antes de alterar a pipeline, ler `workflow.md` e `decisions.md`
- ao mudar comportamento, atualizar estes arquivos
- quando surgir uma regra nova pedida pelo usuário, registrar em `decisions.md`
