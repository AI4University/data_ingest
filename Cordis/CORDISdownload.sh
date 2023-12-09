# Make directories
mkdir -p "$2/cordis-ref"
mkdir -p "$2/HORIZON"
mkdir -p "$2/H2020"
mkdir -p "$2/FP7"


wget -i $1 -P $2 --show-progress

# Move all downloaded files to its own directory
for f in $2/*; do
    if [ -f $f ]; then
        if [[ $f =~ cordisref ]]; then
            mv "$f" "$2/cordis-ref/$(basename $f)"
        elif [[ $f =~ cordis-HORIZON ]]; then
            # horizon
            mv "$f" "$2/HORIZON/$(basename $f)"
        elif [[ $f =~ cordis-h2020 ]]; then
            # h2020
            mv "$f" "$2/H2020/$(basename $f)"
        else
            # FP7
            mv "$f" "$2/FP7/$(basename $f)"
        fi
    fi
done
