package com.learnpath.dto;

import java.util.List;
import java.util.Map;

public class RecommendationDTO {
    private String certificationGoal;
    private String currentLevel;
    private Integer weeklyStudyHours;
    private Integer estimatedCompletionWeeks;
    private Double completionPercentage;
    private String dailyStudyPlan;
    private String recommendedNextAssessment;
    private List<String> priorityTopics;
    private List<MilestoneDTO> milestones;
    private Map<String, String> weeklyPlan;
    private boolean isOnboarding;

    public RecommendationDTO() {
    }

    public RecommendationDTO(String certificationGoal, String currentLevel, Integer weeklyStudyHours, Integer estimatedCompletionWeeks, Double completionPercentage, String dailyStudyPlan, String recommendedNextAssessment, List<String> priorityTopics, List<MilestoneDTO> milestones, Map<String, String> weeklyPlan, boolean isOnboarding) {
        this.certificationGoal = certificationGoal;
        this.currentLevel = currentLevel;
        this.weeklyStudyHours = weeklyStudyHours;
        this.estimatedCompletionWeeks = estimatedCompletionWeeks;
        this.completionPercentage = completionPercentage;
        this.dailyStudyPlan = dailyStudyPlan;
        this.recommendedNextAssessment = recommendedNextAssessment;
        this.priorityTopics = priorityTopics;
        this.milestones = milestones;
        this.weeklyPlan = weeklyPlan;
        this.isOnboarding = isOnboarding;
    }

    public String getCertificationGoal() {
        return certificationGoal;
    }

    public void setCertificationGoal(String certificationGoal) {
        this.certificationGoal = certificationGoal;
    }

    public String getCurrentLevel() {
        return currentLevel;
    }

    public void setCurrentLevel(String currentLevel) {
        this.currentLevel = currentLevel;
    }

    public Integer getWeeklyStudyHours() {
        return weeklyStudyHours;
    }

    public void setWeeklyStudyHours(Integer weeklyStudyHours) {
        this.weeklyStudyHours = weeklyStudyHours;
    }

    public Integer getEstimatedCompletionWeeks() {
        return estimatedCompletionWeeks;
    }

    public void setEstimatedCompletionWeeks(Integer estimatedCompletionWeeks) {
        this.estimatedCompletionWeeks = estimatedCompletionWeeks;
    }

    public Double getCompletionPercentage() {
        return completionPercentage;
    }

    public void setCompletionPercentage(Double completionPercentage) {
        this.completionPercentage = completionPercentage;
    }

    public String getDailyStudyPlan() {
        return dailyStudyPlan;
    }

    public void setDailyStudyPlan(String dailyStudyPlan) {
        this.dailyStudyPlan = dailyStudyPlan;
    }

    public String getRecommendedNextAssessment() {
        return recommendedNextAssessment;
    }

    public void setRecommendedNextAssessment(String recommendedNextAssessment) {
        this.recommendedNextAssessment = recommendedNextAssessment;
    }

    public List<String> getPriorityTopics() {
        return priorityTopics;
    }

    public void setPriorityTopics(List<String> priorityTopics) {
        this.priorityTopics = priorityTopics;
    }

    public List<MilestoneDTO> getMilestones() {
        return milestones;
    }

    public void setMilestones(List<MilestoneDTO> milestones) {
        this.milestones = milestones;
    }

    public Map<String, String> getWeeklyPlan() {
        return weeklyPlan;
    }

    public void setWeeklyPlan(Map<String, String> weeklyPlan) {
        this.weeklyPlan = weeklyPlan;
    }

    public boolean isOnboarding() {
        return isOnboarding;
    }

    public void setOnboarding(boolean onboarding) {
        isOnboarding = onboarding;
    }
}
