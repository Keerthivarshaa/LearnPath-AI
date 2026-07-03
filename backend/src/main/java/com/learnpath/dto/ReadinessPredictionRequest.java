package com.learnpath.dto;

import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.annotation.JsonProperty;

import java.util.Map;

/**
 * Wire-format request DTO for POST /ml/predict-readiness on the FastAPI
 * ai-service.
 *
 * Field names/JSON keys intentionally mirror
 * ai-service/app/schemas/readiness.py's ReadinessRequest exactly
 * (snake_case, no alias on that side of the contract). This class exists
 * purely to talk to that external service and is not a general-purpose
 * application DTO - it is not returned to the frontend.
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
public class ReadinessPredictionRequest {

    @JsonProperty("topic_scores")
    private Map<String, Double> topicScores;

    @JsonProperty("study_hours_per_week")
    private Double studyHoursPerWeek;

    @JsonProperty("total_study_hours")
    private Double totalStudyHours;

    @JsonProperty("current_streak")
    private Double currentStreak;

    @JsonProperty("longest_streak")
    private Double longestStreak;

    @JsonProperty("completed_milestones_count")
    private Double completedMilestonesCount;

    @JsonProperty("total_milestones_count")
    private Double totalMilestonesCount;

    @JsonProperty("completion_percentage")
    private Double completionPercentage;

    public ReadinessPredictionRequest() {
    }

    public Map<String, Double> getTopicScores() {
        return topicScores;
    }

    public void setTopicScores(Map<String, Double> topicScores) {
        this.topicScores = topicScores;
    }

    public Double getStudyHoursPerWeek() {
        return studyHoursPerWeek;
    }

    public void setStudyHoursPerWeek(Double studyHoursPerWeek) {
        this.studyHoursPerWeek = studyHoursPerWeek;
    }

    public Double getTotalStudyHours() {
        return totalStudyHours;
    }

    public void setTotalStudyHours(Double totalStudyHours) {
        this.totalStudyHours = totalStudyHours;
    }

    public Double getCurrentStreak() {
        return currentStreak;
    }

    public void setCurrentStreak(Double currentStreak) {
        this.currentStreak = currentStreak;
    }

    public Double getLongestStreak() {
        return longestStreak;
    }

    public void setLongestStreak(Double longestStreak) {
        this.longestStreak = longestStreak;
    }

    public Double getCompletedMilestonesCount() {
        return completedMilestonesCount;
    }

    public void setCompletedMilestonesCount(Double completedMilestonesCount) {
        this.completedMilestonesCount = completedMilestonesCount;
    }

    public Double getTotalMilestonesCount() {
        return totalMilestonesCount;
    }

    public void setTotalMilestonesCount(Double totalMilestonesCount) {
        this.totalMilestonesCount = totalMilestonesCount;
    }

    public Double getCompletionPercentage() {
        return completionPercentage;
    }

    public void setCompletionPercentage(Double completionPercentage) {
        this.completionPercentage = completionPercentage;
    }
}
