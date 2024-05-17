import os
from config import app,db
from sorvetes.sorvetes_routes import sorvete as sorvete_blueprint
from categorias.index import categoria as categoria_blueprint

app.register_blueprint(sorvete_blueprint)
app.register_blueprint(categoria_blueprint)

with app.app_context():
    db.create_all()

if __name__ == '__main__':
  app.run(host=app.config["HOST"], port = app.config['PORT'],debug=app.config['DEBUG'] )