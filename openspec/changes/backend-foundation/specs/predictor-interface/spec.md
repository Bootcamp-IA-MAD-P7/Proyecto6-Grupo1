## Purpose

Define an internal interface (port) for the prediction capability, enabling alternative
implementations (baseline model, mock, future RAG) without modifying routes or
application logic.

## ADDED Requirements

### Requirement: Predictor interface for extensibility
The service SHALL define an internal abstract interface for the prediction capability. Alternative implementations (real model, mock, future RAG) SHALL be swappable without modifying route handlers or service orchestration code.

#### Scenario: Swapping predictor does not change the route
- **GIVEN** the service uses a predictor interface with dependency injection
- **WHEN** the implementation changes from MockPredictor to BaselinePredictor (or vice versa)
- **THEN** the route handler code and service orchestration remain unchanged; only the startup configuration or injection changes

#### Scenario: New predictor implementation is additive
- **GIVEN** the predictor interface is defined
- **WHEN** a developer creates a new implementation (e.g., RAGPredictor) conforming to the interface
- **THEN** the new implementation can be used without modifying existing predictor classes, routes, or service code
