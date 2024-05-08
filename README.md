# Table Migrations
In order to migrate the models and reflect the changes on the Supabase Database run:

```
cd transcription_service
python manage.py makemigrations db_orm_model
python manage.py migrate db_orm_model
```

This will create a file in the ```db_orm_model/migrations``` directory.

**Note**: It is important to keep the migrations directory up to date because this is what is used by PlanetScale to apply new migrations. It runs every migration in the file in order to get the most up to date one.

# Git Submodule

Whenever a new migration is created it modify the ```db_orm_model``` git repository. It is important that we commit the changes to this repository as well.

```
cd db_orm_model
git add .
git commit -m <commit_message>
git push origin <branch_name>
```
