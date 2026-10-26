**Exercício 1.3 — Decisão de arquitetura com CAP**



**1.** Tabela de saldo bancário de clientes — CP

Para o saldo bancário, a escolha seria CP, pois a consistência é essencial, o saldo precisa estar correto e atualizado em todos os nós. É melhor que uma operação fique temporariamente indisponível do que permitir que o sistema apresente um saldo incorreto.



**2.** Ingestão de 500 mil eventos de firewall por minuto em um SOC — AP

Para a ingestão de eventos de firewall, a escolha seria AP. O mais importante é que o sistema continue disponível para receber uma grande quantidade de eventos, mesmo durante uma falha de comunicação entre os servidores. Uma pequena inconsistência ou atraso na sincronização dos dados pode ser aceita nesse cenário.



**3.** Cache de tokens de sessão de usuários logados — AP

Para o cache de tokens de sessão, a escolha seria AP, pois o sistema deve continuar disponível para que os usuários consigam permanecer conectados mesmo em caso de falhas ou partições na rede. Uma pequena inconsistência temporária no cache pode ser aceita, desde que não comprometa a segurança das sessões.



**4.** Registro de quem autorizou cada transferência — CP

Para os registros de auditoria, a escolha seria CP, pois é fundamental manter os dados consistentes e confiáveis, porque o registro precisa identificar corretamente quem autorizou cada transferência. Não seria aceitável que diferentes servidores apresentassem informações diferentes sobre uma operação financeira.



**5.** Feed de indicadores de ameaça (IOCs) replicado em 5 regiões — AP

Para o feed de IOCs, a escolha seria AP. O sistema precisa permanecer disponível nas diferentes regiões para que as equipes de segurança possam consultar os indicadores de ameaça. Uma pequena diferença ou atraso na atualização entre as regiões é aceitável, desde que o serviço continue acessível.



