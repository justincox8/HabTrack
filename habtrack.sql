use habtrack;

create table users (
    id int AUTO_INCREMENT primary key,
    username varchar(50) unique not null,
    password varchar(200) not null

);

create table habits (
    id int AUTO_INCREMENT primary key,
    user_id int not null,
    habit varchar(50) not null,
    descr text,
    streak int default 0,
    last_day Date,
    foreign key (user_id) references users(id) on delete cascade
);

