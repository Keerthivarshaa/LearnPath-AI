package com.learnpath.model;

public class AuthResponse {
    private String token;
    private Long id;
    private String name;
    private String email;
    private String certificationGoal;
    private Integer studyHoursPerWeek;
    private String currentLevel;

    public AuthResponse() {
    }

    public AuthResponse(String token, Long id, String name, String email, String certificationGoal, Integer studyHoursPerWeek, String currentLevel) {
        this.token = token;
        this.id = id;
        this.name = name;
        this.email = email;
        this.certificationGoal = certificationGoal;
        this.studyHoursPerWeek = studyHoursPerWeek;
        this.currentLevel = currentLevel;
    }

    // Getters and Setters
    public String getToken() {
        return token;
    }

    public void setToken(String token) {
        this.token = token;
    }

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
