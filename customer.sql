-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jun 02, 2024 at 03:05 PM
-- Server version: 10.4.28-MariaDB
-- PHP Version: 8.2.4

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `customer`
--

-- --------------------------------------------------------

--
-- Table structure for table `address`
--

CREATE TABLE `address` (
  `customer_id` varchar(36) NOT NULL,
  `address` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `address`
--

INSERT INTO `address` (`customer_id`, `address`) VALUES
('744a831c-60e1-4a87-85ba-59c46200f260', 'Πετρουπόλεως 25'),
('3f9aa7f8-51ad-4a90-aa4f-e8c1c17a2780', 'Εθνικής Αντιστάσεως 23'),
('38ad030b-5f3a-4082-8616-4138ab086c0b', 'Βλιαμου 3'),
('18feb6a3-4b9a-4161-b77e-52da39ef1e19', 'Τριπόλεως 23'),
('76fd4487-f1ca-4b5a-9111-8e2b138131e8', 'Σαμου 5'),
('e2aa8b88-3baf-4a6c-b63c-833d6e6ca10d', 'Προποντίδος 37'),
('1f66094b-1980-48ba-880d-6589a14e81d5', 'Ανθουπώλεως 34');

-- --------------------------------------------------------

--
-- Table structure for table `customer`
--

CREATE TABLE `customer` (
  `id` varchar(36) NOT NULL,
  `entry_date` date DEFAULT NULL,
  `id_number` varchar(50) NOT NULL,
  `first_name` varchar(50) NOT NULL,
  `last_name` varchar(50) NOT NULL,
  `gender` varchar(10) NOT NULL,
  `birth_date` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `customer`
--

INSERT INTO `customer` (`id`, `entry_date`, `id_number`, `first_name`, `last_name`, `gender`, `birth_date`) VALUES
('18feb6a3-4b9a-4161-b77e-52da39ef1e19', '2024-06-02', 'AT123452', 'Μάρκος', 'Μπότσαρης', 'Male', '2004-01-01'),
('1f66094b-1980-48ba-880d-6589a14e81d5', '2024-06-02', 'ΑΚ123457', 'Μάρκος', 'Μαρκου', 'Male', '1995-02-03'),
('38ad030b-5f3a-4082-8616-4138ab086c0b', '2024-06-02', 'ΑΣ121232', 'Ιωάννα', 'Αυγενάκη', 'Female', '1999-02-03'),
('3f9aa7f8-51ad-4a90-aa4f-e8c1c17a2780', '2024-06-01', 'ΑΣ121212', 'Παναγιώτα ', 'Νικολοπούλου', 'Female', '1994-02-06'),
('744a831c-60e1-4a87-85ba-59c46200f260', '2024-06-01', 'AE123456', 'Μαριος', 'Αρσενιου', 'Male', '2001-02-23'),
('76fd4487-f1ca-4b5a-9111-8e2b138131e8', '2024-06-02', 'ΑΒ123456', 'Μαρια', 'Μαρκου', 'Female', '1998-02-03'),
('b75f3dcb-057e-48f1-b0e5-19cc63e7a37a', '2024-06-02', 'AT123459', 'Παρασκευάς', 'Γιαννακόπουλος', 'Male', '2002-06-27'),
('e2aa8b88-3baf-4a6c-b63c-833d6e6ca10d', '2024-06-02', 'AK234567', 'Αρσένης ', 'Γεωργίου', 'Male', '1990-02-03');

-- --------------------------------------------------------

--
-- Table structure for table `phone_number`
--

CREATE TABLE `phone_number` (
  `customer_id` varchar(36) NOT NULL,
  `phone_number` varchar(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `phone_number`
--

INSERT INTO `phone_number` (`customer_id`, `phone_number`) VALUES
('744a831c-60e1-4a87-85ba-59c46200f260', '1223345678'),
('3f9aa7f8-51ad-4a90-aa4f-e8c1c17a2780', '1111111111'),
('38ad030b-5f3a-4082-8616-4138ab086c0b', '3333333333'),
('18feb6a3-4b9a-4161-b77e-52da39ef1e19', '0987654321'),
('76fd4487-f1ca-4b5a-9111-8e2b138131e8', '5555555555'),
('e2aa8b88-3baf-4a6c-b63c-833d6e6ca10d', '4664646263'),
('1f66094b-1980-48ba-880d-6589a14e81d5', '2222222223');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `address`
--
ALTER TABLE `address`
  ADD KEY `customer_id` (`customer_id`);

--
-- Indexes for table `customer`
--
ALTER TABLE `customer`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `id_number` (`id_number`);

--
-- Indexes for table `phone_number`
--
ALTER TABLE `phone_number`
  ADD KEY `customer_id` (`customer_id`);

--
-- Constraints for dumped tables
--

--
-- Constraints for table `address`
--
ALTER TABLE `address`
  ADD CONSTRAINT `address_ibfk_1` FOREIGN KEY (`customer_id`) REFERENCES `customer` (`id`);

--
-- Constraints for table `phone_number`
--
ALTER TABLE `phone_number`
  ADD CONSTRAINT `phone_number_ibfk_1` FOREIGN KEY (`customer_id`) REFERENCES `customer` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
