package com.learnpath.controller;

import com.learnpath.dto.RecommendationDTO;
import com.learnpath.model.User;
import com.learnpath.service.RecommendationService;
import com.learnpath.service.UserService;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.Optional;

@RestController
@RequestMapping("/api/recommendation")
public class RecommendationController {

    private final RecommendationService recommendationService;
    private final UserService userService;

    public RecommendationController(RecommendationService recommendationService, UserService userService) {
        this.recommendationService = recommendationService;
        this.userService = userService;
    }

    @GetMapping
    public ResponseEntity<?> getRecommendation() {
        Authentication auth = SecurityContextHolder.getContext().getAuthentication();
        if (auth == null || !auth.isAuthenticated()) {
            return ResponseEntity.status(HttpStatus.UNAUTHORIZED).body("Error: Unauthorized access!");
        }

        Optional<User> userOpt = userService.findByEmail(auth.getName());
        if (userOpt.isEmpty()) {
            return ResponseEntity.status(HttpStatus.NOT_FOUND).body("Error: User not found!");
        }

        RecommendationDTO recommendation = recommendationService.getRecommendationForUser(userOpt.get());
        return ResponseEntity.ok(recommendation);
    }
}
