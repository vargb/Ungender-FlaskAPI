from flaskServer.app import app
import flaskServer.config.config as Config


if __name__ == "__main__":
    app.run(Config.conf.server.host,int(Config.conf.server.port))
