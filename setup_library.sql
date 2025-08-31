-- ============================================================
-- Setup Script for LIBRARY Database
-- Drops existing DB and recreates with required tables
-- ============================================================

-- Drop database if it exists
DROP DATABASE IF EXISTS LIBRARY;

-- Create LIBRARY database
CREATE DATABASE LIBRARY;

-- Use the database LIBRARY;
USE LIBRARY;

-- ============================================================
-- Members Table
-- ============================================================

CREATE TABLE MEMBERS (
    member_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE,
    phone VARCHAR(10) NOT NULL,
    address VARCHAR(10),
    join_date DATE DEFAULT (CURRENT_DATE),
    subscription_start DATE DEFAULT (CURRENT_DATE),
    subscription_end DATE GENERATED ALWAYS AS (DATE_ADD(subscription_start, INTERVAL 30 DAY)) STORED
);

-- ============================================================
-- Staff Table
-- ============================================================

CREATE TABLE STAFF (
    staff_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE,
    phone VARCHAR(100) NOT NULL,
    address VARCHAR(100) NOT NULL,
    join_date DATE DEFAULT (CURRENT_DATE)
)

CREATE TABLE STAFF_SALARY (
    staff_id INT PRIMARY KEY,
    salary VARCHAR(10) NOT NULL,
    salary_paid DATE DEFAULT (CURRENT_DATE),
    salary_due DATE GENERATED ALWAYS AS (DATE_ADD(salary_paid, INTERVAL 7 DAY)) STORED,
    FOREIGN KEY (staff_id) REFERENCES STAFF(staff_id) ON DELETE CASCADE
)
 
-- ============================================================
-- Books Table
-- ============================================================

CREATE TABLE BOOKS (
    book_id INT AUTO_INCREMENT PRIMARY_KEY,
    name VARCHAR(100) NOT NULL,
    author VARCHAR(100) NOT NULL,
    publication VARCHAR(100) NOT NULL,
    copies INT,
    lent_copies INT,
    available copies INT GENERATED ALWAYS AS (copies - lent_copies) STORED,
    date_added DATE DEFAULT (CURRENT_DATE) 
)
