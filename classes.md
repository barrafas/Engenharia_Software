# usuário
 - Nome
 - Senha?
 - infos
 - FusoHorario
 - disponibilidade

# disponibilidade
> essa classe é uma lista de intervalos de tempo
 - intervalos
 - QueryDisponibilidade()

# intervalo
> para a disponibilidade, assumimos que todos os horários estão indisponíveis, e o usuário pode marcar intervalos de tempo como disponíveis. Entretando ele também pode criar intervalos de indisponibilidade entre intervalos de disponibilidade - para o resultado final, vale assumir que temos três possiveis estados para um instante, com a seguinte ordem de prioridade: não marcado, disponível, indisponível.
> Assim, para diversas anotações em um mesmo instante, ele será classificado conforme a prioridade: indisponível > disponível > não marcado.
 - inicio
 - fim
 - estado


# evento
 - Criar()
 - Editar()
 - Excluir()
 - titulo
 - notificação
 - data
 - descrição
 - usuários_participantes: [usuário, ... ]
 - criador: usuário
 - concluido?

 ## evento
    - data inicio
    - data fim
    - indisponibilidade vinculada
 ## Tarefa
    - data limite
 ## Lembrete
    - data

# Equipe
 - criador: usuário
 - membros: [(usuário, admin?), ... ]

# FusoHorario
 - fuso
 - universal->local()
 - local->universal()

> Solução para os horários:
> usamos um horário universal para tudo (em GMT: 0), e cada usuário tem um fuso horário, que recebe um horário e converte para o horário do usuário e vice-versa.

# Agenda

# Pesquisa?

# Exportador

# notificação?

# exibição?