package com.learnpath.service;

import com.learnpath.dto.ProgressDTO;
import com.learnpath.model.*;
import com.learnpath.repository.ProgressRepository;
import com.learnpath.repository.AssessmentResultRepository;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.LocalDate;
import java.util.*;
import java.util.stream.Collectors;

@Service
public class ProgressService {

    // XP Reward Configurations
    public static final int DAILY_LOGIN_XP = 25;
    public static final int ASSESSMENT_COMPLETION_XP = 100;
    public static final int MILESTONE_COMPLETION_XP = 200;
    public static final int STUDY_HOUR_XP = 50;

    private final ProgressRepository progressRepository;
    private final AssessmentResultRepository assessmentResultRepository;

    public ProgressService(ProgressRepository progressRepository, AssessmentResultRepository assessmentResultRepository) {
        this.progressRepository = progressRepository;
        this.assessmentResultRepository = assessmentResultRepository;
    }

    @Transactional
    public Progress getOrCreateProgress(User user) {
        return progressRepository.findByUser(user)
                .orElseGet(() -> progressRepository.save(new Progress(user)));
    }

    @Transactional
    public ProgressDTO getProgressDTO(User user) {
        Progress progress = getOrCreateProgress(user);
        
        // Execute active streak check on fetch
        updateActiveStreak(progress);

        // Fetch notifications and copy them, then clear them from database
        List<String> currentNotifications = new ArrayList<>(progress.getNotifications());
        progress.getNotifications().clear();
        progressRepository.save(progress);

        int xpToNextLevel = 1000 - (progress.getXp() % 1000);

        return new ProgressDTO(
                progress.getXp(),
                progress.getLevel(),
                xpToNextLevel,
                progress.getCurrentStreak(),
                progress.getLongestStreak(),
                progress.getTotalStudyHours(),
                progress.getCompletionPercentage(),
                new ArrayList<>(progress.getCompletedTopics()),
                new ArrayList<>(progress.getCompletedMilestones()),
                new ArrayList<>(progress.getUnlockedAchievements()),
                currentNotifications
        );
    }

    @Transactional
    public void awardXp(User user, int xpAmount, String reason) {
        Progress progress = getOrCreateProgress(user);
        
        int currentLevel = progress.getLevel();
        progress.setXp(progress.getXp() + xpAmount);
        progress.addNotification(String.format("+%d XP: %s", xpAmount, reason));

        // Level Up Threshold: Flat 1000 XP per level
        int newLevel = (progress.getXp() / 1000) + 1;
        if (newLevel > currentLevel) {
            progress.setLevel(newLevel);
            progress.addNotification(String.format("🎉 Level Up! You reached Level %d!", newLevel));
        }

        checkAchievements(progress);
        progressRepository.save(progress);
    }

    @Transactional
    public void updateActiveStreak(Progress progress) {
        LocalDate today = LocalDate.now();
        LocalDate lastActive = progress.getLastActiveDate();

        if (lastActive == null) {
            progress.setCurrentStreak(1);
            progress.setLongestStreak(1);
            progress.setLastActiveDate(today);
            awardXpInternal(progress, DAILY_LOGIN_XP, "Daily active session started");
        } else if (!lastActive.equals(today)) {
            if (lastActive.plusDays(1).equals(today)) {
                // Consecutive active day
                int newStreak = progress.getCurrentStreak() + 1;
                progress.setCurrentStreak(newStreak);
                if (newStreak > progress.getLongestStreak()) {
                    progress.setLongestStreak(newStreak);
                }
                progress.addNotification(String.format("🔥 Daily Streak! Active for %d days!", newStreak));
                awardXpInternal(progress, DAILY_LOGIN_XP, "Consecutive daily login");
            } else {
                // Streak broken
                progress.setCurrentStreak(1);
                progress.addNotification("Streak reset. New active session started.");
                awardXpInternal(progress, DAILY_LOGIN_XP, "New daily login");
            }
            progress.setLastActiveDate(today);
        }
    }

    @Transactional
    public ProgressDTO logStudySession(User user, double hours, String topic) {
        Progress progress = getOrCreateProgress(user);
        progress.setTotalStudyHours(progress.getTotalStudyHours() + hours);
        progress.getCompletedTopics().add(topic);

        int xpGained = (int) (hours * STUDY_HOUR_XP);
        awardXpInternal(progress, xpGained, "Logged study session on topic: " + topic);

        // Check if this action completes any milestones
        checkMilestoneCompletions(progress, user.getCertificationGoal(), topic);

        progressRepository.save(progress);
        return getProgressDTO(user);
    }

    @Transactional
    public void checkAssessmentAchievements(User user) {
        Progress progress = getOrCreateProgress(user);
        boolean firstAssessmentResult = assessmentResultRepository.findFirstByUserOrderByCompletedAtDesc(user).isPresent();
        if (firstAssessmentResult && !progress.getUnlockedAchievements().contains("First Assessment")) {
            progress.getUnlockedAchievements().add("First Assessment");
            progress.addNotification("🏆 Achievement Unlocked: First Assessment!");
            awardXpInternal(progress, 150, "First Assessment completed");
            progressRepository.save(progress);
        }
    }

    private void awardXpInternal(Progress progress, int xpAmount, String reason) {
        int currentLevel = progress.getLevel();
        progress.setXp(progress.getXp() + xpAmount);
        progress.addNotification(String.format("+%d XP: %s", xpAmount, reason));

        int newLevel = (progress.getXp() / 1000) + 1;
        if (newLevel > currentLevel) {
            progress.setLevel(newLevel);
            progress.addNotification(String.format("🎉 Level Up! You reached Level %d!", newLevel));
        }
        checkAchievements(progress);
    }

    private void checkAchievements(Progress progress) {
        Set<String> unlocked = progress.getUnlockedAchievements();

        // 1. First Study Session
        if (progress.getTotalStudyHours() > 0 && !unlocked.contains("First Study Session")) {
            unlocked.add("First Study Session");
            progress.addNotification("🏆 Achievement Unlocked: First Study Session!");
            progress.setXp(progress.getXp() + 50);
        }

        // 2. 7-Day Streak
        if (progress.getCurrentStreak() >= 7 && !unlocked.contains("7-Day Streak")) {
            unlocked.add("7-Day Streak");
            progress.addNotification("🏆 Achievement Unlocked: 7-Day Streak!");
            progress.setXp(progress.getXp() + 150);
        }

        // 3. 30-Day Streak
        if (progress.getCurrentStreak() >= 30 && !unlocked.contains("30-Day Streak")) {
            unlocked.add("30-Day Streak");
            progress.addNotification("🏆 Achievement Unlocked: 30-Day Streak!");
            progress.setXp(progress.getXp() + 300);
        }

        // 4. Level 5
        if (progress.getLevel() >= 5 && !unlocked.contains("Level 5")) {
            unlocked.add("Level 5");
            progress.addNotification("🏆 Achievement Unlocked: Level 5!");
            progress.setXp(progress.getXp() + 250);
        }

        // 5. 1000 XP
        if (progress.getXp() >= 1000 && !unlocked.contains("1000 XP")) {
            unlocked.add("1000 XP");
            progress.addNotification("🏆 Achievement Unlocked: 1000 XP!");
            progress.setXp(progress.getXp() + 100);
        }
    }

    private void checkMilestoneCompletions(Progress progress, String goal, String topic) {
        Map<String, String> topicToMilestone = new HashMap<>();
        
        // AWS
        topicToMilestone.put("EC2 Instance Models", "AWS Cloud Infrastructure Basics");
        topicToMilestone.put("IAM Security", "Identity Access Management & Security");
        topicToMilestone.put("RDS Scalability", "Databases: RDS & Relational Scaling");
        topicToMilestone.put("VPC Networking", "Networking & VPC Architecture");
        
        // Java
        topicToMilestone.put("Garbage Collection", "JVM Fundamentals & Garbage Collection");
        topicToMilestone.put("Pattern Matching", "Pattern Matching & Modern Syntax");
        topicToMilestone.put("JDBC Pools", "JDBC Connections & HikariCP Tuning");
        
        // Security+
        topicToMilestone.put("Cryptography", "Integrity Verification & Hashing");
        topicToMilestone.put("Network Security", "Corporate Network Perimeter Defenses");

        // Azure
        topicToMilestone.put("Azure Storage", "Azure Storage Solutions");
        topicToMilestone.put("Azure Regions", "Azure Regions & High Availability");
        topicToMilestone.put("Azure Governance", "Azure Management & Governance");

        String milestone = topicToMilestone.get(topic);
        if (milestone != null && !progress.getCompletedMilestones().contains(milestone)) {
            progress.getCompletedMilestones().add(milestone);
            progress.addNotification(String.format("🏆 Milestone Completed: %s!", milestone));
            awardXpInternal(progress, MILESTONE_COMPLETION_XP, "Milestone completed: " + milestone);
            
            // Calculate new completion percentage
            int totalMilestones = 0;
            if (goal.contains("Solutions Architect")) totalMilestones = 4;
            else if (goal.contains("Java SE 17")) totalMilestones = 3;
            else if (goal.contains("Security+")) totalMilestones = 2;
            else if (goal.contains("AZ-900")) totalMilestones = 3;
            else totalMilestones = 2;

            double percent = ((double) progress.getCompletedMilestones().size() / totalMilestones) * 100.0;
            if (percent > 100.0) percent = 100.0;
            progress.setCompletionPercentage(Math.round(percent * 10.0) / 10.0);
        }
    }
}
