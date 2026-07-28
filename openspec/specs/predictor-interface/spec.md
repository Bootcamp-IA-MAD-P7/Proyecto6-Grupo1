## Purpose

Define an internal prediction port so a baseline model, mock, or a future approved
predictor can be exchanged without rewriting routes or service orchestration.

## Requirements

### Requirement: Predictor interface for extensibility

The service SHALL define an internal abstract prediction interface. Alternative
implementations SHALL be swappable without modifying route handlers or service
orchestration.

#### Scenario: Swapping predictor does not change the route

- **GIVEN** the service injects a predictor through the interface
- **WHEN** startup selects `MockPredictor` or `BaselinePredictor`
- **THEN** route handlers and orchestration remain unchanged

#### Scenario: New predictor implementation is additive

- **GIVEN** the interface exists
- **WHEN** a future approved implementation conforms to it
- **THEN** it can be introduced without modifying existing routes or predictor classes
