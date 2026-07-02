-- Database Setup Script for LearnPath AI
-- Run this inside PostgreSQL to initialize the schema

-- Drop table if exists
DROP TABLE IF EXISTS users CASCADE;

-- Create Users Table
CREATE TABLE users (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    certification_goal VARCHAR(255) DEFAULT 'General Developer Certification',
    study_hours_per_week INTEGER DEFAULT 10,
    current_level VARCHAR(50) DEFAULT 'Beginner'
);
