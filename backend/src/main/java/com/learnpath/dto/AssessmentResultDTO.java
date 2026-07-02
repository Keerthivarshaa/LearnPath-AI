package com.learnpath.dto;

import java.time.LocalDateTime;
import java.util.List;

public class AssessmentResultDTO {
    private Long id;
    private Integer score;
    private Integer totalQuestions;
    private List<String> weakTopics;
    private List<String> strongTopics;
    private LocalDateTime completedAt;
    private List<AssessmentAnswerDTO> answers;

    public AssessmentResultDTO() {
    }

    public AssessmentResultDTO(Long id, Integer score, Integer totalQuestions, List<String> weakTopics, List<String> strongTopics, LocalDateTime completedAt, List<AssessmentAnswerDTO> answers) {
        this.id = id;
        this.score = score;
        this.totalQuestions = totalQuestions;
        this.weakTopics = weakTopics;
        this.strongTopics = strongTopics;
        this.completedAt = completedAt;
        this.answers = answers;
    }

    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public Integer getScore() {
        return score;
    }

    public void setScore(Integer score) {
        this.score = score;
    }

    public Integer getTotalQuestions() {
        return totalQuestions;
    }

    public void setTotalQuestions(Integer totalQuestions) {
        this.totalQuestions = totalQuestions;
    }

    public List<String> getWeakTopics() {
        return weakTopics;
    }

    public void setWeakTopics(List<String> weakTopics) {
        this.weakTopics = weakTopics;
    }

    public List<String> getStrongTopics() {
        return strongTopics;
    }

    public void setStrongTopics(List<String> strongTopics) {
        this.strongTopics = strongTopics;
    }

    public LocalDateTime getCompletedAt() {
        return completedAt;
    }

    public void setCompletedAt(LocalDateTime completedAt) {
        this.completedAt = completedAt;
    }

    public List<AssessmentAnswerDTO> getAnswers() {
        return answers;
    }

    public void setAnswers(List<AssessmentAnswerDTO> answers) {
        this.answers = answers;
    }
}
