package com.learnpath.service;

import com.learnpath.dto.MilestoneDTO;
import com.learnpath.dto.RecommendationDTO;
import com.learnpath.model.AssessmentResult;
import com.learnpath.model.User;
import org.springframework.stereotype.Component;

import java.util.*;

@Component
public class RuleBasedRoadmapGenerator implements RoadmapGenerator {

    @Override
    public RecommendationDTO generate(User user, AssessmentResult latestResult, List<AssessmentResult> history) {
        String goal = user.getCertificationGoal();
        Integer studyHours = user.getStudyHoursPerWeek() != null ? user.getStudyHoursPerWeek() : 10;
        String level = user.getCurrentLevel() != null ? user.getCurrentLevel() : "Beginner";

        // 1. Check if user needs onboarding (no assessment taken)
        if (latestResult == null) {
            return generateOnboardingRoadmap(goal, studyHours, level);
        }

        // 2. Fetch baseline milestones templates for the user's specific goal
        List<MilestoneDTO> templates = getMilestonesTemplate(goal);
        List<String> strongTopics = latestResult.getStrongTopics();
        List<String> weakTopics = latestResult.getWeakTopics();

        List<MilestoneDTO> generatedMilestones = new ArrayList<>();
        int totalHours = 0;
        int completedHours = 0;
        boolean hasSetInProgress = false;

        // Classify milestone status based on test answers
        for (int i = 0; i < templates.size(); i++) {
            MilestoneDTO template = templates.get(i);
            String topic = template.getTopic();
            totalHours += template.getEstimatedHours();

            String status = "LOCKED";
            if (strongTopics.contains(topic)) {
                status = "COMPLETED";
                completedHours += template.getEstimatedHours();
            } else if (!hasSetInProgress) {
                status = "IN_PROGRESS";
                hasSetInProgress = true;
            }

            template.setStatus(status);
            template.setDisplayOrder(i + 1);
            generatedMilestones.add(template);
        }

        // If all template milestones are completed, fallback to make the last one active
        if (!hasSetInProgress && !generatedMilestones.isEmpty()) {
            generatedMilestones.get(generatedMilestones.size() - 1).setStatus("IN_PROGRESS");
            completedHours -= generatedMilestones.get(generatedMilestones.size() - 1).getEstimatedHours();
        }

        // Calculations
        int remainingHours = totalHours - completedHours;
        double completionPercent = Math.round(((double) completedHours / totalHours) * 100.0);
        int completionWeeks = (int) Math.ceil((double) remainingHours / studyHours);
        if (completionWeeks <= 0) completionWeeks = 1;

        // Daily Plan formulation
        double dailyHours = Math.round((double) studyHours / 7.0 * 10.0) / 10.0;
        String currentTopic = generatedMilestones.stream()
                .filter(m -> "IN_PROGRESS".equals(m.getStatus()))
                .map(MilestoneDTO::getTopic)
                .findFirst()
                .orElse("Target Topics");
        String dailyPlan = String.format("Dedicate %s hours daily. Focus primarily on the active module: %s.", dailyHours, currentTopic);

        // Next recommended assessment
        String nextAssessment = goal + " Practice Exam";

        // Priority Topics
        List<String> priorityTopics = new ArrayList<>(weakTopics);
        for (MilestoneDTO m : generatedMilestones) {
            if (!priorityTopics.contains(m.getTopic()) && !strongTopics.contains(m.getTopic())) {
                priorityTopics.add(m.getTopic());
            }
        }

        // Weekly schedule mapper
        Map<String, String> weeklyPlan = new LinkedHashMap<>();
        weeklyPlan.put("Week 1", "Deep-dive into current active focus topic: " + currentTopic);
        weeklyPlan.put("Week 2", "Resolve prerequisites and study core architectural metrics.");
        weeklyPlan.put("Week 3", "Integrate databases, build secure policies, and trace system workflows.");
        weeklyPlan.put("Week 4", "Attempt mock test simulator and check metrics analytics.");

        return new RecommendationDTO(
                goal,
                level,
                studyHours,
                completionWeeks,
                completionPercent,
                dailyPlan,
                nextAssessment,
                priorityTopics,
                generatedMilestones,
                weeklyPlan,
                false
        );
    }

    private RecommendationDTO generateOnboardingRoadmap(String goal, Integer studyHours, String level) {
        List<MilestoneDTO> milestones = new ArrayList<>();
        milestones.add(new MilestoneDTO(
                "Diagnostic Quiz",
                "Onboarding",
                "BEGINNER",
                1,
                Collections.emptyList(),
                Arrays.asList("Diagnostic Test Portal"),
                "IN_PROGRESS",
                1
        ));
        milestones.add(new MilestoneDTO(
                "Skill Gap Assessment",
                "Onboarding",
                "BEGINNER",
                2,
                Arrays.asList("Diagnostic Quiz"),
                Arrays.asList("Weak topics metrics summary board"),
                "LOCKED",
                2
        ));
        milestones.add(new MilestoneDTO(
                "AI Learning Path Orchestration",
                "Onboarding",
                "BEGINNER",
                1,
                Arrays.asList("Skill Gap Assessment"),
                Arrays.asList("Personalized study nodes list"),
                "LOCKED",
                3
        ));

        Map<String, String> weeklyPlan = new LinkedHashMap<>();
        weeklyPlan.put("Step 1", "Start the 3-question diagnostic quiz in the Assessment tab.");
        weeklyPlan.put("Step 2", "Review calculated weak and strong topics on the scorecard.");
        weeklyPlan.put("Step 3", "Access this path console again to view your tailored roadmap.");

        return new RecommendationDTO(
                goal,
                level,
                studyHours,
                1,
                0.0,
                "Spend 15 minutes to complete your Diagnostic Assessment today.",
                "Diagnostic Skill Assessment",
                Arrays.asList("General Cloud", "Coding basics", "SQL Queries"),
                milestones,
                weeklyPlan,
                true
        );
    }

    private List<MilestoneDTO> getMilestonesTemplate(String goal) {
        List<MilestoneDTO> milestones = new ArrayList<>();

        if (goal.contains("Solutions Architect")) {
            milestones.add(new MilestoneDTO(
                    "AWS Cloud Infrastructure Basics",
                    "Cloud",
                    "BEGINNER",
                    12,
                    Collections.emptyList(),
                    Arrays.asList("AWS Cloud Practitioner Essentials", "AWS EC2 User Guide"),
                    "LOCKED",
                    1
            ));
            milestones.get(0).setTopic("EC2 Instance Models");

            milestones.add(new MilestoneDTO(
                    "Identity Access Management & Security",
                    "Security",
                    "INTERMEDIATE",
                    8,
                    Arrays.asList("AWS Cloud Infrastructure Basics"),
                    Arrays.asList("AWS IAM Secure Best Practices", "AWS IAM Policies Reference"),
                    "LOCKED",
                    2
            ));
            milestones.get(1).setTopic("IAM Security");

            milestones.add(new MilestoneDTO(
                    "Databases: RDS & Relational Scaling",
                    "Databases",
                    "INTERMEDIATE",
                    10,
                    Arrays.asList("AWS Cloud Infrastructure Basics"),
                    Arrays.asList("Amazon RDS User Guide", "RDS Read Replicas Tech Note"),
                    "LOCKED",
                    3
            ));
            milestones.get(2).setTopic("RDS Scalability");

            milestones.add(new MilestoneDTO(
                    "Networking & VPC Architecture",
                    "Networking",
                    "ADVANCED",
                    14,
                    Arrays.asList("AWS Cloud Infrastructure Basics"),
                    Arrays.asList("AWS VPC Deep Dive", "Route Tables & Subnets User Guide"),
                    "LOCKED",
                    4
            ));
            milestones.get(3).setTopic("VPC Networking");

        } else if (goal.contains("Java SE 17")) {
            milestones.add(new MilestoneDTO(
                    "JVM Fundamentals & Garbage Collection",
                    "Core Java",
                    "BEGINNER",
                    10,
                    Collections.emptyList(),
                    Arrays.asList("Java G1 Garbage Collector Guide", "JVM Tuning Core Documentation"),
                    "LOCKED",
                    1
            ));
            milestones.get(0).setTopic("Garbage Collection");

            milestones.add(new MilestoneDTO(
                    "Pattern Matching & Modern Syntax",
                    "Core Java",
                    "INTERMEDIATE",
                    8,
                    Arrays.asList("JVM Fundamentals & Garbage Collection"),
                    Arrays.asList("JDK 17 Features Guide", "Instanceof Pattern Matching Tech Docs"),
                    "LOCKED",
                    2
            ));
            milestones.get(1).setTopic("Pattern Matching");

            milestones.add(new MilestoneDTO(
                    "JDBC Connections & HikariCP Tuning",
                    "Databases",
                    "INTERMEDIATE",
                    12,
                    Arrays.asList("JVM Fundamentals & Garbage Collection"),
                    Arrays.asList("HikariCP Configuration Best Practices", "Spring Boot JDBC Guide"),
                    "LOCKED",
                    3
            ));
            milestones.get(2).setTopic("JDBC Pools");

        } else if (goal.contains("Security+")) {
            milestones.add(new MilestoneDTO(
                    "Integrity Verification & Hashing",
                    "Security",
                    "BEGINNER",
                    8,
                    Collections.emptyList(),
                    Arrays.asList("SHA-256 Hashing Specifications", "Data Integrity Guide"),
                    "LOCKED",
                    1
            ));
            milestones.get(0).setTopic("Cryptography");

            milestones.add(new MilestoneDTO(
                    "Corporate Network Perimeter Defenses",
                    "Networking",
                    "INTERMEDIATE",
                    12,
                    Arrays.asList("Integrity Verification & Hashing"),
                    Arrays.asList("CompTIA Security+ Chapter 4: DMZ Architectures", "Firewalling Basics"),
                    "LOCKED",
                    2
            ));
            milestones.get(1).setTopic("Network Security");

        } else {
            // Default General Path
            milestones.add(new MilestoneDTO(
                    "Cloud Computing Basics",
                    "Cloud",
                    "BEGINNER",
                    6,
                    Collections.emptyList(),
                    Arrays.asList("Introduction to Cloud Computing"),
                    "LOCKED",
                    1
            ));
            milestones.get(0).setTopic("Cloud Basics");

            milestones.add(new MilestoneDTO(
                    "Core Database Models",
                    "Databases",
                    "INTERMEDIATE",
                    8,
                    Arrays.asList("Cloud Computing Basics"),
                    Arrays.asList("Relational Database Design Principles"),
                    "LOCKED",
                    2
            ));
            milestones.get(1).setTopic("Database Basics");
        }

        return milestones;
    }
}
