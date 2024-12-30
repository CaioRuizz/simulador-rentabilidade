# Simulador de Rentabilidade

## Objetivo

O **Simulador de Rentabilidade** tem como objetivo fornecer uma plataforma onde investidores possam criar portfólios, simular investimentos e comparar a rentabilidade histórica de ativos ou portfólios. A plataforma permitirá que o usuário personalize o período da análise, a periodicidade dos rebalanceamentos e a forma de reinvestimento dos dividendos, oferecendo ao investidor a possibilidade da realização de um **backtest** antes de utilizar seu dinheiro real (lembrando que rentabilidade passada não garante rentabilidade futura).

## Features Esperadas do Sistema

O **Simulador de Rentabilidade** será desenvolvido com as seguintes funcionalidades principais, que visam oferecer uma experiência completa e eficiente para os investidores:

### 1. **Criação e Gerenciamento de Portfólios**
- Permitir que o usuário crie portfólios de investimentos personalizados.
- Oferecer a possibilidade de adicionar ou remover ativos de um portfólio.
- Suporte à configuração do valor inicial investido.
- Suporte à configuração do valor periódico investido, permitindo que o usuário ajuste os valores e a periodicidade.
- Acompanhamento do desempenho de cada portfólio criado.

### 2. **Simulação de Rentabilidade**
- Realizar simulações de rentabilidade de um portfólio ao longo do tempo.
- Permitir que o usuário escolha o período de análise (por exemplo, últimos 5 anos, 10 anos, etc.).
- Permitir que o usuário configure a periodicidade dos rebalanceamentos do portfólio (mensal, trimestral, anual, etc.).
- Permitir que o usuário escolha a forma de reinvestimento dos dividendos (reinvestir automaticamente no mesmo ou em outro ativo ou retirar os dividendos).
- Exibir resultados de rentabilidade histórica (com gráficos de performance) de acordo com as configurações do usuário.
- Oferecer métricas detalhadas de performance, como retorno absoluto, retorno anualizado, risco, volatilidade e outros indicadores financeiros.

### 3. **Comparação de Rentabilidade entre Ativos e Portfólios**
- Permitir que o usuário compare a rentabilidade de diferentes ativos ou portfólios.
- Exibir gráficos comparativos para facilitar a visualização da performance de múltiplos investimentos.
- Permitir que o usuário selecione diferentes ativos financeiros (ações, fundos, ETFs, etc.) para a comparação de rentabilidade.

### 4. **Ajustes de Parâmetros de Simulação**
- Permitir que o usuário defina parâmetros personalizados para cada simulação, como:
  - Período de tempo para simulação.
  - Frequência de rebalanceamento.
  - Tipo de reinvestimento dos dividendos.
  - Tipo de ativo (ações, fundos, etc.).
  - Valor inicial investido e aportes periódicos.

### 5. **Interface de Usuário Intuitiva**
- Interface amigável e responsiva para facilitar a navegação dos usuários finais (investidores).
- Tela de dashboard com visão geral do portfólio e das simulações.
- Exibição de gráficos interativos para facilitar a análise de rentabilidade.
- Filtros e ferramentas de busca para facilitar a seleção de ativos e a criação de portfólios.

### 6. **Login opcional**
- Permitir que usuários não logados simulem a rentabilidade de portfólios
- Permitir que usuários logados armazenem portfólios diversos
- Permitir que usuários logados comparem os portfólios armazenados

### 7. **Suporte a Diversos Tipos de Ativos**
- Suporte a diversos tipos de ativos financeiros para as simulações, incluindo:
  - Ações
  - ETFs (Exchange-Traded Funds)
  - Fundos Imobiliários
  - Criptomoedas
  
### 8. **Relatórios e Exportação de Dados**
- Geração de relatórios detalhados sobre o desempenho dos portfólios e ativos.
- Possibilidade de exportar os resultados das simulações para formatos como CSV, Excel ou PDF para análise offline.

## Estrutura do Projeto

A estrutura do projeto será organizada de maneira modular, com uma divisão em camadas que visa a escalabilidade e a facilidade de manutenção. O primeiro passo do desenvolvimento será focado na implementação de um **processo ETL** (Extração, Transformação e Carga) para alimentar a base de dados com os dados financeiros necessários para a realização das simulações.

### 1. **ETL (Extract, Transform, Load)**

O **ETL** será a primeira camada a ser desenvolvida, responsável por garantir que os dados financeiros necessários para as simulações sejam carregados e processados adequadamente. O processo de ETL será dividido em duas funcionalidades principais:

#### 1.1. **Carga Total**
A carga total será uma função que realizará a extração completa dos dados financeiros, transformando-os e carregando-os na base de dados. Esta função será executada manualmente pelo administrador da plataforma, que poderá acioná-la através do orquestrador de fluxos de trabalho.

**Responsabilidades**:
- **Extração**: Coletar todos os dados financeiros de ativos ou portfólios (preços históricos, dividendos, etc.).
- **Transformação**: Realizar a limpeza, validação e formatação dos dados, garantindo que eles estejam no formato adequado para armazenamento e uso nas simulações.
- **Carga**: Armazenar os dados transformados na base de dados, garantindo a integridade e a consistência dos mesmos.

#### 1.2. **Carga Incremental**
A carga incremental será um processo diário, executado automaticamente, com a possibilidade do administrador executá-la manualmente através do orquestrador de fluxos de trabalho. Este processo irá extrair os dados financeiros mais recentes, atualizar ou adicionar as informações existentes e carregar os novos dados na base de dados.

**Responsabilidades**:
- **Extração**: Obter apenas os dados financeiros novos ou atualizados desde a última execução do processo de carga.
- **Transformação**: Limpar e validar os dados extraídos, mantendo a consistência com os dados anteriores.
- **Carga**: Atualizar ou adicionar os dados na base de dados, garantindo que os dados históricos permaneçam intactos e que as informações mais recentes sejam incorporadas.

**Benefícios**:
- Garantir que os dados estejam sempre atualizados, permitindo que as simulações de rentabilidade reflitam a situação mais recente do mercado financeiro.
- Otimizar a performance, extraindo e carregando apenas os dados necessários para atualização diária.

### 2. **Banco de Dados**
Após o processo ETL, a próxima camada a ser desenvolvida será a estrutura do **banco de dados**. Ele será responsável por armazenar todos os dados necessários para as simulações e o histórico dos portfólios. O processo de ETL irá garantir que os dados estejam corretamente carregados e atualizados.

**Responsabilidades**:
- Armazenar dados históricos financeiros de ativos e portfólios.
- Armazenar resultados das simulações de rentabilidade.
- Garantir a integridade e consistência dos dados, permitindo a consulta eficiente para as simulações.

### 3. **Backend**
Após a configuração do banco de dados, o backend será responsável pela implementação da lógica de negócio, comunicação com a base de dados e fornecimento de uma API para o frontend.

**Responsabilidades**:
- Implementar a lógica de simulação de rentabilidade, considerando os dados extraídos e transformados no processo de ETL.
- Expor endpoints da API para que o frontend possa interagir com a plataforma, solicitando simulações, visualizando resultados, etc.

### 4. **Frontend**
O frontend será responsável pela interface de usuário, onde os investidores poderão interagir com a plataforma. A interface do usuário final permitirá a criação de portfólios, a configuração de parâmetros de simulação e a visualização dos resultados das simulações de rentabilidade.

**Responsabilidades**:
- Interface para o usuário final: criação de portfólios, configuração de parâmetros de simulação e visualização de resultados.

### 5. **Orquestrador de Fluxos de Trabalho**
A interface para o administrador do sistema não será no frontend, mas sim através de um orquestrador de fluxos de trabalho. O administrador poderá executar e monitorar o processo de carga total e visualizar o status da carga incremental.

**Responsabilidades**:
- Permitir a execução do processo de carga total e monitoramento do status da carga incremental.
- Automação da execução do processo de carga incremental, garantindo que a base de dados esteja sempre atualizada.

### 6. **Testes**
A fase de desenvolvimento incluirá a implementação de testes para garantir que os processos de ETL e as funcionalidades da plataforma funcionem corretamente.

**Responsabilidades**:
- **Testes de ETL**: Garantir que os dados sejam extraídos, transformados e carregados corretamente, tanto no processo de carga total quanto na carga incremental.
- **Testes de Backend**: Verificar se a lógica de negócio para simulação de rentabilidade está correta.
- **Testes de Frontend**: Assegurar que a interface de usuário está funcionando conforme o esperado.

### 7. **Automação e Monitoramento**
O processo de carga incremental será automatizado, sendo executado diariamente para garantir que a base de dados esteja sempre atualizada. Será necessário um mecanismo de monitoramento para garantir que a carga esteja ocorrendo sem falhas.

**Responsabilidades**:
- Automatizar a execução da carga incremental.
- Criar notificações ou relatórios de status de carga para o administrador da plataforma, informando se a carga foi bem-sucedida ou se ocorreu algum erro.

---

## Plano de Desenvolvimento

### Fase 1: **Desenvolvimento do Processo ETL**
- **Objetivo**: Implementar as funcionalidades de carga total e carga incremental.
- **Tarefas**:
  - Criar a função de carga total, permitindo a extração, transformação e carga de todos os dados financeiros.
  - Criar a função de carga incremental, para que apenas os dados novos ou atualizados sejam extraídos e carregados.
  - Testar ambos os processos para garantir que os dados sejam carregados corretamente.
  - Implementar uma interface no orquestrador de fluxos de trabalho para o administrador executar e monitorar as cargas de dados.

### Fase 2: **Desenvolvimento do Banco de Dados**
- **Objetivo**: Criar a estrutura do banco de dados e garantir que os dados sejam armazenados de forma eficiente e consistente.
- **Tarefas**:
  - Implementar o banco de dados para armazenar dados históricos financeiros e resultados das simulações de rentabilidade.
  - Integrar o banco de dados com o processo ETL para garantir a carga correta e eficiente dos dados.
  - Garantir que o banco de dados suporte consultas rápidas e eficientes para as simulações de rentabilidade.

### Fase 3: **Desenvolvimento do Backend**
- **Objetivo**: Criar a lógica de negócio para a simulação de rentabilidade e integração com a base de dados.
- **Tarefas**:
  - Implementar a API para comunicação entre o frontend e o backend.
  - Integrar o backend com a base de dados, utilizando os dados carregados pelo processo ETL.
  - Criar endpoints para realizar simulações de rentabilidade com base nos dados financeiros disponíveis.

### Fase 4: **Desenvolvimento do Frontend**
- **Objetivo**: Criar a interface de usuário para o administrador e para os investidores.
- **Tarefas**:
  - Criar a interface do usuário final, permitindo a criação de portfólios e visualização dos resultados das simulações de rentabilidade.

### Fase 5: **Testes e Validação**
- **Objetivo**: Garantir que todas as funcionalidades estejam funcionando conforme esperado.
- **Tarefas**:
  - Testar o processo ETL (carga total e incremental).
  - Testar o backend (simulação de rentabilidade).
  - Testar a interface de usuário para garantir uma boa experiência.

### Fase 6: **Deploy e Manutenção**
- **Objetivo**: Realizar o deploy do sistema e garantir a manutenção contínua.
- **Tarefas**:
  - Realizar o deploy da aplicação em um ambiente de produção.
  - Monitorar o sistema para garantir que as cargas de dados ocorram corretamente.
  - Realizar manutenções e atualizações conforme necessário.
