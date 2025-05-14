-- phpMyAdmin SQL Dump
-- version 5.1.2
-- https://www.phpmyadmin.net/
--
-- Servidor: localhost:3306
-- Tiempo de generación: 14-05-2025 a las 22:17:59
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
(6, 'werthj', 'sdfgj', '123456', 'wer', 13),
(7, 'Juan', 'gonzalez', '32212133', 'dscew@gmailcom', 16),
(8, 'joceline', 'de la torre', '317018100', 'joceline@gmail.com', 18),
(9, 'pedro', 'juan', '1234123451', '32223@gmail.com', 20),
(10, 'Ian', 'Ian', '1111111111', 'ianrara@gmai.com', 21),
(11, 'pedro', 'pedro', '2222222222', 'mwwce@gmail.com', 24);

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
(1, '07:40:55', '00:00', '2025-04-04', 390, 690, 500, 0, 0, 0, '2025-04-04', 1);

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
(3, 'prueba', 'prueba', '123456789', 'pruebamail.com', 14),
(4, 'pedro', 'lopez', '322223324', 'lopezQgmail.com', 15),
(5, 'Emily', 'Villanueva', '322308474155677', 'emy@gmail.com', 17),
(6, 'Xavier Noel', 'Ibarra', '3223521446', 'xav@gmail.com', 19),
(7, 'Pedro', 'Pedro', '1222223345', 'pedro@gmail.com', 22),
(8, 'pedro', 'juan', '2222222222', 'ian@gmail.com', 23);

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
(16, 12, '2025-04-05', 'wwew', 1),
(17, -6, '2025-04-10', 'ENTRADA DE COCA COLA', 1),
(18, 2, '2025-05-06', 'jojojo', 1),
(19, 12, '2025-05-06', '34', 1),
(20, 22, '2025-05-10', 'eef', 1);

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
(2, 'Pagado'),
(3, 'Pedido Realizado');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `generarpedido`
--

CREATE TABLE `generarpedido` (
  `IdGenerarPedido` int(11) NOT NULL,
  `HoraPedido` time NOT NULL,
  `FechaPedido` date NOT NULL,
  `Producto` varchar(500) DEFAULT NULL,
  `Total` decimal(10,2) DEFAULT NULL,
  `NumeroMesa` int(11) NOT NULL,
  `Estatus` varchar(20) NOT NULL,
  `EstatusPedido_IdEstatusPedido` int(11) NOT NULL,
  `Clientes_Idcliente` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Volcado de datos para la tabla `generarpedido`
--

INSERT INTO `generarpedido` (`IdGenerarPedido`, `HoraPedido`, `FechaPedido`, `Producto`, `Total`, `NumeroMesa`, `Estatus`, `EstatusPedido_IdEstatusPedido`, `Clientes_Idcliente`) VALUES
(32, '23:01:28', '2025-05-11', 'Pizza Hawaiana - Ingredientes: Pina, Jamón, Queso, Mediana, Ensalada, Guacamole', '150.00', 1, 'Pagado', 3, 1),
(33, '23:01:28', '2025-05-11', 'Hamburguesa BBQ - Ingredientes: Doble Carne, Con Queso, Extra Salsa BBQ, Con Tocino, Sin Lechuga y Jitomate, Con Papas, Chica, Ensalada, Salsa Picante', '180.00', 1, 'Pagado', 3, 1),
(34, '23:01:28', '2025-05-11', 'Pizza Hawaiana - Ingredientes: Pina, Jamón, Queso, Mediana, Ensalada, Salsa Picante', '150.00', 1, 'Pagado', 3, 1),
(35, '23:21:24', '2025-05-11', 'Pizza Hawaiana - Ingredientes: Pina, Jamón, Queso, Chica, Ensalada, Salsa Picante', '150.00', 1, 'Pagado', 3, 1),
(36, '23:21:24', '2025-05-11', 'Pizza Hawaiana - Ingredientes: Pina, Jamón, Queso, Chica, Ensalada', '140.00', 1, 'Pagado', 3, 1),
(37, '20:44:46', '2025-05-12', 'Pizza Hawaiana - Ingredientes: Pina, Jamón, Queso, Mediana, Ensalada, Salsa Picante $10', '150.00', 1, 'Pagado', 3, 1),
(38, '20:44:46', '2025-05-12', 'Pizza Hawaiana - Ingredientes: Pina, Jamón, Queso, Mediana, Ensalada, Salsa Picante $10', '150.00', 1, 'Pagado', 3, 1),
(39, '22:12:14', '2025-05-12', 'Pizza Hawaiana - Ingredientes: Pina, Jamón, Queso, Chica, Papas Fritas, Guacamole $10', '150.00', 1, 'Pagado', 3, 1),
(43, '15:43:27', '2025-05-14', '4 comensales | Pizza Hawaiana (2) - sc', '240.00', 7, 'Pagado', 3, 1),
(44, '15:48:23', '2025-05-14', '2 comensales | Hamburguesa BBQ (1) - ww', '150.00', 6, 'Pedido Realizado', 3, 1),
(46, '15:58:49', '2025-05-14', '2 comensales | Hamburguesa BBQ (1) - 22', '150.00', 6, 'Pedido Realizado', 3, 1);

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
-- Estructura de tabla para la tabla `ingresos_egresos`
--

CREATE TABLE `ingresos_egresos` (
  `idMovimiento` int(11) NOT NULL,
  `TipoMovimiento` varchar(20) DEFAULT NULL,
  `Monto` decimal(10,2) DEFAULT NULL,
  `Descripcion` text,
  `Fecha` date DEFAULT NULL,
  `Hora` time DEFAULT NULL
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
(3, 'efe', 232, 12, '3232', '2312', '23', 1),
(4, 'COCA COLA', 324234324132, 20250823, 'REFRESCO QUE LE GUSTA A ELIAS', 'PEPSI COLA', 'PIEZAS', 1),
(5, 'cola', 23, 12032022, 'hola', 'jkjkjlk', '2', 1),
(6, 'cec', 1121, 11111111, 'dss', '33', 'wdawd', 1),
(7, 'wefw', 111.22, 22222222, 'awfafwf', 'qfwfe', 've', 1);

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
(2, 'mewpe', 'asdf', 10, 1),
(3, 'COCA COLA', 'REFRESCO QUE LE GUSTA A ELIAS', 6, 1),
(4, 'cola', 'hola', 1, 1),
(5, 'wefw', 'awfafwf', 22, 1);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `recibos`
--

CREATE TABLE `recibos` (
  `idRecibo` int(11) NOT NULL,
  `Producto` varchar(255) NOT NULL,
  `Total` decimal(10,2) NOT NULL,
  `Fecha` date NOT NULL,
  `Hora` time NOT NULL,
  `Usuario` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Volcado de datos para la tabla `recibos`
--

INSERT INTO `recibos` (`idRecibo`, `Producto`, `Total`, `Fecha`, `Hora`, `Usuario`) VALUES
(1, 'Pizza Hawaiana - Ingredientes: Pina, Jamón, Queso, Mediana, Ensalada, Guacamole', '150.00', '2025-05-13', '11:59:32', 'Invitado'),
(2, 'Pizza Hawaiana - Ingredientes: Pina, Jamón, Queso, Mediana, Ensalada, Guacamole', '150.00', '2025-05-13', '11:59:34', 'Invitado'),
(3, 'Pizza Hawaiana - Ingredientes: Pina, Jamón, Queso, Mediana, Ensalada, Guacamole', '150.00', '2025-05-13', '11:59:34', 'Invitado'),
(4, 'Pizza Hawaiana - Ingredientes: Pina, Jamón, Queso, Mediana, Ensalada, Guacamole', '150.00', '2025-05-13', '11:59:34', 'Invitado'),
(5, 'Pizza Hawaiana - Ingredientes: Pina, Jamón, Queso, Mediana, Ensalada, Guacamole', '150.00', '2025-05-13', '11:59:34', 'Invitado'),
(6, 'Pizza Hawaiana - Ingredientes: Pina, Jamón, Queso, Mediana, Ensalada, Guacamole', '150.00', '2025-05-13', '11:59:34', 'Invitado'),
(7, 'Pizza Hawaiana - Ingredientes: Pina, Jamón, Queso, Mediana, Ensalada, Guacamole', '150.00', '2025-05-13', '11:59:35', 'Invitado'),
(8, 'Pizza Hawaiana - Ingredientes: Pina, Jamón, Queso, Mediana, Ensalada, Guacamole', '150.00', '2025-05-13', '11:59:35', 'Invitado'),
(9, 'Pizza Hawaiana - Ingredientes: Pina, Jamón, Queso, Mediana, Ensalada, Guacamole', '150.00', '2025-05-13', '11:59:35', 'Invitado'),
(10, 'Pizza Hawaiana - Ingredientes: Pina, Jamón, Queso, Mediana, Ensalada, Guacamole', '150.00', '2025-05-13', '11:59:35', 'Invitado'),
(11, 'Pizza Hawaiana - Ingredientes: Pina, Jamón, Queso, Mediana, Ensalada, Guacamole', '150.00', '2025-05-13', '11:59:35', 'Invitado'),
(12, 'Pizza Hawaiana - Ingredientes: Pina, Jamón, Queso, Mediana, Ensalada, Guacamole', '150.00', '2025-05-13', '11:59:36', 'Invitado'),
(13, 'Pizza Hawaiana - Ingredientes: Pina, Jamón, Queso, Mediana, Ensalada, Guacamole', '150.00', '2025-05-13', '11:59:36', 'Invitado'),
(14, 'Pizza Hawaiana - Ingredientes: Pina, Jamón, Queso, Mediana, Ensalada, Guacamole', '150.00', '2025-05-13', '11:59:37', 'Invitado'),
(15, 'Pizza Hawaiana - Ingredientes: Pina, Jamón, Queso, Mediana, Ensalada, Guacamole', '150.00', '2025-05-13', '11:59:37', 'Invitado'),
(16, 'Pizza Hawaiana - Ingredientes: Pina, Jamón, Queso, Mediana, Ensalada, Guacamole', '150.00', '2025-05-13', '11:59:38', 'Invitado'),
(17, 'Pizza Hawaiana - Ingredientes: Pina, Jamón, Queso, Mediana, Ensalada, Guacamole', '150.00', '2025-05-13', '11:59:38', 'Invitado'),
(18, 'Pizza Hawaiana - Ingredientes: Pina, Jamón, Queso, Mediana, Ensalada, Guacamole', '150.00', '2025-05-13', '11:59:38', 'Invitado'),
(19, 'Pizza Hawaiana - Ingredientes: Pina, Jamón, Queso, Mediana, Ensalada, Guacamole', '150.00', '2025-05-13', '11:59:38', 'Invitado'),
(20, 'Pizza Hawaiana - Ingredientes: Pina, Jamón, Queso, Mediana, Ensalada, Guacamole', '150.00', '2025-05-13', '11:59:38', 'Invitado'),
(21, 'Pizza Hawaiana - Ingredientes: Pina, Jamón, Queso, Mediana, Ensalada, Guacamole', '150.00', '2025-05-13', '11:59:38', 'Invitado'),
(22, 'Pizza Hawaiana - Ingredientes: Pina, Jamón, Queso, Mediana, Ensalada, Guacamole', '150.00', '2025-05-13', '11:59:39', 'Invitado'),
(23, 'Pizza Hawaiana - Ingredientes: Pina, Jamón, Queso, Mediana, Ensalada, Guacamole', '150.00', '2025-05-13', '11:59:39', 'Invitado'),
(24, 'Pizza Hawaiana - Ingredientes: Pina, Jamón, Queso, Mediana, Ensalada, Guacamole', '150.00', '2025-05-13', '11:59:39', 'Invitado'),
(25, 'Pizza Hawaiana - Ingredientes: Pina, Jamón, Queso, Mediana, Ensalada, Guacamole', '150.00', '2025-05-13', '11:59:39', 'Invitado'),
(26, 'Hamburguesa BBQ - Ingredientes: Doble Carne, Con Queso, Extra Salsa BBQ, Con Tocino, Sin Lechuga y Jitomate, Con Papas, Chica, Ensalada, Salsa Picante', '180.00', '2025-05-13', '12:02:04', 'Invitado'),
(27, 'Hamburguesa BBQ - Ingredientes: Doble Carne, Con Queso, Extra Salsa BBQ, Con Tocino, Sin Lechuga y Jitomate, Con Papas, Chica, Ensalada, Salsa Picante', '180.00', '2025-05-13', '12:02:05', 'Invitado'),
(28, 'Hamburguesa BBQ - Ingredientes: Doble Carne, Con Queso, Extra Salsa BBQ, Con Tocino, Sin Lechuga y Jitomate, Con Papas, Chica, Ensalada, Salsa Picante', '180.00', '2025-05-13', '12:02:05', 'Invitado'),
(29, 'Pizza Hawaiana - Ingredientes: Pina, Jamón, Queso, Mediana, Ensalada, Salsa Picante', '150.00', '2025-05-13', '12:11:10', 'Invitado'),
(30, 'Pizza Hawaiana - Ingredientes: Pina, Jamón, Queso, Mediana, Ensalada, Salsa Picante', '150.00', '2025-05-13', '12:11:11', 'Invitado'),
(31, 'Pizza Hawaiana - Ingredientes: Pina, Jamón, Queso, Mediana, Ensalada, Salsa Picante', '150.00', '2025-05-13', '12:11:11', 'Invitado'),
(32, 'Pizza Hawaiana - Ingredientes: Pina, Jamón, Queso, Mediana, Ensalada, Salsa Picante', '150.00', '2025-05-13', '12:11:11', 'Invitado'),
(33, 'Pizza Hawaiana - Ingredientes: Pina, Jamón, Queso, Mediana, Ensalada, Salsa Picante', '150.00', '2025-05-13', '12:11:12', 'Invitado'),
(34, 'Pizza Hawaiana - Ingredientes: Pina, Jamón, Queso, Mediana, Ensalada, Salsa Picante', '150.00', '2025-05-13', '12:11:12', 'Invitado'),
(35, 'Pizza Hawaiana - Ingredientes: Pina, Jamón, Queso, Mediana, Ensalada, Salsa Picante', '150.00', '2025-05-13', '12:11:12', 'Invitado'),
(36, 'Pizza Hawaiana - Ingredientes: Pina, Jamón, Queso, Mediana, Ensalada, Salsa Picante', '150.00', '2025-05-13', '12:11:12', 'Invitado'),
(37, 'Pizza Hawaiana - Ingredientes: Pina, Jamón, Queso, Mediana, Ensalada, Salsa Picante', '150.00', '2025-05-13', '12:11:13', 'Invitado'),
(38, 'Pizza Hawaiana - Ingredientes: Pina, Jamón, Queso, Mediana, Ensalada, Salsa Picante', '150.00', '2025-05-13', '12:11:13', 'Invitado'),
(39, 'Pizza Hawaiana - Ingredientes: Pina, Jamón, Queso, Mediana, Ensalada, Salsa Picante', '150.00', '2025-05-13', '12:11:13', 'Invitado'),
(40, 'Pizza Hawaiana - Ingredientes: Pina, Jamón, Queso, Mediana, Ensalada, Salsa Picante', '150.00', '2025-05-13', '12:11:13', 'Invitado'),
(41, 'Pizza Hawaiana - Ingredientes: Pina, Jamón, Queso, Mediana, Ensalada, Salsa Picante', '150.00', '2025-05-13', '12:11:14', 'Invitado'),
(42, 'Pizza Hawaiana - Ingredientes: Pina, Jamón, Queso, Mediana, Ensalada, Salsa Picante', '150.00', '2025-05-13', '12:11:14', 'Invitado'),
(43, 'Pizza Hawaiana - Ingredientes: Pina, Jamón, Queso, Mediana, Ensalada, Salsa Picante', '150.00', '2025-05-13', '12:11:14', 'Invitado'),
(44, 'Pizza Hawaiana - Ingredientes: Pina, Jamón, Queso, Mediana, Ensalada, Salsa Picante', '150.00', '2025-05-13', '12:11:14', 'Invitado'),
(45, 'Pizza Hawaiana - Ingredientes: Pina, Jamón, Queso, Mediana, Ensalada, Salsa Picante', '150.00', '2025-05-13', '12:11:14', 'Invitado'),
(46, 'Pizza Hawaiana - Ingredientes: Pina, Jamón, Queso, Mediana, Ensalada, Salsa Picante', '150.00', '2025-05-13', '12:11:15', 'Invitado'),
(47, 'Pizza Hawaiana - Ingredientes: Pina, Jamón, Queso, Mediana, Ensalada, Salsa Picante', '150.00', '2025-05-13', '12:11:15', 'Invitado'),
(48, 'Pizza Hawaiana - Ingredientes: Pina, Jamón, Queso, Mediana, Ensalada, Salsa Picante', '150.00', '2025-05-13', '12:11:15', 'Invitado'),
(49, 'Pizza Hawaiana - Ingredientes: Pina, Jamón, Queso, Mediana, Ensalada, Salsa Picante', '150.00', '2025-05-13', '12:11:15', 'Invitado'),
(50, 'Pizza Hawaiana - Ingredientes: Pina, Jamón, Queso, Chica, Ensalada, Salsa Picante', '150.00', '2025-05-13', '12:40:58', 'Invitado'),
(51, 'Pizza Hawaiana - Ingredientes: Pina, Jamón, Queso, Chica, Ensalada, Salsa Picante', '150.00', '2025-05-13', '12:41:03', 'Invitado'),
(52, 'Pizza Hawaiana - Ingredientes: Pina, Jamón, Queso, Chica, Ensalada, Salsa Picante', '150.00', '2025-05-13', '12:41:04', 'Invitado'),
(53, 'Pizza Hawaiana - Ingredientes: Pina, Jamón, Queso, Chica, Ensalada, Salsa Picante', '150.00', '2025-05-13', '12:41:04', 'Invitado'),
(54, 'Pizza Hawaiana - Ingredientes: Pina, Jamón, Queso, Chica, Ensalada, Salsa Picante', '150.00', '2025-05-13', '12:41:14', 'Invitado'),
(55, 'Pizza Hawaiana - Ingredientes: Pina, Jamón, Queso, Chica, Ensalada, Salsa Picante', '150.00', '2025-05-13', '12:41:15', 'Invitado'),
(56, 'Pizza Hawaiana - Ingredientes: Pina, Jamón, Queso, Chica, Ensalada, Salsa Picante', '150.00', '2025-05-13', '12:41:16', 'Invitado'),
(57, 'Pizza Hawaiana - Ingredientes: Pina, Jamón, Queso, Mediana, Ensalada, Salsa Picante $10', '150.00', '2025-05-13', '12:41:17', 'Invitado'),
(58, 'Pizza Hawaiana - Ingredientes: Pina, Jamón, Queso, Mediana, Ensalada, Salsa Picante $10', '150.00', '2025-05-13', '12:41:17', 'Invitado'),
(59, 'Pizza Hawaiana - Ingredientes: Pina, Jamón, Queso, Mediana, Ensalada, Salsa Picante $10', '150.00', '2025-05-13', '12:41:17', 'Invitado'),
(60, 'Pizza Hawaiana - Ingredientes: Pina, Jamón, Queso, Chica, Ensalada, Salsa Picante', '150.00', '2025-05-13', '12:41:28', 'Invitado'),
(61, 'Pizza Hawaiana - Ingredientes: Pina, Jamón, Queso, Chica, Ensalada, Salsa Picante', '150.00', '2025-05-13', '12:41:29', 'Invitado'),
(62, 'Pizza Hawaiana - Ingredientes: Pina, Jamón, Queso, Chica, Ensalada, Salsa Picante', '150.00', '2025-05-13', '12:41:29', 'Invitado'),
(63, 'Pizza Hawaiana - Ingredientes: Pina, Jamón, Queso, Chica, Ensalada', '140.00', '2025-05-13', '12:41:29', 'Invitado'),
(64, 'Pizza Hawaiana - Ingredientes: Pina, Jamón, Queso, Chica, Ensalada', '140.00', '2025-05-13', '12:41:30', 'Invitado'),
(65, 'Pizza Hawaiana - Ingredientes: Pina, Jamón, Queso, Chica, Ensalada', '140.00', '2025-05-13', '12:41:30', 'Invitado'),
(66, 'Pizza Hawaiana - Ingredientes: Pina, Jamón, Queso, Mediana, Ensalada, Salsa Picante $10', '150.00', '2025-05-13', '12:41:30', 'Invitado'),
(67, 'Pizza Hawaiana - Ingredientes: Pina, Jamón, Queso, Mediana, Ensalada, Salsa Picante $10', '150.00', '2025-05-13', '12:41:31', 'Invitado'),
(68, 'Pizza Hawaiana - Ingredientes: Pina, Jamón, Queso, Mediana, Ensalada, Salsa Picante $10', '150.00', '2025-05-13', '12:41:31', 'Invitado'),
(69, 'Pizza Hawaiana - Ingredientes: Pina, Jamón, Queso, Mediana, Ensalada, Salsa Picante $10', '150.00', '2025-05-13', '12:41:31', 'Invitado'),
(70, 'Pizza Hawaiana - Ingredientes: Pina, Jamón, Queso, Mediana, Ensalada, Salsa Picante $10', '150.00', '2025-05-13', '12:41:31', 'Invitado'),
(71, 'Pizza Hawaiana - Ingredientes: Pina, Jamón, Queso, Mediana, Ensalada, Salsa Picante $10', '150.00', '2025-05-13', '12:41:32', 'Invitado'),
(72, 'Pizza Hawaiana - Ingredientes: Pina, Jamón, Queso, Chica, Ensalada', '140.00', '2025-05-13', '12:41:32', 'Invitado'),
(73, 'Pizza Hawaiana - Ingredientes: Pina, Jamón, Queso, Chica, Ensalada', '140.00', '2025-05-13', '12:41:33', 'Invitado'),
(74, 'Pizza Hawaiana - Ingredientes: Pina, Jamón, Queso, Chica, Ensalada, Salsa Picante', '150.00', '2025-05-13', '12:41:33', 'Invitado'),
(75, 'Pizza Hawaiana - Ingredientes: Pina, Jamón, Queso, Chica, Ensalada, Salsa Picante', '150.00', '2025-05-13', '12:41:33', 'Invitado'),
(76, 'Pizza Hawaiana - Ingredientes: Pina, Jamón, Queso, Chica, Ensalada, Salsa Picante', '150.00', '2025-05-13', '12:41:33', 'Invitado'),
(77, 'Pizza Hawaiana - Ingredientes: Pina, Jamón, Queso, Chica, Ensalada, Salsa Picante', '150.00', '2025-05-13', '12:41:34', 'Invitado');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `recibospedidos`
--

CREATE TABLE `recibospedidos` (
  `IdRecibosPedidos` int(11) NOT NULL,
  `Producto` varchar(255) NOT NULL,
  `Total` decimal(10,2) NOT NULL,
  `Fecha` date NOT NULL,
  `Hora` time NOT NULL,
  `Usuario` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Volcado de datos para la tabla `recibospedidos`
--

INSERT INTO `recibospedidos` (`IdRecibosPedidos`, `Producto`, `Total`, `Fecha`, `Hora`, `Usuario`) VALUES
(1, 'Pizza Hawaiana - Ingredientes: Pina, Jamón, Queso, Chica, Papas Fritas, Guacamole $10', '150.00', '2025-05-14', '03:04:35', 'Invitado'),
(2, 'Pizza Hawaiana - Ingredientes: Pina, Jamón, Queso, Mediana, Ensalada, Guacamole', '150.00', '2025-05-14', '03:25:36', 'Invitado'),
(3, '4 comensales | Pizza Hawaiana (2) - sc', '240.00', '2025-05-14', '16:14:01', 'Empleado');

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
(2, '2025-04-05', 'ee', '2.0', 1),
(3, '2025-05-06', 'jshjhs', '1.0', 1);

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
  `Contraseña` varchar(79) NOT NULL
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
(14, 'prueba', '123'),
(15, 'lopez', '123'),
(16, 'pedro', '123'),
(17, 'Emikukis', 'Emikukis'),
(18, 'joce', '123'),
(19, 'Xavier2024', 'Xavier12'),
(20, '123', '1234567'),
(21, 'Ian', '5dfaaebff3e8ec0b796b47c7c674652150d92a16837946220d7efea32b8a854d'),
(22, 'admin', '8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918'),
(23, 'mark', 'db55da3fc3098e9c42311c6013304ff36b19ef73d12ea932054b5ad51df4f49d'),
(24, 'pedro222', '36a2c3d76ddd529523197f3cdd8170223b800bfed6f27c56aabbd5092d8c7821');

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
-- Indices de la tabla `ingresos_egresos`
--
ALTER TABLE `ingresos_egresos`
  ADD PRIMARY KEY (`idMovimiento`);

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
-- Indices de la tabla `recibos`
--
ALTER TABLE `recibos`
  ADD PRIMARY KEY (`idRecibo`);

--
-- Indices de la tabla `recibospedidos`
--
ALTER TABLE `recibospedidos`
  ADD PRIMARY KEY (`IdRecibosPedidos`);

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
  MODIFY `IdCliente` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12;

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
  MODIFY `IdEmpleado` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT de la tabla `entradasproductos`
--
ALTER TABLE `entradasproductos`
  MODIFY `IdEntradasProductos` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=21;

--
-- AUTO_INCREMENT de la tabla `estatuspedido`
--
ALTER TABLE `estatuspedido`
  MODIFY `IdEstatusPedido` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT de la tabla `generarpedido`
--
ALTER TABLE `generarpedido`
  MODIFY `IdGenerarPedido` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=47;

--
-- AUTO_INCREMENT de la tabla `ingresos_egresos`
--
ALTER TABLE `ingresos_egresos`
  MODIFY `idMovimiento` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `productos`
--
ALTER TABLE `productos`
  MODIFY `IdProductos` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT de la tabla `productosstock`
--
ALTER TABLE `productosstock`
  MODIFY `IdProductosStock` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT de la tabla `recibos`
--
ALTER TABLE `recibos`
  MODIFY `idRecibo` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=78;

--
-- AUTO_INCREMENT de la tabla `recibospedidos`
--
ALTER TABLE `recibospedidos`
  MODIFY `IdRecibosPedidos` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT de la tabla `salidasproductos`
--
ALTER TABLE `salidasproductos`
  MODIFY `IdSalidasProductos` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT de la tabla `usuario`
--
ALTER TABLE `usuario`
  MODIFY `IdUsuario` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=25;

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
