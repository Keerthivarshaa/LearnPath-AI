package com.learnpath.service;

import com.learnpath.dto.RecommendationDTO;
import com.learnpath.model.AssessmentResult;
import com.learnpath.model.User;
import java.util.List;

public interface RoadmapGenerator {
    RecommendationDTO generate(User user, AssessmentResult latestResult, List<AssessmentResult> history);
}
