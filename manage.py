""" Manage script for Flask application """
import os
from flask_migrate import Migrate
from auth import create_app, db
from auth.models.models import User

# Initialize Flask app
app = create_app()
migrate = Migrate(app, db)

@app.shell_context_processor
def make_shell_context():
    ''' Shell context for Flask CLI '''
    return {'app': app, 'db': db, 'User': User}

# TO Run Migration
#     # Ensure the migrations folder exists
#     if not os.path.exists('migrations'):
#         os.system('flask db init')
#     # Generate an initial migration
#     os.system('flask db migrate -m "Initial migration"')
#     # Apply the migration to the database
#     os.system('flask db upgrade')
#     print("Database created successfully!")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', '5000')))
