# Data Model

## Role

`role_id`, `name`, `name_ru`, `status`, `description`, `competency_ids`.

## Competency

`competency_id`, `role_id`, `name`, `name_en`, `description`, `weight`, `tags`.

## Diagnostic Question

`question_id`, `role_id`, `competency_id`, `type`, `level`, `question`, `options`, `correct_answer`, `expected_points`, `keywords`.

## Learning Material

`material_id`, `role_id`, `competency_id`, `title`, `level`, `path`, `tags`.

## Result

`session_id`, `role_id`, `overall_level`, `readiness_status`, `competency_results`, `priority_gaps`, `learning_track`.
