package com.learnpath.service;

import com.learnpath.dto.ChatMessage;
import com.learnpath.model.Progress;
import com.learnpath.model.User;
import org.springframework.stereotype.Component;
import java.util.List;

@Component
public class RuleBasedChatProvider implements ChatProvider {

    @Override
    public String generateResponse(User user, Progress progress, List<ChatMessage> history, String userMessage) {
        String msg = userMessage.toLowerCase().trim();
        String goal = user.getCertificationGoal();

        // 1. AWS IAM / Security queries
        if (msg.contains("iam") || msg.contains("security") || msg.contains("policy") || msg.contains("role")) {
            return "### AWS Identity and Access Management (IAM)\n\n" +
                    "Since you are studying for **" + goal + "** and have security requirements, here is a detailed review of AWS IAM security policies.\n\n" +
                    "#### IAM Credentials Principle\n" +
                    "Always enforce the **Principle of Least Privilege**. Never use the root account for daily activities, enforce MFA, and grant temporary credentials using IAM Roles instead of permanent access keys.\n\n" +
                    "#### Sample IAM Policy JSON\n" +
                    "Here is a policy configuration block allowing read-only access to a specific S3 bucket:\n\n" +
                    "```json\n" +
                    "{\n" +
                    "  \"Version\": \"2012-10-17\",\n" +
                    "  \"Statement\": [\n" +
                    "    {\n" +
                    "      \"Effect\": \"Allow\",\n" +
                    "      \"Action\": [\n" +
                    "        \"s3:GetObject\",\n" +
                    "        \"s3:ListBucket\"\n" +
                    "      ],\n" +
                    "      \"Resource\": [\n" +
                    "        \"arn:aws:s3:::learnpath-static-content\",\n" +
                    "        \"arn:aws:s3:::learnpath-static-content/*\"\n" +
                    "      ]\n" +
                    "    }\n" +
                    "  ]\n" +
                    "}\n" +
                    "```\n\n" +
                    "#### Core Best Practices:\n" +
                    "- **IAM Roles**: Use roles for EC2 instances and Lambda functions to eliminate hardcoded credentials.\n" +
                    "- **MFA**: Enforce Multi-Factor Authentication on all admin accounts.\n" +
                    "- **Access Analyzer**: Monitor access logs to detect overly permissive permissions.";
        }

        // 2. AWS EC2 queries
        if (msg.contains("ec2") || msg.contains("instance") || msg.contains("compute")) {
            return "### Amazon Elastic Compute Cloud (EC2)\n\n" +
                    "EC2 represents Infrastructure as a Service (IaaS). Let's review the purchasing configurations for your **" + goal + "** path:\n\n" +
                    "#### EC2 Purchase Models Comparison\n\n" +
                    "| Pricing Model | Cost Discount | Ideal Use Case |\n" +
                    "| :--- | :--- | :--- |\n" +
                    "| **On-Demand** | Base Rate | Short-term spiky workloads that cannot be interrupted. |\n" +
                    "| **Reserved** | Up to 72% off | Constant steady-state usage with 1 or 3-year commitment. |\n" +
                    "| **Spot** | Up to 90% off | Batch computing, stateless jobs, and testing. Can be interrupted with 2min notice. |\n" +
                    "| **Dedicated Hosts** | Minimal | Compliance requirements requiring physical hardware isolation. |\n\n" +
                    "#### Simple CLI commands\n" +
                    "You can launch an instance using the AWS CLI:\n" +
                    "```bash\n" +
                    "aws ec2 run-instances --image-id ami-0c55b159cbfafe1f0 --count 1 --instance-type t2.micro\n" +
                    "```";
        }

        // 3. RDS / Database queries
        if (msg.contains("rds") || msg.contains("database") || msg.contains("sql") || msg.contains("postgres") || msg.contains("scaling")) {
            return "### Relational Database Services & Performance Scaling\n\n" +
                    "To support high read throughput or fault tolerance, databases must implement proper scalability patterns.\n\n" +
                    "#### Multi-AZ vs Read Replicas\n" +
                    "- **Multi-AZ Deployments**: Synchrounous replication to a standby instance in a different AZ. Primarily for **High Availability and Disaster Recovery (DR)**.\n" +
                    "- **Read Replicas**: Asynchronous replication to multiple read-only instances. Primarily for **Read Scaling and performance enhancement**.\n\n" +
                    "#### Database Performance Tuning\n" +
                    "Add indexing to avoid full-table scans on query lookups:\n\n" +
                    "```sql\n" +
                    "-- Create indexing for email matching on user table\n" +
                    "CREATE INDEX idx_user_email ON users(email);\n" +
                    "\n" +
                    "-- View query explanation strategy\n" +
                    "EXPLAIN ANALYZE SELECT * FROM users WHERE email = 'test@example.com';\n" +
                    "```";
        }

        // 4. Java JVM / Garbage Collection queries
        if (msg.contains("java") || msg.contains("garbage") || msg.contains("gc") || msg.contains("jvm")) {
            return "### JVM Tuning & Garbage Collection (GC)\n\n" +
                    "Since your preparation track involves **Oracle Certified Java SE 17**, JVM memory management is a key syllabus criteria.\n\n" +
                    "#### Garbage Collection Algorithms\n" +
                    "- **Serial GC**: Single-threaded, ideal for simple CLI scripts and tiny heaps.\n" +
                    "- **Parallel GC**: Multi-threaded collector optimized for high batch throughput.\n" +
                    "- **G1 GC (Garbage-First)**: Segmented heap memory. Balances high throughput with low response times.\n" +
                    "- **ZGC (Z Garbage Collector)**: Ultra-low latency collector supporting petabyte heaps with pausing times under 1 millisecond.\n\n" +
                    "#### GC Execution JVM Options\n" +
                    "```bash\n" +
                    "# Run Java app with G1 Garbage Collector and 4GB Heap bounds\n" +
                    "java -XX:+UseG1GC -Xms4g -Xmx4g -jar learnpath-app.jar\n" +
                    "```";
        }

        // 5. VPC / Network queries
        if (msg.contains("vpc") || msg.contains("network") || msg.contains("subnet")) {
            return "### Virtual Private Cloud (VPC) Networking\n\n" +
                    "A VPC allows you to provision logically isolated networks on the AWS Cloud.\n\n" +
                    "#### Network Subnets\n" +
                    "- **Public Subnets**: Subnets that have a route pointing directly to an **Internet Gateway (IGW)**, granting direct inbound and outbound web access.\n" +
                    "- **Private Subnets**: Isolated subnets. To gain outbound internet access (e.g. download patches) without exposing resources, private subnets must route traffic through a **NAT Gateway** residing in a public subnet.";
        }

        // 6. Practice mock question
        if (msg.contains("question") || msg.contains("practice") || msg.contains("quiz") || msg.contains("mock")) {
            return "### Dynamic Practice Quiz\n\n" +
                    "Here is a mock question tailored to your goal **" + goal + "**:\n\n" +
                    "**Question:** An application requires constant steady-state compute resources for a duration of 3 years. Which purchase option provides the highest cost savings?\n\n" +
                    "- A) On-Demand Instances\n" +
                    "- B) Spot Instances\n" +
                    "- C) Reserved Instances (3-Year Commitment)\n" +
                    "- D) Dedicated Hosts\n\n" +
                    "**Correct Answer: C**\n\n" +
                    "**Explanation:** Reserved Instances provide a significant discount (up to 72%) compared to On-Demand instances in exchange for a commitment to a steady-state instance type for 1 or 3 years. Spot instances are cheaper but can be interrupted, making them unsuitable for steady-state applications.";
        }

        // Default greeting / advice reply
        return "### Welcome to your AI Tutoring Console!\n\n" +
                "I am your personal AI Tutor. I analyze your certification goal (**" + goal + "**), current skill level (**" + user.getCurrentLevel() + "**), and preparation history to answer your questions.\n\n" +
                "Here are some topics we can discuss based on your syllabus:\n" +
                "- **Cloud Architecture**: VPCs, subnets, EC2 pricing models, or S3 tiers.\n" +
                "- **Security**: IAM Roles, AWS Key Management Service (KMS), and security groups.\n" +
                "- **Database tuning**: Read Replicas vs Multi-AZ deployments, indexing, or SQL optimization.\n" +
                "- **Java development**: JVM memory models, garbage collection tuning, or pattern matching syntax.\n\n" +
                "**What topic would you like to deep-dive into today?** Ask a question, or select one of the suggested prompts below!";
    }
}
