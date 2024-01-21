from .app import app, db

@app.cli.command()
def initdb():
    """Crée la base de données """
    db.create_all()
