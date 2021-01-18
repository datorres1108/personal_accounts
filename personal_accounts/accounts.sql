-- phpMyAdmin SQL Dump
-- version 4.7.0
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 07-12-2020 a las 15:51:26
-- Versión del servidor: 10.1.25-MariaDB
-- Versión de PHP: 5.6.31

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `accounts`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `cuenta`
--

CREATE TABLE `cuenta` (
  `id` int(11) NOT NULL,
  `documento` int(11) DEFAULT NULL,
  `nombre` varchar(100) DEFAULT NULL,
  `ingreso` int(11) DEFAULT NULL,
  `estado` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Volcado de datos para la tabla `cuenta`
--

INSERT INTO `cuenta` (`id`, `documento`, `nombre`, `ingreso`, `estado`) VALUES
(6, 71790340, '123312', 3213212, 1),
(8, 13313, 'SDASDAS', 213, 1),
(9, 1232, 'FDSSD', 32, 1),
(10, 32, 'ADSAS', 1232, 1),
(20, 123456789, 'DAVID ALEJANDRO TORRES PEREZ', 2000000, 1);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `egreso_variable`
--

CREATE TABLE `egreso_variable` (
  `id` int(11) NOT NULL,
  `id_cuenta` int(11) NOT NULL,
  `descripcion` varchar(50) NOT NULL,
  `valor` int(11) NOT NULL,
  `fecha` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Volcado de datos para la tabla `egreso_variable`
--

INSERT INTO `egreso_variable` (`id`, `id_cuenta`, `descripcion`, `valor`, `fecha`) VALUES
(5, 20, 'EPM', 320000, '2020-12-10'),
(6, 20, 'PASAJES SEMANA ', 80000, '2020-12-11');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `ingreso_variable`
--

CREATE TABLE `ingreso_variable` (
  `id` int(11) NOT NULL,
  `id_cuenta` int(11) NOT NULL,
  `descripcion` varchar(50) NOT NULL,
  `valor` int(11) NOT NULL,
  `fecha` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Volcado de datos para la tabla `ingreso_variable`
--

INSERT INTO `ingreso_variable` (`id`, `id_cuenta`, `descripcion`, `valor`, `fecha`) VALUES
(25, 20, 'HORAS EXTRAS', 100000, '2020-12-07');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `movi_ingreso`
--

CREATE TABLE `movi_ingreso` (
  `id` int(11) NOT NULL,
  `id_ingresov` int(11) DEFAULT NULL,
  `id_cuenta` int(11) DEFAULT NULL,
  `valor` int(11) NOT NULL,
  `fecha` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `cuenta`
--
ALTER TABLE `cuenta`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `egreso_variable`
--
ALTER TABLE `egreso_variable`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `ingreso_variable`
--
ALTER TABLE `ingreso_variable`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `movi_ingreso`
--
ALTER TABLE `movi_ingreso`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `cuenta`
--
ALTER TABLE `cuenta`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=21;
--
-- AUTO_INCREMENT de la tabla `egreso_variable`
--
ALTER TABLE `egreso_variable`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;
--
-- AUTO_INCREMENT de la tabla `ingreso_variable`
--
ALTER TABLE `ingreso_variable`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=26;
--
-- AUTO_INCREMENT de la tabla `movi_ingreso`
--
ALTER TABLE `movi_ingreso`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
