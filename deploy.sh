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

python $DIR/manage.py load_flashcards $DIR/categories.json
python $DIR/manage.py load_flashcards $DIR/temrs.json
python $DIR/manage.py load_flashcards $DIR/intro.json

# static files
python $DIR/manage.py collectstatic --noinput
