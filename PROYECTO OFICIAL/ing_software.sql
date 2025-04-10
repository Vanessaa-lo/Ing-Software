-- phpMyAdmin SQL Dump
-- version 5.1.2
-- https://www.phpmyadmin.net/
--
-- Servidor: localhost:3306
-- Tiempo de generación: 10-04-2025 a las 22:53:49
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
(4, 'qwdfgh', 'sdfgv', '123456', 'sdfvghbj', 10),
(5, 'qwertyuiop', 'qwertyuiop', '12345', 'wdwewrrvevetvetv', 12),
(6, 'werthj', 'sdfgj', '123456', 'wer', 13);

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

--
-- Volcado de datos para la tabla `cortecaja`
--

INSERT INTO `cortecaja` (`idCorteCaja`, `Hora_Inicio`, `Hora_Terminar`, `Fecha_Inico`, `DineroEnCaja`, `IngresoDia`, `EgresoDIa`, `PlatillosVendidos`, `DineroFinalizar`, `TiempoTrascurrido`, `FechaFinalizar`, `Administrador_idAdministrador`) VALUES
(1, '07:40:55', '00:00', '2025-04-04', 1200, 1200, 0, 0, 0, 0, '2025-04-04', 1);

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

--
-- Volcado de datos para la tabla `detalleventas`
--

INSERT INTO `detalleventas` (`idDetalleVentas`, `Subtotal`, `Impuesto`, `Descuento`, `Total`, `Ventas_IdVentas`) VALUES
(1, 126, 24, 0, 150, 1),
(3, 126, 24, 0, 150, 3),
(4, 126, 24, 0, 150, 4),
(5, 126, 24, 0, 150, 5),
(6, 126, 24, 0, 150, 6),
(7, 126, 24, 0, 150, 7),
(8, 126, 24, 0, 150, 8),
(9, 126, 24, 0, 150, 9);

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
(2, 'qweryu', 'asdfgh', '1234567', 'asdfghj', 11),
(3, 'prueba', 'prueba', '123456789', 'pruebamail.com', 14);

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
  `CorteCaja_idCorteCaja` int(11) NOT NULL DEFAULT '1'
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Volcado de datos para la tabla `entradasproductos`
--

INSERT INTO `entradasproductos` (`IdEntradasProductos`, `Cantidad`, `Fecha`, `Descripcion`, `CorteCaja_idCorteCaja`) VALUES
(1, 2, '2025-03-12', '122', 1),
(2, 2, '2025-03-12', '122', 1),
(3, 12, '2025-03-12', 'acda', 1),
(4, 212, '2025-04-05', '121', 1),
(5, 212, '2025-04-05', '121', 1),
(15, 212, '2025-04-05', '12', 1),
(16, 12, '2025-04-05', 'wwew', 1);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `estatuspedido`
--

CREATE TABLE `estatuspedido` (
  `IdEstatusPedido` int(11) NOT NULL,
  `SituacionPedido` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Volcado de datos para la tabla `estatuspedido`
--

INSERT INTO `estatuspedido` (`IdEstatusPedido`, `SituacionPedido`) VALUES
(1, 'Pagado'),
(2, 'Pagado');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `generarpedido`
--

CREATE TABLE `generarpedido` (
  `IdGenerarPedido` int(11) NOT NULL,
  `HoraPedido` time NOT NULL,
  `FechaPedido` date NOT NULL,
  `Producto` varchar(45) NOT NULL,
  `NumeroMesa` int(11) NOT NULL,
  `Estatus` varchar(20) NOT NULL,
  `EstatusPedido_IdEstatusPedido` int(11) NOT NULL,
  `Clientes_Idcliente` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Volcado de datos para la tabla `generarpedido`
--

INSERT INTO `generarpedido` (`IdGenerarPedido`, `HoraPedido`, `FechaPedido`, `Producto`, `NumeroMesa`, `Estatus`, `EstatusPedido_IdEstatusPedido`, `Clientes_Idcliente`) VALUES
(1, '20:20:58', '2025-03-30', 'Hamburguesa BBQ (Extra Salsa BBQ)', 1, 'Pagado', 1, 1),
(2, '20:21:57', '2025-03-30', 'Pizza Hawaiana (Jamón)', 1, 'Pagado', 1, 1),
(3, '07:12:15', '2025-04-01', 'Hamburguesa BBQ (Sin Lechuga y Jitomate)', 1, 'Pagado', 1, 1),
(4, '02:08:06', '2025-04-05', 'Hamburguesa BBQ (Doble Carne)', 1, 'Pagado', 1, 1),
(5, '02:08:06', '2025-04-05', 'Pizza Hawaiana (Jamón)', 1, 'Pagado', 1, 1),
(6, '02:08:06', '2025-04-05', 'Tacos al Pastor (Cilantro)', 1, 'Pagado', 1, 1),
(7, '09:20:19', '2025-04-10', '11 (2)', 6, 'En preparación', 1, 1),
(8, '09:38:51', '2025-04-10', 'wdqw (dwa) - wdw', 6, 'Pagado', 2, 1),
(9, '09:58:14', '2025-04-10', '3 comensales | Pizza Hawaiana (1) - muuj', 4, 'Pagado', 2, 1);

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
-- Estructura de tabla para la tabla `productos`
--

CREATE TABLE `productos` (
  `IdProductos` int(11) NOT NULL,
  `Nombre` varchar(30) NOT NULL,
  `Precio` double NOT NULL,
  `FechaCaducidad` int(11) NOT NULL,
  `Descripcion` varchar(45) NOT NULL,
  `Marca` varchar(25) NOT NULL,
  `UnidadMedida` varchar(25) NOT NULL,
  `CorteCaja_idCorteCaja` int(11) NOT NULL DEFAULT '1'
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Volcado de datos para la tabla `productos`
--

INSERT INTO `productos` (`IdProductos`, `Nombre`, `Precio`, `FechaCaducidad`, `Descripcion`, `Marca`, `UnidadMedida`, `CorteCaja_idCorteCaja`) VALUES
(1, 'wefgh', 12, 111234, 'sdfghj', 'ml', 'mm', 1),
(2, 'mewpe', 12, 112234, 'asdf', 'jumex', 'mm', 1),
(3, 'efe', 232, 12, '3232', '2312', '23', 1);

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

--
-- Volcado de datos para la tabla `productosstock`
--

INSERT INTO `productosstock` (`IdProductosStock`, `Nombre`, `Descripcion`, `Cantidad`, `CorteCaja_idCorteCaja`) VALUES
(1, 'wefgh', 'sdfghj', 211, 1),
(2, 'mewpe', 'asdf', 10, 1);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `salidasproductos`
--

CREATE TABLE `salidasproductos` (
  `IdSalidasProductos` int(11) NOT NULL,
  `FechaSalida` date NOT NULL,
  `Detalle` varchar(45) NOT NULL,
  `Cantidad` varchar(45) NOT NULL,
  `CorteCaja_idCorteCaja` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Volcado de datos para la tabla `salidasproductos`
--

INSERT INTO `salidasproductos` (`IdSalidasProductos`, `FechaSalida`, `Detalle`, `Cantidad`, `CorteCaja_idCorteCaja`) VALUES
(1, '2025-03-12', '22', '11', NULL),
(2, '2025-04-05', 'ee', '2.0', 1);

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
(6, 'qwedf_c', 'cliente123'),
(7, 'werty_e', 'empleado123'),
(8, 'wertyui_c', 'cliente123'),
(9, 'qqqqqqqqqq', 'qwer'),
(10, 'pppppppppp', 'werh'),
(11, 'yyyyyyyy', 'qwet'),
(12, 'tttttttttt', '11111'),
(13, 'wewwwwww', 'qwef'),
(14, 'prueba', '123');

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
-- Volcado de datos para la tabla `ventas`
--

INSERT INTO `ventas` (`IdVentas`, `Hora`, `FechaVenta`, `DetalleVenta`, `CorteCaja_idCorteCaja`) VALUES
(1, '05:20:05', '2025-04-09', 'Hamburguesa BBQ (Extra Salsa BBQ)', 1),
(3, '23:07:53', '2025-04-09', 'Pizza Hawaiana (Jamón)', 1),
(4, '23:07:57', '2025-04-09', 'Hamburguesa BBQ (Doble Carne)', 1),
(5, '23:07:59', '2025-04-09', 'Pizza Hawaiana (Jamón)', 1),
(6, '23:08:00', '2025-04-09', 'Hamburguesa BBQ (Sin Lechuga y Jitomate)', 1),
(7, '23:08:03', '2025-04-09', 'Tacos al Pastor (Cilantro)', 1),
(8, '16:47:06', '2025-04-10', 'wdqw (dwa) - wdw', 1),
(9, '16:47:20', '2025-04-10', '3 comensales | Pizza Hawaiana (1) - muuj', 1);

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
-- Indices de la tabla `productos`
--
ALTER TABLE `productos`
  ADD PRIMARY KEY (`IdProductos`),
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
  MODIFY `IdCliente` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT de la tabla `comandapedido`
--
ALTER TABLE `comandapedido`
  MODIFY `IdComandaPedido` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `cortecaja`
--
ALTER TABLE `cortecaja`
  MODIFY `idCorteCaja` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT de la tabla `detalleventas`
--
ALTER TABLE `detalleventas`
  MODIFY `idDetalleVentas` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- AUTO_INCREMENT de la tabla `empleado`
--
ALTER TABLE `empleado`
  MODIFY `IdEmpleado` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT de la tabla `entradasproductos`
--
ALTER TABLE `entradasproductos`
  MODIFY `IdEntradasProductos` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=17;

--
-- AUTO_INCREMENT de la tabla `estatuspedido`
--
ALTER TABLE `estatuspedido`
  MODIFY `IdEstatusPedido` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT de la tabla `generarpedido`
--
ALTER TABLE `generarpedido`
  MODIFY `IdGenerarPedido` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- AUTO_INCREMENT de la tabla `productos`
--
ALTER TABLE `productos`
  MODIFY `IdProductos` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT de la tabla `productosstock`
--
ALTER TABLE `productosstock`
  MODIFY `IdProductosStock` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT de la tabla `salidasproductos`
--
ALTER TABLE `salidasproductos`
  MODIFY `IdSalidasProductos` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT de la tabla `usuario`
--
ALTER TABLE `usuario`
  MODIFY `IdUsuario` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=15;

--
-- AUTO_INCREMENT de la tabla `ventas`
--
ALTER TABLE `ventas`
  MODIFY `IdVentas` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

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
  ADD CONSTRAINT `fk_DetalleVentas_Ventas1` FOREIGN KEY (`Ventas_IdVentas`) REFERENCES `ventas` (`IdVentas`);

--
-- Filtros para la tabla `empleado`
--
ALTER TABLE `empleado`
  ADD CONSTRAINT `empleado_ibfk_1` FOREIGN KEY (`Usuario_IdUsuario`) REFERENCES `usuario` (`IdUsuario`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Filtros para la tabla `entradarecibe`
--
ALTER TABLE `entradarecibe`
  ADD CONSTRAINT `fk_EntradaRecibe_CorteCaja1` FOREIGN KEY (`CorteCaja_idCorteCaja`) REFERENCES `cortecaja` (`idCorteCaja`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Filtros para la tabla `generarpedido`
--
ALTER TABLE `generarpedido`
  ADD CONSTRAINT `fk_GenerarPedido_EstatusPedido2` FOREIGN KEY (`EstatusPedido_IdEstatusPedido`) REFERENCES `estatuspedido` (`IdEstatusPedido`) ON DELETE NO ACTION ON UPDATE NO ACTION;

--
-- Filtros para la tabla `generarrecibo`
--
ALTER TABLE `generarrecibo`
  ADD CONSTRAINT `fk_GenerarRecibo_Ventas1` FOREIGN KEY (`Ventas_IdVentas`) REFERENCES `ventas` (`IdVentas`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
