package com.learnpath.model;

import jakarta.persistence.*;
import com.fasterxml.jackson.annotation.JsonProperty;

@Entity
@Table(name = "users")
public class User {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false)
    private String name;

    @Column(nullable = false, unique = true)
    private String email;

    @Column(nullable = false)
    @JsonProperty(access = JsonProperty.Access.WRITE_ONLY)
    private String password;

    @Column(name = "certification_goal")
    private String certificationGoal;

    @Column(name = "study_hours_per_week")
    private Integer studyHoursPerWeek;

    @Column(name = "current_level")
    private String currentLevel;

    public User() {
    }

    public User(String name, String email, String password, String certificationGoal, Integer studyHoursPerWeek, String currentLevel) {
        this.name = name;
        this.email = email;
        this.password = password;
        this.certificationGoal = certificationGoal;
        this.studyHoursPerWeek = studyHoursPerWeek;
        this.currentLevel = currentLevel;
    }

    // Getters and Setters
    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public String getEmail() {
        return email;
    }

    public void setEmail(String email) {
        this.email = email;
    }

    public String getPassword() {
        return password;
    }

    public void setPassword(String password) {
        this.password = password;
    }

    public String getCertificationGoal() {
        return certificationGoal;
    }

    public void setCertificationGoal(String certificationGoal) {
        this.certificationGoal = certificationGoal;
    }

    public Integer getStudyHoursPerWeek() {
        return studyHoursPerWeek;
    }

    public void setStudyHoursPerWeek(Integer studyHoursPerWeek) {
        this.studyHoursPerWeek = studyHoursPerWeek;
    }

    public String getCurrentLevel() {
        return currentLevel;
    }

    public void setCurrentLevel(String currentLevel) {
        this.currentLevel = currentLevel;
    }
}
