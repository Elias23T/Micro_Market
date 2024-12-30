CREATE DATABASE Micro_Market;
USE Micro_Market;

-- Tabla Usuario, define los roles (vendedor, administrador)
CREATE TABLE Usuario(
    Id_Usuario INT PRIMARY KEY IDENTITY(1,1),
    NombreUsuario VARCHAR(100) NOT NULL,
    Contrasena VARCHAR(100) NOT NULL,
    Rol VARCHAR(50) -- 'Vendedor' o 'Administrador'
);
select * from Usuario

-- Tabla Empleado, relacionar con Usuario
CREATE TABLE Empleado(
    Id_Empleado INT PRIMARY KEY IDENTITY(1,1),
    Nombre VARCHAR(100) NOT NULL,
    Apellido_Paterno VARCHAR(100),
    Apellido_Materno VARCHAR(100),
    CI INT,
    Celular VARCHAR(20),
    Id_Usuario INT FOREIGN KEY REFERENCES Usuario(Id_Usuario)
);
ALTER TABLE Empleado
ADD Estado BIT DEFAULT 1;

insert into Empleado(Nombre,Apellido_Paterno,Apellido_Materno,CI,Celular,Id_Usuario) values ('Elias','Terrazas','Azurduy',8954167,'64454120',5)
select* from Empleado

-- Tabla Cliente

CREATE TABLE Cliente(
    Id_Cliente INT PRIMARY KEY IDENTITY(1,1),
    Nombre VARCHAR(100) NOT NULL,
    Apellido_Paterno VARCHAR(100),
    Apellido_Materno VARCHAR(100),
    CI INT,
    Celular VARCHAR(20)
);
insert into Cliente(Nombre,Apellido_Paterno,Apellido_Materno,CI,Celular) values('David','Terrazas','Azurduy',1186452,'67748402')
select * from Cliente
-- Tabla Categoria, especifica sectores
CREATE TABLE Categoria(
    Id_Categoria INT PRIMARY KEY IDENTITY(1,1),
    NombreCategoria VARCHAR(100),
);
insert into Categoria(NombreCategoria,Descripcion) values ('Droga','de las buenas')
select*from Categoria
insert into Categoria(NombreCategoria,Descripcion) values ('bebidas','Cerveza')
select*from Categoria

-- Tabla Productos con relacion a Categoria
CREATE TABLE Productos(
    Id_Producto INT PRIMARY KEY IDENTITY(1,1),
    NombreProducto VARCHAR(100) NOT NULL,
    PrecioUnitario DECIMAL(10,2) NOT NULL,
    Stock INT NOT NULL,
    Id_Categoria INT FOREIGN KEY REFERENCES Categoria(Id_Categoria)
);
ALTER TABLE Productos
ADD CONSTRAINT FK_Productos_Categoria
FOREIGN KEY (Id_Categoria) REFERENCES Categoria(Id_Categoria)
ON DELETE CASCADE;

ALTER TABLE Productos
ADD Estado BIT DEFAULT 1;
ALTER TABLE Productos
ADD EnPromocion BIT DEFAULT 0;
ALTER TABLE Productos
ADD PrecioPromocion DECIMAL(10,2) NULL;

alter table Productos add Costo decimal(10,2)

select * from DetalleDeCompra

select* from Productos

-- Tabla Ventas, relacionar con Empleado y Cliente
CREATE TABLE Ventas(
    Id_Venta INT PRIMARY KEY IDENTITY(1,1),
    FechaVenta DATE NOT NULL,
    MontoTotal DECIMAL(10,2) NOT NULL,
    Id_Empleado INT FOREIGN KEY REFERENCES Empleado(Id_Empleado),
    Id_Cliente INT FOREIGN KEY REFERENCES Cliente(Id_Cliente)
);
select * from Ventas

-- Tabla DetalleVenta, relacionar con Productos y Ventas
CREATE TABLE DetalleVenta(
    Id_DetalleVenta INT PRIMARY KEY IDENTITY(1,1),
    Id_Venta INT FOREIGN KEY REFERENCES Ventas(Id_Venta),
    Id_Producto INT FOREIGN KEY REFERENCES Productos(Id_Producto),
    Cantidad INT NOT NULL,
    TotalVenta DECIMAL(10,2) NOT NULL
);
alter table DetalleVenta add PrecioUnitario decimal(10,2) not null

ALTER TABLE DetalleVenta
ADD CONSTRAINT FK_DetalleVenta_Productos
FOREIGN KEY (Id_Producto) REFERENCES Productos(Id_Producto)
ON DELETE CASCADE;

select * from DetalleVenta

-- Tabla Proveedor
CREATE TABLE Proveedor(
    Id_Proveedor INT PRIMARY KEY IDENTITY(1,1),
    Nombre VARCHAR(100) NOT NULL,
    Apellido_Paterno VARCHAR(100),
    Apellido_Materno VARCHAR(100),
    Celular VARCHAR(20)
);
ALTER TABLE Proveedor
ADD Descripcion VARCHAR(255);
select*from Proveedor

-- Tabla CompraDeProveedor, relacionar con Proveedor
CREATE TABLE CompraDeProveedor(
    Id_Compra INT PRIMARY KEY IDENTITY(1,1),
    FechaCompra DATE NOT NULL,
    MontoTotal DECIMAL(10,2) NOT NULL,
    Id_Proveedor INT FOREIGN KEY REFERENCES Proveedor(Id_Proveedor)
);
ALTER TABLE CompraDeProveedor
ADD Id_Producto INT;
ALTER TABLE CompraDeProveedor
ADD CONSTRAINT FK_CompraDeProveedor_IdProducto
FOREIGN KEY (Id_Producto) REFERENCES Productos(Id_Producto);

select *from CompraDeProveedor

-- Tabla DetalleDeCompra, relacionar con Compra y Productos

-- Tabla Promociones
CREATE TABLE Promociones(
    Id_Promocion INT PRIMARY KEY IDENTITY(1,1),
    NombrePromocion VARCHAR(100) NOT NULL,
    Descuento DECIMAL(5,2),
    FechaInicio DATE,
    FechaFin DATE
);

ALTER TABLE Promociones ADD Producto Varchar(255);


select* from Promociones

-- Tabla ProductosPromocion para relacionar Productos con Promociones
CREATE TABLE ProductosPromocion(
    Id_Promocion INT FOREIGN KEY REFERENCES Promociones(Id_Promocion),
    Id_Producto INT FOREIGN KEY REFERENCES Productos(Id_Producto),
    PRIMARY KEY (Id_Promocion, Id_Producto)
);
select * from ProductosPromocion


