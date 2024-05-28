from flask_migrate import Migrate
from app import create_app, db
from app.models.models import User
import os

app = create_app()
migrate = Migrate(app, db)

@app.shell_context_processor
def make_shell_context():
    return {'app': app, 'db': db, 'User': User}

def create_db():
    # Ensure the migrations folder exists
    if not os.path.exists('migrations'):
        os.system('flask db init')
    # Generate an initial migration
    os.system('flask db migrate -m "Initial migration"')
    # Apply the migration to the database
    os.system('flask db upgrade')
    print("Database created successfully!")
    

if __name__ == '__main__':
    create_db()
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 5000)))
