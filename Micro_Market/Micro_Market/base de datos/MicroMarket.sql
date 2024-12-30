-- Crear base de datos
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
DELETE FROM Usuario
WHERE Id_Usuario = 4;
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
    Descripcion VARCHAR(200)
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
    FechaVencimiento DATE,
    Id_Categoria INT FOREIGN KEY REFERENCES Categoria(Id_Categoria)
);
ALTER TABLE Productos
DROP COLUMN Imagen;
select* from Productos

-- Tabla Ventas, relacionar con Empleado y Cliente
CREATE TABLE Ventas(
    Id_Venta INT PRIMARY KEY IDENTITY(1,1),
    FechaVenta DATE NOT NULL,
    MontoTotal DECIMAL(10,2) NOT NULL,
    Id_Empleado INT FOREIGN KEY REFERENCES Empleado(Id_Empleado),
    Id_Cliente INT FOREIGN KEY REFERENCES Cliente(Id_Cliente)
);


-- Tabla DetalleVenta, relacionar con Productos y Ventas
CREATE TABLE DetalleVenta(
    Id_DetalleVenta INT PRIMARY KEY IDENTITY(1,1),
    Id_Venta INT FOREIGN KEY REFERENCES Ventas(Id_Venta),
    Id_Producto INT FOREIGN KEY REFERENCES Productos(Id_Producto),
    Cantidad INT NOT NULL,
    PrecioUnitario DECIMAL(10,2) NOT NULL,
    TotalVenta DECIMAL(10,2) NOT NULL
);

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

-- Tabla DetalleDeCompra, relacionar con Compra y Productos
CREATE TABLE DetalleDeCompra(
    Id_DetalleCompra INT PRIMARY KEY IDENTITY(1,1),
    Id_Compra INT FOREIGN KEY REFERENCES CompraDeProveedor(Id_Compra),
    Id_Producto INT FOREIGN KEY REFERENCES Productos(Id_Producto),
    Cantidad INT NOT NULL,
    PrecioUnitario DECIMAL(10,2) NOT NULL,
    TotalCompra DECIMAL(10,2) NOT NULL
);

-- Tabla Promociones
CREATE TABLE Promociones(
    Id_Promocion INT PRIMARY KEY IDENTITY(1,1),
    NombrePromocion VARCHAR(100) NOT NULL,
    Descripcion VARCHAR(500),
    Descuento DECIMAL(5,2),
    PrecioDescuento DECIMAL(10,2), -- Precio despues de aplicar el descuento
    FechaInicio DATE,
    FechaFin DATE
);

-- Tabla ProductosPromocion para relacionar Productos con Promociones
CREATE TABLE ProductosPromocion(
    Id_Promocion INT FOREIGN KEY REFERENCES Promociones(Id_Promocion),
    Id_Producto INT FOREIGN KEY REFERENCES Productos(Id_Producto),
    PRIMARY KEY (Id_Promocion, Id_Producto)
);