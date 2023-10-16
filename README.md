# Engenharia_Software
Repositório para trabalho da disciplina Engenharia de Software.


Membros:

    Gustavo Sanches
    Lucas Treuke
    Rodrigo Pintucci
    Tiago Barradas
    Vanessa Berwanger

<hr>

**Requisitos do sistema:**
-   Gerenciamento de Eventos Pessoais:
    -   Um usuário deve ser capaz de organizar sua agenda pessoal, criando e gerenciando eventos pessoais.
    -   O usuário deve poder visualizar, adicionar, editar e excluir eventos em sua agenda.
-   Categorias de Eventos:
    -   Os eventos devem ser categorizados em tipos, como Lembrete, Evento e Tarefa com Prazo.
    -   Cada categoria de evento deve ter características específicas (data/hora, repetição, indisponibilidade).
    -   Lembrete:
        -   Os Lembretes têm data, horário e opção de repetição.
        -   Os usuários devem ser notificados no horário do lembrete
    -   Evento:
        -   Os Eventos possuem horário/data de início e de fim.
        -   Um Evento ocupa o intervalo de tempo entre essas duas datas e horários.
        -   Os usuários têm a opção de indisponibilizar automaticamente esse intervalo na agenda.
        -   Eventos também podem se repetir.
    -   Tarefa com Prazo:
        -   As Tarefas com Prazo possuem uma data de prazo para conclusão.
        -   Os usuários têm a opção de marcar o progresso da tarefa e receber lembretes relacionados ao prazo.
        -   Essas tarefas também podem ser recorrentes, como para objetivos semanais a serem cumpridos.
-   Disponibilidade para Eventos Externos:
    -   Os usuários podem marcar áreas de disponibilidade em sua agenda para permitir que outros usuários vejam quando estão disponíveis para eventos externos.
    -   É possível manter a privacidade dos eventos pessoais enquanto permite que outros vejam quando você está disponível.
-   Resolução de Fusos Horários:
    -   O sistema deve resolver automaticamente os problemas de fuso horário para os usuários, permitindo que vejam a agenda no fuso horário desejado. Sugestão: Os usuários podem configurar períodos de sono e almoço, ajudando na gestão dos fusos horários.
-   Eventos em Grupo:
    -   Os usuários podem adicionar eventos em grupo, como reuniões de equipe ou eventos familiares.
    -   É possível verificar a disponibilidade dos membros do grupo antes de agendar o evento.
    -   A opção de visualizar a sobreposição de agendas dos membros do grupo facilita a escolha do melhor horário.
