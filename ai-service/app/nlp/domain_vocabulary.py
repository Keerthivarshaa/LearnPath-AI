"""
Certification domain vocabulary - Module 4 (NLP Pipeline).

Data only, no logic. Seeds entity_recognizer.py's PhraseMatcher so
domain-specific terms (which spaCy's general-purpose statistical NER
does not meaningfully recognize - see the Section 1 design discussion)
get tagged as entities too.

Mirrors topic names already used across the Java backend
(AssessmentSeeder.java, RuleBasedRoadmapGenerator.java,
ProgressService.java, RuleBasedChatProvider.java's keyword triggers),
plus common shorthand/acronym forms a user would actually type in chat
(e.g. "IAM" as well as "IAM Security").

NOTE: this is a deliberate, acknowledged duplication of vocabulary that
already exists (inconsistently) across several Java files - Python
can't import Java constants directly, and consolidating that vocabulary
into one shared source of truth is a separate, larger change (flagged
in the original architecture review, Finding 6) that touches Java code
and is out of scope for this module.

Each canonical topic maps to the surface forms that should resolve to
it, so entity_recognizer.py's output stays normalized - a user typing
"IAM" or "IAM Security" both resolve to the single canonical topic
"IAM Security".
"""

from typing import Dict, List

DOMAIN_TOPICS: Dict[str, List[str]] = {
    "IAM Security": [
        "iam", "iam security", "identity and access management", "iam role", "iam policy",
    ],
    "EC2 Instance Models": [
        "ec2", "ec2 instance", "elastic compute cloud",
    ],
    "RDS Scalability": [
        "rds", "amazon rds", "read replica", "read replicas", "multi-az",
    ],
    "VPC Networking": [
        "vpc", "virtual private cloud", "subnet", "subnets", "nat gateway",
    ],
    "Cloud Basics": [
        "cloud computing", "cloud basics",
    ],
    "Garbage Collection": [
        "garbage collection", "gc", "g1gc", "g1 garbage collector", "zgc",
    ],
    "Pattern Matching": [
        "pattern matching", "instanceof",
    ],
    "JDBC Pools": [
        "jdbc", "jdbc pool", "hikaricp", "connection pool",
    ],
    "Database Basics": [
        "database", "databases", "sql", "postgres", "postgresql",
    ],
    "Cryptography": [
        "cryptography", "encryption", "sha-256", "hashing",
    ],
    "Network Security": [
        "dmz", "firewall", "network security", "security group", "nacl",
    ],
    "Azure Storage": [
        "azure blob storage", "azure storage",
    ],
    "Azure Regions": [
        "azure region", "availability zone",
    ],
    "Azure Governance": [
        "azure governance", "resource group",
    ],
}
