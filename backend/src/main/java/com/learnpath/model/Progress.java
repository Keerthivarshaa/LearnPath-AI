package com.learnpath.model;

import jakarta.persistence.*;
import java.time.LocalDate;
import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;
import java.util.Set;

@Entity
@Table(name = "user_progress")
public class Progress {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false)
    private Integer xp = 0;

    @Column(nullable = false)
    private Integer level = 1;

    @Column(name = "current_streak", nullable = false)
    private Integer currentStreak = 0;

    @Column(name = "longest_streak", nullable = false)
    private Integer longestStreak = 0;

    @Column(name = "last_active_date")
    private LocalDate lastActiveDate;

    @ElementCollection(fetch = FetchType.EAGER)
    @CollectionTable(name = "progress_completed_topics", joinColumns = @JoinColumn(name = "progress_id"))
    @Column(name = "topic")
    private Set<String> completedTopics = new HashSet<>();

    @ElementCollection(fetch = FetchType.EAGER)
    @CollectionTable(name = "progress_completed_milestones", joinColumns = @JoinColumn(name = "progress_id"))
    @Column(name = "milestone")
    private Set<String> completedMilestones = new HashSet<>();

    @Column(name = "completion_percentage", nullable = false)
    private Double completionPercentage = 0.0;

    @Column(name = "total_study_hours", nullable = false)
    private Double totalStudyHours = 0.0;

    @ElementCollection(fetch = FetchType.EAGER)
    @CollectionTable(name = "progress_achievements", joinColumns = @JoinColumn(name = "progress_id"))
    @Column(name = "achievement")
    private Set<String> unlockedAchievements = new HashSet<>();

    @ElementCollection(fetch = FetchType.EAGER)
    @CollectionTable(name = "progress_notifications", joinColumns = @JoinColumn(name = "progress_id"))
    @Column(name = "notification")
    private List<String> notifications = new ArrayList<>();

    @OneToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "user_id", nullable = false, unique = true)
    private User user;

    public Progress() {
    }

    public Progress(User user) {
        this.user = user;
    }

    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
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

    public LocalDate getLastActiveDate() {
        return lastActiveDate;
    }

    public void setLastActiveDate(LocalDate lastActiveDate) {
        this.lastActiveDate = lastActiveDate;
    }

    public Set<String> getCompletedTopics() {
        return completedTopics;
    }

    public void setCompletedTopics(Set<String> completedTopics) {
        this.completedTopics = completedTopics;
    }

    public Set<String> getCompletedMilestones() {
        return completedMilestones;
    }

    public void setCompletedMilestones(Set<String> completedMilestones) {
        this.completedMilestones = completedMilestones;
    }

    public Double getCompletionPercentage() {
        return completionPercentage;
    }

    public void setCompletionPercentage(Double completionPercentage) {
        this.completionPercentage = completionPercentage;
    }

    public Double getTotalStudyHours() {
        return totalStudyHours;
    }

    public void setTotalStudyHours(Double totalStudyHours) {
        this.totalStudyHours = totalStudyHours;
    }

    public Set<String> getUnlockedAchievements() {
        return unlockedAchievements;
    }

    public void setUnlockedAchievements(Set<String> unlockedAchievements) {
        this.unlockedAchievements = unlockedAchievements;
    }

    public User getUser() {
        return user;
    }

    public void setUser(User user) {
        this.user = user;
    }
    public List<String> getNotifications() {
        return notifications;
    }

    public void setNotifications(List<String> notifications) {
        this.notifications = notifications;
    }

    public void addNotification(String notification) {
        this.notifications.add(notification);
    }
}
