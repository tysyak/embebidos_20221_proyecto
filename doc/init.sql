create table usuario(
       id serial primary key,
       username varchar(40) not null unique,
       password varchar(128) not null,
       create_date timestamp default(now()),
       mod_date timestamp default(now())
);

create table chat(
       id serial primary key,
       usuario_id integer not null references usuario(id),
       chat_id varchar(9) not null unique,
       create_date timestamp default(now()),
       mod_date timestamp default(now())
);

create table alta_notificaciones(
       chat_id varchar(9) REFERENCES chat(chat_id) primary key,
       humo boolean default false,
       proximidad boolean default false,
       edo_cerradura boolean default false
);
