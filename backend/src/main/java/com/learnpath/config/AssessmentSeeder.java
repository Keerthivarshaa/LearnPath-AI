package com.learnpath.config;

import com.learnpath.model.*;
import com.learnpath.repository.QuestionRepository;
import org.springframework.boot.CommandLineRunner;
import org.springframework.stereotype.Component;
import java.util.Arrays;

@Component
public class AssessmentSeeder implements CommandLineRunner {

    private final QuestionRepository questionRepository;

    public AssessmentSeeder(QuestionRepository questionRepository) {
        this.questionRepository = questionRepository;
    }

    @Override
    public void run(String... args) {
        if (questionRepository.count() == 0) {
            seedQuestions();
        }
    }

    private void seedQuestions() {
        // --- 1. AWS Certified Solutions Architect ---
        Question awsQ1 = new Question(
                "Which of the following service models represents AWS EC2?",
                "EC2 Instance Models",
                "Cloud",
                Difficulty.BEGINNER,
                "AWS Elastic Compute Cloud (EC2) provides virtualized computing infrastructure over the internet, classifying it under Infrastructure as a Service (IaaS).",
                1,
                "AWS Certified Solutions Architect"
        );
        awsQ1.addOption(new Option("SaaS (Software as a Service)", false));
        awsQ1.addOption(new Option("PaaS (Platform as a Service)", false));
        awsQ1.addOption(new Option("IaaS (Infrastructure as a Service)", true));
        awsQ1.addOption(new Option("FaaS (Function as a Service)", false));

        Question awsQ2 = new Question(
                "What is the primary function of an IAM Role in AWS?",
                "IAM Security",
                "Security",
                Difficulty.INTERMEDIATE,
                "IAM Roles do not have credentials (password or access keys) associated with them. Instead, they provide temporary security credentials for trusted entities.",
                2,
                "AWS Certified Solutions Architect"
        );
        awsQ2.addOption(new Option("Providing permanent credentials to external systems", false));
        awsQ2.addOption(new Option("Providing temporary security credentials for resources or users", true));
        awsQ2.addOption(new Option("Enabling single sign-on (SSO) globally", false));
        awsQ2.addOption(new Option("Logging account api access calls", false));

        Question awsQ3 = new Question(
                "Which database feature helps improve read scalability in Amazon RDS?",
                "RDS Scalability",
                "Databases",
                Difficulty.INTERMEDIATE,
                "Read Replicas allow read workloads to be offloaded from the primary database instance, thereby improving read performance and scalability.",
                3,
                "AWS Certified Solutions Architect"
        );
        awsQ3.addOption(new Option("Multi-AZ Deployments", false));
        awsQ3.addOption(new Option("Read Replicas", true));
        awsQ3.addOption(new Option("DB Subnet Groups", false));
        awsQ3.addOption(new Option("VPC Peering", false));


        // --- 2. Oracle Certified Professional Java SE 17 ---
        Question javaQ1 = new Question(
                "Which Garbage Collection (GC) algorithm is the default collector starting in Java 9 through Java 17?",
                "Garbage Collection",
                "Core Java",
                Difficulty.BEGINNER,
                "Garbage-First (G1) GC is the default garbage collector algorithm in modern JVM editions since JDK 9.",
                1,
                "Oracle Certified Professional Java SE 17"
        );
        javaQ1.addOption(new Option("Serial Garbage Collector", false));
        javaQ1.addOption(new Option("G1 (Garbage-First) Collector", true));
        javaQ1.addOption(new Option("ZGC (Z Garbage Collector)", false));
        javaQ1.addOption(new Option("Parallel Garbage Collector", false));

        Question javaQ2 = new Question(
                "Which pattern matching enhancement is standard in Java 17?",
                "Pattern Matching",
                "Core Java",
                Difficulty.INTERMEDIATE,
                "Pattern matching for instanceof became standard in Java 16, and pattern matching for switch statement syntax was introduced in preview in Java 17.",
                2,
                "Oracle Certified Professional Java SE 17"
        );
        javaQ2.addOption(new Option("Pattern matching for 'instanceof'", true));
        javaQ2.addOption(new Option("Pattern matching for 'select' statements", false));
        javaQ2.addOption(new Option("Pattern matching for 'catch' blocks", false));
        javaQ2.addOption(new Option("Pattern matching for multi-line strings", false));

        Question javaQ3 = new Question(
                "What is the default JDBC Connection Pool library configured by Spring Boot starter JDBC?",
                "JDBC Pools",
                "Databases",
                Difficulty.INTERMEDIATE,
                "Spring Boot automatically configures HikariCP as the default connection pool because of its superior performance and lightweight signature.",
                3,
                "Oracle Certified Professional Java SE 17"
        );
        javaQ3.addOption(new Option("Commons DBCP2", false));
        javaQ3.addOption(new Option("Tomcat JDBC Pool", false));
        javaQ3.addOption(new Option("HikariCP", true));
        javaQ3.addOption(new Option("C3P0", false));


        // --- 3. CompTIA Security+ ---
        Question secQ1 = new Question(
                "Which hashing algorithm is widely used to verify the cryptographic integrity of files?",
                "Cryptography",
                "Security",
                Difficulty.BEGINNER,
                "SHA-256 (Secure Hash Algorithm) is a widely accepted standard for verifying data integrity and checksum validations.",
                1,
                "CompTIA Security+"
        );
        secQ1.addOption(new Option("AES", false));
        secQ1.addOption(new Option("RSA", false));
        secQ1.addOption(new Option("SHA-256", true));
        secQ1.addOption(new Option("Diffie-Hellman", false));

        Question secQ2 = new Question(
                "What is the primary purpose of a DMZ (Demilitarized Zone) on a corporate network?",
                "Network Security",
                "Networking",
                Difficulty.INTERMEDIATE,
                "A DMZ isolates public-facing servers (like web or mail servers) from the private internal network, providing an extra layer of security.",
                2,
                "CompTIA Security+"
        );
        secQ2.addOption(new Option("To host public-facing servers while isolating internal networks", true));
        secQ2.addOption(new Option("To block all incoming traffic using stateful inspection", false));
        secQ2.addOption(new Option("To encrypt internal router communications", false));
        secQ2.addOption(new Option("To store database backups offsite", false));


        // --- 4. Azure Fundamentals AZ-900 ---
        Question azQ1 = new Question(
                "Which Azure service is optimized for storing large volumes of unstructured data like media assets?",
                "Azure Storage",
                "Cloud",
                Difficulty.BEGINNER,
                "Azure Blob Storage is optimized for storing massive amounts of unstructured object data, such as images, audio, and videos.",
                1,
                "Azure Fundamentals AZ-900"
        );
        azQ1.addOption(new Option("Azure SQL Database", false));
        azQ1.addOption(new Option("Azure Blob Storage", true));
        azQ1.addOption(new Option("Azure Cosmos DB", false));
        azQ1.addOption(new Option("Azure Table Storage", false));

        Question azQ2 = new Question(
                "What is a set of datacenters deployed within a latency-defined perimeter in Microsoft Azure?",
                "Azure Regions",
                "Cloud",
                Difficulty.BEGINNER,
                "An Azure Region is a geographical area containing one or more datacenters connected through a low-latency network.",
                2,
                "Azure Fundamentals AZ-900"
        );
        azQ2.addOption(new Option("Availability Zone", false));
        azQ2.addOption(new Option("Azure Region", true));
        azQ2.addOption(new Option("Resource Group", false));
        azQ2.addOption(new Option("Subscription boundary", false));


        questionRepository.saveAll(Arrays.asList(
                awsQ1, awsQ2, awsQ3,
                javaQ1, javaQ2, javaQ3,
                secQ1, secQ2,
                azQ1, azQ2
        ));
    }
}
