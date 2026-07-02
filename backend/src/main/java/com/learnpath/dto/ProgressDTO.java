package com.learnpath.dto;

import java.util.List;

public class ProgressDTO {
    private Integer xp;
    private Integer level;
    private Integer xpToNextLevel;
    private Integer currentStreak;
    private Integer longestStreak;
    private Double totalStudyHours;
    private Double completionPercentage;
    private List<String> completedTopics;
    private List<String> completedMilestones;
    private List<String> unlockedAchievements;
    private List<String> notifications;

    public ProgressDTO() {
    }

    public ProgressDTO(Integer xp, Integer level, Integer xpToNextLevel, Integer currentStreak, Integer longestStreak, Double totalStudyHours, Double completionPercentage, List<String> completedTopics, List<String> completedMilestones, List<String> unlockedAchievements, List<String> notifications) {
        this.xp = xp;
        this.level = level;
        this.xpToNextLevel = xpToNextLevel;
        this.currentStreak = currentStreak;
        this.longestStreak = longestStreak;
        this.totalStudyHours = totalStudyHours;
        this.completionPercentage = completionPercentage;
        this.completedTopics = completedTopics;
        this.completedMilestones = completedMilestones;
        this.unlockedAchievements = unlockedAchievements;
        this.notifications = notifications;
    }

    public Integer getXp() {
        return xp;
    }

    public void setXp(Integer xp) {
        this.xp = xp;
    }

    public Integer getLevel() {
        return level;
    }

    public void setLevel(Integer level) {
        this.level = level;
    }

    public Integer getXpToNextLevel() {
        return xpToNextLevel;
    }

    public void setXpToNextLevel(Integer xpToNextLevel) {
        this.xpToNextLevel = xpToNextLevel;
    }

    public Integer getCurrentStreak() {
        return currentStreak;
    }

    public void setCurrentStreak(Integer currentStreak) {
        this.currentStreak = currentStreak;
    }

    public Integer getLongestStreak() {
        return longestStreak;
    }

    public void setLongestStreak(Integer longestStreak) {
        this.longestStreak = longestStreak;
    }

    public Double getTotalStudyHours() {
        return totalStudyHours;
    }

    public void setTotalStudyHours(Double totalStudyHours) {
        this.totalStudyHours = totalStudyHours;
    }

    public Double getCompletionPercentage() {
        return completionPercentage;
    }

    public void setCompletionPercentage(Double completionPercentage) {
        this.completionPercentage = completionPercentage;
    }

    public List<String> getCompletedTopics() {
        return completedTopics;
    }

    public void setCompletedTopics(List<String> completedTopics) {
        this.completedTopics = completedTopics;
    }

    public List<String> getCompletedMilestones() {
        return completedMilestones;
    }

    public void setCompletedMilestones(List<String> completedMilestones) {
        this.completedMilestones = completedMilestones;
    }

    public List<String> getUnlockedAchievements() {
        return unlockedAchievements;
    }

    public void setUnlockedAchievements(List<String> unlockedAchievements) {
        this.unlockedAchievements = unlockedAchievements;
    }

    public List<String> getNotifications() {
        return notifications;
    }

    public void setNotifications(List<String> notifications) {
        this.notifications = notifications;
    }
}
