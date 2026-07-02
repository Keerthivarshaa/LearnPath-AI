package com.learnpath.service;

import com.learnpath.dto.RecommendationDTO;
import com.learnpath.model.AssessmentResult;
import com.learnpath.model.User;
import com.learnpath.repository.AssessmentResultRepository;
import org.springframework.stereotype.Service;
import java.util.List;
import java.util.Optional;

@Service
public class RecommendationService {

    private final AssessmentResultRepository assessmentResultRepository;
    private final RoadmapGenerator roadmapGenerator;

    public RecommendationService(AssessmentResultRepository assessmentResultRepository, RoadmapGenerator roadmapGenerator) {
        this.assessmentResultRepository = assessmentResultRepository;
        this.roadmapGenerator = roadmapGenerator;
    }

    public RecommendationDTO getRecommendationForUser(User user) {
        Optional<AssessmentResult> latestResultOpt = assessmentResultRepository.findFirstByUserOrderByCompletedAtDesc(user);
        List<AssessmentResult> history = assessmentResultRepository.findByUserOrderByCompletedAtDesc(user);

        AssessmentResult latestResult = latestResultOpt.orElse(null);
        return roadmapGenerator.generate(user, latestResult, history);
    }
}
