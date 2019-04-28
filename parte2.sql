/* Creas usuarios para incisos A - C*/
CREATE USER operador PASSWORD '3c319c7c92f493a67462f5260998bf66';
CREATE USER gerente PASSWORD 'e575ca002aa2f9a3ea40ebb1324e9467';
CREATE USER administrador PASSWORD '63b54ef139ef9561e16af44b6c6fdc05';

GRANT CONNECT ON DATABASE LAB11 TO operador, gerente, administrador;

/* Todos permisos posibles para admin */
GRANT ALL PRIVILEGES
ON DATABASE LAB11 TO administrador
WITH GRANT OPTION;

GRANT ALL PRIVILEGESON ALL TABLES 
IN SCHEMA public TO administrador
WITH GRANT OPTION; 

/* Permisos lectura a operador */
GRANT SELECT ON ALL TABLES 
IN SCHEMA public TO operador;

/*  Permisos de lectura,  escritura y creacion de objetos a gerente*/
GRANT SELECT,INSERT ON ALL TABLES 
IN SCHEMA public TO gerente;

GRANT CREATE 
ON DATABASE LAB11 TO gerente;

/* Removemos permisos de creación de llaves foráneas y disparadores a operador*/
REVOKE REFERENCES, TRIGGER
ON ALL TABLES
IN SCHEMA public 
FROM operador;
