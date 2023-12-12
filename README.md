# Engenharia_Software
Repositório para trabalho da disciplina Engenharia de Software. Como projeto, optamos por criar um aplicativo de calendário em grupo, focando na compatibilidade de agendas, fusos horários e discussões de eventos.

Membros:

    Gustavo Sanches
    Lucas Treuke
    Rodrigo Pintucci
    Tiago Barradas
    Vanessa Berwanger

<hr>

**Processo de instalação:**
Para certificar-se que todas as dependências foram instaladas em suas versões corretas, rode o comando `pip install -r requirements.txt`. Por padrão, o aplicativo utiliza uma imagem docker local do banco. Para rodar o MongoDB local, rode o seguinte comando, `sudo docker run -d -p 27017:27017 --name=mongo-example mongo:latest`, para que a aplicação consiga interagir com ele. Também implementamos  uma instância EC2 da AWS com essa mesma imagem docker. O ip, o usuário e a senha necessárias para acessar esse banco na nuvem serão enviadas através de um email para o professor, pois não é recomendado armazenar esses dados em um repositório no Github.

Utilizamos a ferramenta SonarQube e SonarScanner para realizar a verificação da qualidade do código. Ambas podem ser instaladas através de imagens docker. Para utilizá-las corretamente depois de suas instalações, é necessário criar um projeto local no SonarQube com o nome e chave sendo 'engenharia_software'. Depois disso, acesse o menu de análise, crie uma token para o projeto, e a interface irá disponibilizar um comando que deverá ser usado na pasta root do projeto, que contém o arquivo sonar-project.properties. Ao rodar esse código, você poderá ter acesso a um dashboard que descreve diversos aspectos da qualidade do seu código, indicando pontos de melhoria, e até mesmo mostrando sua cobertura de testes. Entretanto, para a cobertura funcionar, é preciso utilizar o módulo `coverage.py` para gerar o relatório em formato xml que a interface irá ler. Os comandos para gerar o relatório são: `coverage run --source=. -m pytest` e `coverage xml --omit "*__init__*,*/lib/*,tests/*"`, ambos devem ser rodados na root do aplicativo. O resultado final do SonarScanner foi salvo e armazenado na pasta documentacao/Qualidade_Codigo.png.

**Entrega A1:**
Decidimos atualizar a entrega inicial referente aos casos de uso para melhor refletir as modificações que ocorreram no sistema ao longo do desenvolvimento. O arquivo Entrega_A1_Atualizado.pdf dentro da pasta de documentação é referente à essa entrega atualizada.

**Testes realizados durante TDD:**
Os testes realizados durante o processo de TDD foram registrados em notebooks Jupyter e posteriormente transformados em PDFs que estão disponíveis dentro da pasta 'docs/history'. 

**Relatórios:**
O relatório do projeto (observações, padrões, desenvolvimento...) - Engenharia_de_Software_Relatório - e relatório da cobertura do código - Covarage_report - estão presentes na pasta de documentação docs. 

**Requisitos do sistema:**
-   Gerenciamento de eventos pessoais:
    -   Um usuário deve ser capaz de organizar sua agenda pessoal, criando e gerenciando eventos pessoais.
    -   O usuário deve poder visualizar, adicionar, editar e excluir eventos em sua agenda.
-   Categorias de eventos:
    -   Os eventos devem ser categorizados em tipos, como lembrete, evento e tarefa com prazo.
    -   Cada categoria de evento deve ter características específicas (data/hora, repetição, indisponibilidade).
    -   Lembrete:
        -   Os lembretes têm data, horário e opção de repetição.
        -   Os usuários devem ser notificados no horário do lembrete
    -   Evento:
        -   Os eventos possuem horário/data de início e de fim.
        -   Um evento ocupa o intervalo de tempo entre essas duas datas e horários.
        -   Os usuários têm a opção de indisponibilizar automaticamente esse intervalo na agenda.
        -   Eventos também podem se repetir.
    -   Tarefa com prazo:
        -   As tarefas com prazo possuem uma data de prazo para conclusão.
        -   Os usuários têm a opção de marcar o progresso da tarefa e receber lembretes relacionados ao prazo.
        -   Essas tarefas também podem ser recorrentes, como para objetivos semanais a serem cumpridos.
-   Disponibilidade para eventos externos:
    -   Os usuários podem marcar áreas de disponibilidade em sua agenda para permitir que outros usuários vejam quando estão disponíveis para eventos externos.
    -   É possível manter a privacidade dos eventos pessoais enquanto permite que outros vejam quando você está disponível.
-   Resolução de fusos horários:
    -   O sistema deve resolver automaticamente os problemas de fuso horário para os usuários, permitindo que vejam a agenda no fuso horário desejado. Sugestão: Os usuários podem configurar períodos de sono e almoço, ajudando na gestão dos fusos horários.
-   Eventos em grupo:
    -   Os usuários podem adicionar eventos em grupo, como reuniões de equipe ou eventos familiares.
    -   É possível verificar a disponibilidade dos membros do grupo antes de agendar o evento.
    -   A opção de visualizar a sobreposição de agendas dos membros do grupo facilita a escolha do melhor horário.
