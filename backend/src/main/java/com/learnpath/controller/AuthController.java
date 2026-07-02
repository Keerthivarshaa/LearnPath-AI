package com.learnpath.controller;

import com.learnpath.model.AuthRequest;
import com.learnpath.model.AuthResponse;
import com.learnpath.model.User;
import com.learnpath.service.JwtService;
import com.learnpath.service.UserService;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.security.authentication.AuthenticationManager;
import org.springframework.security.authentication.BadCredentialsException;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.Optional;

@RestController
@RequestMapping("/api/auth")
public class AuthController {

    private final UserService userService;
    private final JwtService jwtService;
    private final AuthenticationManager authenticationManager;

    public AuthController(UserService userService, JwtService jwtService, AuthenticationManager authenticationManager) {
        this.userService = userService;
        this.jwtService = jwtService;
        this.authenticationManager = authenticationManager;
    }

    @PostMapping("/register")
    public ResponseEntity<?> register(@RequestBody AuthRequest request) {
        // Name Validation
        String name = request.getName();
        if (name == null || name.trim().isEmpty()) {
            return ResponseEntity.status(HttpStatus.BAD_REQUEST).body("Error: Name is required!");
        }
        name = name.trim();
        if (name.length() < 2 || name.length() > 50) {
            return ResponseEntity.status(HttpStatus.BAD_REQUEST).body("Error: Name must be between 2 and 50 characters!");
        }

        // Password Validation
        String password = request.getPassword();
        if (password == null || password.length() < 8) {
            return ResponseEntity.status(HttpStatus.BAD_REQUEST).body("Error: Password must be at least 8 characters long!");
        }
        boolean hasUppercase = false;
        boolean hasLowercase = false;
        boolean hasDigit = false;
        for (char c : password.toCharArray()) {
            if (Character.isUpperCase(c)) hasUppercase = true;
            else if (Character.isLowerCase(c)) hasLowercase = true;
            else if (Character.isDigit(c)) hasDigit = true;
        }
        if (!hasUppercase || !hasLowercase || !hasDigit) {
            return ResponseEntity.status(HttpStatus.BAD_REQUEST).body("Error: Password must contain at least one uppercase letter, one lowercase letter, and one digit!");
        }

        if (userService.existsByEmail(request.getEmail())) {
            return ResponseEntity.status(HttpStatus.BAD_REQUEST).body("Error: Email is already registered!");
        }

        User newUser = new User();
        newUser.setName(name);
        newUser.setEmail(request.getEmail());
        newUser.setPassword(password);
        newUser.setCertificationGoal(request.getCertificationGoal() != null ? request.getCertificationGoal() : "General Developer Certification");
        newUser.setStudyHoursPerWeek(request.getStudyHoursPerWeek() != null ? request.getStudyHoursPerWeek() : 10);
        newUser.setCurrentLevel(request.getCurrentLevel() != null ? request.getCurrentLevel() : "Beginner");

        User savedUser = userService.saveUser(newUser);
        String token = jwtService.generateToken(savedUser.getEmail());

        AuthResponse response = new AuthResponse(
                token,
                savedUser.getId(),
                savedUser.getName(),
                savedUser.getEmail(),
                savedUser.getCertificationGoal(),
                savedUser.getStudyHoursPerWeek(),
                savedUser.getCurrentLevel()
        );

        return ResponseEntity.ok(response);
    }

    @PostMapping("/login")
    public ResponseEntity<?> login(@RequestBody AuthRequest request) {
        try {
            authenticationManager.authenticate(
                    new UsernamePasswordAuthenticationToken(request.getEmail(), request.getPassword())
            );
        } catch (BadCredentialsException e) {
            return ResponseEntity.status(HttpStatus.UNAUTHORIZED).body("Error: Invalid email or password!");
        }

        Optional<User> userOpt = userService.findByEmail(request.getEmail());
        if (userOpt.isEmpty()) {
            return ResponseEntity.status(HttpStatus.UNAUTHORIZED).body("Error: User details not found!");
        }

        User user = userOpt.get();
        String token = jwtService.generateToken(user.getEmail());

        AuthResponse response = new AuthResponse(
                token,
                user.getId(),
                user.getName(),
                user.getEmail(),
                user.getCertificationGoal(),
                user.getStudyHoursPerWeek(),
                user.getCurrentLevel()
        );

        return ResponseEntity.ok(response);
    }
}
