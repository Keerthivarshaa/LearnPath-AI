package com.learnpath.service;

import com.learnpath.dto.ReadinessPredictionRequest;
import com.learnpath.dto.ReadinessPredictionResponse;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;
import org.springframework.web.reactive.function.client.WebClient;

import java.time.Duration;
import java.util.Optional;

/**
 * HTTP client for the FastAPI ai-service's readiness prediction endpoint.
 *
 * This is the ONLY class that talks to the AI service directly. All
 * failure handling (service down, timeout, malformed response, non-2xx
 * status) is isolated here and converted into an empty Optional rather
 * than a thrown exception - callers (MLRoadmapGenerator) are expected to
 * treat an empty result as "fall back to existing behavior", never as an
 * error to surface to the frontend.
 */
@Component
public class AiReadinessClient {

    private static final Logger log = LoggerFactory.getLogger(AiReadinessClient.class);

    private final WebClient webClient;
    private final Duration timeout;

    public AiReadinessClient(
            WebClient.Builder webClientBuilder,
            @Value("${learnpath.ai-service.base-url:http://localhost:8001}") String baseUrl,
            @Value("${learnpath.ai-service.timeout-ms:3000}") long timeoutMs
    ) {
        this.webClient = webClientBuilder.baseUrl(baseUrl).build();
        this.timeout = Duration.ofMillis(timeoutMs);
    }

    /**
     * Requests a readiness prediction. Returns Optional.empty() for ANY
     * failure mode - connection refused, timeout, non-2xx response, or a
     * malformed body - so a single call site (MLRoadmapGenerator) can
     * decide how to fall back, without the AI service's availability ever
     * being able to turn into a user-facing error.
     */
    public Optional<ReadinessPredictionResponse> predictReadiness(ReadinessPredictionRequest request) {
        try {
            ReadinessPredictionResponse response = webClient.post()
                    .uri("/ml/predict-readiness")
                    .bodyValue(request)
                    .retrieve()
                    .bodyToMono(ReadinessPredictionResponse.class)
                    .timeout(timeout)
                    .block();
            return Optional.ofNullable(response);
        } catch (Exception ex) {
            // Deliberately broad: connection failures, timeouts, 4xx/5xx
            // responses, and deserialization errors must all degrade to the
            // same safe outcome (fall back to rule-based recommendations),
            // not propagate to the caller.
            log.warn("AI readiness service call failed ({}); falling back to rule-based recommendations.",
                    ex.getMessage());
            return Optional.empty();
        }
    }
}
