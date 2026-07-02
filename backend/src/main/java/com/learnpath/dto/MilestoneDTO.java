package com.learnpath.dto;

import java.util.List;

public class MilestoneDTO {
    private String topic;
    private String category;
    private String difficulty;
    private Integer estimatedHours;
    private List<String> prerequisites;
    private List<String> recommendedResources;
    private String status;
    private Integer displayOrder;

    public MilestoneDTO() {
    }

    public MilestoneDTO(String topic, String category, String difficulty, Integer estimatedHours, List<String> prerequisites, List<String> recommendedResources, String status, Integer displayOrder) {
        this.topic = topic;
        this.category = category;
        this.difficulty = difficulty;
        this.estimatedHours = estimatedHours;
        this.prerequisites = prerequisites;
        this.recommendedResources = recommendedResources;
        this.status = status;
        this.displayOrder = displayOrder;
    }

    public String getTopic() {
        return topic;
    }

    public void setTopic(String topic) {
        this.topic = topic;
    }

    public String getCategory() {
        return category;
    }

    public void setCategory(String category) {
        this.category = category;
    }

    public String getDifficulty() {
        return difficulty;
    }

    public void setDifficulty(String difficulty) {
        this.difficulty = difficulty;
    }

    public Integer getEstimatedHours() {
        return estimatedHours;
    }

    public void setEstimatedHours(Integer estimatedHours) {
        this.estimatedHours = estimatedHours;
    }

    public List<String> getPrerequisites() {
        return prerequisites;
    }

    public void setPrerequisites(List<String> prerequisites) {
        this.prerequisites = prerequisites;
    }

    public List<String> getRecommendedResources() {
        return recommendedResources;
    }

    public void setRecommendedResources(List<String> recommendedResources) {
        this.recommendedResources = recommendedResources;
    }

    public String getStatus() {
        return status;
    }

    public void setStatus(String status) {
        this.status = status;
    }

    public Integer getDisplayOrder() {
        return displayOrder;
    }

    public void setDisplayOrder(Integer displayOrder) {
        this.displayOrder = displayOrder;
    }
}
