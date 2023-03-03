#!/bin/sh

#use env variables to set up options
#for example:
#TD_PAD-SIZE=L becomes --pad-size L
#TD_PLANETARY=N becomes --planetary N
#TD_PROGRESS='' becomes --progress
#and so on

OPTIONS=$(python src/ExtractOpts.py)

case "$EXEC" in
    cli)
        exec trade run $OPTIONS "$@"
    ;;
    shell)
        exec /bin/sh
    ;;
    web)
        exec flask --app src/app.py run --host=0.0.0.0
    ;;
    *)
      echo "Unknown command: $EXEC"
    ;;
esac


