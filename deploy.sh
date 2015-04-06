#!/bin/sh
# deployment script run by Viper server after push

echo "Starting deploy script"
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

cd $DIR

#requirements
pip install -r $DIR/requirements.txt

# database
python $DIR/manage.py syncdb
python $DIR/manage.py migrate

python $DIR/manage.py load_flashcards $DIR/data/categories.json
python $DIR/manage.py load_flashcards $DIR/data/terms.json
python $DIR/manage.py load_flashcards $DIR/data/intro.json

# static files
python $DIR/manage.py collectstatic --noinput
