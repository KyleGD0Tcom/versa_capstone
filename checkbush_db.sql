-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Sep 05, 2025 at 05:35 AM
-- Server version: 11.7.2-MariaDB
-- PHP Version: 8.0.30

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `checkbush_db`
--

-- --------------------------------------------------------

--
-- Table structure for table `adminpanel_inventoryitem`
--

CREATE TABLE `adminpanel_inventoryitem` (
  `id` bigint(20) NOT NULL,
  `item_code` varchar(100) NOT NULL,
  `category` varchar(50) NOT NULL,
  `unit_item` varchar(255) NOT NULL,
  `details` longtext NOT NULL,
  `supplier` varchar(255) NOT NULL,
  `quantity` int(10) UNSIGNED NOT NULL CHECK (`quantity` >= 0),
  `date_received` date NOT NULL,
  `photo` varchar(100) DEFAULT NULL,
  `serial_number` varchar(50) DEFAULT NULL,
  `department` varchar(50) NOT NULL,
  `unit_price` decimal(10,2) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `adminpanel_inventoryitem`
--

INSERT INTO `adminpanel_inventoryitem` (`id`, `item_code`, `category`, `unit_item`, `details`, `supplier`, `quantity`, `date_received`, `photo`, `serial_number`, `department`, `unit_price`) VALUES
(53, 'HVY-067285', 'Heavy Equipment', 'Excavator Long Arm', 'Long arm models for water projects, ports, and dredging.', 'XCMG', 45, '2025-05-31', 'inventory_photos/Long_arm_a65RJZT.png', '0023341323', 'Sales', 3400000.00),
(54, 'HVY-434208', 'Heavy Equipment', 'Bulldozer', '12 power grades (80–520 HP). For wetland, desert, plateau, forestry, coal, and sanitation work.', 'Shantui', 23, '2025-05-30', 'inventory_photos/Bulldozer_hTdIjBI.png', '0011244331', 'Sales', 4300000.00),
(55, 'HVY-017740', 'Heavy Equipment', 'Concrete Mixer', 'Use 4D tech for efficient, reliable mixing.', 'Xugong Shi Weiying', 54, '2025-05-31', 'inventory_photos/mixer_p0gbkaw.png', '77523409123', 'Sales', 4500000.00),
(56, 'HVY-977770', 'Heavy Equipment', 'Concrete Spraying Machine', 'Walks, pumps, and sprays fiber concrete with low rebound and high quality.', 'Xugong Shi Weiying', 41, '2025-05-31', 'inventory_photos/Concrete_spray_machine.png', '00112234346', 'Sales', 3500000.00),
(57, 'HVY-479885', 'Heavy Equipment', 'Single Drum Roller', 'XCMG vibratory roller: heavy-duty compaction for soil and rock on major construction sites.', 'XCMG', 38, '2025-05-31', 'inventory_photos/drum_roller.png', '002399823', 'Sales', 3700000.00),
(58, 'HVY-973583', 'Heavy Equipment', 'Motor Grader', 'XCMG motor grader uses energy-saving tech to cut costs, with a comfy cab and easy operation.', 'XCMG', 48, '2025-05-31', 'inventory_photos/motor_grader.png', '009984323', 'Sales', 4700000.00),
(59, 'SP-417467', 'Spare Parts', 'Hyraulic Pumps', 'Power fluid flow for machine movement.', 'XCMG', 54, '2025-05-31', 'inventory_photos/hydraulic_pumps.png', '001693463', 'Warehouse', 1300000.00),
(61, 'SP-059645', 'Spare Parts', 'Oil Filters', 'Cleans engine oil to protect engine parts.', 'XCMG', 34, '2025-05-31', 'inventory_photos/oil_filter.png', '0093572323', 'Warehouse', 23000.00),
(62, 'SP-674352', 'Spare Parts', 'Track Chains', 'Support and drive crawler machines.', 'XCMG', 39, '2025-05-31', 'inventory_photos/trach_chains_ir3zgbq.png', '00553312341', 'Warehouse', 20000.00),
(63, 'SP-684264', 'Spare Parts', 'Bucket teeth', 'Tough tips for digging and scooping.', 'XCMG', 45, '2025-05-31', 'inventory_photos/bucket_teeth.png', '8802350034', 'Warehouse', 16000.00),
(64, 'SP-544230', 'Spare Parts', 'Control valves', 'Direct hydraulic fluid to machine parts.', 'XCMG', 41, '2025-05-31', 'inventory_photos/control_valves.png', '012383421', 'Warehouse', 25000.00),
(65, 'SP-282237', 'Spare Parts', 'Radiators', 'Cool the engine to prevent overheating.', 'XCMG', 60, '2025-05-31', 'inventory_photos/radiators.png', '783230023', 'Warehouse', 25000.00),
(66, 'HVY-304288', 'Heavy Equipment', 'Excavator CJ7', 'asdhcsjkfghsdhjfgsdjhfsdgfhjsdgfhjsdgf', 'SHACMAN', 15, '2025-05-31', 'inventory_photos/Screenshot_2025-02-06_230040_3MUNJcl.png', '013435892', 'Sales', 4300000.00);

-- --------------------------------------------------------

--
-- Table structure for table `adminpanel_userprofile`
--

CREATE TABLE `adminpanel_userprofile` (
  `id` bigint(20) NOT NULL,
  `gender` varchar(20) DEFAULT NULL,
  `dob` date DEFAULT NULL,
  `mobile_number` varchar(20) DEFAULT NULL,
  `department` varchar(100) DEFAULT NULL,
  `role` varchar(100) DEFAULT NULL,
  `work_shift` varchar(100) DEFAULT NULL,
  `status` varchar(20) DEFAULT NULL,
  `employee_type` varchar(50) DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  `plain_password` varchar(255) DEFAULT NULL,
  `date_of_joining` datetime(6) NOT NULL,
  `profile_picture` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `adminpanel_userprofile`
--

INSERT INTO `adminpanel_userprofile` (`id`, `gender`, `dob`, `mobile_number`, `department`, `role`, `work_shift`, `status`, `employee_type`, `user_id`, `plain_password`, `date_of_joining`, `profile_picture`) VALUES
(45, 'Male', '2025-09-16', '09368872989', 'Sales', 'Manager', '09:00 AM - 05:00 PM', 'Full-time', 'Permanent', 2, 'jinyiadmin123', '2025-09-03 02:48:40.684603', 'profile_pictures/wp9139425-purple-neon-lights-4k-wallpapers.jpg'),
(46, 'Male', '2025-09-14', '09368872989', 'Warehouse', 'Manager', '08:00 AM - 04:00 PM', 'Full-time', 'Permanent', 3, 'jinyiadmin123', '2025-09-03 02:52:35.120373', 'profile_pictures/asdasdasd.jpg'),
(47, 'Male', '2025-09-06', '09368287298', 'Motorpool', 'Manager', '10:00 AM - 06:00 PM', 'Full-time', 'Permanent', 4, 'jinyiadmin123', '2025-09-03 02:55:30.441532', 'profile_pictures/wp6022640-aesthetics-1920x1080-wallpapers.jpg'),
(48, 'Male', '2025-10-03', '09368287298', 'Delivery', 'Manager', '08:00 AM - 04:00 PM', 'Full-time', 'Permanent', 5, 'jinyiadmin123', '2025-09-03 02:58:36.396734', 'profile_pictures/star.png'),
(50, 'Male', '2025-09-28', '09368872989', 'Aftersales', 'Manager', '09:00 AM - 05:00 PM', 'Full-time', 'Permanent', 6, 'jinyiadmin123', '2025-09-03 03:02:49.816444', 'profile_pictures/circle-48.png');

-- --------------------------------------------------------

--
-- Table structure for table `adminpanel_usersettings`
--

CREATE TABLE `adminpanel_usersettings` (
  `id` bigint(20) NOT NULL,
  `timezone` varchar(50) NOT NULL,
  `date_format` varchar(20) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `user_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `adminpanel_usersettings`
--

INSERT INTO `adminpanel_usersettings` (`id`, `timezone`, `date_format`, `created_at`, `updated_at`, `user_id`) VALUES
(1, 'UTC+08:00', 'MM/DD/YYYY', '2025-08-21 04:19:25.378698', '2025-08-24 04:16:39.664520', 1),
(7, 'UTC+08:00', 'MM/DD/YYYY', '2025-09-03 02:49:06.637239', '2025-09-03 02:49:06.637252', 2),
(8, 'UTC+08:00', 'MM/DD/YYYY', '2025-09-03 02:53:10.475370', '2025-09-03 02:53:10.475388', 3),
(9, 'UTC+08:00', 'MM/DD/YYYY', '2025-09-03 02:56:10.907700', '2025-09-03 02:56:10.907715', 4),
(10, 'UTC+08:00', 'MM/DD/YYYY', '2025-09-03 02:59:02.971308', '2025-09-03 02:59:02.971321', 5),
(11, 'UTC+08:00', 'MM/DD/YYYY', '2025-09-03 03:03:02.960403', '2025-09-03 03:03:02.960420', 6);

-- --------------------------------------------------------

--
-- Table structure for table `aftersales_maintenancerecord`
--

CREATE TABLE `aftersales_maintenancerecord` (
  `maintenance_id` varchar(20) NOT NULL,
  `service_id` varchar(20) NOT NULL,
  `unit_name` varchar(100) NOT NULL,
  `serial_number` varchar(50) NOT NULL,
  `client_name` varchar(100) NOT NULL,
  `status` varchar(20) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `diagnosis` longtext DEFAULT NULL,
  `findings_note` longtext DEFAULT NULL,
  `reported_problem` longtext DEFAULT NULL,
  `work_performed` longtext DEFAULT NULL,
  `service_record_id` bigint(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `aftersales_maintenancerecord_technicians`
--

CREATE TABLE `aftersales_maintenancerecord_technicians` (
  `id` bigint(20) NOT NULL,
  `maintenancerecord_id` varchar(20) NOT NULL,
  `technician_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `aftersales_servicerecord`
--

CREATE TABLE `aftersales_servicerecord` (
  `id` bigint(20) NOT NULL,
  `service_id` varchar(20) NOT NULL,
  `unit_name` varchar(255) NOT NULL,
  `serial_number` varchar(100) NOT NULL,
  `client_name` varchar(255) NOT NULL,
  `warranty_start` date NOT NULL,
  `warranty_end` date NOT NULL,
  `status` varchar(20) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `delivery_schedule_id` bigint(20) DEFAULT NULL,
  `invoice_id` bigint(20) DEFAULT NULL,
  `sales_order_id` bigint(20) DEFAULT NULL,
  `usage_unit` varchar(10) NOT NULL,
  `usage_value` decimal(10,2) NOT NULL,
  `warranty_type` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `aftersales_servicerecord`
--

INSERT INTO `aftersales_servicerecord` (`id`, `service_id`, `unit_name`, `serial_number`, `client_name`, `warranty_start`, `warranty_end`, `status`, `created_at`, `updated_at`, `delivery_schedule_id`, `invoice_id`, `sales_order_id`, `usage_unit`, `usage_value`, `warranty_type`) VALUES
(38, 'AS-25-0001', 'Excavator Long Arm', '0023341323', 'lowe', '2025-09-27', '2026-09-27', 'Warranty Active', '2025-09-03 08:21:00.047105', '2025-09-03 08:21:00.047117', 86, 119, 132, 'hrs', 0.00, 'Heavy Equipment');

-- --------------------------------------------------------

--
-- Table structure for table `aftersales_technician`
--

CREATE TABLE `aftersales_technician` (
  `id` bigint(20) NOT NULL,
  `name` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `auth_group`
--

CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL,
  `name` varchar(150) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `auth_group`
--

INSERT INTO `auth_group` (`id`, `name`) VALUES
(7, 'Accounts'),
(1, 'Admin'),
(6, 'Aftersales'),
(4, 'Delivery'),
(5, 'Motorpool'),
(2, 'Sales'),
(3, 'Warehouse');

-- --------------------------------------------------------

--
-- Table structure for table `auth_group_permissions`
--

CREATE TABLE `auth_group_permissions` (
  `id` bigint(20) NOT NULL,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `auth_permission`
--

CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `auth_permission`
--

INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES
(1, 'Can add log entry', 1, 'add_logentry'),
(2, 'Can change log entry', 1, 'change_logentry'),
(3, 'Can delete log entry', 1, 'delete_logentry'),
(4, 'Can view log entry', 1, 'view_logentry'),
(5, 'Can add permission', 2, 'add_permission'),
(6, 'Can change permission', 2, 'change_permission'),
(7, 'Can delete permission', 2, 'delete_permission'),
(8, 'Can view permission', 2, 'view_permission'),
(9, 'Can add group', 3, 'add_group'),
(10, 'Can change group', 3, 'change_group'),
(11, 'Can delete group', 3, 'delete_group'),
(12, 'Can view group', 3, 'view_group'),
(13, 'Can add user', 4, 'add_user'),
(14, 'Can change user', 4, 'change_user'),
(15, 'Can delete user', 4, 'delete_user'),
(16, 'Can view user', 4, 'view_user'),
(17, 'Can add content type', 5, 'add_contenttype'),
(18, 'Can change content type', 5, 'change_contenttype'),
(19, 'Can delete content type', 5, 'delete_contenttype'),
(20, 'Can view content type', 5, 'view_contenttype'),
(21, 'Can add session', 6, 'add_session'),
(22, 'Can change session', 6, 'change_session'),
(23, 'Can delete session', 6, 'delete_session'),
(24, 'Can view session', 6, 'view_session'),
(25, 'Can add user', 7, 'add_user'),
(26, 'Can change user', 7, 'change_user'),
(27, 'Can delete user', 7, 'delete_user'),
(28, 'Can view user', 7, 'view_user'),
(29, 'Can add user profile', 8, 'add_userprofile'),
(30, 'Can change user profile', 8, 'change_userprofile'),
(31, 'Can delete user profile', 8, 'delete_userprofile'),
(32, 'Can view user profile', 8, 'view_userprofile'),
(33, 'Can add inventory item', 9, 'add_inventoryitem'),
(34, 'Can change inventory item', 9, 'change_inventoryitem'),
(35, 'Can delete inventory item', 9, 'delete_inventoryitem'),
(36, 'Can view inventory item', 9, 'view_inventoryitem'),
(37, 'Can add Global Settings', 10, 'add_globalsettings'),
(38, 'Can change Global Settings', 10, 'change_globalsettings'),
(39, 'Can delete Global Settings', 10, 'delete_globalsettings'),
(40, 'Can view Global Settings', 10, 'view_globalsettings'),
(41, 'Can add notification', 11, 'add_notification'),
(42, 'Can change notification', 11, 'change_notification'),
(43, 'Can delete notification', 11, 'delete_notification'),
(44, 'Can view notification', 11, 'view_notification'),
(45, 'Can add order item', 12, 'add_orderitem'),
(46, 'Can change order item', 12, 'change_orderitem'),
(47, 'Can delete order item', 12, 'delete_orderitem'),
(48, 'Can view order item', 12, 'view_orderitem'),
(49, 'Can add sales order', 13, 'add_salesorder'),
(50, 'Can change sales order', 13, 'change_salesorder'),
(51, 'Can delete sales order', 13, 'delete_salesorder'),
(52, 'Can view sales order', 13, 'view_salesorder'),
(53, 'Can add invoice', 14, 'add_invoice'),
(54, 'Can change invoice', 14, 'change_invoice'),
(55, 'Can delete invoice', 14, 'delete_invoice'),
(56, 'Can view invoice', 14, 'view_invoice'),
(57, 'Can add request', 15, 'add_request'),
(58, 'Can change request', 15, 'change_request'),
(59, 'Can delete request', 15, 'delete_request'),
(60, 'Can view request', 15, 'view_request'),
(61, 'Can add request note', 16, 'add_requestnote'),
(62, 'Can change request note', 16, 'change_requestnote'),
(63, 'Can delete request note', 16, 'delete_requestnote'),
(64, 'Can view request note', 16, 'view_requestnote'),
(65, 'Can add inspection', 17, 'add_inspection'),
(66, 'Can change inspection', 17, 'change_inspection'),
(67, 'Can delete inspection', 17, 'delete_inspection'),
(68, 'Can view inspection', 17, 'view_inspection'),
(69, 'Can add equipment inspection', 18, 'add_equipmentinspection'),
(70, 'Can change equipment inspection', 18, 'change_equipmentinspection'),
(71, 'Can delete equipment inspection', 18, 'delete_equipmentinspection'),
(72, 'Can view equipment inspection', 18, 'view_equipmentinspection'),
(73, 'Can add delivery request', 19, 'add_deliveryrequest'),
(74, 'Can change delivery request', 19, 'change_deliveryrequest'),
(75, 'Can delete delivery request', 19, 'delete_deliveryrequest'),
(76, 'Can view delivery request', 19, 'view_deliveryrequest'),
(77, 'Can add delivery schedule', 20, 'add_deliveryschedule'),
(78, 'Can change delivery schedule', 20, 'change_deliveryschedule'),
(79, 'Can delete delivery schedule', 20, 'delete_deliveryschedule'),
(80, 'Can view delivery schedule', 20, 'view_deliveryschedule'),
(81, 'Can add client record', 21, 'add_clientrecord'),
(82, 'Can change client record', 21, 'change_clientrecord'),
(83, 'Can delete client record', 21, 'delete_clientrecord'),
(84, 'Can view client record', 21, 'view_clientrecord'),
(85, 'Can add service record', 22, 'add_servicerecord'),
(86, 'Can change service record', 22, 'change_servicerecord'),
(87, 'Can delete service record', 22, 'delete_servicerecord'),
(88, 'Can view service record', 22, 'view_servicerecord'),
(89, 'Can add maintenance record', 23, 'add_maintenancerecord'),
(90, 'Can change maintenance record', 23, 'change_maintenancerecord'),
(91, 'Can delete maintenance record', 23, 'delete_maintenancerecord'),
(92, 'Can view maintenance record', 23, 'view_maintenancerecord'),
(93, 'Can add technician', 24, 'add_technician'),
(94, 'Can change technician', 24, 'change_technician'),
(95, 'Can delete technician', 24, 'delete_technician'),
(96, 'Can view technician', 24, 'view_technician'),
(97, 'Can add warehouse order', 25, 'add_warehouseorder'),
(98, 'Can change warehouse order', 25, 'change_warehouseorder'),
(99, 'Can delete warehouse order', 25, 'delete_warehouseorder'),
(100, 'Can view warehouse order', 25, 'view_warehouseorder'),
(101, 'Can add warehouse order item', 26, 'add_warehouseorderitem'),
(102, 'Can change warehouse order item', 26, 'change_warehouseorderitem'),
(103, 'Can delete warehouse order item', 26, 'delete_warehouseorderitem'),
(104, 'Can view warehouse order item', 26, 'view_warehouseorderitem'),
(105, 'Can add warehouse invoice', 27, 'add_warehouseinvoice'),
(106, 'Can change warehouse invoice', 27, 'change_warehouseinvoice'),
(107, 'Can delete warehouse invoice', 27, 'delete_warehouseinvoice'),
(108, 'Can view warehouse invoice', 27, 'view_warehouseinvoice'),
(109, 'Can add warehouse client record', 28, 'add_warehouseclientrecord'),
(110, 'Can change warehouse client record', 28, 'change_warehouseclientrecord'),
(111, 'Can delete warehouse client record', 28, 'delete_warehouseclientrecord'),
(112, 'Can view warehouse client record', 28, 'view_warehouseclientrecord'),
(113, 'Can add notification', 29, 'add_notification'),
(114, 'Can change notification', 29, 'change_notification'),
(115, 'Can delete notification', 29, 'delete_notification'),
(116, 'Can view notification', 29, 'view_notification'),
(117, 'Can add user settings', 30, 'add_usersettings'),
(118, 'Can change user settings', 30, 'change_usersettings'),
(119, 'Can delete user settings', 30, 'delete_usersettings'),
(120, 'Can view user settings', 30, 'view_usersettings');

-- --------------------------------------------------------

--
-- Table structure for table `auth_user`
--

CREATE TABLE `auth_user` (
  `id` int(11) NOT NULL,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `auth_user`
--

INSERT INTO `auth_user` (`id`, `password`, `last_login`, `is_superuser`, `username`, `first_name`, `last_name`, `email`, `is_staff`, `is_active`, `date_joined`) VALUES
(1, 'pbkdf2_sha256$1000000$o9vV523rnEW2vprTHuEKBN$Cvsu+XXbUTYauRgNgeDu7n2mDDb/s7EcFHtNQAklEjM=', '2025-09-03 08:32:18.320481', 1, 'admin', 'Christian', 'Jude', 'admin@administrator.com', 1, 1, '2025-04-17 15:58:51.000000'),
(2, 'pbkdf2_sha256$1000000$gVLuqX4sOPGcYNDYk8WteO$OTXTpv1IB47BdWVQP2KFi3KHblQDAfhr8/Q6NzdbGFk=', '2025-09-03 08:17:26.981744', 0, 'salesadmin@1', 'Christian', 'Jude', 'christianjude@gmail.com', 0, 1, '2025-09-03 02:48:40.300845'),
(3, 'pbkdf2_sha256$1000000$nWTxNXSK77kwwNgcn8mtbY$LSBTny3uT+n/LMNFcpBVyFEM2zfV7IXEcUH717mxXmM=', '2025-09-03 03:22:14.000098', 0, 'warehouseadmin@1', 'Kyle james', 'ar', 'kyle123123@gmail.com', 0, 1, '2025-09-03 02:52:34.741329'),
(4, 'pbkdf2_sha256$1000000$d8BWiXEk2ryJ8h0XJ7Kq4B$w7B8UQXYz13fmbZ6AqvZLVrKQXQf3EQ9Kviqtq1t51c=', '2025-09-03 07:45:57.394304', 0, 'motorpooladmin@1', 'jear', 'ar', 'jear@gmail.com', 0, 1, '2025-09-03 02:55:30.022609'),
(5, 'pbkdf2_sha256$1000000$vRbUQ2u1n6aVilttN2Or8w$uk+3SIS++ILuwusmsWXXQteKZd8H2cdaAfRMae9bark=', '2025-09-03 07:54:23.694705', 0, 'deliveryadmin@1', 'Hubert', 'Debalucos', 'Hubert@gmail.com', 0, 1, '2025-09-03 02:58:36.011153'),
(6, 'pbkdf2_sha256$1000000$n9lkQtoHLJONAIhiKgFbCC$kM8KqbySK5x6nTXfksT8TkQ6SBVtrAjfI/za6WLW5JU=', '2025-09-03 08:05:39.253768', 0, 'aftersalesadmin@1', 'benny', 'qt', 'benny1212@gmail.com', 0, 1, '2025-09-03 03:02:49.439973');

-- --------------------------------------------------------

--
-- Table structure for table `auth_user_groups`
--

CREATE TABLE `auth_user_groups` (
  `id` bigint(20) NOT NULL,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `auth_user_groups`
--

INSERT INTO `auth_user_groups` (`id`, `user_id`, `group_id`) VALUES
(11, 1, 1),
(89, 2, 2),
(90, 3, 3),
(91, 4, 5),
(92, 5, 4),
(94, 6, 6);

-- --------------------------------------------------------

--
-- Table structure for table `auth_user_user_permissions`
--

CREATE TABLE `auth_user_user_permissions` (
  `id` bigint(20) NOT NULL,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `delivery_deliveryrequest`
--

CREATE TABLE `delivery_deliveryrequest` (
  `id` bigint(20) NOT NULL,
  `request_id` varchar(20) NOT NULL,
  `pdi_request_id` varchar(50) NOT NULL,
  `invoice_number` varchar(50) NOT NULL,
  `unit_info` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL CHECK (json_valid(`unit_info`)),
  `client_info` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL CHECK (json_valid(`client_info`)),
  `status` varchar(20) NOT NULL,
  `created_at` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `delivery_deliveryrequest`
--

INSERT INTO `delivery_deliveryrequest` (`id`, `request_id`, `pdi_request_id`, `invoice_number`, `unit_info`, `client_info`, `status`, `created_at`) VALUES
(163, 'DVR-2025-0001', 'RQ-20250903-0001', 'INV-25-0001', '{\"unit_name\": \"Excavator Long Arm\", \"serial_number\": \"0023341323\"}', '{\"client_name\": \"lowe\", \"client_address\": \"lasang \", \"client_contact\": \"09368872989\", \"client_email\": \"lowe@gmail.com\", \"company_name\": \"jinyi\", \"company_address\": \"lasang\", \"company_contact\": \"09972474711\", \"company_email\": \"jinyi@gmail.com\"}', 'Completed', '2025-09-03 08:00:20.332415');

-- --------------------------------------------------------

--
-- Table structure for table `delivery_deliveryschedule`
--

CREATE TABLE `delivery_deliveryschedule` (
  `id` bigint(20) NOT NULL,
  `schedule_id` varchar(20) NOT NULL,
  `assigned_driver` varchar(100) NOT NULL,
  `delivery_date` date NOT NULL,
  `delivery_instructions` longtext DEFAULT NULL,
  `status` varchar(20) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `delivery_request_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `delivery_deliveryschedule`
--

INSERT INTO `delivery_deliveryschedule` (`id`, `schedule_id`, `assigned_driver`, `delivery_date`, `delivery_instructions`, `status`, `created_at`, `updated_at`, `delivery_request_id`) VALUES
(86, 'DVS-2025-0001', 'loweeee', '2025-09-27', 'asdasdasdasdas', 'Delivered', '2025-09-03 08:00:40.736700', '2025-09-03 08:21:00.039542', 163);

-- --------------------------------------------------------

--
-- Table structure for table `django_admin_log`
--

CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext DEFAULT NULL,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) UNSIGNED NOT NULL CHECK (`action_flag` >= 0),
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `django_admin_log`
--

INSERT INTO `django_admin_log` (`id`, `action_time`, `object_id`, `object_repr`, `action_flag`, `change_message`, `content_type_id`, `user_id`) VALUES
(1, '2025-04-17 16:00:20.581758', '1', 'Admin', 1, '[{\"added\": {}}]', 3, 1),
(2, '2025-04-17 16:00:23.879831', '2', 'Sales', 1, '[{\"added\": {}}]', 3, 1),
(3, '2025-04-17 16:00:28.346377', '3', 'Warehouse', 1, '[{\"added\": {}}]', 3, 1),
(4, '2025-04-17 16:00:32.545724', '4', 'Delivery', 1, '[{\"added\": {}}]', 3, 1),
(5, '2025-04-17 16:00:36.872793', '5', 'Motorpool', 1, '[{\"added\": {}}]', 3, 1),
(6, '2025-04-17 16:00:41.141457', '6', 'Aftersales', 1, '[{\"added\": {}}]', 3, 1),
(7, '2025-04-17 16:00:45.439781', '7', 'Accounts', 1, '[{\"added\": {}}]', 3, 1),
(8, '2025-04-17 16:01:10.597334', '2', 'salesadmin@1', 1, '[{\"added\": {}}]', 4, 1),
(9, '2025-04-17 16:01:19.525356', '2', 'salesadmin@1', 2, '[{\"changed\": {\"fields\": [\"First name\", \"Last name\", \"Email address\", \"Groups\"]}}]', 4, 1),
(10, '2025-04-19 03:28:46.300977', '1', 'admin', 2, '[{\"changed\": {\"fields\": [\"Groups\"]}}]', 4, 1),
(11, '2025-04-19 03:29:41.568863', '1', 'admin', 2, '[]', 4, 1),
(12, '2025-04-19 03:31:26.158683', '3', 'admin@1', 1, '[{\"added\": {}}]', 4, 1),
(13, '2025-04-19 03:31:30.051315', '3', 'admin@1', 2, '[{\"changed\": {\"fields\": [\"Groups\"]}}]', 4, 1),
(14, '2025-04-19 03:33:13.030683', '4', 'deliveryadmin@1', 1, '[{\"added\": {}}]', 4, 1),
(15, '2025-04-19 03:33:19.178303', '4', 'deliveryadmin@1', 2, '[{\"changed\": {\"fields\": [\"Groups\"]}}]', 4, 1),
(16, '2025-04-19 03:41:09.645122', '3', 'admin@1', 2, '[]', 4, 1),
(17, '2025-04-19 03:42:08.937958', '1', 'admin', 2, '[{\"changed\": {\"fields\": [\"Groups\"]}}]', 4, 1),
(18, '2025-04-19 03:43:00.662293', '5', 'kurapika@1', 1, '[{\"added\": {}}]', 4, 1),
(19, '2025-04-19 03:43:04.662218', '5', 'kurapika@1', 2, '[{\"changed\": {\"fields\": [\"Groups\"]}}]', 4, 1),
(20, '2025-04-26 07:49:29.059269', '3', 'admin@1', 3, '', 4, 1),
(21, '2025-04-26 07:52:20.217534', '12', 'jear@1', 2, '[{\"changed\": {\"fields\": [\"Groups\"]}}]', 4, 1),
(22, '2025-04-26 08:11:03.399756', '5', 'kurapika@1', 3, '', 4, 1),
(23, '2025-04-26 08:11:10.440475', '4', 'deliveryadmin@1', 3, '', 4, 1),
(24, '2025-04-26 08:11:17.832955', '7', 'jobet@123', 3, '', 4, 1),
(25, '2025-04-26 08:11:21.623811', '14', 'alyssa@1', 2, '[]', 4, 1),
(26, '2025-04-26 08:11:31.678745', '2', 'salesadmin@1', 2, '[]', 4, 1),
(27, '2025-04-26 08:11:40.643727', '6', 'jobet@1', 2, '[]', 4, 1),
(28, '2025-04-26 08:12:49.773139', '1', 'admin', 2, '[{\"changed\": {\"fields\": [\"First name\", \"Last name\", \"Groups\"]}}]', 4, 1),
(29, '2025-04-26 08:13:07.594207', '10', 'arar@1', 3, '', 4, 1),
(30, '2025-04-26 08:13:23.611410', '6', 'jobet@1', 3, '', 4, 1),
(31, '2025-04-26 08:13:35.650763', '2', 'salesadmin@1', 3, '', 4, 1),
(32, '2025-04-26 08:13:54.463102', '1', 'admin', 2, '[{\"changed\": {\"fields\": [\"Groups\"]}}]', 4, 1),
(33, '2025-04-26 08:14:08.476473', '1', 'admin', 2, '[{\"changed\": {\"fields\": [\"Groups\"]}}]', 4, 1),
(34, '2025-04-26 08:17:12.285170', '14', 'alyssa@1', 3, '', 4, 1),
(35, '2025-04-26 08:17:15.963993', '13', 'ambot@1', 3, '', 4, 1),
(36, '2025-04-26 08:17:18.964466', '12', 'jear@1', 3, '', 4, 1),
(37, '2025-04-26 08:17:31.668215', '1', 'admin', 2, '[]', 4, 1),
(38, '2025-04-26 10:07:36.846579', '15', 'salesadmin@1', 3, '', 4, 1),
(39, '2025-04-26 10:16:07.979729', '16', 'jear@1', 3, '', 4, 1),
(40, '2025-04-26 10:36:16.526514', '17', 'Kyle@1', 3, '', 4, 1),
(41, '2025-04-26 12:03:20.629900', '18', 'jear@1', 3, '', 4, 1),
(42, '2025-04-26 12:15:57.768132', '19', 'jane@1', 3, '', 4, 1),
(43, '2025-04-26 12:22:27.573050', '20', 'sahur@1', 3, '', 4, 1),
(44, '2025-04-26 13:45:07.669077', '3', 'aufder@1', 3, '', 4, 1),
(45, '2025-04-26 13:45:12.810195', '5', 'bombordilo@1', 3, '', 4, 1),
(46, '2025-04-26 13:45:16.026970', '4', 'jear@1', 3, '', 4, 1),
(47, '2025-04-26 13:45:19.690716', '6', 'kurapika@1', 3, '', 4, 1),
(48, '2025-04-26 13:45:23.108786', '2', 'sahur@1', 3, '', 4, 1),
(49, '2025-04-26 13:45:25.789231', '7', 'tralala@1', 3, '', 4, 1),
(50, '2025-04-26 13:45:28.714374', '8', 'uhahay@1', 3, '', 4, 1),
(51, '2025-04-27 06:49:28.973147', '11', 'asdasdasd23@', 2, '[]', 4, 1),
(52, '2025-04-27 07:14:11.716224', '4', 'hradmin@1', 2, '[{\"changed\": {\"fields\": [\"Last name\"]}}]', 4, 1),
(53, '2025-04-27 14:07:29.941490', '5', 'admin@1', 1, '[{\"added\": {}}]', 4, 1),
(54, '2025-04-27 14:07:33.647341', '5', 'admin@1', 2, '[{\"changed\": {\"fields\": [\"Groups\"]}}]', 4, 1),
(55, '2025-04-27 14:09:10.563743', '2', 'asdasd@1', 2, '[{\"changed\": {\"fields\": [\"Active\"]}}]', 4, 1);

-- --------------------------------------------------------

--
-- Table structure for table `django_content_type`
--

CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `django_content_type`
--

INSERT INTO `django_content_type` (`id`, `app_label`, `model`) VALUES
(1, 'admin', 'logentry'),
(10, 'adminpanel', 'globalsettings'),
(9, 'adminpanel', 'inventoryitem'),
(11, 'adminpanel', 'notification'),
(7, 'adminpanel', 'user'),
(8, 'adminpanel', 'userprofile'),
(30, 'adminpanel', 'usersettings'),
(23, 'aftersales', 'maintenancerecord'),
(22, 'aftersales', 'servicerecord'),
(24, 'aftersales', 'technician'),
(3, 'auth', 'group'),
(2, 'auth', 'permission'),
(4, 'auth', 'user'),
(5, 'contenttypes', 'contenttype'),
(19, 'delivery', 'deliveryrequest'),
(20, 'delivery', 'deliveryschedule'),
(18, 'motorpool', 'equipmentinspection'),
(17, 'motorpool', 'inspection'),
(29, 'notifications', 'notification'),
(21, 'sales', 'clientrecord'),
(14, 'sales', 'invoice'),
(12, 'sales', 'orderitem'),
(15, 'sales', 'request'),
(16, 'sales', 'requestnote'),
(13, 'sales', 'salesorder'),
(6, 'sessions', 'session'),
(28, 'warehouse', 'warehouseclientrecord'),
(27, 'warehouse', 'warehouseinvoice'),
(25, 'warehouse', 'warehouseorder'),
(26, 'warehouse', 'warehouseorderitem');

-- --------------------------------------------------------

--
-- Table structure for table `django_migrations`
--

CREATE TABLE `django_migrations` (
  `id` bigint(20) NOT NULL,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `django_migrations`
--

INSERT INTO `django_migrations` (`id`, `app`, `name`, `applied`) VALUES
(1, 'contenttypes', '0001_initial', '2025-04-17 15:56:05.383756'),
(2, 'auth', '0001_initial', '2025-04-17 15:56:05.686409'),
(3, 'admin', '0001_initial', '2025-04-17 15:56:05.761789'),
(4, 'admin', '0002_logentry_remove_auto_add', '2025-04-17 15:56:05.770894'),
(5, 'admin', '0003_logentry_add_action_flag_choices', '2025-04-17 15:56:05.780069'),
(6, 'contenttypes', '0002_remove_content_type_name', '2025-04-17 15:56:05.867215'),
(7, 'auth', '0002_alter_permission_name_max_length', '2025-04-17 15:56:05.902385'),
(8, 'auth', '0003_alter_user_email_max_length', '2025-04-17 15:56:05.933094'),
(9, 'auth', '0004_alter_user_username_opts', '2025-04-17 15:56:05.944748'),
(10, 'auth', '0005_alter_user_last_login_null', '2025-04-17 15:56:05.992191'),
(11, 'auth', '0006_require_contenttypes_0002', '2025-04-17 15:56:05.995295'),
(12, 'auth', '0007_alter_validators_add_error_messages', '2025-04-17 15:56:06.004555'),
(13, 'auth', '0008_alter_user_username_max_length', '2025-04-17 15:56:06.024680'),
(14, 'auth', '0009_alter_user_last_name_max_length', '2025-04-17 15:56:06.068553'),
(15, 'auth', '0010_alter_group_name_max_length', '2025-04-17 15:56:06.089159'),
(16, 'auth', '0011_update_proxy_permissions', '2025-04-17 15:56:06.100380'),
(17, 'auth', '0012_alter_user_first_name_max_length', '2025-04-17 15:56:06.119668'),
(18, 'sessions', '0001_initial', '2025-04-17 15:56:06.144794'),
(19, 'adminpanel', '0001_initial', '2025-04-26 06:14:00.846373'),
(20, 'adminpanel', '0002_userprofile_delete_user', '2025-04-26 07:35:17.926112'),
(21, 'adminpanel', '0003_userprofile_plain_password', '2025-04-26 13:23:52.622649'),
(22, 'adminpanel', '0004_userprofile_date_of_joining', '2025-04-26 13:36:10.497743'),
(23, 'adminpanel', '0005_inventoryitem', '2025-05-04 04:02:35.280050'),
(24, 'adminpanel', '0006_inventoryitem_serial_number', '2025-05-04 05:36:47.208487'),
(25, 'adminpanel', '0007_remove_inventoryitem_status_inventoryitem_department', '2025-05-04 12:02:57.609082'),
(26, 'adminpanel', '0008_globalsettings', '2025-05-14 11:44:29.059507'),
(27, 'adminpanel', '0008_notification', '2025-05-16 11:16:30.053657'),
(28, 'sales', '0001_initial', '2025-05-17 06:50:43.758448'),
(29, 'sales', '0002_salesorder_company_address_and_more', '2025-05-17 06:57:31.960517'),
(30, 'adminpanel', '0008_inventoryitem_unit_price', '2025-05-17 07:53:53.928056'),
(31, 'sales', '0003_invoice', '2025-05-17 13:07:37.111262'),
(32, 'sales', '0004_request', '2025-05-18 01:27:14.825556'),
(33, 'sales', '0005_request_requested_by_name', '2025-05-18 01:32:02.285157'),
(34, 'sales', '0006_request_notes', '2025-05-18 01:56:27.346379'),
(35, 'sales', '0007_requestnote', '2025-05-18 02:11:02.094464'),
(36, 'motorpool', '0001_initial', '2025-05-18 04:34:22.255255'),
(37, 'motorpool', '0002_alter_inspection_status', '2025-05-18 04:55:49.714916'),
(38, 'motorpool', '0003_remove_inspection_technician_and_more', '2025-05-18 05:00:43.154969'),
(39, 'motorpool', '0004_remove_inspection_department', '2025-05-18 05:05:57.757253'),
(40, 'motorpool', '0005_equipmentinspection_delete_inspection', '2025-05-18 06:42:50.559396'),
(41, 'motorpool', '0006_alter_equipmentinspection_assigned_technician', '2025-05-18 08:38:44.047488'),
(42, 'motorpool', '0007_equipmentinspection_checklist_reference', '2025-05-18 08:47:34.754205'),
(43, 'motorpool', '0008_equipmentinspection_assisted_by', '2025-05-18 08:51:02.298984'),
(44, 'motorpool', '0009_equipmentinspection_corrective_actions_and_more', '2025-05-18 08:54:44.167153'),
(45, 'motorpool', '0010_equipmentinspection_inspection_photos_and_more', '2025-05-18 09:02:43.176999'),
(46, 'delivery', '0001_initial', '2025-05-18 12:17:27.001578'),
(47, 'delivery', '0002_deliveryschedule', '2025-05-18 13:50:30.708730'),
(48, 'delivery', '0003_alter_deliveryschedule_status', '2025-05-18 14:06:43.059238'),
(49, 'delivery', '0004_auto_20250518_2208', '2025-05-18 14:08:26.450046'),
(51, 'delivery', '0005_alter_deliveryrequest_client_info_and_more', '2025-05-19 01:27:09.787085'),
(52, 'delivery', '0006_alter_deliveryrequest_client_info_and_more', '2025-05-19 01:27:09.791816'),
(53, 'sales', '0008_clientrecord', '2025-05-19 04:56:47.248856'),
(54, 'sales', '0009_invoice_client_record_salesorder_client_record', '2025-05-19 05:46:44.562963'),
(55, 'aftersales', '0001_initial', '2025-05-19 09:03:29.633155'),
(56, 'aftersales', '0002_maintenancerecord', '2025-05-19 11:56:13.227236'),
(57, 'aftersales', '0003_maintenancerecord_diagnosis_and_more', '2025-05-19 13:13:24.617917'),
(58, 'aftersales', '0004_technician_remove_maintenancerecord_assigned_tech_and_more', '2025-05-19 13:33:32.148217'),
(59, 'aftersales', '0005_maintenancerecord_service_record', '2025-05-20 01:39:23.293781'),
(60, 'warehouse', '0001_initial', '2025-05-20 04:34:22.760614'),
(61, 'warehouse', '0002_warehouseorder_client_company', '2025-05-20 04:43:17.135833'),
(62, 'warehouse', '0003_warehouseorderitem_item_code_and_more', '2025-05-20 04:46:09.370069'),
(63, 'warehouse', '0004_remove_warehouseorder_client_company', '2025-05-20 04:53:19.452483'),
(64, 'warehouse', '0005_warehouseinvoice', '2025-05-20 05:36:11.599635'),
(65, 'warehouse', '0006_warehouseclientrecord', '2025-05-20 13:40:57.580714'),
(66, 'notifications', '0001_initial', '2025-05-23 12:09:08.473637'),
(67, 'notifications', '0002_auto_20250523_2009', '2025-05-23 12:09:08.480699'),
(68, 'aftersales', '0006_servicerecord_usage_unit_servicerecord_usage_value_and_more', '2025-06-09 09:46:24.297689'),
(69, 'adminpanel', '0009_usersettings', '2025-08-21 04:19:22.786150'),
(70, 'warehouse', '0007_alter_warehouseclientrecord_options_and_more', '2025-08-24 05:11:14.549895'),
(71, 'adminpanel', '0010_userprofile_profile_picture', '2025-09-03 02:46:43.800550');

-- --------------------------------------------------------

--
-- Table structure for table `django_session`
--

CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `django_session`
--

INSERT INTO `django_session` (`session_key`, `session_data`, `expire_date`) VALUES
('0ke70gi0719qtjt674c1b9bhtit3taoe', '.eJxVjDsOwjAQBe_iGlnOJusPJT1nsNbeDQkgW4qTCnF3iJQC2jcz76UibesUtyZLnFmdFajT75YoP6TsgO9UblXnWtZlTnpX9EGbvlaW5-Vw_w4matO3dgQ9SwooAfMIDr0ZOs8WjSRyNApS3yEQD5CAZXSdDxKMxSFY8b1X7w_qhje5:1uHQ3F:gdtnpuNRxsx0CwHx0v6YSNNFtrG24RAhIULSLE2Yxzw', '2025-06-03 16:42:49.274549'),
('42ltxsayq0zfu4h2m1s8exlxrphy50sq', '.eJxVjMEOwiAQRP-FsyGFUtj16L3fQJYFpGpoUtqT8d9tkx70NMm8N_MWnra1-K2lxU9RXIUVl98uED9TPUB8UL3Pkue6LlOQhyJP2uQ4x_S6ne7fQaFW9rUO0RBm6ACdDXsOSmPMNPTQhw5IsSXknMFpRsOYwDgOGilaBdlk8fkC55c4Kg:1uHBrb:KI8V8C5UCg_B1XM27lVyT_eJoUUXiUxtxB-dyTVGC3o', '2025-06-03 01:33:51.636681'),
('4mv6d2zzwfnj05roi5hrvq0ylc2jijlg', '.eJxVjMsOwiAQRf-FtSHAlMe4dO83EB6DVA0kpV0Z_12bdKHbe865L-bDtla_DVr8nNmZATv9bjGkB7Ud5Htot85Tb-syR74r_KCDX3um5-Vw_w5qGPVbR1dIo0MgQxlDTFbEEi2kYgoCKjsVXQAt4ARCQHZGC0NSOiWVNkGy9wfx_zcz:1udSX5:fJo-jYlLbycJlYy2UV-PuFznzIsqZpoUHEkd6rGevts', '2025-08-03 11:48:43.908221'),
('5oz33d4q5p898ao3pg6t125zj76fgmzj', '.eJxVjDsOwjAQRO_iGln-ZR1T0ucM1tq7wgFkS3FSIe5OIqWAZop5b-YtIm5riVvnJc4krgLE5bdLmJ9cD0APrPcmc6vrMid5KPKkXU6N-HU73b-Dgr3sa6UYUCvt2QceUWUIXmtHo8FBOZsgWQTjMbFTxhHbsEfO4IIG0nkQny_I8Tdi:1uq2Gq:qm4boe5RTvsGXhYBIg2gM503OgsTZ67X_JAb5NWZ-us', '2025-09-07 04:23:56.069870'),
('5qx96naerctxs8jel5lfofw4pxmf7gbm', '.eJxVjEEOwiAQRe_C2pAilCku3XsGMgMzUjU0Ke3KeHfbpAvd_vfef6uI61Li2niOY1YXZdXpdyNMT647yA-s90mnqS7zSHpX9EGbvk2ZX9fD_Tso2MpW95QtBccBEiUQAR8GQAMSemeyZMGEgaALfiOG2XmyxjrfDXSWhF59vgBCOFc:1uHFaK:RK6sRei0Pc8_9IpwSSF3QL6XFUzeLreztl8HU0iq63E', '2025-06-03 05:32:16.709721'),
('5rcmm84lia2baf4lefanqkuf9sss82sz', 'e30:1u5z8j:2UQ-VNDFJzzclke-3qem6Bwi1uCdiGtoFDIZdGqF57s', '2025-05-03 03:45:13.695159'),
('623mtgtguu6vdk618nq0nhv46ikj8hhk', 'e30:1u5yzh:oiyx_ntt64E_-ItNqkToaaNOfP74cxH2gQUiD5ycmdw', '2025-05-03 03:35:53.431759'),
('87vol49och1v1l5aryxv8lud67ym40ph', '.eJxVjEEOwiAQRe_C2hA6TAO4dO8ZyMAMUjU0Ke3KeHdt0oVu_3vvv1Skba1x67LEidVZgTr9bonyQ9oO-E7tNus8t3WZkt4VfdCurzPL83K4fweVev3WzvpApnhnTUmuGCPkSOzIABBAyCL7Yjh4sn7MwyCIlBwWNBkQmdX7A9uwN8s:1ute7a:DeV_u8xkhMg0Fi0HuxwBr8N3ZEJJhvurbLV4FHnf_X8', '2025-09-17 03:25:18.093248'),
('87yudvnasuv201xge40cifqs7ujf3ug3', '.eJxVjMsOwiAQRf-FtSHAlMe4dO83EB6DVA0kpV0Z_12bdKHbe865L-bDtla_DVr8nNmZATv9bjGkB7Ud5Htot85Tb-syR74r_KCDX3um5-Vw_w5qGPVbR1dIo0MgQxlDTFbEEi2kYgoCKjsVXQAt4ARCQHZGC0NSOiWVNkGy9wfx_zcz:1uJ3Yk:sFEdNXlCJNxe92QoU0LRaNJEkPoE7s4il2LUucUVCA0', '2025-06-08 05:06:06.330070'),
('9s3rjytp5jzuvg7pw23n5ari8dw7s3h6', 'e30:1uF1fg:mdIMugEJ7kgIjvofKjInTalzawWyXcUHTEPZGfMeyco', '2025-05-28 02:16:36.208150'),
('am19mfw6mhyd0x8blm7zk6rnk9gr74qc', '.eJxVjDsOwjAQRO_iGln-ZR1T0ucM1tq7wgFkS3FSIe5OIqWAZop5b-YtIm5riVvnJc4krgLE5bdLmJ9cD0APrPcmc6vrMid5KPKkXU6N-HU73b-Dgr3sa6UYUCvt2QceUWUIXmtHo8FBOZsgWQTjMbFTxhHbsEfO4IIG0nkQny_I8Tdi:1uOZZe:qbeNZIZaTcdSAFvq7ozSbHHRQfj77ToW_Y3_OxiNDkE', '2025-06-23 10:17:50.522464'),
('bdgakm74165zz3cd0znkawmi85isiozk', '.eJxVjEEOwiAQRe_C2pAilCku3XsGMgMzUjU0Ke3KeHfbpAvd_vfef6uI61Li2niOY1YXZdXpdyNMT647yA-s90mnqS7zSHpX9EGbvk2ZX9fD_Tso2MpW95QtBccBEiUQAR8GQAMSemeyZMGEgaALfiOG2XmyxjrfDXSWhF59vgBCOFc:1uHC7o:Xn76FKVHJ2MfaDANMbuPpd4BVMU3YyE_-OS3HIYwXBM', '2025-06-03 01:50:36.458976'),
('dtq0lph01fhs4au65vfig6dct79c1rhw', '.eJxVjMsOwiAQRf-FtSHlIRSX7v0GMjAzUjWQlHZl_HfbpAvdnnPufYsI61Li2mmOE4qL0OL0yxLkJ9Vd4APqvcnc6jJPSe6JPGyXt4b0uh7t30GBXra1yqgHT2Z0bggpEANnHM5aJUajUyY2Y4YNMpuAFoKlBME5r4JXVrP4fAEOezj6:1u6SwH:WQ_z63DVWxk4skOf0YC5SYUVqcf-jtzAFj4Hka7dTF8', '2025-05-04 11:34:21.762802'),
('eo1igq7bwedco520qsojiu99x644zu90', '.eJxVjEEOwiAQRe_C2hCQgYJL9z0DgZlBqoYmpV0Z765NutDtf-_9l4hpW2vcOi9xInERVpx-t5zwwW0HdE_tNkuc27pMWe6KPGiX40z8vB7u30FNvX5rR9mZNGAIitF4sOC5FHd2JqgMOQAGbQtr0AykFDB6GCxplw34BCzeH9xRN4U:1utiJz:9O-sFkvHwJUF3hD7tgGLBW46i0D3Xz6OhZnNDn2yGeY', '2025-09-17 07:54:23.696048'),
('fs7va7fqlgrockrmtrgzmlrxu79vzljx', 'e30:1uBvrU:DGU2OvHh-0pyCQJfhn02mhWiTYmJqfdH0stOaAoBJ8A', '2025-05-19 13:28:00.339332'),
('fsqh39wb9gt4vz0vmtezfubqp3s3gd9e', '.eJxVjMsOwiAQAP-FsyEs73r07jeQhV2lamhS2pPx3w1JD3qdmcxbJNy3mvbOa5pJnAWI0y_LWJ7chqAHtvsiy9K2dc5yJPKwXV4X4tflaP8GFXsdW9DRR7JgTAFtyJuSGRRAyFq54BB4YjuRKrnY4KLON9IcDaKzqMCLzxe2nzce:1uIQmQ:Zc3MBJ_6M-2lvKaz07zGtNAG4ZB6QPibEMI4ea-7I4g', '2025-06-06 11:41:38.450785'),
('ihadk3da7c6uvz4iqfcyq83upo4t6zm8', '.eJxVjMsOwiAQRf-FtSEMj0JduvcbCDMMUjU0Ke3K-O_apAvd3nPOfYmYtrXGrfMSpyzOwojT74aJHtx2kO-p3WZJc1uXCeWuyIN2eZ0zPy-H-3dQU6_fWlkDiOC1YU2QBgTCwIUJLAceMzmLHgByydYEQ0ppZ03xIQ0WHY_i_QHrYjfv:1uJ1iE:ExD0Ftj7sA0t73qp8e4Co7YJ29gBwu2Qs_88cBMWbDo', '2025-06-08 03:07:46.859591'),
('kvtz1ldgudcqaibm58wxs0ithjxp59f6', '.eJxVjMsOwiAQRf-FtSEMj0JduvcbCDMMUjU0Ke3K-O_apAvd3nPOfYmYtrXGrfMSpyzOwojT74aJHtx2kO-p3WZJc1uXCeWuyIN2eZ0zPy-H-3dQU6_fWlkDiOC1YU2QBgTCwIUJLAceMzmLHgByydYEQ0ppZ03xIQ0WHY_i_QHrYjfv:1uIRyA:2ayEkXBzpsY_Cg3TuyrTe6I6BwF9jLkCq81x2lm9YVQ', '2025-06-06 12:57:50.614249'),
('ldnwk7leywtqeqwnfp12v8vsz6bgzbik', '.eJxVjDsOwjAQBe_iGln-xJs1JT1niHa9Ng4gR8qnQtwdIqWA9s3Me6mBtrUO25LnYRR1Vk6dfjem9MhtB3Kndpt0mto6j6x3RR900ddJ8vNyuH8HlZb6ral3VhATWy59oEiFxSIWH4wnEArB9BEsgDEZvXUdeXASocPsCwOq9wfhOjdJ:1uIqwU:UAsbcDedBk0_dXsHAIgCajwCxADRWiV4f7RKO1WCCrU', '2025-06-07 15:37:46.977684'),
('nhz6wpocphatj58otvo1ed4yny06ephw', '.eJxVjDsOwjAQBe_iGlneOP4sJX3OYK1_OIBsKU4qxN1JpBTQzsx7b-ZoW4vbelrcHNmVAbv8Mk_hmeoh4oPqvfHQ6rrMnh8JP23nU4vpdTvbv4NCvexrIQwpj6MACjJao1HocSBEawGEzqR3GkCisslnqbJXgyILGFQQRlv2-QK03Ta_:1uN4s1:scjY4nJDKR-nfwJcEHnls7bFeMbEmESnkjUScOE9Yls', '2025-06-19 07:18:37.592515'),
('ntrvyahggo4cyojdakdl1vqgfik35hyn', '.eJxVjMsOwiAQRf-FtSEw5TF16d5vIANDpWogKe3K-O_apAvd3nPOfYlA21rC1vMSZhZnYcXpd4uUHrnugO9Ub02mVtdljnJX5EG7vDbOz8vh_h0U6uVbG2d4ss6AS6hRKQUekYGZcLQEnMmzGgb0FJ2HBHpykQYbR2OsRuvE-wPCyTbq:1uHP8n:_H6IX4eFvyVZqmkj-IGOjvcWpu0a8gg0AlYrB6CvoOQ', '2025-06-03 15:44:29.891660'),
('oiby2dn4a7g8vmesog6m9e80zic6wmi8', 'e30:1uF1or:BXQOPG9GA3T7rtjGG6T5e2Vgn15knrEYWjEZKqufFUE', '2025-05-28 02:26:05.839348'),
('oqsw5pm2vlfu3fptjrgt4i0lwp71ggid', '.eJxVjMsOwiAQAP-FsyEs73r07jeQhV2lamhS2pPx3w1JD3qdmcxbJNy3mvbOa5pJnAWI0y_LWJ7chqAHtvsiy9K2dc5yJPKwXV4X4tflaP8GFXsdW9DRR7JgTAFtyJuSGRRAyFq54BB4YjuRKrnY4KLON9IcDaKzqMCLzxe2nzce:1uAU2M:WQxW70r5s-jp_BBlMIECAAMDiqIZIWZffcy-rlzonmI', '2025-05-15 13:33:14.876385'),
('q3x8hfw6oddyvwsq085gf0y63my887z6', '.eJxVjMEOwiAQRP-FsyGFUtj16L3fQJYFpGpoUtqT8d9tkx70NMm8N_MWnra1-K2lxU9RXIUVl98uED9TPUB8UL3Pkue6LlOQhyJP2uQ4x_S6ne7fQaFW9rUO0RBm6ACdDXsOSmPMNPTQhw5IsSXknMFpRsOYwDgOGilaBdlk8fkC55c4Kg:1uGzMO:q1djRyffcA_dDmo6racdyM8uk3eaTgNhBkz3eBoMcTM', '2025-06-02 12:12:48.866639'),
('sq54qnixlqlhta2gxecp7ubfqs3bmstw', '.eJxVjEEOgjAURO_StWk-hf5Sl-49Q_OHthY1kFBYGe-uJCx0O--9eakg21rCVtMSxqjOitXpd4MMjzTtIN5lus16mKd1GaF3RR-06usc0_NyuH8HRWr51s47TxgsvMlsvScnwsQGiXLj0QtzG53p0KAHOmMtCB3YmNy2sKTeH86INz0:1utiUt:hXE3fqdVRE6UHmSfDrhxvH8POHgFdVuDGpGvlmzHR6Q', '2025-09-17 08:05:39.254965'),
('vfst36y30ayuykvmuqefsl3bp3om1a3t', '.eJxVjDsOwjAQBe_iGlneOP4sJX3OYK1_OIBsKU4qxN1JpBTQzsx7b-ZoW4vbelrcHNmVAbv8Mk_hmeoh4oPqvfHQ6rrMnh8JP23nU4vpdTvbv4NCvexrIQwpj6MACjJao1HocSBEawGEzqR3GkCisslnqbJXgyILGFQQRlv2-QK03Ta_:1utiug:MlRLHuliZzK9gS2vuhT-Tz9jwWzKRnhUsqCFd-IsifU', '2025-09-17 08:32:18.321651'),
('wc699qdu6jbnsoptqep39fjbhri79itz', 'e30:1uBm7V:LrGeMmCB5rZeaBUYviqxQ7HLTLBZ8hWMtvMSMmquzI8', '2025-05-19 03:03:53.338805'),
('wtypj8p9fdt46byblsh6xdu7jogsnkha', '.eJxVjEEOwiAQRe_C2pAilCku3XsGMgMzUjU0Ke3KeHfbpAvd_vfef6uI61Li2niOY1YXZdXpdyNMT647yA-s90mnqS7zSHpX9EGbvk2ZX9fD_Tso2MpW95QtBccBEiUQAR8GQAMSemeyZMGEgaALfiOG2XmyxjrfDXSWhF59vgBCOFc:1uGEzN:ei8FtADv9i-u57QRDc5PleXBfNFPDXLnafzMZqp-h-g', '2025-05-31 10:41:57.356867'),
('xlnq58ypqo2lsryavrx90gxhisz6yknt', '.eJxVjEEOwiAQRe_C2pAilCku3XsGMgMzUjU0Ke3KeHfbpAvd_vfef6uI61Li2niOY1YXZdXpdyNMT647yA-s90mnqS7zSHpX9EGbvk2ZX9fD_Tso2MpW95QtBccBEiUQAR8GQAMSemeyZMGEgaALfiOG2XmyxjrfDXSWhF59vgBCOFc:1uHOKc:0Rd33063jquxngEPv_gg6x6nRGu472qpkjCarRgEjKw', '2025-06-03 14:52:38.213491');

-- --------------------------------------------------------

--
-- Table structure for table `motorpool_equipmentinspection`
--

CREATE TABLE `motorpool_equipmentinspection` (
  `id` bigint(20) NOT NULL,
  `inspection_id` varchar(20) NOT NULL,
  `request_type` varchar(50) NOT NULL,
  `unit` varchar(255) NOT NULL,
  `date_received` datetime(6) NOT NULL,
  `status` varchar(50) NOT NULL,
  `invoice_number` varchar(50) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `assigned_technician` varchar(100) DEFAULT NULL,
  `pdi_request_id` bigint(20) DEFAULT NULL,
  `checklist_reference` varchar(100) DEFAULT NULL,
  `assisted_by` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL CHECK (json_valid(`assisted_by`)),
  `corrective_actions` longtext DEFAULT NULL,
  `inspection_result` varchar(20) DEFAULT NULL,
  `issues_found` longtext DEFAULT NULL,
  `notes` longtext DEFAULT NULL,
  `spare_parts_used` longtext DEFAULT NULL,
  `inspection_photos` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL CHECK (json_valid(`inspection_photos`)),
  `signed_form` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `motorpool_equipmentinspection`
--

INSERT INTO `motorpool_equipmentinspection` (`id`, `inspection_id`, `request_type`, `unit`, `date_received`, `status`, `invoice_number`, `created_at`, `updated_at`, `assigned_technician`, `pdi_request_id`, `checklist_reference`, `assisted_by`, `corrective_actions`, `inspection_result`, `issues_found`, `notes`, `spare_parts_used`, `inspection_photos`, `signed_form`) VALUES
(76, 'INS-20250903-0001', 'PDI', 'Excavator Long Arm', '2025-09-03 07:51:23.022045', 'Delivery', 'INV-25-0001', '2025-09-03 07:51:23.023168', '2025-09-03 08:00:20.335803', 'sadfas', 113, 'inspections/76/checklist_DATA-MINING_VERSA.docx', '[\"Kyle\"]', 'None', 'Passed', 'None', 'None', 'None', '[\"inspections/76/photos/20250903_155340_adasdasd.png\", \"inspections/76/photos/20250903_155340_asdasdasd.jpg\", \"inspections/76/photos/20250903_155340_sdsdsdsdsd.jpg\"]', 'inspections/76/signed_form_PREDICTED-DEMAND-SPIKES (1).docx');

-- --------------------------------------------------------

--
-- Table structure for table `notifications_notification`
--

CREATE TABLE `notifications_notification` (
  `id` bigint(20) NOT NULL,
  `title` varchar(255) NOT NULL,
  `message` longtext NOT NULL,
  `notification_type` varchar(50) NOT NULL,
  `from_department` varchar(50) NOT NULL,
  `to_department` varchar(50) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `related_id` int(11) DEFAULT NULL,
  `related_link` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `notifications_notification`
--

INSERT INTO `notifications_notification` (`id`, `title`, `message`, `notification_type`, `from_department`, `to_department`, `created_at`, `related_id`, `related_link`) VALUES
(295, 'New Invoice Generated', 'New invoice INV-25-0001 has been generated for lowe', 'new_invoice', 'sales', 'admin', '2025-09-03 07:46:23.289367', 119, '/adminpanel/invoicing/?invoice_number=INV-25-0001'),
(296, 'New Sales Order Created', 'New order ORD-20250903-0001 has been created for lowe', 'new_sales_order', 'sales', 'admin', '2025-09-03 07:46:23.290471', 132, '/adminpanel/sales&Orders/?order_number=ORD-20250903-0001'),
(297, 'New PDI Request', 'New PDI request (RQ-20250903-0001) for unit Excavator Long Arm from Christian Jude', 'pdi_request', 'sales', 'motorpool', '2025-09-03 07:46:30.623655', 113, '/motorpool/received_requests/?request_id=RQ-20250903-0001'),
(298, 'New PDI Request', 'New PDI request (RQ-20250903-0001) for unit Excavator Long Arm from Christian Jude', 'pdi_request_admin', 'sales', 'admin', '2025-09-03 07:46:30.624734', 113, '/adminpanel/motorpool/?request_id=RQ-20250903-0001'),
(299, 'New Invoice Generated', 'New invoice INV-25-0002 has been generated for ararsss', 'new_invoice', 'sales', 'admin', '2025-09-03 07:50:05.678936', 120, '/adminpanel/invoicing/?invoice_number=INV-25-0002'),
(300, 'New Sales Order Created', 'New order ORD-20250903-0002 has been created for ararsss', 'new_sales_order', 'sales', 'admin', '2025-09-03 07:50:05.679837', 133, '/adminpanel/sales&Orders/?order_number=ORD-20250903-0002'),
(301, 'New PDI Request', 'New PDI request (RQ-20250903-0002) for unit Bulldozer from Christian Jude', 'pdi_request', 'sales', 'motorpool', '2025-09-03 07:50:21.547079', 114, '/motorpool/received_requests/?request_id=RQ-20250903-0002'),
(302, 'New PDI Request', 'New PDI request (RQ-20250903-0002) for unit Bulldozer from Christian Jude', 'pdi_request_admin', 'sales', 'admin', '2025-09-03 07:50:21.547813', 114, '/adminpanel/motorpool/?request_id=RQ-20250903-0002'),
(303, 'New Delivery Request', 'New delivery request (DVR-2025-0001) for unit Excavator Long Arm from Motorpool Department', 'delivery_request', 'motorpool', 'delivery', '2025-09-03 07:58:08.664588', 162, '/delivery/requests/?request_id=DVR-2025-0001'),
(304, 'New Delivery Request', 'New delivery request (DVR-2025-0001) for unit Excavator Long Arm from Motorpool Department', 'delivery_request', 'motorpool', 'delivery', '2025-09-03 08:00:20.334745', 163, '/delivery/requests/?request_id=DVR-2025-0001'),
(305, 'New Delivery Schedule Created', 'New delivery schedule DVS-2025-0001 has been created for lowe', 'new_delivery_schedule', 'delivery', 'admin', '2025-09-03 08:00:40.739333', 86, '/adminpanel/delivery&Tracking/?schedule_id=DVS-2025-0001'),
(306, 'New Delivery Completed', 'Delivery DVS-2025-0001 has been completed for lowe', 'delivery_complete', 'delivery', 'aftersales', '2025-09-03 08:21:00.049016', 86, '/aftersales/logs/?schedule_id=DVS-2025-0001'),
(307, 'Order Delivered', 'Order INV-25-0001 has been delivered to lowe', 'order_delivered', 'delivery', 'sales', '2025-09-03 08:21:00.049568', 86, '/sales/orders/?order_number=INV-25-0001'),
(308, 'Sales Delivery Completed', 'Sales delivery DVS-2025-0001 has been completed for lowe', 'sales_delivery_complete', 'delivery', 'admin', '2025-09-03 08:21:00.050038', 86, '/adminpanel/delivery&Tracking/?schedule_id=DVS-2025-0001');

-- --------------------------------------------------------

--
-- Table structure for table `notifications_notification_read_by`
--

CREATE TABLE `notifications_notification_read_by` (
  `id` bigint(20) NOT NULL,
  `notification_id` bigint(20) NOT NULL,
  `user_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `notifications_notification_read_by`
--

INSERT INTO `notifications_notification_read_by` (`id`, `notification_id`, `user_id`) VALUES
(446, 297, 4),
(447, 301, 4),
(448, 303, 5),
(449, 304, 5),
(450, 307, 2);

-- --------------------------------------------------------

--
-- Table structure for table `sales_clientrecord`
--

CREATE TABLE `sales_clientrecord` (
  `id` bigint(20) NOT NULL,
  `client_name` varchar(255) NOT NULL,
  `company_name` varchar(255) DEFAULT NULL,
  `contact_info` varchar(100) NOT NULL,
  `email` varchar(254) DEFAULT NULL,
  `address` longtext NOT NULL,
  `total_orders` int(10) UNSIGNED NOT NULL CHECK (`total_orders` >= 0),
  `status` varchar(20) NOT NULL,
  `last_order_date` date NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `delivery_schedule_id` bigint(20) DEFAULT NULL,
  `sales_order_id` bigint(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `sales_clientrecord`
--

INSERT INTO `sales_clientrecord` (`id`, `client_name`, `company_name`, `contact_info`, `email`, `address`, `total_orders`, `status`, `last_order_date`, `created_at`, `updated_at`, `delivery_schedule_id`, `sales_order_id`) VALUES
(35, 'lowe', 'jinyi', '09368872989', 'lowe@gmail.com', 'lasang ', 1, 'Active', '2025-09-03', '2025-09-03 08:21:00.041212', '2025-09-03 08:21:00.041221', 86, NULL);

-- --------------------------------------------------------

--
-- Table structure for table `sales_invoice`
--

CREATE TABLE `sales_invoice` (
  `id` bigint(20) NOT NULL,
  `invoice_number` varchar(20) NOT NULL,
  `client_name` varchar(255) NOT NULL,
  `department` varchar(100) NOT NULL,
  `amount` decimal(10,2) NOT NULL,
  `invoice_date` date NOT NULL,
  `due_date` date NOT NULL,
  `status` varchar(20) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `order_id` bigint(20) NOT NULL,
  `client_record_id` bigint(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `sales_invoice`
--

INSERT INTO `sales_invoice` (`id`, `invoice_number`, `client_name`, `department`, `amount`, `invoice_date`, `due_date`, `status`, `created_at`, `updated_at`, `order_id`, `client_record_id`) VALUES
(119, 'INV-25-0001', 'lowe', 'Sales', 3400000.00, '2025-09-03', '2025-09-11', 'Paid', '2025-09-03 07:46:23.288374', '2025-09-03 07:46:23.288390', 132, 35),
(120, 'INV-25-0002', 'ararsss', 'Sales', 4300000.00, '2025-09-03', '2025-09-20', 'Paid', '2025-09-03 07:50:05.678253', '2025-09-03 07:50:05.678262', 133, NULL);

-- --------------------------------------------------------

--
-- Table structure for table `sales_orderitem`
--

CREATE TABLE `sales_orderitem` (
  `id` bigint(20) NOT NULL,
  `quantity` int(10) UNSIGNED NOT NULL CHECK (`quantity` >= 0),
  `unit_price` decimal(12,2) NOT NULL,
  `total_price` decimal(12,2) NOT NULL,
  `inventory_item_id` bigint(20) NOT NULL,
  `order_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `sales_orderitem`
--

INSERT INTO `sales_orderitem` (`id`, `quantity`, `unit_price`, `total_price`, `inventory_item_id`, `order_id`) VALUES
(218, 1, 3400000.00, 3400000.00, 53, 132),
(219, 1, 4300000.00, 4300000.00, 54, 133);

-- --------------------------------------------------------

--
-- Table structure for table `sales_request`
--

CREATE TABLE `sales_request` (
  `id` bigint(20) NOT NULL,
  `request_id` varchar(20) NOT NULL,
  `request_type` varchar(50) NOT NULL,
  `unit` varchar(100) NOT NULL,
  `invoice_number` varchar(50) NOT NULL,
  `invoice_id` varchar(50) NOT NULL,
  `assigned_to` varchar(100) NOT NULL,
  `status` varchar(20) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `requested_by_id` int(11) NOT NULL,
  `requested_by_name` varchar(255) NOT NULL,
  `notes` longtext DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `sales_request`
--

INSERT INTO `sales_request` (`id`, `request_id`, `request_type`, `unit`, `invoice_number`, `invoice_id`, `assigned_to`, `status`, `created_at`, `updated_at`, `requested_by_id`, `requested_by_name`, `notes`) VALUES
(113, 'RQ-20250903-0001', 'PDI', 'Excavator Long Arm', 'INV-25-0001', '119', 'Motorpool', 'In Progress', '2025-09-03 07:46:30.622587', '2025-09-03 07:51:23.018132', 2, 'Christian Jude', NULL),
(114, 'RQ-20250903-0002', 'PDI', 'Bulldozer', 'INV-25-0002', '120', 'Motorpool', 'Pending', '2025-09-03 07:50:21.546231', '2025-09-03 07:50:21.546241', 2, 'Christian Jude', NULL);

-- --------------------------------------------------------

--
-- Table structure for table `sales_requestnote`
--

CREATE TABLE `sales_requestnote` (
  `id` bigint(20) NOT NULL,
  `note` longtext NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `created_by_id` int(11) NOT NULL,
  `request_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `sales_requestnote`
--

INSERT INTO `sales_requestnote` (`id`, `note`, `created_at`, `created_by_id`, `request_id`) VALUES
(102, 'Status updated to: In Progress', '2025-09-03 07:51:23.020387', 4, 113);

-- --------------------------------------------------------

--
-- Table structure for table `sales_salesorder`
--

CREATE TABLE `sales_salesorder` (
  `id` bigint(20) NOT NULL,
  `order_number` varchar(20) NOT NULL,
  `client_name` varchar(255) NOT NULL,
  `client_address` longtext NOT NULL,
  `client_contact` varchar(100) NOT NULL,
  `client_email` varchar(254) NOT NULL,
  `order_date` date NOT NULL,
  `delivery_date` date NOT NULL,
  `delivery_instructions` longtext NOT NULL,
  `payment_mode` varchar(20) NOT NULL,
  `due_date` date NOT NULL,
  `amount_paid` decimal(12,2) NOT NULL,
  `residence_location` longtext DEFAULT NULL,
  `bank_account` varchar(255) DEFAULT NULL,
  `account_number` varchar(100) DEFAULT NULL,
  `id_attachment` varchar(100) DEFAULT NULL,
  `business_permit` varchar(100) DEFAULT NULL,
  `bir_attachment` varchar(100) DEFAULT NULL,
  `status` varchar(20) NOT NULL,
  `total_amount` decimal(12,2) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `company_address` longtext DEFAULT NULL,
  `company_contact` varchar(100) DEFAULT NULL,
  `company_email` varchar(254) DEFAULT NULL,
  `company_name` varchar(255) DEFAULT NULL,
  `client_record_id` bigint(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `sales_salesorder`
--

INSERT INTO `sales_salesorder` (`id`, `order_number`, `client_name`, `client_address`, `client_contact`, `client_email`, `order_date`, `delivery_date`, `delivery_instructions`, `payment_mode`, `due_date`, `amount_paid`, `residence_location`, `bank_account`, `account_number`, `id_attachment`, `business_permit`, `bir_attachment`, `status`, `total_amount`, `created_at`, `updated_at`, `company_address`, `company_contact`, `company_email`, `company_name`, `client_record_id`) VALUES
(132, 'ORD-20250903-0001', 'lowe', 'lasang ', '09368872989', 'lowe@gmail.com', '2025-09-03', '2025-09-27', 'asdasdasdasdas', 'cash', '2025-09-11', 3400000.00, NULL, NULL, NULL, 'sales_orders/ids/wp8015700-gaming-light-4k-wallpapers.jpg', '', '', 'Completed', 3400000.00, '2025-09-03 07:46:23.280657', '2025-09-03 08:21:00.053945', 'lasang', '09972474711', 'jinyi@gmail.com', 'jinyi', 35),
(133, 'ORD-20250903-0002', 'ararsss', 'kitolao@gmail.com', '09051069013', 'arar@gmail.com', '2025-09-03', '2025-09-27', 'sadasdasdasd', 'cash', '2025-09-20', 4300000.00, NULL, NULL, NULL, 'sales_orders/ids/wp9139425-purple-neon-lights-4k-wallpapers.jpg', '', '', 'Pending', 4300000.00, '2025-09-03 07:50:05.663444', '2025-09-03 07:50:05.675748', 'lasang', '09972474711', 'jinyi@gmail.com', 'jinyi', NULL);

-- --------------------------------------------------------

--
-- Table structure for table `warehouse_warehouseclientrecord`
--

CREATE TABLE `warehouse_warehouseclientrecord` (
  `id` bigint(20) NOT NULL,
  `client_name` varchar(255) NOT NULL,
  `company_name` varchar(255) DEFAULT NULL,
  `contact_info` varchar(255) DEFAULT NULL,
  `email` varchar(254) DEFAULT NULL,
  `address` longtext DEFAULT NULL,
  `total_orders` int(10) UNSIGNED NOT NULL,
  `status` varchar(20) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `delivery_schedule_id` bigint(20) DEFAULT NULL,
  `last_order_date` date NOT NULL,
  `warehouse_order_id` bigint(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `warehouse_warehouseinvoice`
--

CREATE TABLE `warehouse_warehouseinvoice` (
  `id` bigint(20) NOT NULL,
  `invoice_number` varchar(20) NOT NULL,
  `status` varchar(20) NOT NULL,
  `invoice_date` date NOT NULL,
  `due_date` date NOT NULL,
  `amount` decimal(12,2) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `order_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `warehouse_warehouseorder`
--

CREATE TABLE `warehouse_warehouseorder` (
  `id` bigint(20) NOT NULL,
  `order_number` varchar(20) NOT NULL,
  `client_name` varchar(255) NOT NULL,
  `client_address` longtext NOT NULL,
  `client_contact` varchar(100) NOT NULL,
  `client_email` varchar(254) NOT NULL,
  `company_name` varchar(255) DEFAULT NULL,
  `company_address` longtext DEFAULT NULL,
  `company_contact` varchar(100) DEFAULT NULL,
  `company_email` varchar(254) DEFAULT NULL,
  `order_date` date NOT NULL,
  `delivery_date` date NOT NULL,
  `delivery_instructions` longtext NOT NULL,
  `payment_mode` varchar(20) NOT NULL,
  `due_date` date NOT NULL,
  `amount_paid` decimal(12,2) NOT NULL,
  `residence_location` longtext DEFAULT NULL,
  `bank_account` varchar(255) DEFAULT NULL,
  `account_number` varchar(100) DEFAULT NULL,
  `id_attachment` varchar(100) DEFAULT NULL,
  `business_permit` varchar(100) DEFAULT NULL,
  `bir_attachment` varchar(100) DEFAULT NULL,
  `status` varchar(20) NOT NULL,
  `total_amount` decimal(12,2) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `created_by_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `warehouse_warehouseorderitem`
--

CREATE TABLE `warehouse_warehouseorderitem` (
  `id` bigint(20) NOT NULL,
  `quantity` int(10) UNSIGNED NOT NULL CHECK (`quantity` >= 0),
  `unit_price` decimal(12,2) NOT NULL,
  `total_price` decimal(12,2) NOT NULL,
  `inventory_item_id` bigint(20) NOT NULL,
  `order_id` bigint(20) NOT NULL,
  `item_code` varchar(100) DEFAULT NULL,
  `serial_number` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `adminpanel_inventoryitem`
--
ALTER TABLE `adminpanel_inventoryitem`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `item_code` (`item_code`);

--
-- Indexes for table `adminpanel_userprofile`
--
ALTER TABLE `adminpanel_userprofile`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `user_id` (`user_id`);

--
-- Indexes for table `adminpanel_usersettings`
--
ALTER TABLE `adminpanel_usersettings`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `user_id` (`user_id`);

--
-- Indexes for table `aftersales_maintenancerecord`
--
ALTER TABLE `aftersales_maintenancerecord`
  ADD PRIMARY KEY (`maintenance_id`),
  ADD KEY `aftersales_maintenan_service_record_id_9262ef8d_fk_aftersale` (`service_record_id`);

--
-- Indexes for table `aftersales_maintenancerecord_technicians`
--
ALTER TABLE `aftersales_maintenancerecord_technicians`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `aftersales_maintenancere_maintenancerecord_id_tec_dae91810_uniq` (`maintenancerecord_id`,`technician_id`),
  ADD KEY `aftersales_maintenan_technician_id_237a8d8b_fk_aftersale` (`technician_id`);

--
-- Indexes for table `aftersales_servicerecord`
--
ALTER TABLE `aftersales_servicerecord`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `service_id` (`service_id`),
  ADD KEY `aftersales_servicere_delivery_schedule_id_56a9958c_fk_delivery_` (`delivery_schedule_id`),
  ADD KEY `aftersales_servicerecord_invoice_id_c65760ed_fk_sales_invoice_id` (`invoice_id`),
  ADD KEY `aftersales_servicere_sales_order_id_7901049f_fk_sales_sal` (`sales_order_id`);

--
-- Indexes for table `aftersales_technician`
--
ALTER TABLE `aftersales_technician`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `auth_group`
--
ALTER TABLE `auth_group`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `name` (`name`);

--
-- Indexes for table `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  ADD KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`);

--
-- Indexes for table `auth_permission`
--
ALTER TABLE `auth_permission`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`);

--
-- Indexes for table `auth_user`
--
ALTER TABLE `auth_user`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`);

--
-- Indexes for table `auth_user_groups`
--
ALTER TABLE `auth_user_groups`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  ADD KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`);

--
-- Indexes for table `auth_user_user_permissions`
--
ALTER TABLE `auth_user_user_permissions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  ADD KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`);

--
-- Indexes for table `delivery_deliveryrequest`
--
ALTER TABLE `delivery_deliveryrequest`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `request_id` (`request_id`);

--
-- Indexes for table `delivery_deliveryschedule`
--
ALTER TABLE `delivery_deliveryschedule`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `schedule_id` (`schedule_id`),
  ADD KEY `delivery_deliverysch_delivery_request_id_d773f8be_fk_delivery_` (`delivery_request_id`);

--
-- Indexes for table `django_admin_log`
--
ALTER TABLE `django_admin_log`
  ADD PRIMARY KEY (`id`),
  ADD KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  ADD KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`);

--
-- Indexes for table `django_content_type`
--
ALTER TABLE `django_content_type`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`);

--
-- Indexes for table `django_migrations`
--
ALTER TABLE `django_migrations`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `django_session`
--
ALTER TABLE `django_session`
  ADD PRIMARY KEY (`session_key`),
  ADD KEY `django_session_expire_date_a5c62663` (`expire_date`);

--
-- Indexes for table `motorpool_equipmentinspection`
--
ALTER TABLE `motorpool_equipmentinspection`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `inspection_id` (`inspection_id`),
  ADD KEY `motorpool_equipmenti_pdi_request_id_6f36679c_fk_sales_req` (`pdi_request_id`);

--
-- Indexes for table `notifications_notification`
--
ALTER TABLE `notifications_notification`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `notifications_notification_read_by`
--
ALTER TABLE `notifications_notification_read_by`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `notifications_notificati_notification_id_user_id_77c19b6a_uniq` (`notification_id`,`user_id`),
  ADD KEY `notifications_notifi_user_id_99d6dcfb_fk_auth_user` (`user_id`);

--
-- Indexes for table `sales_clientrecord`
--
ALTER TABLE `sales_clientrecord`
  ADD PRIMARY KEY (`id`),
  ADD KEY `sales_clientrecord_delivery_schedule_id_ffb1a50b_fk_delivery_` (`delivery_schedule_id`),
  ADD KEY `sales_clientrecord_sales_order_id_1bcf3ad2_fk_sales_sal` (`sales_order_id`);

--
-- Indexes for table `sales_invoice`
--
ALTER TABLE `sales_invoice`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `invoice_number` (`invoice_number`),
  ADD UNIQUE KEY `order_id` (`order_id`),
  ADD KEY `sales_invoice_client_record_id_d420c446_fk_sales_clientrecord_id` (`client_record_id`);

--
-- Indexes for table `sales_orderitem`
--
ALTER TABLE `sales_orderitem`
  ADD PRIMARY KEY (`id`),
  ADD KEY `sales_orderitem_inventory_item_id_65341d25_fk_adminpane` (`inventory_item_id`),
  ADD KEY `sales_orderitem_order_id_7845449c_fk_sales_salesorder_id` (`order_id`);

--
-- Indexes for table `sales_request`
--
ALTER TABLE `sales_request`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `request_id` (`request_id`),
  ADD KEY `sales_request_requested_by_id_e9d08a08_fk_auth_user_id` (`requested_by_id`);

--
-- Indexes for table `sales_requestnote`
--
ALTER TABLE `sales_requestnote`
  ADD PRIMARY KEY (`id`),
  ADD KEY `sales_requestnote_created_by_id_22b7e88a_fk_auth_user_id` (`created_by_id`),
  ADD KEY `sales_requestnote_request_id_181c46d8_fk_sales_request_id` (`request_id`);

--
-- Indexes for table `sales_salesorder`
--
ALTER TABLE `sales_salesorder`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `order_number` (`order_number`),
  ADD KEY `sales_salesorder_client_record_id_10210614_fk_sales_cli` (`client_record_id`);

--
-- Indexes for table `warehouse_warehouseclientrecord`
--
ALTER TABLE `warehouse_warehouseclientrecord`
  ADD PRIMARY KEY (`id`),
  ADD KEY `warehouse_warehousec_delivery_schedule_id_f26c9e22_fk_delivery_` (`delivery_schedule_id`),
  ADD KEY `warehouse_warehousec_warehouse_order_id_bea27433_fk_warehouse` (`warehouse_order_id`);

--
-- Indexes for table `warehouse_warehouseinvoice`
--
ALTER TABLE `warehouse_warehouseinvoice`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `invoice_number` (`invoice_number`),
  ADD UNIQUE KEY `order_id` (`order_id`);

--
-- Indexes for table `warehouse_warehouseorder`
--
ALTER TABLE `warehouse_warehouseorder`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `order_number` (`order_number`),
  ADD KEY `warehouse_warehouseorder_created_by_id_0e52c270_fk_auth_user_id` (`created_by_id`);

--
-- Indexes for table `warehouse_warehouseorderitem`
--
ALTER TABLE `warehouse_warehouseorderitem`
  ADD PRIMARY KEY (`id`),
  ADD KEY `warehouse_warehouseo_inventory_item_id_dade5adc_fk_adminpane` (`inventory_item_id`),
  ADD KEY `warehouse_warehouseo_order_id_613d85f3_fk_warehouse` (`order_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `adminpanel_inventoryitem`
--
ALTER TABLE `adminpanel_inventoryitem`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=67;

--
-- AUTO_INCREMENT for table `adminpanel_userprofile`
--
ALTER TABLE `adminpanel_userprofile`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=51;

--
-- AUTO_INCREMENT for table `adminpanel_usersettings`
--
ALTER TABLE `adminpanel_usersettings`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12;

--
-- AUTO_INCREMENT for table `aftersales_maintenancerecord_technicians`
--
ALTER TABLE `aftersales_maintenancerecord_technicians`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=42;

--
-- AUTO_INCREMENT for table `aftersales_servicerecord`
--
ALTER TABLE `aftersales_servicerecord`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=39;

--
-- AUTO_INCREMENT for table `aftersales_technician`
--
ALTER TABLE `aftersales_technician`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=31;

--
-- AUTO_INCREMENT for table `auth_group`
--
ALTER TABLE `auth_group`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT for table `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `auth_permission`
--
ALTER TABLE `auth_permission`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=121;

--
-- AUTO_INCREMENT for table `auth_user`
--
ALTER TABLE `auth_user`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `auth_user_groups`
--
ALTER TABLE `auth_user_groups`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=95;

--
-- AUTO_INCREMENT for table `auth_user_user_permissions`
--
ALTER TABLE `auth_user_user_permissions`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `delivery_deliveryrequest`
--
ALTER TABLE `delivery_deliveryrequest`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=164;

--
-- AUTO_INCREMENT for table `delivery_deliveryschedule`
--
ALTER TABLE `delivery_deliveryschedule`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=87;

--
-- AUTO_INCREMENT for table `django_admin_log`
--
ALTER TABLE `django_admin_log`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=56;

--
-- AUTO_INCREMENT for table `django_content_type`
--
ALTER TABLE `django_content_type`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=31;

--
-- AUTO_INCREMENT for table `django_migrations`
--
ALTER TABLE `django_migrations`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=72;

--
-- AUTO_INCREMENT for table `motorpool_equipmentinspection`
--
ALTER TABLE `motorpool_equipmentinspection`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=77;

--
-- AUTO_INCREMENT for table `notifications_notification`
--
ALTER TABLE `notifications_notification`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=309;

--
-- AUTO_INCREMENT for table `notifications_notification_read_by`
--
ALTER TABLE `notifications_notification_read_by`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=451;

--
-- AUTO_INCREMENT for table `sales_clientrecord`
--
ALTER TABLE `sales_clientrecord`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=36;

--
-- AUTO_INCREMENT for table `sales_invoice`
--
ALTER TABLE `sales_invoice`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=121;

--
-- AUTO_INCREMENT for table `sales_orderitem`
--
ALTER TABLE `sales_orderitem`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=220;

--
-- AUTO_INCREMENT for table `sales_request`
--
ALTER TABLE `sales_request`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=115;

--
-- AUTO_INCREMENT for table `sales_requestnote`
--
ALTER TABLE `sales_requestnote`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=103;

--
-- AUTO_INCREMENT for table `sales_salesorder`
--
ALTER TABLE `sales_salesorder`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=134;

--
-- AUTO_INCREMENT for table `warehouse_warehouseclientrecord`
--
ALTER TABLE `warehouse_warehouseclientrecord`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `warehouse_warehouseinvoice`
--
ALTER TABLE `warehouse_warehouseinvoice`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=27;

--
-- AUTO_INCREMENT for table `warehouse_warehouseorder`
--
ALTER TABLE `warehouse_warehouseorder`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=37;

--
-- AUTO_INCREMENT for table `warehouse_warehouseorderitem`
--
ALTER TABLE `warehouse_warehouseorderitem`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=44;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `adminpanel_userprofile`
--
ALTER TABLE `adminpanel_userprofile`
  ADD CONSTRAINT `adminpanel_userprofile_user_id_30679c46_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Constraints for table `adminpanel_usersettings`
--
ALTER TABLE `adminpanel_usersettings`
  ADD CONSTRAINT `adminpanel_usersettings_user_id_19556484_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Constraints for table `aftersales_maintenancerecord`
--
ALTER TABLE `aftersales_maintenancerecord`
  ADD CONSTRAINT `aftersales_maintenan_service_record_id_9262ef8d_fk_aftersale` FOREIGN KEY (`service_record_id`) REFERENCES `aftersales_servicerecord` (`id`);

--
-- Constraints for table `aftersales_maintenancerecord_technicians`
--
ALTER TABLE `aftersales_maintenancerecord_technicians`
  ADD CONSTRAINT `aftersales_maintenan_maintenancerecord_id_06acad01_fk_aftersale` FOREIGN KEY (`maintenancerecord_id`) REFERENCES `aftersales_maintenancerecord` (`maintenance_id`),
  ADD CONSTRAINT `aftersales_maintenan_technician_id_237a8d8b_fk_aftersale` FOREIGN KEY (`technician_id`) REFERENCES `aftersales_technician` (`id`);

--
-- Constraints for table `aftersales_servicerecord`
--
ALTER TABLE `aftersales_servicerecord`
  ADD CONSTRAINT `aftersales_servicere_delivery_schedule_id_56a9958c_fk_delivery_` FOREIGN KEY (`delivery_schedule_id`) REFERENCES `delivery_deliveryschedule` (`id`),
  ADD CONSTRAINT `aftersales_servicere_sales_order_id_7901049f_fk_sales_sal` FOREIGN KEY (`sales_order_id`) REFERENCES `sales_salesorder` (`id`),
  ADD CONSTRAINT `aftersales_servicerecord_invoice_id_c65760ed_fk_sales_invoice_id` FOREIGN KEY (`invoice_id`) REFERENCES `sales_invoice` (`id`);

--
-- Constraints for table `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  ADD CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  ADD CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`);

--
-- Constraints for table `auth_permission`
--
ALTER TABLE `auth_permission`
  ADD CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`);

--
-- Constraints for table `auth_user_groups`
--
ALTER TABLE `auth_user_groups`
  ADD CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  ADD CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Constraints for table `auth_user_user_permissions`
--
ALTER TABLE `auth_user_user_permissions`
  ADD CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  ADD CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Constraints for table `delivery_deliveryschedule`
--
ALTER TABLE `delivery_deliveryschedule`
  ADD CONSTRAINT `delivery_deliverysch_delivery_request_id_d773f8be_fk_delivery_` FOREIGN KEY (`delivery_request_id`) REFERENCES `delivery_deliveryrequest` (`id`);

--
-- Constraints for table `django_admin_log`
--
ALTER TABLE `django_admin_log`
  ADD CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  ADD CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Constraints for table `motorpool_equipmentinspection`
--
ALTER TABLE `motorpool_equipmentinspection`
  ADD CONSTRAINT `motorpool_equipmenti_pdi_request_id_6f36679c_fk_sales_req` FOREIGN KEY (`pdi_request_id`) REFERENCES `sales_request` (`id`);

--
-- Constraints for table `notifications_notification_read_by`
--
ALTER TABLE `notifications_notification_read_by`
  ADD CONSTRAINT `notifications_notifi_notification_id_a2eba8c3_fk_notificat` FOREIGN KEY (`notification_id`) REFERENCES `notifications_notification` (`id`),
  ADD CONSTRAINT `notifications_notifi_user_id_99d6dcfb_fk_auth_user` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Constraints for table `sales_clientrecord`
--
ALTER TABLE `sales_clientrecord`
  ADD CONSTRAINT `sales_clientrecord_delivery_schedule_id_ffb1a50b_fk_delivery_` FOREIGN KEY (`delivery_schedule_id`) REFERENCES `delivery_deliveryschedule` (`id`),
  ADD CONSTRAINT `sales_clientrecord_sales_order_id_1bcf3ad2_fk_sales_sal` FOREIGN KEY (`sales_order_id`) REFERENCES `sales_salesorder` (`id`);

--
-- Constraints for table `sales_invoice`
--
ALTER TABLE `sales_invoice`
  ADD CONSTRAINT `sales_invoice_client_record_id_d420c446_fk_sales_clientrecord_id` FOREIGN KEY (`client_record_id`) REFERENCES `sales_clientrecord` (`id`),
  ADD CONSTRAINT `sales_invoice_order_id_3db25fae_fk_sales_salesorder_id` FOREIGN KEY (`order_id`) REFERENCES `sales_salesorder` (`id`);

--
-- Constraints for table `sales_orderitem`
--
ALTER TABLE `sales_orderitem`
  ADD CONSTRAINT `sales_orderitem_inventory_item_id_65341d25_fk_adminpane` FOREIGN KEY (`inventory_item_id`) REFERENCES `adminpanel_inventoryitem` (`id`),
  ADD CONSTRAINT `sales_orderitem_order_id_7845449c_fk_sales_salesorder_id` FOREIGN KEY (`order_id`) REFERENCES `sales_salesorder` (`id`);

--
-- Constraints for table `sales_request`
--
ALTER TABLE `sales_request`
  ADD CONSTRAINT `sales_request_requested_by_id_e9d08a08_fk_auth_user_id` FOREIGN KEY (`requested_by_id`) REFERENCES `auth_user` (`id`);

--
-- Constraints for table `sales_requestnote`
--
ALTER TABLE `sales_requestnote`
  ADD CONSTRAINT `sales_requestnote_created_by_id_22b7e88a_fk_auth_user_id` FOREIGN KEY (`created_by_id`) REFERENCES `auth_user` (`id`),
  ADD CONSTRAINT `sales_requestnote_request_id_181c46d8_fk_sales_request_id` FOREIGN KEY (`request_id`) REFERENCES `sales_request` (`id`);

--
-- Constraints for table `sales_salesorder`
--
ALTER TABLE `sales_salesorder`
  ADD CONSTRAINT `sales_salesorder_client_record_id_10210614_fk_sales_cli` FOREIGN KEY (`client_record_id`) REFERENCES `sales_clientrecord` (`id`);

--
-- Constraints for table `warehouse_warehouseclientrecord`
--
ALTER TABLE `warehouse_warehouseclientrecord`
  ADD CONSTRAINT `warehouse_warehousec_delivery_schedule_id_f26c9e22_fk_delivery_` FOREIGN KEY (`delivery_schedule_id`) REFERENCES `delivery_deliveryschedule` (`id`),
  ADD CONSTRAINT `warehouse_warehousec_warehouse_order_id_bea27433_fk_warehouse` FOREIGN KEY (`warehouse_order_id`) REFERENCES `warehouse_warehouseorder` (`id`);

--
-- Constraints for table `warehouse_warehouseinvoice`
--
ALTER TABLE `warehouse_warehouseinvoice`
  ADD CONSTRAINT `warehouse_warehousei_order_id_eeda38bd_fk_warehouse` FOREIGN KEY (`order_id`) REFERENCES `warehouse_warehouseorder` (`id`);

--
-- Constraints for table `warehouse_warehouseorder`
--
ALTER TABLE `warehouse_warehouseorder`
  ADD CONSTRAINT `warehouse_warehouseorder_created_by_id_0e52c270_fk_auth_user_id` FOREIGN KEY (`created_by_id`) REFERENCES `auth_user` (`id`);

--
-- Constraints for table `warehouse_warehouseorderitem`
--
ALTER TABLE `warehouse_warehouseorderitem`
  ADD CONSTRAINT `warehouse_warehouseo_inventory_item_id_dade5adc_fk_adminpane` FOREIGN KEY (`inventory_item_id`) REFERENCES `adminpanel_inventoryitem` (`id`),
  ADD CONSTRAINT `warehouse_warehouseo_order_id_613d85f3_fk_warehouse` FOREIGN KEY (`order_id`) REFERENCES `warehouse_warehouseorder` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
