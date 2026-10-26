use ativo_vulnerabilidade; 

create table alertas (
    id int auto_increment primary key,
    tipo varchar(50),
    ip_origem varchar(45),
    severidade enum('baixa','media','alta','critica'),
    status varchar(20) default 'aberto',
    criado_em timestamp default current_timestamp
);

insert into alertas (tipo, ip_origem, severidade) values
('Tentativa de acesso indevido', '192.168.1.20', 'alta'),
('Port Scan', '10.0.0.15', 'critica'),
('Falha de autenticação', '192.168.1.30', 'alta'),
('Tentativa de login suspeita', '192.168.1.40', 'media');

select * from alertas where severidade = 'alta';

update alertas set status = 'resolvido' where id = 1;

select severidade, COUNT(*) as total from alertas group by severidade;

delete from alertas where criado_em < NOW() - interval 90 day;