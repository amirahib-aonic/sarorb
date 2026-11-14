#!/bin/sh
root=$(git rev-parse --show-toplevel)
cd "$root" || exit 1
file=docs/OBJECTIVES.md
strict=0
[ "$1" = "--strict" ] && strict=1
fail=0
level=""
cr=$(printf '\r')

while IFS= read -r line || [ -n "$line" ]; do
  line=${line%"$cr"}
  case "$line" in
    "## "*) level=${line#"## "} ;;
    "- ["*"] "*": "*)
      mark=$(printf '%s' "$line" | cut -c4)
      id=$(printf '%s' "$line" | sed 's/^- \[.\] \([^:]*\):.*/\1/')
      evidence=$(printf '%s' "$line" | sed -n 's/.*| evidence:[[:space:]]*//p')
      if [ "$mark" = "x" ]; then
        if [ -z "$evidence" ]; then
          echo "FAIL $id ticked with no evidence"; fail=1; continue
        fi
        old_ifs=$IFS; IFS=,
        for p in $evidence; do
          p=$(printf '%s' "$p" | sed 's/^[[:space:]]*//;s/[[:space:]]*$//')
          [ -e "$p" ] || { echo "FAIL $id evidence missing: $p"; fail=1; }
        done
        IFS=$old_ifs
      else
        ready=0
        if [ -n "$evidence" ]; then
          ready=1
          old_ifs=$IFS; IFS=,
          for p in $evidence; do
            p=$(printf '%s' "$p" | sed 's/^[[:space:]]*//;s/[[:space:]]*$//')
            [ -e "$p" ] || ready=0
          done
          IFS=$old_ifs
        fi
        if [ $ready -eq 1 ]; then
          echo "READY $id (evidence exists, tick it once the objective is really met)"
        elif [ "$level" = "Must" ]; then
          echo "TODO $id"
        fi
        [ "$level" = "Must" ] && [ $strict -eq 1 ] && fail=1
      fi
      ;;
  esac
done < "$file"

hits=$(git ls-files | grep -iE '(nasa[-_ ]?(logo|meatball|worm|insignia)|meatball)\.(svg|png|jpe?g|webp|gif)$')
if [ -n "$hits" ]; then
  echo "FAIL prohibited NASA logo asset:"; echo "$hits"; fail=1
fi
hits=$(git grep -liE 'nasa[-_ ]?(meatball|worm|insignia)' -- ':!docs/OBJECTIVES.md' ':!scripts/check-objectives.sh' 2>/dev/null)
if [ -n "$hits" ]; then
  echo "FAIL prohibited NASA logo reference in:"; echo "$hits"; fail=1
fi

[ $fail -eq 0 ] && echo "objectives: ok"
exit $fail
