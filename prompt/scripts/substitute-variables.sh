#!/usr/bin/env bash
set -euo pipefail

TEMPLATE_FILE="$1"
shift

if [[ ! -f "$TEMPLATE_FILE" ]]; then
    echo "❌ Template introuvable : $TEMPLATE_FILE" >&2
    exit 1
fi

CONTENT=$(cat "$TEMPLATE_FILE")

# Variables globales (depuis analyze-context.sh)
CONTENT=$(echo "$CONTENT" | sed "s/{PROJECT_NAME}/${PROJECT_NAME}/g")
CONTENT=$(echo "$CONTENT" | sed "s/{NAMESPACE}/${NAMESPACE}/g")
CONTENT=$(echo "$CONTENT" | sed "s/{AUTHOR}/${AUTHOR_NAME}/g")
CONTENT=$(echo "$CONTENT" | sed "s/{DATE}/${DATE}/g")

# Variables spécifiques (depuis args CLI)
while [[ $# -gt 0 ]]; do
    case $1 in
        --entity=*)
            ENTITY_NAME="${1#*=}"
            CONTENT=$(echo "$CONTENT" | sed "s/{ENTITY_NAME}/${ENTITY_NAME}/g")
            shift
            ;;
        --feature=*)
            FEATURE_NAME="${1#*=}"
            CONTENT=$(echo "$CONTENT" | sed "s/{FEATURE_NAME}/${FEATURE_NAME}/g")
            shift
            ;;
        --bounded-context=*)
            BOUNDED_CONTEXT="${1#*=}"
            CONTENT=$(echo "$CONTENT" | sed "s/{BOUNDED_CONTEXT}/${BOUNDED_CONTEXT}/g")
            shift
            ;;
        --duration=*)
            DURATION="${1#*=}"
            CONTENT=$(echo "$CONTENT" | sed "s/{DURATION}/${DURATION}/g")
            shift
            ;;
        --target-file=*)
            TARGET_FILE="${1#*=}"
            CONTENT=$(echo "$CONTENT" | sed "s/{TARGET_FILE}/${TARGET_FILE}/g")
            shift
            ;;
        --optimization-type=*)
            OPTIMIZATION_TYPE="${1#*=}"
            CONTENT=$(echo "$CONTENT" | sed "s/{OPTIMIZATION_TYPE}/${OPTIMIZATION_TYPE}/g")
            shift
            ;;
        --current-complexity=*)
            CURRENT_COMPLEXITY="${1#*=}"
            CONTENT=$(echo "$CONTENT" | sed "s/{CURRENT_COMPLEXITY}/${CURRENT_COMPLEXITY}/g")
            shift
            ;;
        --improvement-target=*)
            IMPROVEMENT_TARGET="${1#*=}"
            CONTENT=$(echo "$CONTENT" | sed "s/{IMPROVEMENT_TARGET}/${IMPROVEMENT_TARGET}/g")
            shift
            ;;
        --service-name=*)
            SERVICE_NAME="${1#*=}"
            CONTENT=$(echo "$CONTENT" | sed "s/{SERVICE_NAME}/${SERVICE_NAME}/g")
            shift
            ;;
        --event-type=*)
            EVENT_TYPE="${1#*=}"
            CONTENT=$(echo "$CONTENT" | sed "s/{EVENT_TYPE}/${EVENT_TYPE}/g")
            shift
            ;;
        --webhook-url-var=*)
            WEBHOOK_URL_VAR="${1#*=}"
            CONTENT=$(echo "$CONTENT" | sed "s/{WEBHOOK_URL_VAR}/${WEBHOOK_URL_VAR}/g")
            shift
            ;;
        --component-name=*)
            COMPONENT_NAME="${1#*=}"
            CONTENT=$(echo "$CONTENT" | sed "s/{COMPONENT_NAME}/${COMPONENT_NAME}/g")
            shift
            ;;
        --workflow-name=*)
            WORKFLOW_NAME="${1#*=}"
            CONTENT=$(echo "$CONTENT" | sed "s/{WORKFLOW_NAME}/${WORKFLOW_NAME}/g")
            shift
            ;;
        --config-name=*)
            CONFIG_NAME="${1#*=}"
            CONTENT=$(echo "$CONTENT" | sed "s/{CONFIG_NAME}/${CONFIG_NAME}/g")
            shift
            ;;
        --task-name=*)
            TASK_NAME="${1#*=}"
            CONTENT=$(echo "$CONTENT" | sed "s/{TASK_NAME}/${TASK_NAME}/g")
            shift
            ;;
        *)
            echo "❌ Argument inconnu : $1" >&2
            exit 1
            ;;
    esac
done

echo "$CONTENT"
