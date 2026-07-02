package com.learnpath.model;

import jakarta.persistence.*;
import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.List;

@Entity
@Table(name = "assessment_results")
public class AssessmentResult {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false)
    private Integer score;

    @Column(name = "total_questions", nullable = false)
    private Integer totalQuestions;

    @ElementCollection
    @CollectionTable(name = "assessment_weak_topics", joinColumns = @JoinColumn(name = "result_id"))
    @Column(name = "topic")
    private List<String> weakTopics = new ArrayList<>();

    @ElementCollection
    @CollectionTable(name = "assessment_strong_topics", joinColumns = @JoinColumn(name = "result_id"))
    @Column(name = "topic")
    private List<String> strongTopics = new ArrayList<>();

    @Column(name = "completed_at", nullable = false)
    private LocalDateTime completedAt;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "user_id", nullable = false)
    private User user;

    @OneToMany(mappedBy = "assessmentResult", cascade = CascadeType.ALL, orphanRemoval = true, fetch = FetchType.LAZY)
    private List<AssessmentAnswer> answers = new ArrayList<>();

    public AssessmentResult() {
    }

    public AssessmentResult(Integer score, Integer totalQuestions, List<String> weakTopics, List<String> strongTopics, LocalDateTime completedAt, User user) {
        this.score = score;
        this.totalQuestions = totalQuestions;
        this.weakTopics = weakTopics;
        this.strongTopics = strongTopics;
        this.completedAt = completedAt;
        this.user = user;
    }

    public void addAnswer(AssessmentAnswer answer) {
        answers.add(answer);
        answer.setAssessmentResult(this);
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

    public User getUser() {
        return user;
    }

    public void setUser(User user) {
        this.user = user;
    }

    public List<AssessmentAnswer> getAnswers() {
        return answers;
    }

    public void setAnswers(List<AssessmentAnswer> answers) {
        this.answers = answers;
    }
}
