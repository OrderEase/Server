for i in { 1..100 }; do
    if ! curl -s database:3306 > /dev/null; then
        echo waiting on database for $i seconds...;
        sleep $i;
    fi;
done;

echo database is ready, start web server...

python3 manage.py runserver