
create table env (
    id integer primary key,
    name text unique,
    value BLOB
);
