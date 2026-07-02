package com.learnpath.model;

public class AuthRequest {
    private String name;
    private String email;
    private String password;
    private String certificationGoal;
    private Integer studyHoursPerWeek;
    private String currentLevel;

    public AuthRequest() {
    }

    // Getters and Setters
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
