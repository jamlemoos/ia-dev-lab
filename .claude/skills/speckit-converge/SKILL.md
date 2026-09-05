---
name: "speckit-converge"
description: "Assess the current codebase against the feature's spec, plan, and tasks, then append any remaining unbuilt work as new tasks to tasks.md so implement can complete it."
compatibility: "Requires spec-kit project structure with .specify/ directory"
metadata:
  author: "github-spec-kit"
  source: "templates/commands/converge.md"
user-invocable: true
disable-model-invocation: false
---

# Convergir codigo e spec (SpecKit)

Compara o que esta implementado com o que a spec, o plano e as tarefas pedem, e
acrescenta em `tasks.md` o que ainda falta.

## Passos

1. `.specify/scripts/bash/check-prerequisites.sh --json` para achar a pasta.
2. Leia `spec.md`, `plan.md` e `tasks.md` e monte a lista do que foi prometido.
3. Olhe o codigo e classifique cada item: feito, feito pela metade, ausente ou
   feito diferente do que a spec diz.
4. Atribua severidade a cada lacuna.
5. Mostre o resumo dos achados.
6. Acrescente as tarefas que faltam ao fim de `tasks.md`, numerando na
   sequencia. Se nao faltar nada, diga que convergiu e nao escreva nada.

Nao apague nem renumere tarefas que ja existem.
