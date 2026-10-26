create database ativo_vulnerabilidade;
use ativo_vulnerabilidade; 

create table ativos (
	id int auto_increment primary key,
	nome varchar(100) not null,
    ip varchar(45) not null,
    tipo varchar(50) not null,
    criticidade enum('baixa', 'media', 'alta', 'critica') not null
);

create table vulnerabilidades (
    id int auto_increment primary key,
    cve_id varchar(20) not null unique,
    descricao varchar(300),
    severidade enum('baixa', 'media', 'alta', 'critica') not null,
    cvss decimal(3,1) not null
);

create table ativo_vulnerabilidade (
    ativo_id int not null,
    vuln_id int not null,
    status varchar(20),
    detectada_em timestamp default current_timestamp,
    primary key (ativo_id, vuln_id),
    foreign key (ativo_id) references ativos(id),
    foreign key (vuln_id) references vulnerabilidades(id)
);

