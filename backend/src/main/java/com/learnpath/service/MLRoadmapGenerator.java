package com.learnpath.service;

import com.learnpath.dto.MilestoneDTO;
import com.learnpath.dto.ReadinessPredictionRequest;
import com.learnpath.dto.ReadinessPredictionResponse;
import com.learnpath.dto.RecommendationDTO;
import com.learnpath.model.AssessmentAnswer;
import com.learnpath.model.AssessmentResult;
import com.learnpath.model.Progress;
import com.learnpath.model.User;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.context.annotation.Primary;
import org.springframework.stereotype.Component;

import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Optional;
import java.util.stream.Collectors;

/**
 * ML-backed RoadmapGenerator. Delegates the actual roadmap structure
 * (milestones, weekly plan, priority topics) entirely to the existing,
 * proven RuleBasedRoadmapGenerator - this class's only responsibility is
 * to enrich that result with a readiness score predicted by the FastAPI
 * ai-service.
 *
 * Marked @Primary so RecommendationService (unmodified) automatically
 * receives this bean instead of RuleBasedRoadmapGenerator, per the
 * existing Strategy pattern - no changes needed to RecommendationService
 * or RecommendationController.
 *
 * If the AI service is unavailable, generate() returns exactly what
 * RuleBasedRoadmapGenerator would have returned (readiness fields simply
 * stay null) - the frontend never sees an error caused by the ML service
 * being offline.
 */
@Component
@Primary
public class MLRoadmapGenerator implements RoadmapGenerator {

    private static final Logger log = LoggerFactory.getLogger(MLRoadmapGenerator.class);

    private final AiReadinessClient aiReadinessClient;
    private final ProgressService progressService;
    private final RuleBasedRoadmapGenerator ruleBasedRoadmapGenerator;

    public MLRoadmapGenerator(
            AiReadinessClient aiReadinessClient,
            ProgressService progressService,
            RuleBasedRoadmapGenerator ruleBasedRoadmapGenerator
    ) {
        this.aiReadinessClient = aiReadinessClient;
        this.progressService = progressService;
        this.ruleBasedRoadmapGenerator = ruleBasedRoadmapGenerator;
    }

    @Override
    public RecommendationDTO generate(User user, AssessmentResult latestResult, List<AssessmentResult> history) {
        // Reuse the existing, proven roadmap logic unconditionally - this
        // is both our fallback AND the base recommendation we enrich.
        // Milestones/priority topics/weekly plan are untouched; only the
        // readiness fields below are new.
        RecommendationDTO recommendation = ruleBasedRoadmapGenerator.generate(user, latestResult, history);

        ReadinessPredictionRequest request = buildRequest(user, latestResult);
        Optional<ReadinessPredictionResponse> prediction = aiReadinessClient.predictReadiness(request);

        if (prediction.isPresent()) {
            ReadinessPredictionResponse response = prediction.get();
            recommendation.setReadinessScore(response.getReadinessScore());
            recommendation.setReadinessLevel(response.getReadinessLevel());
            recommendation.setReadinessExplanation(response.getExplanation());
        } else {
            log.info("Readiness prediction unavailable for user {} - roadmap generated without ML readiness fields.",
                    user.getEmail());
        }

        return recommendation;
    }

    private ReadinessPredictionRequest buildRequest(User user, AssessmentResult latestResult) {
        Progress progress = progressService.getOrCreateProgress(user);

        ReadinessPredictionRequest request = new ReadinessPredictionRequest();
        request.setTopicScores(computeTopicScores(latestResult));
        request.setStudyHoursPerWeek(toDouble(user.getStudyHoursPerWeek()));
        request.setTotalStudyHours(progress.getTotalStudyHours());
        request.setCurrentStreak(toDouble(progress.getCurrentStreak()));
        request.setLongestStreak(toDouble(progress.getLongestStreak()));
        request.setCompletedMilestonesCount((double) progress.getCompletedMilestones().size());
        request.setTotalMilestonesCount(getTotalMilestoneCount(user.getCertificationGoal()));
        request.setCompletionPercentage(progress.getCompletionPercentage());
        return request;
    }

    /**
     * Computes a per-topic correct-ratio map from the latest assessment's
     * answers. This ratio is not persisted anywhere - AssessmentService
     * only persists the final strong/weak topic classification, not the
     * raw ratio - so it is recomputed here directly from the already-
     * loaded AssessmentAnswer records. Returns null (no assessment data)
     * for onboarding users, matching what the ai-service expects for that
     * case.
     */
    private Map<String, Double> computeTopicScores(AssessmentResult latestResult) {
        if (latestResult == null || latestResult.getAnswers() == null || latestResult.getAnswers().isEmpty()) {
            return null;
        }

        Map<String, List<AssessmentAnswer>> byTopic = latestResult.getAnswers().stream()
                .collect(Collectors.groupingBy(AssessmentAnswer::getTopic));

        Map<String, Double> topicScores = new HashMap<>();
        for (Map.Entry<String, List<AssessmentAnswer>> entry : byTopic.entrySet()) {
            long correct = entry.getValue().stream().filter(AssessmentAnswer::isCorrect).count();
            topicScores.put(entry.getKey(), (double) correct / entry.getValue().size());
        }
        return topicScores;
    }

    /**
     * Reuses RuleBasedRoadmapGenerator's existing per-goal milestone
     * templates as the single source of truth for "how many milestones
     * exist for this certification goal" - deliberately NOT a second
     * hardcoded goal-to-count table (one already exists inside
     * ProgressService, which is off-limits to modify here).
     */
    private Double getTotalMilestoneCount(String certificationGoal) {
        List<MilestoneDTO> template = ruleBasedRoadmapGenerator.getMilestonesTemplate(certificationGoal);
        return (double) template.size();
    }

    private static Double toDouble(Integer value) {
        return value == null ? null : value.doubleValue();
    }
}
