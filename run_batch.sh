#!/bin/bash
# Batch runner shell script - runs each condition as a direct subprocess.
# More robust than the Python parent process approach.
set -e

DATA_DIR="data_v2"
PROGRESS_FILE="$DATA_DIR/_progress.json"
RESULTS_FILE="$DATA_DIR/results.json"
PYTHON="python3"

SEEDS=(42 123 256)
PROBLEMS=("regex_parser" "n_queens" "median_stream" "word_break" "median_two_sorted" "serialize_tree" "max_path_sum" "merge_k_lists")
CONDITIONS=("continuous" "raw" "brief" "wake" "no_handoff")

# Check for venv python
if [ -f ".venv/bin/python3" ]; then
    PYTHON=".venv/bin/python3"
fi

# Initialize progress file if needed
if [ ! -f "$PROGRESS_FILE" ]; then
    echo '{"completed": [], "results": []}' > "$PROGRESS_FILE"
fi

build_key() {
    echo "${1}_${3}_s${2}"
}

is_completed() {
    python3 -c "
import json
p = json.load(open('$PROGRESS_FILE'))
print('yes' if '$1' in p['completed'] else 'no')
"
}

save_result() {
    local key="$1"
    local result_json="$2"
    python3 -c "
import json
p = json.load(open('$PROGRESS_FILE'))
p['completed'].append('$key')
p['results'].append($result_json)
json.dump(p, open('$PROGRESS_FILE', 'w'), indent=2)
"
}

# Count total and done
TOTAL=0
for seed in "${SEEDS[@]}"; do
    for prob in "${PROBLEMS[@]}"; do
        for cond in "${CONDITIONS[@]}"; do
            TOTAL=$((TOTAL + 1))
        done
    done
done

DONE=$(python3 -c "import json; print(len(json.load(open('$PROGRESS_FILE'))['completed']))")

echo "=== Handoff V2 Batch Runner (Shell) ==="
echo "Total runs: $TOTAL, Already done: $DONE, Remaining: $((TOTAL - DONE))"
echo "Seeds: ${SEEDS[*]}"
echo "Progress file: $PROGRESS_FILE"
echo "Results file: $RESULTS_FILE"
echo ""

RUN_NUM=$DONE

for seed in "${SEEDS[@]}"; do
  for prob in "${PROBLEMS[@]}"; do
    for cond in "${CONDITIONS[@]}"; do
      KEY=$(build_key "$prob" "$seed" "$cond")
      
      if [ "$(is_completed "$KEY")" = "yes" ]; then
        continue
      fi
      
      RUN_NUM=$((RUN_NUM + 1))
      echo "[$RUN_NUM/$TOTAL] $prob $cond seed=$seed"
      
      # Clean work dir if exists
      rm -rf "$DATA_DIR/${KEY}"
      
      # Run (no timeout on macOS, each model call has own internal timeout)
      RESULT=$(gtimeout 600 $PYTHON handoff_v2.py run_single "$cond" "$prob" "$seed" 2>&1 2>/dev/null || $PYTHON handoff_v2.py run_single "$cond" "$prob" "$seed" 2>&1)
      EXIT_CODE=$?
      
      if [ $EXIT_CODE -eq 0 ]; then
        RESULT_LINE=$(echo "$RESULT" | grep "^RESULT:")
        if [ -n "$RESULT_LINE" ]; then
          RESULT_JSON="${RESULT_LINE#RESULT:}"
          PASSED=$(echo "$RESULT_JSON" | python3 -c "import sys,json; print(json.load(sys.stdin)['passed'])")
          A_TURNS=$(echo "$RESULT_JSON" | python3 -c "import sys,json; print(json.load(sys.stdin)['a_turns'])")
          B_TURNS=$(echo "$RESULT_JSON" | python3 -c "import sys,json; print(json.load(sys.stdin)['b_turns'])")
          HOFF=$(echo "$RESULT_JSON" | python3 -c "import sys,json; print(json.load(sys.stdin)['handoff_tokens'])")
          echo "  $(if [ "$PASSED" = "True" ]; then echo "PASS"; else echo "FAIL"; fi) | A:$A_TURNS B:$B_TURNS hoff:$HOFF"
          save_result "$KEY" "$RESULT_JSON"
        else
          echo "  ERROR: No result marker in output"
          echo "  Output: $RESULT"
          save_result "$KEY" "{\"task_id\": \"handoff/$prob\", \"condition\": \"$cond\", \"passed\": false, \"a_turns\": -1, \"b_turns\": -1, \"handoff_tokens\": -1, \"seed\": $seed, \"error\": \"no result marker\"}"
        fi
      else
        echo "  ERROR: Exit code $EXIT_CODE"
        echo "  Output: $(echo "$RESULT" | tail -3)"
        save_result "$KEY" "{\"task_id\": \"handoff/$prob\", \"condition\": \"$cond\", \"passed\": false, \"a_turns\": -1, \"b_turns\": -1, \"handoff_tokens\": -1, \"seed\": $seed, \"error\": \"exit code $EXIT_CODE\"}"
      fi
      
      # Small delay between runs
      sleep 2
    done
  done
done

# Save final results
python3 -c "
import json
p = json.load(open('$PROGRESS_FILE'))
with open('$RESULTS_FILE', 'w') as f:
    json.dump(p['results'], f, indent=2)
print('Final results saved')
"

# Summary
python3 -c "
import json
from collections import defaultdict
p = json.load(open('$PROGRESS_FILE'))
by_cond = defaultdict(list)
for r in p['results']:
    if 'condition' in r:
        by_cond[r['condition']].append(r.get('passed', False))
for c in ${CONDITIONS[@]}: 
    p = by_cond[c]
    if p:
        print(f'{c:15s}: {sum(p)}/{len(p)} ({100*sum(p)//len(p)}%)')
print(f'Total: {len(p[\"results\"])} runs')
"
