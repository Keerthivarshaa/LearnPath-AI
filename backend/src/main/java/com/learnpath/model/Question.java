package com.learnpath.model;

import com.fasterxml.jackson.annotation.JsonManagedReference;
import jakarta.persistence.*;
import java.util.ArrayList;
import java.util.List;

@Entity
@Table(name = "questions")
public class Question {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false, columnDefinition = "TEXT")
    private String text;

    @Column(nullable = false)
    private String topic;

    @Column(nullable = false)
    private String category;

    @Enumerated(EnumType.STRING)
    @Column(nullable = false)
    private Difficulty difficulty;

    @Column(name = "correct_explanation", columnDefinition = "TEXT")
    private String correctExplanation;

    @Column(name = "display_order", nullable = false)
    private Integer displayOrder;

    @Column(name = "certification_goal", nullable = false)
    private String certificationGoal;

    @OneToMany(mappedBy = "question", cascade = CascadeType.ALL, orphanRemoval = true, fetch = FetchType.LAZY)
    @JsonManagedReference
    private List<Option> options = new ArrayList<>();

    public Question() {
    }

    public Question(String text, String topic, String category, Difficulty difficulty, String correctExplanation, Integer displayOrder, String certificationGoal) {
        this.text = text;
        this.topic = topic;
        this.category = category;
        this.difficulty = difficulty;
        this.correctExplanation = correctExplanation;
        this.displayOrder = displayOrder;
        this.certificationGoal = certificationGoal;
    }

    // Helper method to add options
    public void addOption(Option option) {
        options.add(option);
        option.setQuestion(this);
    }

    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public String getText() {
        return text;
    }

    public void setText(String text) {
        this.text = text;
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

    public Difficulty getDifficulty() {
        return difficulty;
    }

    public void setDifficulty(Difficulty difficulty) {
        this.difficulty = difficulty;
    }

    public String getCorrectExplanation() {
        return correctExplanation;
    }

    public void setCorrectExplanation(String correctExplanation) {
        this.correctExplanation = correctExplanation;
    }

    public Integer getDisplayOrder() {
        return displayOrder;
    }

    public void setDisplayOrder(Integer displayOrder) {
        this.displayOrder = displayOrder;
    }

    public String getCertificationGoal() {
        return certificationGoal;
    }

    public void setCertificationGoal(String certificationGoal) {
        this.certificationGoal = certificationGoal;
    }

    public List<Option> getOptions() {
        return options;
    }

    public void setOptions(List<Option> options) {
        this.options = options;
    }
}
