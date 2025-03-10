-- phpMyAdmin SQL Dump
-- version 5.1.2
-- https://www.phpmyadmin.net/
--
-- Servidor: localhost:3306
-- Tiempo de generación: 10-03-2025 a las 04:21:07
-- Versión del servidor: 5.7.24
-- Versión de PHP: 8.3.1

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `ing_software`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `cliente`
--

CREATE TABLE `cliente` (
  `IdCliente` int(11) NOT NULL,
  `Nombre` varchar(50) NOT NULL,
  `Apellido` varchar(50) NOT NULL,
  `Telefono` varchar(15) NOT NULL,
  `Correo` varchar(100) NOT NULL,
  `Usuario_IdUsuario` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Volcado de datos para la tabla `cliente`
--

INSERT INTO `cliente` (`IdCliente`, `Nombre`, `Apellido`, `Telefono`, `Correo`, `Usuario_IdUsuario`) VALUES
(1, 'qwedf', 'qwsdfg', '1234', 'waada', 6),
(2, 'wertyui', 'wertyu', '12345', 'asdfgh', 8),
(3, 'asdfg', 'qwerty', '12345', 'asdfg', 9),
(4, 'qwdfgh', 'sdfgv', '123456', 'sdfvghbj', 10);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `comandapedido`
--

CREATE TABLE `comandapedido` (
  `IdComandaPedido` int(11) NOT NULL,
  `GenerarComanda` varchar(50) NOT NULL,
  `GenerarPedido_IdGenerarPedido` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `cortecaja`
--

CREATE TABLE `cortecaja` (
  `idCorteCaja` int(11) NOT NULL,
  `Hora_Inicio` varchar(10) NOT NULL,
  `Hora_Terminar` varchar(10) NOT NULL,
  `Fecha_Inico` varchar(10) NOT NULL,
  `DineroEnCaja` double NOT NULL,
  `IngresoDia` double NOT NULL,
  `EgresoDIa` double NOT NULL,
  `PlatillosVendidos` int(11) NOT NULL,
  `DineroFinalizar` double NOT NULL,
  `TiempoTrascurrido` int(11) NOT NULL,
  `FechaFinalizar` date NOT NULL,
  `Administrador_idAdministrador` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `detalleventas`
--

CREATE TABLE `detalleventas` (
  `idDetalleVentas` int(11) NOT NULL,
  `Subtotal` float NOT NULL,
  `Impuesto` float NOT NULL,
  `Descuento` float NOT NULL,
  `Total` float NOT NULL,
  `Ventas_IdVentas` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `empleado`
--

CREATE TABLE `empleado` (
  `IdEmpleado` int(11) NOT NULL,
  `Nombre` varchar(50) NOT NULL,
  `Apellido` varchar(50) NOT NULL,
  `Telefono` varchar(15) NOT NULL,
  `Correo` varchar(100) NOT NULL,
  `Usuario_IdUsuario` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Volcado de datos para la tabla `empleado`
--

INSERT INTO `empleado` (`IdEmpleado`, `Nombre`, `Apellido`, `Telefono`, `Correo`, `Usuario_IdUsuario`) VALUES
(1, 'werty', 'ergh', '2342345', 'qwf', 7),
(2, 'qweryu', 'asdfgh', '1234567', 'asdfghj', 11);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `entradarecibe`
--

CREATE TABLE `entradarecibe` (
  `IdEntradaProductoa` int(11) NOT NULL,
  `FechaRecibo` date NOT NULL,
  `EmpleadoRecibio` varchar(45) NOT NULL,
  `CorteCaja_idCorteCaja` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `entradasproductos`
--

CREATE TABLE `entradasproductos` (
  `IdEntradasProductos` int(11) NOT NULL,
  `Cantidad` int(11) NOT NULL,
  `Fecha` date NOT NULL,
  `Descripcion` varchar(45) NOT NULL,
  `CorteCaja_idCorteCaja` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `estatuspedido`
--

CREATE TABLE `estatuspedido` (
  `IdEstatusPedido` int(11) NOT NULL,
  `SituacionPedido` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `generarpedido`
--

CREATE TABLE `generarpedido` (
  `IdGenerarPedido` int(11) NOT NULL,
  `HoraPedido` int(11) NOT NULL,
  `FechaPedido` date NOT NULL,
  `Producto` varchar(45) NOT NULL,
  `NumeroMesa` int(11) NOT NULL,
  `Estatus` varchar(20) NOT NULL,
  `EstatusPedido_IdEstatusPedido` int(11) NOT NULL,
  `Clientes_Idcliente` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `generarrecibo`
--

CREATE TABLE `generarrecibo` (
  `IdGenerarRecibo` int(11) NOT NULL,
  `FechaRecibo` varchar(45) NOT NULL,
  `HoraRecibo` varchar(45) NOT NULL,
  `descripcion` varchar(45) NOT NULL,
  `Ventas_IdVentas` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `platillos`
--

CREATE TABLE `platillos` (
  `IdPlatillos` int(11) NOT NULL,
  `Nombre` varchar(45) NOT NULL,
  `Precio` float NOT NULL,
  `Cantidad` varchar(45) NOT NULL,
  `Descripcion` varchar(45) NOT NULL,
  `Ingredientes` varchar(45) NOT NULL,
  `Porciones` varchar(45) NOT NULL,
  `CorteCaja_idCorteCaja` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `productos`
--

CREATE TABLE `productos` (
  `IdProductos` int(11) NOT NULL,
  `Nombre` varchar(30) NOT NULL,
  `Precio` double NOT NULL,
  `FechaCaducidad` date NOT NULL,
  `Descripcion` varchar(45) NOT NULL,
  `Marca` varchar(25) NOT NULL,
  `UnidadMedida` varchar(25) NOT NULL,
  `CorteCaja_idCorteCaja` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `productosstock`
--

CREATE TABLE `productosstock` (
  `IdProductosStock` int(11) NOT NULL,
  `Nombre` varchar(45) NOT NULL,
  `Descripcion` varchar(35) NOT NULL,
  `Cantidad` double NOT NULL,
  `CorteCaja_idCorteCaja` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `salidasproductos`
--

CREATE TABLE `salidasproductos` (
  `IdSalidasProductos` int(11) NOT NULL,
  `FechaSalida` date NOT NULL,
  `Detalle` varchar(45) NOT NULL,
  `Cantidad` varchar(45) NOT NULL,
  `CorteCaja_idCorteCaja` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `tipossalidas`
--

CREATE TABLE `tipossalidas` (
  `idTiposSalidas` int(11) NOT NULL,
  `ConceptoSalida` varchar(45) NOT NULL,
  `SalidasProductos_IdSalidasProductos` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuario`
--

CREATE TABLE `usuario` (
  `IdUsuario` int(11) NOT NULL,
  `NombreUsuario` varchar(45) NOT NULL,
  `Contraseña` varchar(45) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Volcado de datos para la tabla `usuario`
--

INSERT INTO `usuario` (`IdUsuario`, `NombreUsuario`, `Contraseña`) VALUES
(2, 'eertyre', 'wert'),
(3, 'puta', '121213'),
(6, 'qwedf_c', 'cliente123'),
(7, 'werty_e', 'empleado123'),
(8, 'wertyui_c', 'cliente123'),
(9, 'qqqqqqqqqq', 'qwer'),
(10, 'pppppppppp', 'werh'),
(11, 'yyyyyyyy', 'qwet');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `ventas`
--

CREATE TABLE `ventas` (
  `IdVentas` int(11) NOT NULL,
  `Hora` varchar(45) NOT NULL,
  `FechaVenta` date NOT NULL,
  `DetalleVenta` varchar(45) NOT NULL,
  `CorteCaja_idCorteCaja` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `cliente`
--
ALTER TABLE `cliente`
  ADD PRIMARY KEY (`IdCliente`),
  ADD UNIQUE KEY `Correo` (`Correo`),
  ADD KEY `Usuario_IdUsuario` (`Usuario_IdUsuario`);

--
-- Indices de la tabla `comandapedido`
--
ALTER TABLE `comandapedido`
  ADD PRIMARY KEY (`IdComandaPedido`),
  ADD KEY `fk_ComandaPedido_GenerarPedido1_idx` (`GenerarPedido_IdGenerarPedido`);

--
-- Indices de la tabla `cortecaja`
--
ALTER TABLE `cortecaja`
  ADD PRIMARY KEY (`idCorteCaja`),
  ADD KEY `fk_CorteCaja_Administrador1_idx` (`Administrador_idAdministrador`);

--
-- Indices de la tabla `detalleventas`
--
ALTER TABLE `detalleventas`
  ADD PRIMARY KEY (`idDetalleVentas`),
  ADD KEY `fk_DetalleVentas_Ventas1_idx` (`Ventas_IdVentas`);

--
-- Indices de la tabla `empleado`
--
ALTER TABLE `empleado`
  ADD PRIMARY KEY (`IdEmpleado`),
  ADD UNIQUE KEY `Correo` (`Correo`),
  ADD KEY `Usuario_IdUsuario` (`Usuario_IdUsuario`);

--
-- Indices de la tabla `entradarecibe`
--
ALTER TABLE `entradarecibe`
  ADD PRIMARY KEY (`IdEntradaProductoa`),
  ADD KEY `fk_EntradaRecibe_CorteCaja1_idx` (`CorteCaja_idCorteCaja`);

--
-- Indices de la tabla `entradasproductos`
--
ALTER TABLE `entradasproductos`
  ADD PRIMARY KEY (`IdEntradasProductos`),
  ADD KEY `fk_EntradasProductos_CorteCaja1_idx` (`CorteCaja_idCorteCaja`);

--
-- Indices de la tabla `estatuspedido`
--
ALTER TABLE `estatuspedido`
  ADD PRIMARY KEY (`IdEstatusPedido`);

--
-- Indices de la tabla `generarpedido`
--
ALTER TABLE `generarpedido`
  ADD PRIMARY KEY (`IdGenerarPedido`),
  ADD KEY `fk_GenerarPedido_EstatusPedido2_idx` (`EstatusPedido_IdEstatusPedido`),
  ADD KEY `fk_GenerarPedido_Clientes1_idx` (`Clientes_Idcliente`);

--
-- Indices de la tabla `generarrecibo`
--
ALTER TABLE `generarrecibo`
  ADD PRIMARY KEY (`IdGenerarRecibo`),
  ADD KEY `fk_GenerarRecibo_Ventas1_idx` (`Ventas_IdVentas`);

--
-- Indices de la tabla `platillos`
--
ALTER TABLE `platillos`
  ADD PRIMARY KEY (`IdPlatillos`),
  ADD KEY `fk_Platillos_CorteCaja1_idx` (`CorteCaja_idCorteCaja`);

--
-- Indices de la tabla `productos`
--
ALTER TABLE `productos`
  ADD KEY `fk_Productos_CorteCaja1_idx` (`CorteCaja_idCorteCaja`);

--
-- Indices de la tabla `productosstock`
--
ALTER TABLE `productosstock`
  ADD PRIMARY KEY (`IdProductosStock`),
  ADD KEY `fk_ProductosStock_CorteCaja1_idx` (`CorteCaja_idCorteCaja`);

--
-- Indices de la tabla `salidasproductos`
--
ALTER TABLE `salidasproductos`
  ADD PRIMARY KEY (`IdSalidasProductos`),
  ADD KEY `fk_SalidasProductos_CorteCaja1_idx` (`CorteCaja_idCorteCaja`);

--
-- Indices de la tabla `tipossalidas`
--
ALTER TABLE `tipossalidas`
  ADD PRIMARY KEY (`idTiposSalidas`),
  ADD KEY `fk_TiposSalidas_SalidasProductos1_idx` (`SalidasProductos_IdSalidasProductos`);

--
-- Indices de la tabla `usuario`
--
ALTER TABLE `usuario`
  ADD PRIMARY KEY (`IdUsuario`);

--
-- Indices de la tabla `ventas`
--
ALTER TABLE `ventas`
  ADD PRIMARY KEY (`IdVentas`),
  ADD KEY `fk_Ventas_CorteCaja1_idx` (`CorteCaja_idCorteCaja`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `cliente`
--
ALTER TABLE `cliente`
  MODIFY `IdCliente` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT de la tabla `empleado`
--
ALTER TABLE `empleado`
  MODIFY `IdEmpleado` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT de la tabla `estatuspedido`
--
ALTER TABLE `estatuspedido`
  MODIFY `IdEstatusPedido` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `usuario`
--
ALTER TABLE `usuario`
  MODIFY `IdUsuario` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `cliente`
--
ALTER TABLE `cliente`
  ADD CONSTRAINT `cliente_ibfk_1` FOREIGN KEY (`Usuario_IdUsuario`) REFERENCES `usuario` (`IdUsuario`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Filtros para la tabla `comandapedido`
--
ALTER TABLE `comandapedido`
  ADD CONSTRAINT `fk_ComandaPedido_GenerarPedido1` FOREIGN KEY (`GenerarPedido_IdGenerarPedido`) REFERENCES `generarpedido` (`IdGenerarPedido`) ON DELETE NO ACTION ON UPDATE NO ACTION;

--
-- Filtros para la tabla `detalleventas`
--
ALTER TABLE `detalleventas`
  ADD CONSTRAINT `fk_DetalleVentas_Ventas1` FOREIGN KEY (`Ventas_IdVentas`) REFERENCES `ventas` (`IdVentas`) ON DELETE NO ACTION ON UPDATE NO ACTION;

--
-- Filtros para la tabla `empleado`
--
ALTER TABLE `empleado`
  ADD CONSTRAINT `empleado_ibfk_1` FOREIGN KEY (`Usuario_IdUsuario`) REFERENCES `usuario` (`IdUsuario`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Filtros para la tabla `entradarecibe`
--
ALTER TABLE `entradarecibe`
  ADD CONSTRAINT `fk_EntradaRecibe_CorteCaja1` FOREIGN KEY (`CorteCaja_idCorteCaja`) REFERENCES `cortecaja` (`idCorteCaja`) ON DELETE NO ACTION ON UPDATE NO ACTION;

--
-- Filtros para la tabla `entradasproductos`
--
ALTER TABLE `entradasproductos`
  ADD CONSTRAINT `fk_EntradasProductos_CorteCaja1` FOREIGN KEY (`CorteCaja_idCorteCaja`) REFERENCES `cortecaja` (`idCorteCaja`) ON DELETE NO ACTION ON UPDATE NO ACTION;

--
-- Filtros para la tabla `generarpedido`
--
ALTER TABLE `generarpedido`
  ADD CONSTRAINT `fk_GenerarPedido_EstatusPedido2` FOREIGN KEY (`EstatusPedido_IdEstatusPedido`) REFERENCES `estatuspedido` (`IdEstatusPedido`) ON DELETE NO ACTION ON UPDATE NO ACTION;

--
-- Filtros para la tabla `generarrecibo`
--
ALTER TABLE `generarrecibo`
  ADD CONSTRAINT `fk_GenerarRecibo_Ventas1` FOREIGN KEY (`Ventas_IdVentas`) REFERENCES `ventas` (`IdVentas`) ON DELETE NO ACTION ON UPDATE NO ACTION;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
